# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bestpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bestpy',
    'version': '0.0.1',
    'description': "A package to find out what's best",
    'long_description': None,
    'author': 'Gustav Odinger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
