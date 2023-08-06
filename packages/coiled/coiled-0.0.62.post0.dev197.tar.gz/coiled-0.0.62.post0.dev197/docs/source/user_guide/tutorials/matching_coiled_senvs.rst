==================================
Local Coiled software environments
==================================

This article will show you how you can use an environment.yml file to duplicate 
one of the default Coiled software environments.

Coiled documentation contains additional information on using software 
environments with Coiled. Coiled also maintains 
a number of `default software environments <https://cloud.coiled.io/coiled/software>`_.

While it is often possible to use ``coiled install <account>/<sofware-environment>``
to create a coiled sofware environment locally that contains the same dependencies
as the coiled software environment, it is also easy to do this with an 
``environment.yml`` file and conda.

Using an environment.yml file
-----------------------------

On the `Coiled software environments page <https://cloud.coiled.io/coiled/software>`_, 
when you click on the 'eye' icon, you can view a Python dict with the 
conda channels and dependencies for each environment. 

.. figure:: ../images/view-senv-dependencies.png
   :width: 80%
   :alt: Viewing Software Environment Dependencies

   Coiled Software Envionments (click image to enlarge)

That can then be pasted into a script like this to create an ``environment.yml`` file:

.. code:: python

    coiled_env_name = "coiled-default"
    coiled_env = {
        "channels": ["conda-forge", "defaults"],
        "dependencies": [
            "bokeh>=2.1.1",
            "bottleneck",
            "cytoolz",
            "dask-image>=0.3.0",
            "dask-ml>=1.5.0",
            "dask=2021.5.0",
            "h5py",
            "lz4",
            "numba",
            "numpy>=1.19.0",
            "pandas>=1.1.0",
            "pillow>=7.2.0",
            "pip",
            "pyarrow>=0.15.1",
            "python-blosc",
            "python-graphviz",
            "python=3.9",
            "requests",
            "s3fs",
            "scikit-learn>=0.23.1",
            "xarray",
        ],
    }

    with open("environment.yml", "w") as output:
        output.write(f"name: {coiled_env_name} \n")
        output.write("channels: \n")
        for channel in coiled_env["channels"]:
            output.write(f"  - {channel} \n")
        output.write("dependencies: \n")
        for package in coiled_env["dependencies"]:
            output.write(f"  - {package} \n")

Which creates output like this:

.. code::

    name: coiled-default
    channels:
      - conda-forge
      - defaults
    dependencies:
      - bokeh>=2.1.1
      - bottleneck
      - cytoolz
      - dask-image>=0.3.0
      - dask-ml>=1.5.0
      - dask=2021.5.0
      - h5py
      - lz4
      - numba
      - numpy>=1.19.0
      - pandas>=1.1.0
      - pillow>=7.2.0
      - pip
      - pyarrow>=0.15.1
      - python-blosc
      - python-graphviz
      - python=3.9
      - requests
      - s3fs
      - scikit-learn>=0.23.1
      - xarray


Then, simply run ``conda env create -f environment.yml`` from a terminal 
(or Windows command prompt) to have conda create that sofware environment.

Note that you will still need to add any code-specific dependencies you
might have, and because not all of the dependencies are pinned, it is 
still possible for ``client = Client(cluster)`` to report version mismatches.
You should update your local packages accordingly.
