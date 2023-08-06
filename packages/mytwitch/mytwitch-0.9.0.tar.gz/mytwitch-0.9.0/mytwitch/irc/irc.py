import socket
import ssl

from typing import Sequence, Union, Generator

from queue import Queue
from queue import Empty as QueueIsEmpty

from .message import IRCMessage
from ..auth import UserToken



class TwitchIRC:
    """Socket connection to the Twitch IRC"""

    def __init__(self, user_token: UserToken, channels: Sequence[str], log_commands: bool = True):
        self.user_token = user_token
        self.channels = channels
        self.log_commands = log_commands

        self.history = Queue()

    def is_connected(self) -> bool:
        """Get connection status of socket"""
        return hasattr(self, 'irc')

    def ensure_connection(self) -> None:
        """Ensure that connection is established"""
        if not self.is_connected():
            self.connect()

    def send_command(self, command: str) -> None:
        """Send a command to the IRC"""
        
        # Only print to console if not the password
        if not command.startswith('PASS'):
            if self.log_commands:
                print(f'< {command}')

        # Send command to IRC
        self.irc.send((command + '\r\n').encode())

    def send_message(self, channel: str, text: str) -> None:
        """Send a message to a channel"""
        self.send_command(f'PRIVMSG #{channel} : {text}')

    def connect(self) -> None:
        """Connect to the Twitch IRC over a socket"""

        # Connect to IRC
        self.irc = ssl.wrap_socket(socket.socket())
        self.irc.connect(('irc.chat.twitch.tv', 6697))

        # Authenticate to Twitch
        self.send_command(f'PASS oauth:{self.user_token}')
        self.send_command(f'NICK {self.user_token.login}')

        # Connect to all channels
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')

    def get_message(self) -> Union[IRCMessage, None]:
        """Get one message from the history"""

        # Refill history
        if self.history.empty():
            list(map(self.history.put, self._get_new_messages()))

        try:
            return self.history.get_nowait()
        except QueueIsEmpty:
            return None

    def _get_new_messages(self) -> Generator[IRCMessage, None, None]:
        """Get new messages"""

        messages = self.irc.recv(2048).decode()

        for raw_message in messages.split('\r\n'):
            # Ignore if empty
            if len(raw_message) == 0:
                continue

            # Parse message
            message = IRCMessage(raw_message)

            # PONG if Twitch PINGs the client
            # to make sure the connection is maintained
            if message.irc_command == 'PING':
                self.send_command('PONG :tmi.twitch.tv')

            yield message

    def feed(self):
        """Receive messages from channels and loop over them"""

        # Connect if not already connect
        self.ensure_connection()

        # Receive messages
        while True:
            for message in self._get_new_messages():
                yield message