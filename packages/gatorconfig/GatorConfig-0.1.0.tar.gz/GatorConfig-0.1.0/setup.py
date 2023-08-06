# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatorconfig', 'gatorconfig.gui']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'ruamel.yaml>=0.17.20,<0.18.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['gatorconfig = gatorconfig.gator_config:cli']}

setup_kwargs = {
    'name': 'gatorconfig',
    'version': '0.1.0',
    'description': 'Autogeneration of GatorGradle configuration files.',
    'long_description': None,
    'author': 'Daniel Ullrich',
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
