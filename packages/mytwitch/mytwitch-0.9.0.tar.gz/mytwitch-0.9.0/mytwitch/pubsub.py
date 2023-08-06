# -------------------------------------
# -- Thanks to Willow for helping me --
# -- with asyncio and websockets     --
# --                                 --
# -- Willow                          --
# --   * Discord: Willow#1152        --
# --   * Website: aricodes.net       --
# -------------------------------------


import asyncio
import time
import json
import lzon

import websockets
from websockets import WebSocketClientProtocol
from websockets import ConnectionClosed 

from typing import Union

from .auth import UserToken

from .exceptions import APIRequestError



class TwitchPubSub:
    """A template class for a Twitch PubSub websocket"""

    uri: str = 'wss://pubsub-edge.twitch.tv'

    user_token: UserToken
    topics: list[str]
    auto_reconnect: bool
    websocket: WebSocketClientProtocol

    def __init__(self, user_token: UserToken, topics: list[str], auto_reconnect: bool = True):
        self.user_token = user_token
        self.topics = topics
        
        self.auto_reconnect = auto_reconnect
        self.websocket = None


    async def ping(self, websocket: WebSocketClientProtocol):
        """Ping websocket every 4 and a half minutes"""
        while websocket.open:
            await websocket.send('{"type": "PING"}')
            await asyncio.sleep(270)

    async def subscribe(self, websocket: WebSocketClientProtocol, topics: list[str]):
        """Subscribe to topics"""

        await websocket.send(json.dumps({
            'type': 'LISTEN',
            'data': {
                'topics': topics,
                'auth_token': str(self.user_token)
            }
        }))

        # Await response to make sure subscription was successful
        response = json.loads(await websocket.recv())
        
        if response.get('error') != "":
            raise APIRequestError(None, response['error'])

    async def on_open(self, websocket: WebSocketClientProtocol):
        """What to do when a connection is established"""

    async def on_message(self, websocket: WebSocketClientProtocol, message: Union[list, dict]):
        """What to do when a new message is received"""

    async def on_close(self):
        """What to do when the websocket connection has been shut down"""

    async def on_error(self, websocket: WebSocketClientProtocol, exception: Exception):
        """What to do when an error occurs in the main loop"""
        raise exception

    async def loop(self):
        """Main loop for the websocket connection"""
        
        async for self.websocket in websockets.connect(self.uri):
            # Default to reconnecting if auto_reconnect is on
            reconnect = self.auto_reconnect

            try:
                # Subscribe to all selected topics on start-up
                await self.subscribe(self.websocket, self.topics)
                
                # Do whatever is defined to be done
                # once a connection is established
                await self.on_open(self.websocket)

                # Start pinging in the background
                asyncio.create_task(self.ping(self.websocket))
                
                # Read and process incoming messages
                async for message in self.websocket:
                    response = lzon.loads(message)
        
                    # Reconnect if necessary
                    if response.get('type') == 'RECONNECT':
                        reconnect = True
                        await self.disconnect(websocket)

                    # Ignore all pongs
                    elif response.get('type') == 'PONG':
                        pass

                    else:
                        # Do whatever is defined to be done
                        # with a message when received
                        await self.on_message(self.websocket, response)
            
            except websockets.ConnectionClosed as e:
                # Stop the for-loop to avoid reconnection
                if not reconnect:
                    break

            except Exception as e:
                await self.on_error(self.websocket, e)

        # Remove old connection
        self.websocket = None
        
        # Do whatever is defined to be done
        # when the connection has been closed
        await self.on_close()

    async def disconnect(self, websocket: WebSocketClientProtocol):
        """Disconnect from websocket
        Must be raised within the loop
        """
        await websocket.close()
        raise ConnectionClosed(200, 'Voluntary disconnect')

    def connect(self):
        """Start the main loop and connect to the websocket"""
        asyncio.get_event_loop().run_until_complete(self.loop())