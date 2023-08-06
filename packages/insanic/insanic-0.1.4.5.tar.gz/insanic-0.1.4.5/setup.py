# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['insanic', 'insanic.commands']

package_data = \
{'': ['*']}

install_requires = \
['asyncmy>=0.2.3,<0.3.0',
 'cryptography>=36.0.1,<37.0.0',
 'sanic>=21.12.0,<22.0.0',
 'tortoise-orm>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'insanic',
    'version': '0.1.4.5',
    'description': 'Django like web framework based on Sanic and TortoiseORM',
    'long_description': None,
    'author': 'Dmitry Ovchinnikov',
    'author_email': 'mail@dimka.online',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
