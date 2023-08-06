# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyatom_finance']

package_data = \
{'': ['*'], 'pyatom_finance': ['templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'pydantic>=1.8.1,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyatom-finance',
    'version': '0.1.1',
    'description': 'Module to collect data from Atom IO',
    'long_description': None,
    'author': 'carbonarok',
    'author_email': 'carbonarok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
