# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datalake', 'datalake.provider']

package_data = \
{'': ['*']}

install_requires = \
['Babel>=2.9.1,<3.0.0',
 'azure-eventhub>=5.6.1,<6.0.0',
 'azure-identity>=1.7.1,<2.0.0',
 'azure-keyvault-secrets>=4.3.0,<5.0.0',
 'azure-storage-blob>=12.9.0,<13.0.0',
 'boto3>=1.20.26,<2.0.0',
 'google-cloud-monitoring>=2.8.0,<3.0.0',
 'google-cloud-pubsub>=2.9.0,<3.0.0',
 'google-cloud-secret-manager>=2.8.0,<3.0.0',
 'google-cloud-storage>=1.43.0,<2.0.0',
 'influxdb-client>=1.24.0,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'datalake-framework',
    'version': '1.0.0',
    'description': 'Datalake Framework',
    'long_description': None,
    'author': 'Didier SCHMITT',
    'author_email': 'dschmitt@equancy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.equancy.cloud/equancy/data-technologies/datalake-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
