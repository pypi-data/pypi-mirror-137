# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytu',
    'version': '0.1.5',
    'description': 'My personal Python Tuuls :-)',
    'long_description': '# PyTu\nMy personal Python Tuuls :-) \n\n## Install & init\n```\n> pip install pytu\n```\n\n```py\nfrom pytu.tools import Tools  # general python tools\nfrom pytu.matt import Matt    # GUI autoMATion tool based on PyAutoGUI\n```\n\n## Logging\n```py\nTools.log(\'Hello world\')  # prints "[2022-02-07 16:31:14] Hello world"\n\nTools.log_path = "log/{year}-{month}-{day}_{hour}.log"  # from now log messages are also saved in text file\n```\n\n## Type conversions\n```py\nTools.str(datetime.now())                      # "2022-02-07 16:31:14"\nTools.str("5.1234000")                         # "5.1234"\nTools.str(ValueError(\'something went wrong\'))  # "ValueError: something went wrong"\n\nTools.datetime(\'7.2.2022\')    # datetime(2022, 2, 7)\nTools.datetime(\'2/7/2022\')    # datetime(2022, 2, 7)\nTools.datetime(\'2022-07-02\')  # datetime(2022, 2, 7)\n```\n\n## Automation \n```py\n# Init\nmatt = Matt(\n\tcache_file = \'temp/cache/matt.json\',\n\tlogger = Tools,\n)\nmatt.set_ui({                     # recommended, but not mandatory\n\t\'btn_ok\' => \'ui/btn_ok.png\',\n\t\'btn_home\' => \'ui/btn_home.png\',\n\t\'msg_ok\' => \'ui/msg_ok.png\',\n\t\'msg_error\' => \'ui/msg_error.png\',\n\t\'homescreen\' => \'ui/homescreen.png\',\n})\n\n# Automate\nmatt.click(\'btn_ok\')\n\nfound = matt.which([\'msg_ok\', \'msg_error\'])  # waits for one of the messages to show up\nif found == \'msg_error\':\n\tprint(\'Error message found\')\nelif found == \'msg_ok\':\n\tmatt.click(\'btn_home\')\n\tmatt.wait(\'homepage\')\n```\n',
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
