from __future__ import annotations

import logging
import uuid
import warnings
import weakref
from typing import Dict, Generic, Optional, Set, Union

import dask
import dask.distributed
from coiled.context import track_context

from ..cluster import Cluster, CredentialsPreferred
from ..compatibility import DISTRIBUTED_VERSION
from ..core import IsAsynchronous
from ..errors import ClusterCreationError, DoesNotExist
from ..utils import COILED_LOGGER_NAME
from .core import AWSOptions, CloudBeta, setup_up_logging
from .states import ProcessStateEnum

logger = logging.getLogger(COILED_LOGGER_NAME)


class ClusterBeta(Cluster, Generic[IsAsynchronous]):
    """Create a Dask cluster with Coiled

    Parameters
    ----------
    n_workers
        Number of workers in this cluster. Defaults to 4.
    configuration
        Name of cluster configuration to create cluster from.
        If not specified, defaults to ``coiled/default`` for the
        current Python version.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    worker_class
        Worker class to use. Defaults to "dask.distributed.Nanny".
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults to ``{}``.
    worker_vm_types
        List of instance types that you would like workers to use, this list can have up to five items.
        You can use the command ``coiled.list_instance_types()`` to se a list of allowed types.
    scheduler_class
        Scheduler class to use. Defaults to "dask.distributed.Scheduler".
    scheduler_options
        Mapping with keyword arguments to pass to ``scheduler_class``. Defaults to ``{}``.
    scheduler_vm_types
        List of instance types that you would like the scheduler to use, this list can have up to
        five items.
        You can use the command ``coiled.list_instance_types()`` to se a list of allowed types.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled.
    account
        Name of Coiled account to use. If not provided, will
        default to the user account for the ``cloud`` object being used.
    shutdown_on_close
        Whether or not to shut down the cluster when it finishes.
        Defaults to True, unless name points to an existing cluster.
    use_scheduler_public_ip
        Boolean value that determines if the Python client connects to the Dask scheduler using the scheduler machine's
        public IP address. The default behaviour when set to True is to connect to the scheduler using its public IP
        address, which means traffic will be routed over the public internet. When set to False, traffic will be
        routed over the local network the scheduler lives in, so make sure the scheduler private IP address is
        routable from where this function call is made when setting this to False.
    credentials
        Which credentials to use for Dask operations and forward to Dask clusters --
        options are "account", "local", or "none". The default behavior is to prefer
        credentials associated with the Coiled Account, if available, then try to
        use local credentials, if available.
        NOTE: credential handling currently only works with AWS credentials.
    timeout
        Timeout in seconds to wait for a cluster to start, will use ``default_cluster_timeout``
        set on parent Cloud by default.
    environ
        Dictionary of environment variables.
    show_state_updates
        Whether to show all state updates related to the cluster during launch.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        software_environment: str = None,
        n_workers: int = 4,
        worker_class: str = None,
        worker_options: dict = None,
        worker_vm_types: Optional[list] = None,
        scheduler_class: str = None,
        scheduler_options: dict = None,
        scheduler_vm_types: Optional[list] = None,
        asynchronous: bool = False,
        cloud: CloudBeta = None,
        account: str = None,
        shutdown_on_close=None,
        use_scheduler_public_ip: Optional[bool] = None,
        credentials: Optional[str] = "account",
        timeout: Optional[int] = None,
        environ: Optional[Dict[str, str]] = None,
        backend_options: Optional[
            AWSOptions
        ] = None,  # intentionally not in the docstring yet
        show_state_updates: bool = False,
        configure_logging: bool = True,
    ):

        if configure_logging:
            setup_up_logging()

        self.show_state_updates = show_state_updates
        # Determine consistent sync/async
        if cloud and asynchronous is not None and cloud.asynchronous != asynchronous:
            warnings.warn(
                f"Requested a Cluster with asynchronous={asynchronous}, but "
                f"cloud.asynchronous={cloud.asynchronous}, so the cluster will be"
                f"{cloud.asynchronous}"
            )
            asynchronous = cloud.asynchronous

        self.scheduler_comm: Optional[dask.distributed.rpc] = None

        self.cloud: CloudBeta[IsAsynchronous] = cloud or CloudBeta.current(
            asynchronous=asynchronous
        )

        # As of distributed 2021.12.0, deploy.Cluster has a ``loop`` attribute on the
        # base class. We add the attribute manually here for backwards compatibility.
        # TODO: if/when we set the minimum distributed version to be >= 2021.12.0,
        # remove this check.
        if DISTRIBUTED_VERSION >= "2021.12.0":
            kwargs = {"loop": self.cloud.loop}
        else:
            kwargs = {}
            self.loop = self.cloud.loop

        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super(Cluster, self).__init__(asynchronous, **kwargs)

        self.timeout = (
            timeout if timeout is None else self.cloud.default_cluster_timeout
        )

        self.software_environment = software_environment
        self.worker_class = worker_class
        self.worker_options = {
            **(dask.config.get("coiled.worker-options", {})),
            **(worker_options or {}),
        }
        self.worker_vm_types = worker_vm_types
        self.scheduler_class = scheduler_class
        self.scheduler_options = {
            **(dask.config.get("coiled.scheduler-options", {})),
            **(scheduler_options or {}),
        }
        self.scheduler_vm_types = scheduler_vm_types
        self.name = name
        self.account = account or self.cloud.default_account
        self._start_n_workers = n_workers
        self._lock = None
        self._asynchronous = asynchronous
        self.shutdown_on_close = shutdown_on_close
        self.environ = {k: str(v) for (k, v) in (environ or {}).items() if v}
        self.credentials = CredentialsPreferred(credentials)
        self._default_protocol = dask.config.get("coiled.protocol", "tls")

        # these are sets of names of workers, only including workers in states that might eventually reach
        # a "started" state
        # they're used in our implementation of scale up/down (mostly inherited from coiled.Cluster)
        # and their corresponding properties are used in adaptive scaling (at least once we
        # make adaptive work with ClusterBeta).
        #
        # (Adaptive expects attributes `requested` and `plan`, which we implement as properties below.)
        #
        # Some good places to learn about adaptive:
        # https://github.com/dask/distributed/blob/39024291e429d983d7b73064c209701b68f41f71/distributed/deploy/adaptive_core.py#L31-L43
        # https://github.com/dask/distributed/issues/5080
        self._requested: Set[str] = set()
        self._plan: Set[str] = set()

        self._adaptive_options: Dict[str, Union[str, int]] = {}
        self.cluster_id: Optional[int] = None
        self.use_scheduler_public_ip: bool = (
            dask.config.get("coiled.use_scheduler_public_ip", True)
            if use_scheduler_public_ip is None
            else use_scheduler_public_ip
        )

        self._name = (
            "coiled._beta.ClusterBeta"  # Used in Dask's Cluster._ipython_display_
        )
        self.backend_options = backend_options

        if not self.asynchronous:
            try:
                self.sync(self._start)
            except ClusterCreationError as e:
                raise e.with_traceback(None)
            except Exception as e:
                raise e

    @track_context
    async def _start(self):
        cloud = self.cloud

        if self.name:
            try:
                self.cluster_id = await cloud._get_cluster_by_name(
                    name=self.name,
                    account=self.account,
                )
            except DoesNotExist:
                should_create = True
            else:
                logger.info(f"Using existing cluster: '{self.name}'")
                should_create = False
                if self.shutdown_on_close is None:
                    self.shutdown_on_close = False
        else:
            should_create = True
            self.name = (
                self.name
                or (self.account or cloud.default_account)
                + "-"
                + str(uuid.uuid4())[:10]
            )

        if should_create:
            logger.info("Creating Cluster. This might take a few minutes...")
            # ignoring typechecker here -- I didn't figure out how to make it happy with this
            self.cluster_id = await cloud.create_cluster(  # type: ignore
                account=self.account,
                name=self.name,
                workers=self._start_n_workers,
                software=self.software_environment,
                worker_class=self.worker_class,
                worker_options=self.worker_options,
                scheduler_class=self.scheduler_class,
                scheduler_options=self.scheduler_options,
                environ=self.environ,
                scheduler_vm_types=self.scheduler_vm_types,
                worker_vm_types=self.worker_vm_types,
                backend_options=self.backend_options,
            )
        if not self.cluster_id:
            raise RuntimeError(f"Failed to find/create cluster {self.name}")

        logger.debug(f"cluster ID is {self.cluster_id}")

        if self.shutdown_on_close:
            weakref.finalize(self, cloud.delete_cluster, self.cluster_id)

        # update our view of workers in case someone tries scaling
        # it might be better to continually update this while waiting for the
        # cluster in _security below, but this seems OK for now
        await self._set_plan_requested()

        # this is what waits for the cluster to be "ready"
        self.security, info = await cloud._security(
            cluster_id=self.cluster_id,
            account=self.account,
            show_state_updates=self.show_state_updates,
        )
        await self._set_plan_requested()  # update our view of workers
        self._proxy = bool(self.security.extra_conn_args)

        # TODO (Declarative): (or also relevant for non-declarative?):
        # dashboard address should be private IP when use_scheduler_public_ip is False
        self._dashboard_address = info["dashboard_address"]

        if self.use_scheduler_public_ip:
            rpc_address = info["public_address"]
        else:
            rpc_address = info["private_address"]
            logger.info(
                f"Connecting to scheduler on its internal address: {rpc_address}"
            )

        try:
            self.scheduler_comm = dask.distributed.rpc(
                rpc_address,
                connection_args=self.security.get_connection_args("client"),
            )
            await self._send_credentials(cloud)
        except IOError as e:
            if "Timed out" in "".join(e.args):
                raise RuntimeError(
                    "Unable to connect to Dask cluster. This may be due "
                    "to different versions of `dask` and `distributed` "
                    "locally and remotely.\n\n"
                    f"You are using distributed={DISTRIBUTED_VERSION} locally.\n\n"
                    "With pip, you can upgrade to the latest with:\n\n"
                    "\tpip install --upgrade dask distributed"
                )
            raise

        await super(Cluster, self)._start()

        # Set adaptive maximum value based on available config and user quota
        self._set_adaptive_options(info)

    async def _set_plan_requested(self):
        eventually_maybe_good_statuses = [
            ProcessStateEnum.starting,
            ProcessStateEnum.pending,
            ProcessStateEnum.started,
        ]
        eventually_maybe_good_workers = await self.cloud._get_worker_names(
            account=self.account,
            cluster_id=self.cluster_id,
            statuses=eventually_maybe_good_statuses,
        )
        self._plan = eventually_maybe_good_workers
        self._requested = eventually_maybe_good_workers

    @track_context
    async def _scale(self, n: int) -> None:
        await self._set_plan_requested()  # need to update our understanding of current workers before scaling
        logger.debug(f"current _plan: {self._plan}")
        if not self.cluster_id:
            raise ValueError("No cluster available to scale!")
        recommendations = await self.recommendations(n)
        logger.debug(f"scale recommmendations: {recommendations}")
        status = recommendations.pop("status")
        if status == "same":
            return
        if status == "up":
            return await self.scale_up(**recommendations)
        if status == "down":
            return await self.scale_down(**recommendations)

    @track_context
    async def scale_up(self, n: int) -> None:
        """
        Scales up *to* a target number of ``n`` workers

        It's documented that scale_up should scale up to a certain target, not scale up BY a certain amount:

        https://github.com/dask/distributed/blob/main/distributed/deploy/adaptive_core.py#L60
        """
        if not self.cluster_id:
            raise ValueError(
                "No cluster available to scale! "
                "Check cluster was not closed by another process."
            )
        target = n - len(self.plan)
        response = await self.cloud._scale_up(
            account=self.account,
            cluster_id=self.cluster_id,
            n=target,
        )
        if response:
            self._plan.update(set(response.get("workers", [])))
            self._requested.update(set(response.get("workers", [])))

    def _set_adaptive_options(self, info):
        self._adaptive_options = {
            "interval": "5s",
            "wait_count": 60,
            "minimum": 1,
            # TODO: want a more sensible limit; see _set_adaptive_options in coiled.Cluster
            # for inspiration from the logic there
            "maximum": 200,
        }
