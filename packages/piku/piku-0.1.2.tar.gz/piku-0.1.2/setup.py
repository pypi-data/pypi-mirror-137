# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piku', 'piku.commands', 'piku.core', 'piku.template.project']

package_data = \
{'': ['*'], 'piku': ['template/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'pyserial>=3.5,<4.0',
 'requests>=2.27.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['piku = piku.main:main']}

setup_kwargs = {
    'name': 'piku',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Piku\nA small command line utility for managing CircuitPython projects\n',
    'author': 'Mark Raleson',
    'author_email': 'markraleson@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mraleson/rag.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
