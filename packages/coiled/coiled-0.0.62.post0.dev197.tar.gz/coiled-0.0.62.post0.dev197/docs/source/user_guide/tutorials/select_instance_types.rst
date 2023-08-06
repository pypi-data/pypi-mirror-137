Selecting Instance Types
========================

.. note::
  This feature is currently experimental, with new features under active
  development.

When creating clusters, Coiled will match the instance type with the
requirements that you specify for CPU, Memory and GPU. Coiled chooses five
instance types to serve as a fallback when creating a Cluster since sometimes
a specific instance type might not be available in your cloud provider of choice.

You might not wish to get allocated random instance types, and you might want to
provide a list of instance types when creating a Cluster. This will allow you to
have more fine-grain control of the type of Cluster that you create.

With the keyword argument ``scheduler_vm_types`` and ``worker_vm_types``, you can
specify instance types for both the Scheduler and Workers. For example:

.. code:: python

  import coiled

  cluster = coiled.Cluster(
      scheduler_vm_types=["t3.large", "t3.xlarge"],
      worker_vm_types=["m5n.large", "m5zn.large"],
  )

It's recommended that you specify more than one instance type in your list to
avoid instance availability issues in the cloud provider and region that
you are using Coiled.

.. note::

  The order of the instance type will not be preserved when creating the cluster.

Instance types allowed
------------------------

Currently,  you are allowed to choose an instance type from a subset of all the
instance types available in the cloud provider configured on your account. In this list, you have
the most common instances used by users when creating Clusters with Coiled.

You can use the command :meth:`coiled.list_instance_types()` to see a list of all
allowed instance types for your configured cloud provider.

.. code:: python

  import coiled

  coiled.list_instance_types(min_cores=4)


You might be interested in reading :doc:`select_gpu_type`.
