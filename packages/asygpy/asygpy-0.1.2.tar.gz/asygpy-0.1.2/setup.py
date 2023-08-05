# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asygpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asygpy',
    'version': '0.1.2',
    'description': 'asyncio signal handlers for Windows and Unix',
    'long_description': None,
    'author': 'asleep-cult',
    'author_email': 'asleep.cult@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
