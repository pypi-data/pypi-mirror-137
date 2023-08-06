# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbus_player_status']

package_data = \
{'': ['*']}

install_requires = \
['dbus-python>=1.2.18,<2.0.0']

entry_points = \
{'console_scripts': ['dbus-player-status = dbus_player_status.main:main']}

setup_kwargs = {
    'name': 'dbus-player-status',
    'version': '0.1.0',
    'description': 'Tool to extract media player status via DBus in JSON format',
    'long_description': None,
    'author': 'Tom Evans',
    'author_email': 'tevans.uk@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
