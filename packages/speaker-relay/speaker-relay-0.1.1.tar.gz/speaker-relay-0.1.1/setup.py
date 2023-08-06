# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['speaker_relay']

package_data = \
{'': ['*'], 'speaker_relay': ['static/*']}

install_requires = \
['SoundCard>=0.4.1,<0.5.0',
 'aiohttp>=3.8.1,<4.0.0',
 'numpy>=1.22.0,<2.0.0',
 'python-socketio>=5.5.1,<6.0.0']

entry_points = \
{'console_scripts': ['speaker-relay = speaker_relay:main']}

setup_kwargs = {
    'name': 'speaker-relay',
    'version': '0.1.1',
    'description': 'Streaming loopback audio through websocket to another device.',
    'long_description': 'Streaming loopback audio through websocket to another device.\n\nAudioContext is used. Tested with Chrome. \n',
    'author': 'yetanothercheer',
    'author_email': 'yetanothercheer@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
