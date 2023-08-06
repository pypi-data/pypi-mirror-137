# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mps_invidious']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'requests>=2.27.1,<3.0.0', 'rich>=11.1.0,<12.0.0']

setup_kwargs = {
    'name': 'mps-invidious',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'JoseKilo',
    'author_email': 'jose.eduardo.gd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
