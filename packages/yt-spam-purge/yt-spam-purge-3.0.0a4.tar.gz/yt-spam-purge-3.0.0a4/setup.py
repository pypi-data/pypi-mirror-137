# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yt_spam_purge']

package_data = \
{'': ['*'], 'yt_spam_purge': ['assets/*']}

install_requires = \
['anyio>=3.5.0,<4.0.0',
 'confusables>=1.2.0,<2.0.0',
 'google-api-python-client>=2.36.0,<3.0.0',
 'google-auth-oauthlib>=0.4.6,<0.5.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'rich>=11.1.0,<12.0.0',
 'rtfunicode>=2.0,<3.0',
 'tld>=0.12.6,<0.13.0',
 'trio>=0.19.0,<0.20.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ytsp = yt_spam_purge.cli:main']}

setup_kwargs = {
    'name': 'yt-spam-purge',
    'version': '3.0.0a4',
    'description': 'Easily scan for and delete scam comments on your YouTube channel.',
    'long_description': '# yt-spam-purge\n\n[![ci](https://github.com/dekoza/yt-spam-purge/workflows/ci/badge.svg)](https://github.com/dekoza/yt-spam-purge/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://dekoza.github.io/yt-spam-purge/)\n[![pypi version](https://img.shields.io/pypi/v/yt-spam-purge.svg)](https://pypi.org/project/yt-spam-purge/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/yt-spam-purge/community)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nEasily scan for and delete scam comments on your YouTube channel.\n\nThis is REWRITE of the tool made by ThioJoe. I want to refactor it into a proper library with CLI and utilizing async for blazing-fast operation.\n\n\n<hr>\nPart of original README:\n\n**What Is This?** - Allows you to filter and search for spammer comments on your channel and other\'s channel(s) in many different ways AND delete/report them all at once (see features below).\n\n**How to Download:** Click the "[Releases](https://github.com/ThioJoe/YouTube-Spammer-Purge/releases)" link on the right, then on the latest release, under \'Assets\' click to download "YTSpammerPurge.exe". (You might have to click "Assets" to view the files for the release)\n> * [Linux Setup Instructions](https://github.com/ThioJoe/YouTube-Spammer-Purge/wiki/Linux-Installation-Instructions)\n> * [MacOS Setup Instructions](https://github.com/ThioJoe/YouTube-Spammer-Purge/wiki/MacOS-Instructions)\n> * (Windows installation not necessary if using exe file. But see how to set up required API key [on this page](https://github.com/ThioJoe/YT-Spammer-Purge/wiki/Instructions:-Obtaining-an-API-Key))\n\n### **Detailed Info & Documentation →** Visit the wiki [(Click Here)](https://github.com/ThioJoe/YT-Spammer-Purge/wiki) for more detailed writeups on the program\n\n## Features\n\n* 15 Different Filtering Methods\n  * **Auto-Smart Mode (Recommended)**: Automatically detects multiple spammer techniques\n  * **Sensitive-Smart Mode**: More likely to catch elusive spammers, but with more false positives\n  * **Scan by Channel ID**: Enter a known spammer\'s channel link or ID directly\n  * **Scan Usernames** for: Individual special characters, individual strings, or using a custom Regex expression\n  * **Scan Comment Text**: (Same 3 options as above)\n  * **Scan Usernames and Comment Text** simultaneously: (Same 3 options as above)\n  * **ASCII Mode**: Scan Usernames for non-ASCII special characters (three different sensitivities)\n* 4 Different Scanning Modes\n  * Scan a **single video**\n  * Scan **Recent Videos** (Up to 5)\n  * Scan recent comments across **entire channel** (all videos)\n  * *Experimental*: Scan a **community post**\n* Automatic deletion of all found comments (after confirmation), as well as the option to ban them\n* Options to instead Report spam comments or \'Hold For Review\'\n* Ability to create config file to skip pre-set options\n* Rich text log files\n* \'Recovery Mode\' option to re-instate previously deleted comments\n* Displays "match samples" after printing comments list to easily spot false positives\n* Ability to exclude selected authors before deletion / reporting\n\n## Purpose\n\nRecently, there has been a massive infestation of spam on YouTube where fake impersonator accounts leave spam/scam replies to hundreds of users on a creator\'s videos. For some god-forsaken reason, YouTube offers no way to delete all comments by a specific user at once, meaning you must delete them one by one BY HAND.\n\nYouTube offers a functionality to ban a user, but it does NOT delete previous comments. Therefore I created this script to allow you to instantly purge their spam replies, and since then it has evolved into a fully featured spam scanner as well. **IT DOES NOT PREVENT SPAMMERS - It only makes it easier to delete them when they show up!** YouTube still must implement better native tools for dealing with spammers.\n\n## 🤔 Pro-Tip If This Seems Sketchy: Limiting The App\'s Access 🤔\n\nIf you feel sketched out about giving the app the required high level permissions to your channel (very understandable), you could instead use the app in \'moderator mode\' (set in the config file). First, some context: When you grant access to another channel to be a moderator for your channel, they are able to mark comments for \'held for review\', and this permission works through the API as well.\n\n_Therefore,_ what you could do is create an _blank dummy-google-account_ with nothing on it except a empty new channel. Then you can grant _that_ channel permission to be a moderator, and use the app through _the dummy moderator account_. **This way, you know that the app will never have the ability to do more than mark comments as held for review** (which the app supports) on your main channel, and have no other access to your account\'s data. You just won\'t be able to ban the spammers through this app directly, but you can still remove/hide their comments instead of deleting them. Just make sure to create the google cloud API project on the dummy account instead.\n\nRead some additional details about \'moderator mode\' on the [wiki page here](https://github.com/ThioJoe/YT-Spammer-Purge/wiki/Moderator-Mode-&-Limiting-Permissions).\n\n## Usage Notes -READ THIS\n\n1. To use this script, you will need to obtain your own API credentials file by making a project via the Google Developers Console (aka \'Google Cloud Platform\'). The credential file should be re-named `client_secret.json` and be placed in the same directory as this script. [See Instructions Here](https://github.com/ThioJoe/YT-Spammer-Purge/wiki/Instructions:-Obtaining-an-API-Key).\n\n2. **IF IT FREEZES** while scanning, it is probably because you clicked within the command prompt window and entered "selection mode" which pauses everything. **To unfreeze it, simply right click within the window, or press the Escape key.**\n\n3. I\'m a total amateur, so if something doesn\'t work I\'ll try to fix it but might not even know how, so don\'t expect too much. Therefore **I OFFER NO WARRANTY OR GUARANTEE FOR THIS SCRIPT. USE AT YOUR OWN RISK.** I tested it on my own and implemented some failsafes as best as I could, but there could always be some kind of unexpected bug. You should inspect the code yourself.\n\n\n\n<hr>\n\n\n## Requirements\n\nyt-spam-purge requires Python 3.10 or above.\n\n<details>\n<summary>To install Python 3.10, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.10\npyenv install 3.10.0\n\n# make it available globally\npyenv global system 3.10.0\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.10 -m pip install yt-spam-purge\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.10 -m pip install --user pipx\n\npipx install --python python3.10 yt-spam-purge\n```\n\n',
    'author': 'ThioJoe',
    'author_email': 'joe@thiojoe.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ThioJoe/YT-Spammer-Purge',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
