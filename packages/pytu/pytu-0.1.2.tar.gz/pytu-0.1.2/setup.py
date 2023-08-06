# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytu',
    'version': '0.1.2',
    'description': 'My personal Python Tuuls :-)',
    'long_description': '# PyTu\n\n## Logging\n```py\nfrom pytu.tools import Tools\n\nTools.log(\'Hello world\')  # prints "[2022-02-07 16:31:14] Hello world"\n\nTools.log_path = "log/{year}-{month}-{day}_{hour}.log"  # from now log messages are also saved in text file\n```\n\n## Type conversions\n```py\nTools.str(datetime.now())                      # "2022-02-07 16:31:14"\nTools.str("5.1234000")                         # "5.123"\nTools.str(ValueError(\'something went wrong\'))  # "ValueError: something went wrong"\n\nTools.datetime(\'7.2.2022\')    # datetime(2022, 2, 7)\nTools.datetime(\'2/7/2022\')    # datetime(2022, 2, 7)\nTools.datetime(\'2022-07-02\')  # datetime(2022, 2, 7)\n```\n\n## Automation \nTODO: finish the docs\n',
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
