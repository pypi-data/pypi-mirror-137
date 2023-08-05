# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rashsetup']

package_data = \
{'': ['*'],
 'rashsetup': ['Drivers/*',
               'Drivers/Profiles/*',
               'Drivers/Profiles/cache2/*',
               'Drivers/Profiles/cache2/doomed/*',
               'Drivers/Profiles/cache2/entries/*',
               'Drivers/Profiles/cache2/trash9638/*',
               'Drivers/Profiles/datareporting/*',
               'Drivers/Profiles/datareporting/archived/2022-02/*',
               'Drivers/Profiles/datareporting/glean/db/*',
               'Drivers/Profiles/safebrowsing/*',
               'Drivers/Profiles/safebrowsing/google4/*',
               'Drivers/Profiles/saved-telemetry-pings/*',
               'Drivers/Profiles/sessionstore-backups/*',
               'Drivers/Profiles/settings/main/ms-language-packs/browser/newtab/*',
               'Drivers/Profiles/shader-cache/*',
               'Drivers/Profiles/startupCache/*',
               'Drivers/Profiles/storage/*',
               'Drivers/Profiles/storage/default/moz-extension+++6573d4e8-cca9-47a3-a788-fe9622d8c39e^userContextId=4294967295/*',
               'Drivers/Profiles/storage/default/moz-extension+++6573d4e8-cca9-47a3-a788-fe9622d8c39e^userContextId=4294967295/idb/*',
               'Drivers/Profiles/storage/permanent/chrome/*',
               'Drivers/Profiles/storage/permanent/chrome/idb/*',
               'Drivers/Profiles/thumbnails/*',
               'Drivers/drivers/geckodriver/win64/v0.30.0/*']}

install_requires = \
['selenium==4.1.0', 'webdriver_manager==3.5.2']

setup_kwargs = {
    'name': 'rashsetup',
    'version': '1.6.0',
    'description': 'Sets up some Rash Things for us',
    'long_description': None,
    'author': 'RahulARanger',
    'author_email': 'saihanumarahul66@gmail.com',
    'maintainer': 'RahulARanger',
    'maintainer_email': 'saihanumarahul66@gmail.com',
    'url': 'https://github.com/RahulARanger/RashSetup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
