# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fibberio']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['fibber = fibberio.cli:cli']}

setup_kwargs = {
    'name': 'fibberio',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sethjuarez',
    'author_email': 'me@sethjuarez.com',
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
