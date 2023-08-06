# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiowire']

package_data = \
{'': ['*']}

install_requires = \
['zmq>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'aiowire',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'David M. Rogers',
    'author_email': 'predictivestatmech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
