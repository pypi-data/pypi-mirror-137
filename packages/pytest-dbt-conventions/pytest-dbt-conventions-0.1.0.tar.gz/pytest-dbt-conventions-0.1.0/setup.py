# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_dbt_conventions']

package_data = \
{'': ['*']}

install_requires = \
['artefacts>=1.0.0a2,<2.0.0', 'pytest>=6.2.5,<7.0.0']

entry_points = \
{'pytest11': ['dbt-conventions = pytest_dbt_conventions.plugin']}

setup_kwargs = {
    'name': 'pytest-dbt-conventions',
    'version': '0.1.0',
    'description': "A pytest plugin for linting a dbt project's conventions",
    'long_description': None,
    'author': 'Tom Waterman',
    'author_email': 'tjwaterman99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
