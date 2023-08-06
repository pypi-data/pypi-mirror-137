# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_typechecker']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.931,<0.932', 'pyright>=0.0.13,<0.0.14', 'pytest>=6.2.5,<7.0.0']

entry_points = \
{'pytest11': ['pytest_typechecker = pytest_typechecker.plugin']}

setup_kwargs = {
    'name': 'pytest-typechecker',
    'version': '0.3.3',
    'description': 'Run type checkers on specified test files',
    'long_description': '# pytest-typechecker\n\nthis is a plugin for pytest that allows you to create tests\nthat verify how a type checker responds to your code.\n\nThis currently supports these type checkers:\n\n* pyright\n* mypy\n\n## File name format\n\nthis plugin looks for files starting with `test` and ending with `types.py` or `types_xfail.py`.\nfor example `test_something_types.py`\n\n### global xfail\n\nif you want to mark the hole test as `xfail` end it with `types_xfail.py`, for example.\n\n```python\n# test_wrong_types_xfail.py\n\nx: 123 = "abc"\ny: str = 123\n```\n\n### Only run specific checkers\n\nif you include the name of a checker with `_` around it only those checkers will be run.\nfor example `test_recursion_pyright_types.py`\n\n### xfail specific checkers\n\nif you provide a `x` before the checker name, it will be run in xfail mode.\nfor example `test_recursion_xmypy_types.py` will run all checkers, but mark the mypy one as `xfail`\n\nif you only want to run mypy and have it be xfail use this workaround: `test_recursion_mypy_types_xfail.py`\n\nthis can be combined, for example `test_recursion_pyright_xmypy_types.py` will run only pyright and mypy, but run mypy in xfail mode.\n\n### dont run specific checkers\n\nif you provide a `n` before the checker name, it will not be run.\nfor example `test_recursion_nmypy_types.py` will run all checkers, except mypy.\n',
    'author': 'vivax',
    'author_email': 'vivax3794@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vivax3794/pytest-typechecker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
