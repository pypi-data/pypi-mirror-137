# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rwthcolors', 'rwthcolors.colors']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'rwthcolors',
    'version': '0.1.1',
    'description': 'Simple library that makes it easier to use RWTH CI colors in python projects',
    'long_description': '',
    'author': 'Philipp Simon Leibner',
    'author_email': 'philipp.leibner@ifs.rwth-aachen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
