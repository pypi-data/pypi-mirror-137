.. _gpus:

GPUs
====

Coiled supports running computations with GPU-enabled machines. In principle, 
doing this is as simple as setting ``worker_gpu=1`` in the ``coiled.Cluster()`` 
constructor:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(
       ...,
       worker_gpu=1,
   )

.. note::

    When asking for GPU enabled workers, Coiled will always use on demand instances
    instead of the default Spot instances. If you want to use spot instances you can
    add ``backend_options={"spot": True}`` to the ``coiled.Cluster`` constructor.

But in practice there are additional considerations.

Getting Started 
---------------

First, note that free individual cloud accounts do not 
have GPU access enabled (see Account Access, below).

Next, you will need a suitable software environment. The specifics will vary
with your need.  An example suitable for some initial work and testing is given 
here:

.. code-block:: python

   import coiled

   # Create a software environment with GPU accelerated libraries
   # and CUDA drivers installed
   coiled.create_software_environment(
       name="gpu-test",
       container="gpuci/miniconda-cuda:11.2-runtime-ubuntu20.04",
       conda={
           "channels": [
               "rapidsai",
               "conda-forge",
               "defaults",
           ],
           "dependencies": [
               "dask",
               "dask-cuda",
               "cupy",
               "cudatoolkit=11.2",
           ],
       },
   )

More information on GPU software environments is given below.

With a suitable software environment, creating a cluster is straightforward.
Simply set ``worker_gpu=1``. Currently, Coiled only permits a single GPU per worker.  

.. code-block:: python

   # Create a Coiled cluster that uses
   # a GPU-compatible software environment
   cluster = coiled.Cluster(
       scheduler_cpu=2,
       scheduler_memory="4 GiB",
       worker_cpu=4,
       worker_memory="16 GiB",
       worker_gpu=1,
       worker_class="dask_cuda.CUDAWorker",
       software="gpu-test",
   )

If desired, the cluster specified above can be tested with the following computation:

.. code-block:: python

    from dask.distributed import Client


    def test_gpu():
        import numpy as np
        import cupy as cp

        x = cp.arange(6).reshape(2, 3).astype("f")
        return cp.asnumpy(x.sum())


    client = Client(cluster)

    f = client.submit(test_gpu)
    f.result()

If successful, this should return ``array(15., dtype=float32)``.

You can also verify that workers are using GPUs with the following command:

.. code-block:: python

    cluster.scheduler_info["workers"]

.. note::

    If you are a member of more than one team (remember, you are automatically a
    member of your own personal account), you must specify the team under which
    to create the cluster (defaults to your personal account). You can do this
    with either the ``account=`` keyword argument, or by adding it as a prefix
    to the name of the cluster, such as ``name="<account>/<cluster-name>"``.
    Learn more about :doc:`teams <teams>`.

GPUs + Afar
-----------

`afar <https://github.com/eriknw/afar>`_ allows you to run code on a remote Dask cluster. This 
means that you can run gpu code on a Coiled cluster without having to have a GPU where the 
client is hosted (your laptop for example). 

First, you will need to create a software environment that contains all the GPU
software you need to run your computations, but also you will need ``afar>=0.6.1``. We 
recommend basing your software environment on a ``RAPIDS`` container. You choose your 
image using the `Rapids release Selector <https://rapids.ai/start.html#get-rapids>`_. The 
choice of software environment packages will vary depending on your needs. An example 
we tested uses the following:


.. code-block:: python

    import coiled

    coiled.create_software_environment(
        name="gpu-afar-test",
        container="rapidsai/rapidsai-nightly:21.10-cuda11.2-runtime-ubuntu20.04-py3.8",
        conda_env_name="rapids",
        conda={
            "channels": ["conda-forge"],
            "dependencies": ["afar=0.6.1"],
        },
    )

Then we can create a cluster as shown before but now using ``software="gpu-afar-test"``, 
and you can test this with the following computations

read_csv() with dask-cudf
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from dask.distributed import Client
    import afar

    client = Client(cluster)

    with afar.run, remotely:
        import dask_cudf

        df = dask_cudf.read_csv(
            "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.csv",
            parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"],
            storage_options={"anon": True},
            assume_missing=True,
        ).persist()

        res = (
            df.groupby("passenger_count").tip_amount.mean().compute().to_pandas()
        )  # return as pandas dataframe

    res.result()


Notice that in the ``df.groupby(...)`` line we convert the resulting cuDF dataframe to a 
pandas dataframe. This is needed to be able to bring back the object to the client 
which does not know about any CUDA or GPUs software. 

cupy arrays
~~~~~~~~~~~

.. code-block:: python

    from dask.distributed import Client
    import afar

    client = Client(cluster)

    with afar.run, remotely:
        import cupy as cp

        x_gpu = cp.array([1, 2, 3])
        l2_gpu = cp.linalg.norm(x_gpu)
        l2_cpu = cp.asnumpy(l2_gpu)  # return as numpy array

    l2_cpu.result()



Software Environments
---------------------

When creating a software environment for GPUs, you will need to install the GPU
accelerated libraries needed (e.g. PyTorch, RAPIDS, XGBoost, Numba,
etc.) and also ensure that the container in use has the
correct CUDA drivers installed.

Coiled infrastructure generally runs with CUDA version 10.2. If you already have
a Docker image with your desired software and the drivers match, then you should
be good to go.

If you plan to make a software environment with conda or pip packages then we
recommend basing your software environment on a container with the correct
drivers installed. For example: ``gpuci/miniconda-cuda:10.2-runtime-ubuntu18.04``


.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="gpu-test",
       container="gpuci/miniconda-cuda:10.2-runtime-ubuntu18.04",
       conda={
           "channels": ["conda-forge", "rapidsai", "defaults"],
           "dependencies": ["dask", "dask-cuda", "cupy", "cudatoolkit=10.2"],
       },
   )


Current Hardware
----------------

Currently Coiled mostly deploys cost efficient T4 GPUs by default. If you are
interested in using higher performance GPUs then please `contact us`_.

Account Access
--------------

Free individual accounts do not have GPU access turned on by default. If you are
interested in testing out GPU access then please `contact us`_.

If you have been granted access it may be as part of a team account. If so,
please be aware that you will have to specify the account under which you want
to create your cluster in the ``coiled.Cluster`` constructor:

.. code-block:: python

   cluster = coiled.Cluster(
       scheduler_cpu=2,
       scheduler_memory="4 GiB",
       worker_cpu=4,
       worker_memory="16 GiB",
       worker_gpu=1,
       software="gpu-test",
       account="MY-TEAM-ACCOUNT",
   )

.. _contact us: sales@coiled.io
