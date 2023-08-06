# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bestpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bestpy',
    'version': '0.0.3',
    'description': "A package to find out what's best",
    'long_description': '# bestpy\n\n[![License](https://badgen.net/github/license/gustavwilliam/bestpy)](https://github.com/gustavwilliam/bestpy/blob/main/LICENSE)\n[![Linting](https://github.com/gustavwilliam/bestpy/actions/workflows/linting.yaml/badge.svg?branch=main)](https://github.com/gustavwilliam/bestpy/actions/workflows/linting.yaml)\n[![Testing](https://github.com/gustavwilliam/bestpy/actions/workflows/testing.yaml/badge.svg?branch=main)](https://github.com/gustavwilliam/bestpy/actions/workflows/testing.yaml)\n[![Build & Push](https://github.com/gustavwilliam/bestpy/actions/workflows/publish.yml/badge.svg)](https://github.com/gustavwilliam/bestpy/actions/workflows/publish.yml)\n[![Coverage Status](https://coveralls.io/repos/github/gustavwilliam/bestpy/badge.svg?branch=main)](https://coveralls.io/github/gustavwilliam/bestpy?branch=main)\n[![GitHub stars](https://img.shields.io/github/stars/gustavwilliam/bestpy?style=social&label=Star&maxAge=2592000)](https://github.com/gustavwilliam/bestpy/stargazers/)\n\nA module to prove your friends (or adversaries) wrong.\n\nEver needed to decide on what is the best thing out? That\'s exactly what bestpy does.\nWe may or may not try to make the answers support your view. Here\'s a quick demo:\n\n```python\n>>> best.language\n"python"\n>>> best.module\n"bestpy"\n```\n\n<details>\n<summary>Table of content</summary>\n\n## Table of content\n\n- [Installation](#installation)<br>\n- [Basic usage](#basic-usage)<br>\n- [Final words](#final-words)\n\n</details>\n\n## Installation\nThis is simple with pip. Just run the following in your command line or terminal:\n\n```\npip install bestpy\n```\n\nYou can also use your magic powers to get the module from the latest version of the source code using the following:\n\n```\npip install git+https://github.com/gustavwilliam/bestpy.git@main\n``` \nNote: you will likely need to restart your terminal before using the module\n\n## Basic usage\nWe were kind and made importing it super simple and nice. Just do the following to import bestpy, once the installation is complete:\n\n```python\n>>> from bestpy import best\n```\n\nNow you\'ll be ready to take on any of life\'s greatest challenges, all with the help of bestpy.\n\nHere\'s how you can find out some hard coded, fundamental laws of the universe:\n\n```py\n>>> best.year\n1984\n>>> best.phone\nBlackBerry\n```\n\nThere are also a few things that may sneakily check your preferences and adjust based on it, like the following.\nYou\'ll get your current OS back, since you obviously have a good taste in what OS you use.\n\n```python\n>>> best.os\n```\n\nThere are also a few ones that use randomness to find the truth, like this:\n\n```py\n>>> best.name\nGuido\n>>> best.name\nGustav\n```\n\nAt the end of the day, I\'d recommend just playing around with it and seeing what\'s available.\nWe\'ll be adding a lot of fun categories. If there\'s something you\'d like to see added,\nfeel free to open an issue or submit a PR. The available categories will expand over time,\nthanks to our awesome contributors.\n\n## Final words\nGood luck proving what things are actually best. Bestpy is never wrong,\nso you now know everything you need to use the single source of truth. \nFeel free to share what you create with bestpy. I can\'t wait to see what you do!\n\nMay the bestpy be with you. The bestpy is strong with this one.\n',
    'author': 'Gustav Odinger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gustavwilliam/bestpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
