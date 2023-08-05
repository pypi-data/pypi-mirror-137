# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_random_cat']

package_data = \
{'': ['*']}

install_requires = \
['httpx-socks>=0.7.3,<0.8.0', 'httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'nonebot-plugin-random-cat',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'alphaAE',
    'author_email': 'a1226123914@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
