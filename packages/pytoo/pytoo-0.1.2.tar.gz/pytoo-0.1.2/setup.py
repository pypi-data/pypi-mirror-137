# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytoo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytoo',
    'version': '0.1.2',
    'description': 'Example Python Library',
    'long_description': None,
    'author': 'Juraj Figura',
    'author_email': 'guitarist90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
