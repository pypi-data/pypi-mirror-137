.. _configuration:

=============
Configuration
=============

``coiled`` uses Dask's built in
`configuration system <https://docs.dask.org/en/latest/configuration.html>`_ to
manage configuration options. Namely, configuration settings can be set:

- In the configuration file ``~/.config/dask/coiled.yaml``
- Using environment variables like ``DASK_COILED__ACCOUNT="alice"``
- Configured directly in Python code using ``dask.config.set``


Configuration reference
-----------------------

The YAML snippet below shows the possible configuration options, along with
their default values:

.. code-block:: yaml

    coiled:
      account: null                      # Default account
      backend-options: null              # Default backend_options
      server: https://cloud.coiled.io    # Default server
      token: ""                          # Default token
      user: ""                           # Default username


The ``account`` option
^^^^^^^^^^^^^^^^^^^^^^

If you are part of a :doc:`teams account <teams>`, and you know that you will
launch clusters mostly in your team account, you can set the ``account`` option
to point to to your team slug. By setting this option, the default behavior of
launching clusters or any other service in your account is overwritten and will
use the team account instead.

You can pass your team account slug in the  ``coiled login`` command line tool
with the ``-a`` or ``--account`` flag as follows:

.. code-block:: bash

    $ coiled login --account team_slug


The ``account`` keyword argument is also accepted in most of our :doc:`API <api>`,
this keyword argument gives you the flexibility of switching between your team
and personal accounts when using the Coiled API.

.. note::

  You don't need a distinct token to use your team account -- please continue to
  use your personal token


The ``backend-options`` option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several :doc:`backend specific <backends>` options that you can
specify to customize Coiled's behaviour. For example, if you are using a
specific region to keep your assets and you want always to use this region when
using Coiled, then you could add it to this configuration file to overwrite
Coiled's default region choice.

.. code-block::yaml

    coiled:
      account: null
      backend-options:
        region: us-east-1
      server: https://cloud.coiled.io    # Default server
      token: ""                          # Default token
      user: ""


.. note::

  Make sure to check if your region is supported in the
  :doc:`backends documentation <backends>`. If your region is not supported you
  can :doc:`get in touch with us <support>`.
