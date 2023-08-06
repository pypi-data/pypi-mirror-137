# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastproj', 'fastproj.{fastproj.project_name}.backend.backend']

package_data = \
{'': ['*'], 'fastproj': ['{fastproj.project_name}/docker/*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['fastproj = fastproj.main:run']}

setup_kwargs = {
    'name': 'fastproj',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Michael Kalashnikov',
    'author_email': 'kalashnikovsystem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
