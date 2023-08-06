# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodb_atlas_api_sdk']

package_data = \
{'': ['*']}

install_requires = \
['compose-x-common>=0.4,<0.5', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'mongodb-atlas-api-sdk',
    'version': '0.0.1',
    'description': 'MongoDB Atlas Admin API SDK',
    'long_description': '=============\nAtlas API SDK\n=============\n\n\n.. image:: https://img.shields.io/pypi/v/atlas_api_sdk.svg\n        :target: https://pypi.python.org/pypi/atlas_api_sdk\n\nAtlas Admin API SDK\n\n\n* Free software: MPL-2.0\n* Documentation: https://atlas-api-sdk.readthedocs.io.\n\n\nFeatures\n--------\n\n* DatabaseUser management (CRUD-L)\n* Database User Roles / Scopes updates\n',
    'author': 'johnpreston',
    'author_email': 'john@ews-network.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
