# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dragon_cache_manager', 'dragon_cache_manager.management.commands']

package_data = \
{'': ['*'], 'dragon_cache_manager': ['templates/dragon/*']}

install_requires = \
['Django==3.1.13', 'django-redis==5.0.0', 'redis-py-cluster==2.1.3']

setup_kwargs = {
    'name': 'django-dragon',
    'version': '0.1.1',
    'description': 'A cache manager for Django admin',
    'long_description': None,
    'author': 'Logan Bibby',
    'author_email': 'lbibby@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
