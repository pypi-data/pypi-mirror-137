Self-Managed Deployments
========================
|
You can create a self-managed deployment for an active self-managed environment.
When using a self-managed deployment, you take full control of procuring the resources needed to run engine instances.

When you create a self-managed deployment, you define the engine type, version, and configuration to deploy.
You also select the installation type to use - either a tarball or a Docker image

For more details, refer to the `StreamSets DataOps Platform Documentation <https://docs.streamsets.com/portal/#platform-controlhub/controlhub/UserGuide/Deployments/Self.html#concept_xnm_v5z_gpb>`_.

Data Collector with Docker Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
The SDK is designed to mirror the UI workflow. This section shows you how to create a self-managed deployment for
Data Collector using the Docker Image installation type in the UI and how to achieve the same using StreamSets DataOps
Platform SDK for Python code step by step.

Define Deployment
-----------------

In the UI, a deployment is defined as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_define_deployment_sdc.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='DC',
                                          engine_version='4.1.0',
                                          deployment_tags=['self-managed-tag'])

Configure Engine
-----------------

In the UI, engines for deployments are configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_configure_engine.png

|
In the above UI, when you click on `3 stage libraries selected`, the following dialog opens and allows you to select stage libraries.

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_stage_lib_selection_screen.png

|
In the above UI, once you select JDBC and click on any of the '+' signs, then it shows the following:

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_stage_lib_selection_as_a_list.png
|
This multi-step process of selecting stage libraries can be achieved using the SDK as follows:

.. code-block:: python

    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

Configure Install Type
----------------------

In the UI, Install Type for a deployment is configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/common/configure_install_type_docker.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment.install_type = 'DOCKER'

Review and Launch
-----------------

In the UI, a deployment can be reviewed and launched as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_review_and_launch_sdc.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Complete example for Data Collector with Docker Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
To create a new :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object and add it to Control Hub, use the
:py:class:`streamsets.sdk.sch_models.DeploymentBuilder` class.
Use the :py:meth:`streamsets.sdk.ControlHub.get_deployment_builder` method to instantiate the builder object:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

Next, retrieve the :py:class:`streamsets.sdk.sch_models.SelfManagedEnvironment` object which represents an active
self-managed environment where engine instances will be deployed, pass it to the
:py:meth:`streamsets.sdk.sch_models.DeploymentBuilder.build` method along with other parameters, and pass the
resulting :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object to the
:py:meth:`streamsets.sdk.ControlHub.add_deployment` method:


.. code-block:: python

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='DC',
                                          engine_version='4.1.0',
                                          deployment_tags=['self-managed-tag'])
    deployment.install_type = 'DOCKER'
    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Data Collector with Tarball
~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
The SDK is designed to mirror the UI workflow. This section shows you how to create a self-managed deployment for
Data Collector using the Tarball installation type in the UI and how to achieve the same using StreamSets DataOps
Platform SDK for Python code step by step.

Define Deployment
-----------------

In the UI, a deployment is defined as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_define_deployment_sdc.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='DC',
                                          engine_version='4.1.0',
                                          deployment_tags=['self-managed-tag'])

Configure Engine
-----------------

In the UI, engines for deployments are configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_configure_engine.png

|
In the above UI, when you click on `3 stage libraries selected`, the following dialog opens and allows you to select stage libraries.

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_stage_lib_selection_screen.png

|
In the above UI, once you select JDBC and click on any of the '+' signs, then it shows the following:

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_stage_lib_selection_as_a_list.png
|
This multi-step process of selecting stage libraries can be achieved using the SDK as follows:

.. code-block:: python

    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

Configure Install Type
----------------------

In the UI, Install Type for a deployment is configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/common/configure_install_type_tarball.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment.install_type = 'TARBALL'

Review and Launch
-----------------

In the UI, a deployment can be reviewed and launched as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_review_and_launch_sdc.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Complete example for Data Collector with Tarball
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
To create a new :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object and add it to Control Hub, use the
:py:class:`streamsets.sdk.sch_models.DeploymentBuilder` class.
Use the :py:meth:`streamsets.sdk.ControlHub.get_deployment_builder` method to instantiate the builder object:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

Next, retrieve the :py:class:`streamsets.sdk.sch_models.SelfManagedEnvironment` object which represents an active
self-managed environment where engine instances will be deployed, pass it to the
:py:meth:`streamsets.sdk.sch_models.DeploymentBuilder.build` method along with other parameters, and pass the
resulting :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object to the
:py:meth:`streamsets.sdk.ControlHub.add_deployment` method:


.. code-block:: python

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='DC',
                                          engine_version='4.1.0',
                                          deployment_tags=['self-managed-tag'])
    deployment.install_type = 'TARBALL'
    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Transformer with Docker Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
The SDK is designed to mirror the UI workflow. This section shows you how to create a self-managed deployment for
Transformer using the Docker Image installation type in the UI and how to achieve the same using StreamSets DataOps
Platform SDK for Python code step by step.

Define Deployment
-----------------

In the UI, a deployment is defined as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_define_deployment_transformer.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='TF',
                                          engine_version='4.1.0',
                                          scala_binary_version='2.11',
                                          deployment_tags=['self-managed-tag'])

Configure Engine
-----------------

In the UI, engines for deployments are configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_configure_engine.png

|
In the above UI, when you click on `3 stage libraries selected`, the following dialog opens and allows you to select stage libraries.

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_transformer_stage_lib_selection_screen.png

|
In the above UI, once you select JDBC and click on any of the '+' signs, then it shows the following:

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_transformer_stage_lib_selection_as_a_list.png
|
This multi-step process of selecting stage libraries can be achieved using the SDK as follows:

.. code-block:: python

    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

Configure Install Type
----------------------

In the UI, Install Type for a deployment is configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/common/configure_install_type_docker.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment.install_type = 'DOCKER'

Review and Launch
-----------------

In the UI, a deployment can be reviewed and launched as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_review_and_launch_transformer.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Complete example for Transformer with Docker Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
To create a new :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object and add it to Control Hub, use the
:py:class:`streamsets.sdk.sch_models.DeploymentBuilder` class.
Use the :py:meth:`streamsets.sdk.ControlHub.get_deployment_builder` method to instantiate the builder object:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

Next, retrieve the :py:class:`streamsets.sdk.sch_models.SelfManagedEnvironment` object which represents an active
self-managed environment where engine instances will be deployed, pass it to the
:py:meth:`streamsets.sdk.sch_models.DeploymentBuilder.build` method along with other parameters, and pass the
resulting :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object to the
:py:meth:`streamsets.sdk.ControlHub.add_deployment` method:


.. code-block:: python

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='TF',
                                          engine_version='4.1.0',
                                          scala_binary_version='2.11',
                                          deployment_tags=['self-managed-tag'])
    deployment.install_type = 'DOCKER'
    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Transformer with Tarball
~~~~~~~~~~~~~~~~~~~~~~~~
|
The SDK is designed to mirror the UI workflow. This section shows you how to create a self-managed deployment for
Transformer using the Tarball installation type in the UI and how to achieve the same using StreamSets DataOps
Platform SDK for Python code step by step.

Define Deployment
-----------------

In the UI, a deployment is defined as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_define_deployment_transformer.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='TF',
                                          engine_version='4.1.0',
                                          scala_binary_version='2.11',
                                          deployment_tags=['self-managed-tag'])

Configure Engine
-----------------

In the UI, engines for deployments are configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_configure_engine.png

|
In the above UI, when you click on `3 stage libraries selected`, the following dialog opens and allows you to select stage libraries.

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_transformer_stage_lib_selection_screen.png

|
In the above UI, once you select JDBC and click on any of the '+' signs, then it shows the following:

.. image:: ../../../_static/images/set_up/deployments/common/creation_configure_engine_transformer_stage_lib_selection_as_a_list.png
|
This multi-step process of selecting stage libraries can be achieved using the SDK as follows:

.. code-block:: python

    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

Configure Install Type
----------------------

In the UI, Install Type for a deployment is configured as seen below:

.. image:: ../../../_static/images/set_up/deployments/common/configure_install_type_tarball.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    deployment.install_type = 'TARBALL'

Review and Launch
-----------------

In the UI, a deployment can be reviewed and launched as seen below:

.. image:: ../../../_static/images/set_up/deployments/self_managed_deployments/creation_review_and_launch_transformer.png

|
The same effect can be achieved by using the SDK as seen below:

.. code-block:: python

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)

Complete example for Transformer with Tarball
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|
To create a new :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object and add it to Control Hub, use the
:py:class:`streamsets.sdk.sch_models.DeploymentBuilder` class.
Use the :py:meth:`streamsets.sdk.ControlHub.get_deployment_builder` method to instantiate the builder object:

.. code-block:: python

    deployment_builder = sch.get_deployment_builder(deployment_type='SELF')

Next, retrieve the :py:class:`streamsets.sdk.sch_models.SelfManagedEnvironment` object which represents an active
self-managed environment where engine instances will be deployed, pass it to the
:py:meth:`streamsets.sdk.sch_models.DeploymentBuilder.build` method along with other parameters, and pass the
resulting :py:class:`streamsets.sdk.sch_models.SelfManagedDeployment` object to the
:py:meth:`streamsets.sdk.ControlHub.add_deployment` method:


.. code-block:: python

    # sample_environment is an instance of streamsets.sdk.sch_models.SelfManagedEnvironment
    deployment = deployment_builder.build(deployment_name='Sample Deployment',
                                          deployment_type='SELF',
                                          environment=sample_environment,
                                          engine_type='TF',
                                          engine_version='4.1.0',
                                          scala_binary_version='2.11',
                                          deployment_tags=['self-managed-tag'])
    deployment.install_type = 'TARBALL'
    # Optional - add sample stage libs
    deployment.engine_configuration.stage_libs = ['jdbc']

    sch.add_deployment(deployment)
    # Optional - equivalent to clicking on 'Start & Generate Install Script'
    sch.start_deployment(deployment)