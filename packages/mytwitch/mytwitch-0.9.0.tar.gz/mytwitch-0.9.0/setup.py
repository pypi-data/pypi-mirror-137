# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mytwitch', 'mytwitch.auth', 'mytwitch.irc']

package_data = \
{'': ['*']}

install_requires = \
['lzon>=0.1.0,<0.2.0', 'websockets>=10.0,<11.0']

setup_kwargs = {
    'name': 'mytwitch',
    'version': '0.9.0',
    'description': 'Twitch API interaction',
    'long_description': "# mytwitch\n\n## Overview\n\n- [Security Warning](#security-warning)\n- [Installation](#installation)\n- [Application setup for authentication](#application-setup-for-authentication)\n- [Examples](#examples)\n- [Terminal Commands](#terminal-commands)\n\n\n## Security Warning\n\nAs this package allows you to easily generate a user access token with the specified permissions, it too has access to send your token off to a third party without your knowledge. You are advised to always check the source code for such operations of any application you use and make sure this isn't the case.\n\n### Where to look?\n\nIt would be best for you to search through the entire package to assure you aren't being mislead.\nHowever, this is time consuming, so if you're not inclined, here are links to the supposedly relevant files. You can also browse the files after installation to make sure the published content doesn't differ from that in the repository.\n\n- [mytwitch.auth.user_token:UserToken](https://gitlab.com/thedisruptproject/mytwitch/-/blob/main/mytwitch/auth/user_token.py)\n- [mytwitch.auth.auth_app:AuthenticationApp](https://gitlab.com/thedisruptproject/mytwitch/-/blob/main/mytwitch/auth/authapp.py)\n\n\n## Installation\n\n```sh\npython -m pip install mytwitch\n```\n\n\n## Application setup for authentication\n\n### Redirect URI\n\n1. Log in to [Twitch Developers](https://dev.twitch.tv/).\n2. Go to the **Applications** tab.\n3. Register your application with the URL as `http://localhost:` followed by the port you choose to use. By default, this package uses `6319`. This would be `http://localhost:6319`.\n\n### Client ID\n\n1. Log in to [Twitch Developers](https://dev.twitch.tv/).\n2. Go to the **Applications** tab.\n3. Select **Manage** by the application you're using.\n4. The client ID should be found on this page.\n\n**NOTE**: Client IDs are public and may be shared. You may use Mytwitch's client ID, but you're advised to set up your own application in case this were to ever get removed for any reason. Mytwitch's client ID can be imported from `mytwitch.client_id`.\n\n\n## Examples\n\n- [IRC](#irc)\n- [PubSub](#pubsub)\n- [User access token](#user-access-token)\n\n### IRC\n\n```py\nfrom mytwitch.auth import UserToken\nfrom mytwitch.irc import TwitchIRC\n\n\nclient_id = 'abcdefghijklmnopqrstuvwxyz0123456789'\nscope = ['chat:read']  # Permissions to read chat\n\n# Create a user access token for authentication\nuser_token = UserToken(client_id, scope)\n\nchannel = 'twitch'  # Which channel to connect to\nirc = TwitchIRC(user_token, [channel])  # Create your IRC\n\n# Read incoming messages\nfor message in irc.feed():\n    print(message)\n```\n\n### PubSub\n\n```py\nfrom mytwitch.auth import UserToken\nfrom mytwitch.pubsub import TwitchPubSub\n\n\nclient_id = 'abcdefghijklmnopqrstuvwxyz0123456789'\nscope = ['channel:read:redemptions']  # Permissions to read reward redemptions\n\n# Create a user access token for authentication\nuser_token = UserToken(client_id, scope)\n\n\n# Define a PubSub with your own events\nclass MyPubSub(TwitchPubSub):  # Inherit from `TwitchPubSub`\n    \n    async def on_open(self, websocket):\n        print('PubSub has been opened.')\n\n    async def on_message(self, ws, message):\n        print(f'Message received:\\n{message}\\n\\n')\n\n    async def on_close(self):\n        print('PubSub has been closed.')\n\n    async def on_error(self, ws, exception):\n        print(f'An error has occurred:\\n{exception}\\n\\n')\n\n\n# Topic for reading reward redemption\ntopics = [f'channel-points-channel-v1.{user_token.user_id}']\npubsub = MyPubSub(user_token, topics)  # Create your PubSub\n\n# Start the PubSub connection\npubsub.connect()\n```\n\n### User access token\n\n```py\nfrom mytwitch.auth import UserToken\n\nclient_id = 'abcdefghijklmnopqrstuvwxyz0123456789'\nscope = ['chat:read']\n\nuser_token = UserToken(\n    client_id,  # Application client ID\n    scope,      # Permissions you want\n\n    immed_auth = True  # You can set this to False if you don't want\n    # to generate a token on creation, as it opens a window in the browser\n)\n\n# Convert into a string to get the current token or generate a new one if necessary\nprint(f'My requested token is `{user_token}`')\n```\n\n\n## Terminal Commands\n\nThere are commands for authentication if you don't want to have to set up a file for such simple operations.\nThese commands use Mytwitch's client ID, by default, but you can specify your own with `-C`.\n\n### Create new token\n\n```sh\npython -m mytwitch auth -NS 'chat:read' 'chat:edit'\n```\n\n### Revoke token\n\n```sh\npython -m mytwitch auth -RT 'abcdefghijklmnopqrstuvwxyz0123456789'\n```",
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/thedisruptproject/mytwitch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
