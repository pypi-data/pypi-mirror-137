# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configator']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['configator = configator.main:app']}

setup_kwargs = {
    'name': 'pyconfigator',
    'version': '1.0.0',
    'description': 'A Configuration File Generator for GatorGradle',
    'long_description': None,
    'author': 'Kyrie Doniz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
