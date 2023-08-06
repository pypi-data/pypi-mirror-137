from typing import Union

from collections import namedtuple



_IRCMessage = namedtuple('IRCMessage', [
    'raw',
    'prefix',
    'user',
    'channel',
    'text',
    'irc_command',
    'irc_args'
])


class IRCMessage:
    """Twitch IRC message in an understandable format"""

    def __new__(cls, string: str) -> _IRCMessage:
        """Parses a string received from the Twitch IRC"""

        parts = string.split(" ")

        # Initialize all fields as None,
        # so that the message is always valid
        prefix = None
        user = None
        channel = None
        text = None
        irc_command = None
        irc_args = None


        # If the first part starts with a colon,
        # we know that it's the prefix and can set it
        if parts[0].startswith(':'):
            prefix = parts[0][1:]

            # Extract user from prefix
            user = cls.get_user_from_prefix(prefix)

            # Remove prefix from parts
            parts = parts[1:]


        # Find and extract message content
        text_start = next((i for i, part in enumerate(parts) if part.startswith(':')), None)

        if text_start is not None:
            # All words of the message text
            # lie in front of and includes this index
            text_parts = parts[text_start:]

            # Remove starting colon from first word
            text_parts[0] = text_parts[0][1:]

            # Join all words back together for the full content
            text = " ".join(text_parts)

            # Remove all text from parts
            parts = parts[:text_start]


        # Get the IRC command and arguments
        # from the remaining parts
        irc_command = parts[0]
        irc_args = parts[1:]


        # Find channel in IRC commands
        hash_start = next((i for i, part in enumerate(irc_args) if part.startswith('#')), None)

        if hash_start is not None:
            channel = irc_args[hash_start][1:]


        return _IRCMessage(
            raw=string,
            prefix=prefix,
            user=user,
            channel=channel,
            text=text,
            irc_command=irc_command,
            irc_args=irc_args
        )

    @classmethod
    def get_user_from_prefix(cls, prefix: str) -> Union[str, None]:
        """Extract user from message prefix"""
        
        domain = prefix.split('!')[0]

        if domain.endswith('.tmi.twitch.tv'):
            return domain[:-len('.tmi.twitch.tv')]

        if 'tmi.twitch.tv' not in domain:
            return domain

        return None