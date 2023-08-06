# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fs9721_utils']

package_data = \
{'': ['*']}

install_requires = \
['bitstruct>=8.12.1,<9.0.0']

entry_points = \
{'console_scripts': ['test = tests:run']}

setup_kwargs = {
    'name': 'fs9721-utils',
    'version': '0.0.2',
    'description': 'Python based utilities for interacting with digital multimeters that are built on the FS9721-LP3 chipset.',
    'long_description': None,
    'author': 'Fergus In London',
    'author_email': 'fergus@fergus.london',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
