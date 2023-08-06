class TwitchAPIException(Exception):
    """Base class for errors relating to the Twitch API"""


class APIRequestError(TwitchAPIException):
    """Error included in a response from the Twitch API"""

    def __init__(self, status, message):
        super().__init__(f'[{status}] {message}')

        self.status = status
        self.message = message


class InvalidToken(TwitchAPIException):
    """User access token used for request is invalid"""