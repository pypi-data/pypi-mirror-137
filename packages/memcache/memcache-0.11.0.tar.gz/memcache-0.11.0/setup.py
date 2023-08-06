# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memcache']

package_data = \
{'': ['*']}

install_requires = \
['hashring>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'memcache',
    'version': '0.11.0',
    'description': 'Memcached client for Python',
    'long_description': "# memcache\n\nExperimental memcached client library for python. This project is in WIP status, please don't use it in production environment.\n\nKey features:\n\n- Based on memcached's new meta commands;\n- Asyncio support;\n- Type hints.\n\n## Installation\n\n```sh\n$ pip install memcache\n```\n\n## About the Project\n\nMemcache is &copy; 2020-2021 by [aisk](https://github.com/aisk).\n\n### License\n\nMemcache is distributed by a [MIT license](https://github.com/aisk/memcache/tree/master/LICENSE).\n",
    'author': 'An Long',
    'author_email': 'aisk1988@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
