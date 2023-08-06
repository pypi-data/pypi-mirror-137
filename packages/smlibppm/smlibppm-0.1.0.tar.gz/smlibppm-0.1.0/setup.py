# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smlibppm', 'smlibppm.api', 'smlibppm.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'smlibppm',
    'version': '0.1.0',
    'description': 'A small library for creating and manipulating PPMs',
    'long_description': None,
    'author': 'Nathan Reed',
    'author_email': 'nreed@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
