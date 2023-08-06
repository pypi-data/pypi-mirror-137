# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ldtkpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ldtkpy',
    'version': '0.9.3',
    'description': 'Load and parse LDtk files, with full types definitions.',
    'long_description': None,
    'author': 'Yann Vaillant',
    'author_email': 'va@yan.pm',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
