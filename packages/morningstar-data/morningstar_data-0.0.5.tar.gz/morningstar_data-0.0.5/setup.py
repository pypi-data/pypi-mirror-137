# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morningstar_data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'morningstar-data',
    'version': '0.0.5',
    'description': 'Morningstar Data',
    'long_description': None,
    'author': 'Morningstar, Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
