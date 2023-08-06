# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toolib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'toolib',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
