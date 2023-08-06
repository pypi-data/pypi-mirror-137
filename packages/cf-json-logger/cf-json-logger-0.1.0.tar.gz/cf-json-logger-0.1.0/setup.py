# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cf_json_logger']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'cf-json-logger',
    'version': '0.1.0',
    'description': 'Consistent web logs by Carnall Farrar Ltd.',
    'long_description': None,
    'author': 'Leo Edwards',
    'author_email': 'leo.edwards@carnallfarrar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
