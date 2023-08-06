# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_on_dfs']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'pandas>=1.4.0,<2.0.0', 'sql-metadata>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'sql-on-dfs',
    'version': '0.2.0',
    'description': 'For when you want to execute an arbitrary SQL query on one or more Pandas DataFrames',
    'long_description': None,
    'author': 'max',
    'author_email': 'mepstein68@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MaxPowerWasTaken/sqlondfs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
