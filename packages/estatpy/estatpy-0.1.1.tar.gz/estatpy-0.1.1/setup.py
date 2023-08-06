# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estatpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'estatpy',
    'version': '0.1.1',
    'description': 'e-Stat API Client',
    'long_description': '# estatpy\n\nThis is a package with no contents yet. I only registered it first to get the package name.\n',
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
