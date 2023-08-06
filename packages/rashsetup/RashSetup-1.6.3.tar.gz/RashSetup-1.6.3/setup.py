# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rashsetup']

package_data = \
{'': ['*']}

install_requires = \
['selenium==4.1.0', 'webdriver_manager==3.5.2']

setup_kwargs = {
    'name': 'rashsetup',
    'version': '1.6.3',
    'description': 'RashSetup sets up Some RashThings for us',
    'long_description': None,
    'author': 'RahulARanger',
    'author_email': 'saihanumarahul66@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
