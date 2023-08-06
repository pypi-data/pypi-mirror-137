# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gateau_api',
 'gateau_api.common',
 'gateau_api.game_ram',
 'gateau_api.game_ram.pokemon',
 'gateau_api.routers']

package_data = \
{'': ['*']}

install_requires = \
['Pyrebase4>=4.5.0,<5.0.0',
 'bidict>=0.21.4,<0.22.0',
 'fastapi-camelcase>=1.0.5,<2.0.0',
 'fastapi>=0.71.0,<0.72.0',
 'firebase-admin>=5.2.0,<6.0.0',
 'uvicorn>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'gateau-api',
    'version': '0.15.1',
    'description': '',
    'long_description': None,
    'author': 'Kevin Duff',
    'author_email': 'kevinkelduff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
