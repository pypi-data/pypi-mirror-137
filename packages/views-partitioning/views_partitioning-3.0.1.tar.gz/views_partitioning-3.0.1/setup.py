# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_partitioning']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0', 'toolz>=0.11.1,<0.12.0', 'views-schema>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'views-partitioning',
    'version': '3.0.1',
    'description': '',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
