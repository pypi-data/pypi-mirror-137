Creating Pipelines
==================
|
Pipeline creation and management in Control Hub is extremely similar to the syntax and structure
:ref:`used in DataCollector <sdc_pipeline>`.

Instantiating a Pipeline Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step of creating a pipeline on Control Hub is to instantiate a :py:class:`streamsets.sdk.sch_models.PipelineBuilder`
instance. This class handles the majority of the pipeline configuration on your behalf by building the initial JSON
representation of the pipeline, and setting default values for essential properties (instead of requiring each to be
set manually). Use the :py:meth:`streamsets.sdk.ControlHub.get_pipeline_builder` method to instantiate the builder
object with the address of an Authoring Data Collector or an Authoring Transformer for the pipeline:

.. code-block:: python

    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_url='<data_collector_address>')

Or

.. code-block:: python

    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_url='<transformer_address>')

If you have a particular :py:class:`streamsets.sdk.DataCollector` instance to use as the Authoring Data Collector
for the pipeline, it can be done as follows:

.. code-block:: python

    sdc = sch.data_collectors.get(url='<data_collector_address>')

    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_url=sdc.url)

Similarly, you can instantiate the builder object with a particular :py:class:`streamsets.sdk.Transformer` instance
as the Authoring Transformer for the pipeline:

.. code-block:: python

    transformer = sch.transformers.get(url='<transformer_address>')

    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_url=transformer.url)

Adding Stages to the Pipeline Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding stages to the pipeline can be done by calling the :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.add_stage`
method - see the API reference for this method for details on the arguments this method takes.

As shown in the :ref:`first example <first-example>`, the simplest type of pipeline directs one origin into one
destination. For this example, you can do this with ``Dev Raw Data Source`` origin and ``Trash`` destination,
respectively:

.. code-block:: python

    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    trash = pipeline_builder.add_stage('Trash')

Connecting the Stages
~~~~~~~~~~~~~~~~~~~~~

With :py:class:`streamsets.sdk.sch_models.SchSdcStage` instances in hand, you can connect them by using the ``>>``
operator. Connecting the ``Dev Raw Data Source`` origin and ``Trash`` destination from the example above would look
like the following:

.. code-block:: python

    dev_raw_data_source >> trash

**Output:**

.. code-block:: python

    <com_streamsets_pipeline_stage_destination_devnull_NullDTarget (instance_name=Trash_01)>

You can also connect a stage's event stream to another stage, like a pipeline finisher, using a similar convention. To
connect a stage's event stream to another stage, use the ``>=`` operator:

.. code-block:: python

    pipeline_finisher = pipeline_builder.add_stage('Pipeline Finisher Executor')
    dev_raw_data_source >= pipeline_finisher

**Output:**

.. code-block:: python

    True

Once the stages are connected, you can build the :py:class:`streamsets.sdk.sch_models.Pipeline` instance with
the :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.build` method:

.. code-block:: python

    pipeline = pipeline_builder.build('My first pipeline')
    pipeline

**Output:**

.. code-block:: python

    <Pipeline (pipeline_id=None, commit_id=None, name=My first pipeline, version=None)>

Add the Pipeline to Control Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, to add this pipeline to your Control Hub organization, pass it to the :py:meth:`streamsets.sdk.ControlHub.publish_pipeline`
method:

.. code-block:: python

    sch.publish_pipeline(pipeline, commit_message='First commit of my first pipeline')
    
**Output:**

.. code-block:: python

    <streamsets.sdk.sch_api.Command object at 0x7f8f2e0579b0>

