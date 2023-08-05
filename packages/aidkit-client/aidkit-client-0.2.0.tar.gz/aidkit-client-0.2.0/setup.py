# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aidkit_client', 'aidkit_client._endpoints', 'aidkit_client.resources']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==8.4',
 'httpx>=0.21.1,<0.22.0',
 'pandas>=1.1.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'aidkit-client',
    'version': '0.2.0',
    'description': 'aidkit for your CI/CD and j-notebooks.',
    'long_description': '![aidkit](https://www.neurocat.ai/wp-content/uploads/2018/11/addkit-hori.png)\n\naidkit is an MLOps platform that allows you to assess and defend against threads\nand vulnerabilities of AI models before they deploy to production.\naidkit-client is a companion python client library to seamlessly integrate with\naidkit in python projects.\n\n## Changelog\n\nBreaking changes are written in bold text.\n\n### Version 0.2.0\n\n* **Rename `resources.Report.table` to `resources.Report.table_string`.**\n* Add `resources.Report.table` function returning a pandas dataframe.\n* **Move `endpoints` module to `_endpoints`.**\n* **Remove class `aidkit.Aidkit`.**\n* Add docstrings.\n* **Rename `exceptions.AidkitCLIError` to `exceptions.AidkitClientError`.**\n* Add class `exceptions.AuthenticationError`, which is raised whenever the client fails to authenticate to the server.\n* Include http error code and http body returned by the aidkit server in all exceptions.\n* Make http request timeout configurable.\n* Add `id` and `name` properties to resources.\n* Add option to use progress bar in `PipelineRun.report` and `MLModelVersion.upload`.\n* Add `PipelineRun.get_progress` method, which can be used to check how far a pipeline run has progressed.\n* **Update web API version**.\n* Add functionality to manage datasets and subsets from the client including data upload with added resources\n`Dataset` and `Observation` and updated resource `Subset`.\n* Add functionality to download artifacts from the report.\n',
    'author': 'neurocat GmbH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
