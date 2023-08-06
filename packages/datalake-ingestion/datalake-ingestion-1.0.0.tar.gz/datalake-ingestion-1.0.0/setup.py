# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datalake_ingestion']

package_data = \
{'': ['*'], 'datalake_ingestion': ['schemas/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'datalake-framework>=1.0.0,<2.0.0',
 'jsonschema>=4.2.1,<5.0.0',
 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'datalake-ingestion',
    'version': '1.0.0',
    'description': 'Datalake ingestion workflow',
    'long_description': None,
    'author': 'Didier SCHMITT',
    'author_email': 'dschmitt@equancy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
