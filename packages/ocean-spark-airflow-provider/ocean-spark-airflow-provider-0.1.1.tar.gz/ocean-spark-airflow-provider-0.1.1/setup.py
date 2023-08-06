# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocean_spark']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=1', 'requests>=2.0.0,<3.0.0']

entry_points = \
{'airflow.plugins': ['ocean_spark = ocean_spark.plugins:OceanSparkPlugin'],
 'apache_airflow_provider': ['provider_info = ocean_spark:get_provider_info']}

setup_kwargs = {
    'name': 'ocean-spark-airflow-provider',
    'version': '0.1.1',
    'description': 'Apache Airflow connector for Ocean Spark',
    'long_description': '# Airflow connector for Ocean Apache Spark\n\nAn Airflow plugin and provider to launch and monitor Spark\napplications on the [Ocean for\nSpark](https://spot.io/products/ocean-apache-spark/).\n\n## Compatibility\n\n`ocean-spark-airflow-provider` is compatible with both Airflow 1 and\nAirflow 2. it is detected as an Airflow plugin by Airflow 1 and up,\nand as a provider by Airflow 2.\n\n\n## Installation\n\n```\npip install ocean-spark-airflow-provider\n```\n\n## Usage\n\nFor general usage of Ocean for Spark, refer to the [official\ndocumentation](https://docs.spot.io/ocean-spark/getting-started/?id=get-started-with-ocean-for-apache-spark).\n\n### Setting up the connection\n\nIn the connection menu, register a new connection of type **Ocean For\nSpark**. The default connection name is `ocean_spark_default`. You will\nneed to have:\n\n - The Ocean Spark cluster ID of the cluster you just created (of the\n   format `osc-e4089a00`). You can find this in the console in the\n   [list of\n   clusters](https://docs.spot.io/ocean-spark/product-tour/manage-clusters),\n   or by using the [Get Cluster\n   List](https://docs.spot.io/api/#operation/OceanSparkClusterList) in\n   the API.\n - [A Spot\n   token](https://docs.spot.io/administration/api/create-api-token?id=create-an-api-token)\n   to interact with Spot API.\n \n![connection setup dialog](./images/connection_setup.png) \n\nThe **Ocean For Spark** connection type is not available for Airflow\n1, instead create an **HTTP** connection and fill your cluster id as\n**host** your API token as **password**.\n\nYou will need to create a separate connection for every Ocean Spark\ncluster that you plan to use with Airflow.  In the\n`OceanSparkOperator`, you can select which Ocean Spark connection to\nuse with the `connection_name` argument (defaults to\n`ocean_spark_default`).\n\n### Using the operator\n\n```python\nfrom airflow import __version__ as airflow_version\nif airflow_version.starts_with("1."):\n    # Airflow 1, import as plugin\n    from airflow.operators.ocean_spark import OceanSparkOperator\nelse:\n    # Airflow 2\n    from ocean_spark.operators import OceanSparkOperator\n    \n# DAG creation\n    \nspark_pi_task = OceanSparkOperator(\n    job_id="spark-pi",\n    task_id="compute-pi",\n    dag=dag,\n    config_overrides={\n        "type": "Scala",\n        "sparkVersion": "3.2.0",\n        "image": "gcr.io/datamechanics/spark:platform-3.2-latest",\n        "imagePullPolicy": "IfNotPresent",\n        "mainClass": "org.apache.spark.examples.SparkPi",\n        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",\n        "arguments": ["10000"],\n        "driver": {\n            "cores": 1,\n        },\n        "executor": {\n            "cores": 2,\n            "instances": 1,\n        },\n    },\n)\n```\n\nmore examples are available for [Airflow 1](./deploy/airflow1/example_dags) and [Airflow 2](./deploy/airflow2/dags).\n\n## Test locally\n\nYou can test the plugin locally using the docker compose setup in this\nrepository. Run `make serve_airflow2` at the root of the repository to\nlaunch an instance of Airflow 2 with the provider already installed.\n',
    'author': 'Ocean for Spark authors',
    'author_email': 'clement.rezvoy@netapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://spot.io/products/ocean-apache-spark/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.15,<4.0.0',
}


setup(**setup_kwargs)
