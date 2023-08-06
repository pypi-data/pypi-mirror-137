# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytu',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Michal Mikolas',
    'author_email': 'nanuqcz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
