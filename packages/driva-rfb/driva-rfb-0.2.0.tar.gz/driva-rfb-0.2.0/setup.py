# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['driva_rfb']

package_data = \
{'': ['*'], 'driva_rfb': ['scripts/*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'httpx>=0.22.0,<0.23.0',
 'pywget>=0.31,<0.32',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['driva-rfb = driva_rfb.main:app']}

setup_kwargs = {
    'name': 'driva-rfb',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Driva-RFB \nCLI para ajudar a interagir com a base da Receita Federal Brasileira',
    'author': 'Victor Belinello',
    'author_email': 'victor@datadriva.com',
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
