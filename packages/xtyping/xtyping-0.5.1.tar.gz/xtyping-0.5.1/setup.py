# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['xtyping']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'xtyping',
    'version': '0.5.1',
    'description': 'xtyping = typing + typing_extensions',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/master/libs/xtyping',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
