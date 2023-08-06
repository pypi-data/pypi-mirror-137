from __future__ import annotations

import asyncio
import datetime
import logging
import weakref
from collections import namedtuple
from typing import (
    Awaitable,
    Dict,
    Generic,
    List,
    NamedTuple,
    NoReturn,
    Optional,
    Set,
    Tuple,
    Union,
    overload,
)

import dask
from coiled.context import track_context
from distributed.utils import Log, Logs

from ..core import Async
from ..core import Cloud as OldCloud
from ..core import IsAsynchronous, Sync
from ..errors import ClusterCreationError, DoesNotExist, ServerError
from ..utils import COILED_LOGGER_NAME, GatewaySecurity
from .states import (
    ClusterStateEnum,
    ProcessStateEnum,
    flatten_log_states,
    log_states,
    summarize_status,
)

logger = logging.getLogger(COILED_LOGGER_NAME)


def setup_up_logging():
    logging.getLogger(COILED_LOGGER_NAME).setLevel(logging.INFO)
    logging.basicConfig()


async def handle_api_exception(response, exception_cls=ServerError) -> NoReturn:
    error_body = await response.json()
    if "message" in error_body:
        raise exception_cls(error_body["message"])
    if "detail" in error_body:
        raise exception_cls(error_body["detail"])
    raise exception_cls(error_body)


class BackendOptions(NamedTuple):
    region_name: Optional[str]


class AWSOptions(BackendOptions):
    pass
    # future: add region_name!
    # future: add stuff like "spot" when supported
    # future: make a GCPOptions


class CloudBeta(OldCloud, Generic[IsAsynchronous]):
    _recent_sync: list[weakref.ReferenceType[CloudBeta[Sync]]] = list()
    _recent_async: list[weakref.ReferenceType[CloudBeta[Async]]] = list()

    # just overriding to get the right signature (CloudBeta, not Cloud)
    def __enter__(self: CloudBeta[Sync]) -> CloudBeta[Sync]:
        return self

    def __exit__(self: CloudBeta[Sync], typ, value, tb) -> None:
        self.close()

    # these overloads are necessary for the typechecker to know that we really have a CloudBeta, not a Cloud
    # without them, CloudBeta.current would be typed to return a Cloud
    #
    # https://www.python.org/dev/peps/pep-0673/ would remove the need for this.
    # That PEP also mentions a workaround with type vars, which doesn't work for us because type vars aren't
    # subscribtable
    @overload
    @classmethod
    def current(cls, asynchronous: Sync) -> CloudBeta[Sync]:
        ...

    @overload
    @classmethod
    def current(cls, asynchronous: Async) -> CloudBeta[Async]:
        ...

    @overload
    @classmethod
    def current(cls, asynchronous: bool) -> CloudBeta:
        ...

    @classmethod
    def current(cls, asynchronous: bool) -> CloudBeta:
        recent: list[weakref.ReferenceType[CloudBeta]]
        if asynchronous:
            recent = cls._recent_async
        else:
            recent = cls._recent_sync
        try:
            cloud = recent[-1]()
            while cloud is None or cloud.status != "running":
                recent.pop()
                cloud = recent[-1]()
        except IndexError:
            if asynchronous:
                return cls(asynchronous=True)
            else:
                return cls(asynchronous=False)
        else:
            return cloud

    async def _list_clusters_page(
        self, page: int, account: str = None
    ) -> Tuple[dict, Optional[str]]:
        account = account or self.default_account
        # /api/v2/clusters/account/<account>/
        response = await self._do_request(
            "GET",
            self.server
            + f"/api/v2/clusters/account/{account}/",  # , params={"page": page}
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        results = {d["name"]: d for d in results}
        # TODO: need an appropriate "next" instead of None to get all pages
        return results, None

    @track_context
    async def _create_cluster(
        self,
        # todo: make name optional and pick one for them, like pre-declarative?
        # https://gitlab.com/coiled/cloud/-/issues/4305
        name: str,
        *,
        software_environment: str = None,
        worker_class: str = None,
        worker_options: dict = None,
        scheduler_class: str = None,
        scheduler_options: dict = None,
        account: str = None,
        workers: int = 0,
        environ: Optional[Dict] = None,
        scheduler_vm_types: Optional[list] = None,
        worker_gpu_type: str = None,
        worker_vm_types: Optional[list] = None,
        backend_options: Optional[AWSOptions] = None,
    ) -> int:
        if backend_options is not None and not isinstance(
            backend_options, BackendOptions
        ):
            raise ValueError(
                "backend_options should be an instance of coiled._beta.BackendOptions"
            )
        # TODO (Declarative): support these args, or decide not to
        # https://gitlab.com/coiled/cloud/-/issues/4305
        if worker_class is not None:
            raise ValueError("worker_class is not supported in beta/new Coiled yet")
        if worker_options:
            raise ValueError("worker_options is not supported in beta/new Coiled yet")
        if scheduler_class is not None:
            raise ValueError("scheduler_class is not supported in beta/new Coiled yet")
        if scheduler_options:
            raise ValueError(
                "scheduler_options is not supported in beta/new Coiled yet"
            )
        if environ:
            raise ValueError("environ is not supported in beta/new Coiled yet")
        if worker_gpu_type is not None:
            raise ValueError("worker_gpu_type is not supported in beta/new Coiled yet")

        account = account or self.default_account
        account, name = self._normalize_name(
            name,
            context_account=account,
            allow_uppercase=True,
        )
        self._verify_account(account)
        data = {
            "name": name,
            "workers": workers,
            "worker_instance_types": worker_vm_types,
            "scheduler_instance_types": scheduler_vm_types,
            "software_environment": software_environment,
        }
        if backend_options and backend_options.region_name:
            data["options"] = {"region_name": backend_options.region_name}

        response = await self._do_request(
            "POST", self.server + f"/api/v2/clusters/account/{account}/", json=data
        )
        if response.status >= 400:
            await handle_api_exception(response)
        json = await response.json()
        return json["id"]

    def create_cluster(
        self,
        name: str = None,
        *,
        software: str = None,
        worker_class: str = None,
        worker_options: dict = None,
        scheduler_class: str = None,
        scheduler_options: dict = None,
        account: str = None,
        workers: int = 0,
        environ: Optional[Dict] = None,
        scheduler_vm_types: Optional[list] = None,
        worker_gpu_type: str = None,
        worker_vm_types: Optional[list] = None,
        backend_options: Optional[AWSOptions] = None,
    ) -> int:

        return self._sync(
            self._create_cluster,
            name=name,
            software_environment=software,
            worker_class=worker_class,
            worker_options=worker_options,
            scheduler_class=scheduler_class,
            scheduler_options=scheduler_options,
            account=account,
            workers=workers,
            environ=environ,
            scheduler_vm_types=scheduler_vm_types,
            worker_gpu_type=worker_gpu_type,
            worker_vm_types=worker_vm_types,
            backend_options=backend_options,
        )

    @track_context
    async def _delete_cluster(self, cluster_id: int, account: str = None) -> None:
        account = account or self.default_account

        route = f"/api/v2/clusters/account/{account}/id/{cluster_id}"

        response = await self._do_request(
            "DELETE",
            self.server + route,
        )
        if response.status >= 400:
            await handle_api_exception(response)
        else:
            logger.info("Cluster deleted successfully.")

    async def _get_cluster_details(self, cluster_id: int, account: str = None):
        account = account or self.default_account
        r = await self._do_request(
            "GET", self.server + f"/api/v2/clusters/account/{account}/id/{cluster_id}"
        )
        if r.status >= 400:
            await handle_api_exception(r)
        return await r.json()

    def _get_cluster_details_synced(self, cluster_id: int, account: str = None):
        return self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            account=account,
        )

    @track_context
    async def _get_worker_names(
        self,
        account: str,
        cluster_id: int,
        statuses: Optional[List[ProcessStateEnum]] = None,
    ) -> Set[str]:
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/workers/account/{account}/cluster/{cluster_id}/",
        )
        if response.status >= 400:
            await handle_api_exception(response)

        worker_infos = await response.json()
        logger.debug(f"workers: {worker_infos}")
        return {
            w["name"]
            for w in worker_infos
            if statuses is None or w["current_state"]["state"] in statuses
        }

    @track_context
    async def _security(
        self, cluster_id: int, account: str = None, show_state_updates=False
    ) -> Tuple[dask.distributed.Security, dict]:
        times_waited = 0
        latest_dt_seen = None
        while True:
            states_by_type = await self._get_cluster_states_declarative(
                cluster_id, account, start_time=latest_dt_seen
            )
            states = flatten_log_states(states_by_type)
            if states:
                latest_dt_seen = states[-1].updated
            log_states(states, only_errors=(not show_state_updates))

            cluster = await self._get_cluster_details(
                cluster_id=cluster_id, account=account
            )
            state_summary = summarize_status(cluster)

            state = ClusterStateEnum(cluster["current_state"]["state"])

            # just showing states periodically even if no change
            # I was tempted to also show the states any time they changed, but that would be
            # very noisy with a lot of workers.
            if times_waited % 10 == 0:
                logger.info(state_summary)

            times_waited += 1

            if state == ClusterStateEnum.ready:
                public_ip = cluster["scheduler"]["instance"]["public_ip_address"]
                private_ip = cluster["scheduler"]["instance"]["private_ip_address"]
                tls_cert = cluster["cluster_options"]["tls_cert"]
                tls_key = cluster["cluster_options"]["tls_key"]

                # TODO (Declarative): pass extra_conn_args if we care about proxying through Coiled to the scheduler
                security = GatewaySecurity(tls_key, tls_cert)

                return security, {
                    # TODO (Declarative):
                    #  if Declarative ever supports schedulers on other ports, stop hard-coding the portop
                    "private_address": f"tls://{private_ip}:8786",
                    "public_address": f"tls://{public_ip}:8786",
                    "dashboard_address": f"http://{public_ip}:8787",
                }

            elif state.awaiting_readiness():
                await asyncio.sleep(1.0)
            else:
                # TODO (Declarative): give more info about what the problem is
                raise ClusterCreationError(f"Cluster status is {state.value}")

    @track_context
    async def _requested_workers(
        self, cluster_id: int, account: str = None
    ) -> Set[str]:
        raise NotImplementedError("TODO")

    @track_context
    async def _get_cluster_by_name(self, name: str, account: str = None) -> int:
        account, name = self._normalize_name(
            name, context_account=account, allow_uppercase=True
        )

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{account}/name/{name}",
        )
        if response.status == 404:
            raise DoesNotExist
        elif response.status >= 400:
            await handle_api_exception(response)

        cluster = await response.json()
        return cluster["id"]

    @track_context
    async def _cluster_status(
        self, cluster_id: int, account: str = None, exclude_stopped: bool = True
    ) -> dict:
        raise NotImplementedError("TODO?")

    @track_context
    async def _get_cluster_states_declarative(
        self,
        cluster_id: int,
        account: str = None,
        start_time: datetime.datetime = None,
    ) -> int:
        account = account or self.default_account

        params = (
            {"start_time": start_time.isoformat()} if start_time is not None else {}
        )

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{account}/id/{cluster_id}/states",
            params=params,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        return await response.json()

    def get_cluster_states(
        self,
        cluster_id: int,
        account: str = None,
        start_time: datetime.datetime = None,
    ) -> Union[int, Awaitable[int]]:
        return self._sync(
            self._get_cluster_states_declarative,
            cluster_id=cluster_id,
            account=account,
            start_time=start_time,
        )

    @overload
    def cluster_logs(
        self,
        cluster_id: int,
        account: str = None,
        scheduler: bool = True,
        workers: bool = True,
    ) -> Logs:
        ...

    @overload
    def cluster_logs(
        self,
        cluster_id: int,
        account: str = None,
        scheduler: bool = True,
        workers: bool = True,
    ) -> Awaitable[Logs]:
        ...

    def cluster_logs(
        self,
        cluster_id: int,
        account: str = None,
        scheduler: bool = True,
        workers: bool = True,
    ) -> Union[Logs, Awaitable[Logs]]:
        return self._sync(
            self._cluster_logs,
            cluster_id=cluster_id,
            account=account,
            scheduler=scheduler,
            workers=workers,
        )

    @track_context
    async def _cluster_logs(
        self,
        cluster_id: int,
        account: str = None,
        scheduler: bool = True,
        workers: bool = True,
    ) -> Logs:

        account = account or self.default_account

        # hits endpoint in order to get scheduler and worker instance names
        cluster_info = await self._get_cluster_details(
            cluster_id=cluster_id, account=account
        )

        scheduler_name = cluster_info["scheduler"]["instance"]["name"]
        worker_names = [
            worker["instance"]["name"] for worker in cluster_info["workers"]
        ]

        LabeledInstance = namedtuple("LabeledInstance", ("name", "label"))

        instances = []
        if scheduler and scheduler_name:
            instances.append(LabeledInstance(scheduler_name, "Scheduler"))
        if workers and worker_names:
            instances.extend(
                [
                    LabeledInstance(worker_name, worker_name)
                    for worker_name in worker_names
                ]
            )

        # this will hit logs endpoint for each instance in parallel, might be a problem for large cluster
        results = await asyncio.gather(
            *[
                self._instance_logs(account=account, instance_name=inst.name)
                for inst in instances
            ]
        )

        out = {
            instance_label: instance_log
            for (_, instance_label), instance_log in zip(instances, results)
        }

        return Logs(out)

    async def _instance_logs(self, account: str, instance_name: str) -> Log:
        response = await self._do_request(
            "GET",
            self.server
            + "/api/v2/instances/{}/instance/{}/logs".format(account, instance_name),
        )
        if response.status >= 400:
            await handle_api_exception(response)

        data = await response.json()

        messages = [logline.get("message", "") for logline in data]

        return Log(messages)

    @track_context
    async def _scale_up(self, cluster_id: int, n: int, account: str = None) -> Dict:
        """
        Increases the number of workers by ``n``.
        """
        account = account or self.default_account
        response = await self._do_request(
            "POST",
            f"{self.server}/api/v2/workers/account/{account}/cluster/{cluster_id}/",
            json={"n_workers": n},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        workers_info = await response.json()

        return {"workers": {w["name"] for w in workers_info}}

    @track_context
    async def _scale_down(
        self, cluster_id: int, workers: Set[str], account: str = None
    ) -> None:
        pass
        account = account or self.default_account
        response = await self._do_request(
            "DELETE",
            f"{self.server}/api/v2/workers/account/{account}/cluster/{cluster_id}/",
            params={"name": workers},
        )
        if response.status >= 400:
            await handle_api_exception(response)
