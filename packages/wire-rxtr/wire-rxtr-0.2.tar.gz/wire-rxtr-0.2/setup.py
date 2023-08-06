# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wire_rxtr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wire-rxtr',
    'version': '0.2',
    'description': '',
    'long_description': None,
    'author': 'cheetahbyte',
    'author_email': 'bernerdoodle@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
