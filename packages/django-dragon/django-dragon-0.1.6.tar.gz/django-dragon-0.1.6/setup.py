# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dragon_cache_manager', 'dragon_cache_manager.management.commands']

package_data = \
{'': ['*'], 'dragon_cache_manager': ['templates/dragon/*']}

install_requires = \
['Django>=3.1.13,<4.0.0']

setup_kwargs = {
    'name': 'django-dragon',
    'version': '0.1.6',
    'description': 'A cache manager for Django admin',
    'long_description': '# Django Dragon Cache Manager 🐲\n\nA cache manager for Django admin.\n\n```\n"What did he promise you, a share of the treasure? As if it was his to give.\nI will not part with a single coin! Not one piece of it!"\n\n- Smaug\n```\n\n## Installation\n\n1. Install the package: `pip install django-dragon`\n2. Add `dragon_cache_manager` to your `INSTALLED_APPS` in Django settings.\n3. Add the Dragon URLs **before** `admin/`: `path(\'admin/dragon/\', include(\'dragon_cache_manager.urls\')),`\n4. Dragon will be accessible from `/admin/dragon`.\n\n## Configuration\n\nAll Dragon settings are prefixed by `DRAGON_`. \n\n### `USER_TEST_CALLBACK`\n\n`request` is the only argument and is the current `Request` instance.\n\nCallback for determining access to the Dragon pages.\n\nShould return `True` if allowed. Otherwise, `False`.\n\nBy default, any staff or superuser will be able to access Dragon.\n\n### `USER_IS_SUPERUSER`\n\nIndicates if a superuser is allowed to view Dragon.\n\nDefault: `True`\n\n### `USER_IS_STAFF`\n\nSame as `USER_IS_SUPERUSER` but for staff. \n\nDefault: `False`\n\n### `ENABLE_INDEX`\n\nIndicates if the Redis key index should be shown.\n\nDefault: `False`\n\n### `MAX_RESULTS`\n\nMaximum number of results to return on a key search.\n\nDefault: `50`\n\n## Commands\n\n### `load_test_cache`\n\nAdds X keys to a cache specified in `settings.CACHES`. \n\nFor each key, a random word from `dragon/management/commands/random_words.txt` will be used as the key and value.\n\n- `-c/--cache` - Specify the name of the cache to populate (defaults to all).\n- `-k/--keys` - Specify the number items to generate (defaults to 50).\n',
    'author': 'Logan Bibby',
    'author_email': 'lbibby@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lenders-Cooperative/django-dragon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
