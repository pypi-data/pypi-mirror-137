# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fossil_cli']

package_data = \
{'': ['*']}

install_requires = \
['click', 'questionary', 'semver']

entry_points = \
{'console_scripts': ['fossil-cli = fossil_cli:cli']}

setup_kwargs = {
    'name': 'fossil-cli',
    'version': '4.3.1',
    'description': 'Fossil Cli Helper',
    'long_description': '',
    'author': 'Lorenzo Antonio Garcia Calzadilla',
    'author_email': 'lorenzogarciacalzadilla@gmail.com',
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
