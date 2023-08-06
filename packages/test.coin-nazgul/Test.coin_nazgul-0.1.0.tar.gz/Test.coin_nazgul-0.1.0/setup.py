# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nazgul']

package_data = \
{'': ['*']}

install_requires = \
['base58==2.1.1', 'pynacl==1.5.0', 'test.coin-gandalf>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'test.coin-nazgul',
    'version': '0.1.0',
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
