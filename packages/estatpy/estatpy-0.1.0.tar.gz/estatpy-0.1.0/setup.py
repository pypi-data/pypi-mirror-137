# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estatpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'estatpy',
    'version': '0.1.0',
    'description': 'e-Stat API Client',
    'long_description': '# estatpy: Project Description\n\n[![PyPI Version](https://img.shields.io/pypi/v/estatpy.svg)](https://pypi.org/pypi/estatpy/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/estatpy.svg)](https://pypi.org/pypi/estatpy/)\n[![License](https://img.shields.io/pypi/l/estatpy.svg)](https://github.com/poyo46/estatpy/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## Installation\n\nestatpy is available on PyPI:\n\n```console\n$ pip install estatpy\n```\n\nYou can also use [poetry](https://python-poetry.org/) to add it to a specific Python project.\n\n```console\n$ poetry add estatpy\n```\n',
    'author': 'poyo46',
    'author_email': 'poyo4rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poyo46/estatpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
