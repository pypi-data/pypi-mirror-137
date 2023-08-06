# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_typechecker']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.5,<7.0.0']

entry_points = \
{'pytest11': ['pytest_typechecker = pytest_typechecker.plugin']}

setup_kwargs = {
    'name': 'pytest-typechecker',
    'version': '0.1.0',
    'description': 'Run type checkers on specified test files',
    'long_description': None,
    'author': 'vivax',
    'author_email': 'vivax3794@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
