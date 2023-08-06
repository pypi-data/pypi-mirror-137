# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ldtkpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ldtkpy',
    'version': '0.9.4',
    'description': 'Load and parse LDtk files, with full types definitions.',
    'long_description': '# LDtk Python \n\nLoad and parse LDtk files, with full types definitions. \n\nAutomatically generated from Json Schema using QuickType.\n\nSee https://ldtk.io/api/\n\ncan be used like that:\n\n\n```python \nimport json\nfrom ldtkpy.api import ldtk_json_from_dict\n\nresult = ldtk_json_from_dict(json.loads(json_string))\n```',
    'author': 'Yann Vaillant',
    'author_email': 'va@yan.pm',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ldtk.io/api/',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
