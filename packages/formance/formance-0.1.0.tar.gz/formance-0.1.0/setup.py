# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formance']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'formance',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'limonyellow',
    'author_email': 'lemon@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/limonyellow/formance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
