# mytwitch

## Overview

- [Security Warning](#security-warning)
- [Installation](#installation)
- [Application setup for authentication](#application-setup-for-authentication)
- [Examples](#examples)
- [Terminal Commands](#terminal-commands)


## Security Warning

As this package allows you to easily generate a user access token with the specified permissions, it too has access to send your token off to a third party without your knowledge. You are advised to always check the source code for such operations of any application you use and make sure this isn't the case.

### Where to look?

It would be best for you to search through the entire package to assure you aren't being mislead.
However, this is time consuming, so if you're not inclined, here are links to the supposedly relevant files. You can also browse the files after installation to make sure the published content doesn't differ from that in the repository.

- [mytwitch.auth.user_token:UserToken](https://gitlab.com/thedisruptproject/mytwitch/-/blob/main/mytwitch/auth/user_token.py)
- [mytwitch.auth.auth_app:AuthenticationApp](https://gitlab.com/thedisruptproject/mytwitch/-/blob/main/mytwitch/auth/authapp.py)


## Installation

```sh
python -m pip install mytwitch
```


## Application setup for authentication

### Redirect URI

1. Log in to [Twitch Developers](https://dev.twitch.tv/).
2. Go to the **Applications** tab.
3. Register your application with the URL as `http://localhost:` followed by the port you choose to use. By default, this package uses `6319`. This would be `http://localhost:6319`.

### Client ID

1. Log in to [Twitch Developers](https://dev.twitch.tv/).
2. Go to the **Applications** tab.
3. Select **Manage** by the application you're using.
4. The client ID should be found on this page.

**NOTE**: Client IDs are public and may be shared. You may use Mytwitch's client ID, but you're advised to set up your own application in case this were to ever get removed for any reason. Mytwitch's client ID can be imported from `mytwitch.client_id`.


## Examples

- [IRC](#irc)
- [PubSub](#pubsub)
- [User access token](#user-access-token)

### IRC

```py
from mytwitch.auth import UserToken
from mytwitch.irc import TwitchIRC


client_id = 'abcdefghijklmnopqrstuvwxyz0123456789'
scope = ['chat:read']  # Permissions to read chat

# Create a user access token for authentication
user_token = UserToken(client_id, scope)

channel = 'twitch'  # Which channel to connect to
irc = TwitchIRC(user_token, [channel])  # Create your IRC

# Read incoming messages
for message in irc.feed():
    print(message)
```

### PubSub

```py
from mytwitch.auth import UserToken
from mytwitch.pubsub import TwitchPubSub


client_id = 'abcdefghijklmnopqrstuvwxyz0123456789'
scope = ['channel:read:redemptions']  # Permissions to read reward redemptions

# Create a user access token for authentication
user_token = UserToken(client_id, scope)


# Define a PubSub with your own events
class MyPubSub(TwitchPubSub):  # Inherit from `TwitchPubSub`
    
    async def on_open(self, websocket):
        print('PubSub has been opened.')

    async def on_message(self, ws, message):
        print(f'Message received:\n{message}\n\n')

    async def on_close(self):
        print('PubSub has been closed.')

    async def on_error(self, ws, exception):
        print(f'An error has occurred:\n{exception}\n\n')


# Topic for reading reward redemption
topics = [f'channel-points-channel-v1.{user_token.user_id}']
pubsub = MyPubSub(user_token, topics)  # Create your PubSub

# Start the PubSub connection
pubsub.connect()
```

### User access token

```py
from mytwitch.auth import UserToken

client_id = 'abcdefghijklmnopqrstuvwxyz0123456789'
scope = ['chat:read']

user_token = UserToken(
    client_id,  # Application client ID
    scope,      # Permissions you want

    immed_auth = True  # You can set this to False if you don't want
    # to generate a token on creation, as it opens a window in the browser
)

# Convert into a string to get the current token or generate a new one if necessary
print(f'My requested token is `{user_token}`')
```


## Terminal Commands

There are commands for authentication if you don't want to have to set up a file for such simple operations.
These commands use Mytwitch's client ID, by default, but you can specify your own with `-C`.

### Create new token

```sh
python -m mytwitch auth -NS 'chat:read' 'chat:edit'
```

### Revoke token

```sh
python -m mytwitch auth -RT 'abcdefghijklmnopqrstuvwxyz0123456789'
```