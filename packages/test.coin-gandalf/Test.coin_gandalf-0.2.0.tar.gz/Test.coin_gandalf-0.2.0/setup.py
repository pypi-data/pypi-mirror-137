# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gandalf']

package_data = \
{'': ['*']}

install_requires = \
['base58==2.1.1', 'pynacl==1.5.0']

setup_kwargs = {
    'name': 'test.coin-gandalf',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Paul Guénézan',
    'author_email': 'paul@guenezan.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
