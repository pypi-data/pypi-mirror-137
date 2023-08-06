# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SwSpotify']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Cors>=3.0.10,<4.0.0', 'flask>=2.0.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{':sys_platform == "linux"': ['dbus-python>=1.2.16,<2.0.0'],
 ':sys_platform == "win32"': ['pywin32>=301,<304']}

setup_kwargs = {
    'name': 'swspotify',
    'version': '1.2.3',
    'description': 'Get currently playing song and artist from Spotify faster without using the API.',
    'long_description': '# SwSpotify\n\n[![Discord Server](https://badgen.net/badge/discord/join%20chat/7289DA?icon=discord)](https://discord.gg/DSUZGK4)\n[![Build Status](https://travis-ci.com/SwagLyrics/SwSpotify.svg?branch=master)](https://travis-ci.com/SwagLyrics/SwSpotify)\n[![Build status](https://ci.appveyor.com/api/projects/status/c8heviwe9q2m8lb0?svg=true)](https://ci.appveyor.com/project/TheClashster/swspotify)\n[![codecov](https://codecov.io/gh/SwagLyrics/SwSpotify/branch/master/graph/badge.svg)](https://codecov.io/gh/SwagLyrics/SwSpotify)\n![PyPI](https://img.shields.io/pypi/v/swspotify.svg)\n[![Downloads](https://pepy.tech/badge/swspotify)](https://pepy.tech/project/swspotify)\n\nSwSpotify is a Python library to get the song and artist of the currently playing song from the Spotify application faster and without using the API. It works on Windows, Linux, macOS and even the Spotify Web Player! 🥳\n\nIn order to add support for the Spotify Web Player, the [SwagLyrics Chrome Extension](https://chrome.google.com/webstore/detail/swaglyrics-for-spotify/miopldoofdhmipepmnclnoangcdffmlk) needs to be installed. We have plans to extend this for other browsers as well.\n\nIf you\'re a developer using SwSpotify, you can direct your end users to install the extension to automatically make your application work with the Spotify Web Player. The source of the Chrome Extension is open sourced at https://github.com/SwagLyrics/SwagLyrics-Chrome-Extension.\n\nThe original repository was [spotilib](https://github.com/XanderMJ/spotilib) which worked just for Windows and hasn\'t been updated since a long while when it broke on account of Spotify updating their application.\n\nOriginally made for use in [SwagLyrics for Spotify](https://github.com/SwagLyrics/SwagLyrics-For-Spotify).\n\n## Installation\n\nRequires Python3. Use pip or pip3 depending on your installation. You might want to use the `--user` flag on Linux to \navoid using pip as root.\n```shell\npip install SwSpotify\n```\nFor linux you need `dbus` which is usually pre-installed.\n## Usage\n\nUse it in your project by importing it as:\n\n```py\nfrom SwSpotify import spotify\n```\n\nThen you can access the song and artist as:\n\n```py\n>>> spotify.song()\n\'Hello\'\n>>> spotify.artist()\n\'Adele\'\n```\n\nSince mostly song and artist are used in conjunction, there is a `current()` method as well.\n\n```py\n>>> spotify.current()\n(\'Hello\', \'Adele\')\n```\n\nThis allows you to access song and artist by tuple unpacking as:\n\n```py\n>>> song, artist = spotify.current()\n```\n\nA `SpotifyNotRunning` Exception is raised if Spotify is closed or paused. `SpotifyClosed` and `SpotifyPaused` inherit from `SpotifyNotRunning`, meaning that you can catch both at the same time:\n\n```py\ntry:\n    title, artist = spotify.current()\nexcept SpotifyNotRunning as e:\n    print(e)\nelse:\n    print(f"{title} - {artist}")\n```\nIn case Spotify is closed or paused, that will automatically be reflected in the value of `e`.\n\nFor finer control you can catch `SpotifyClosed` and `SpotifyPaused` separately.\n## Compiling SwSpotify for Development\n\n- Clone the repo by `git clone https://github.com/SwagLyrics/SwSpotify.git` or use ssh.\n- `cd` into the cloned repo.\n- `pip install -e .` the -e flag installs it locally in editable mode.\n\n\n## Contributing\n\nSure, improvements/fixes/issues everything is welcome :)\n',
    'author': 'Aadi Bajpai',
    'author_email': 'clash@swaglyrics.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SwagLyrics/SwSpotify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
