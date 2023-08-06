import webbrowser
import time
import subprocess

from typing import Union, Sequence
from urllib.parse import urlparse, quote

from .authapp import AuthorizationApp

from ..request import APIRequest

from ..exceptions import APIRequestError
from ..exceptions import InvalidToken



class UserToken:
    """A user access token for Twitch"""

    def __init__(self,
        client_id: str, scope: Union[str, Sequence] = "",
        host: str = 'localhost', port: int = 6319, token: str = None,
        immed_auth: bool = True
    ):
        self.client_id = client_id
        self.scope = scope.split(" ") if isinstance(scope, str) else scope
        
        self.host = host
        self.port = port
        
        self.token = token
        self.expires_at = None


        # All parameters required for the token request
        self.query = {
            'client_id': client_id,
            'redirect_uri': get_redirect_uri(self.host, self.port),
            'response_type': 'token',
            'scope': quote(" ").join(self.scope)
        }

        # Make sure to start with a valid token
        if immed_auth:
            str(self)

    def __str__(self) -> str:
        """Make sure the token is valid and then return it"""

        if not self.is_valid():
            self.request_new()

        return self.token

    def is_valid(self) -> bool:
        """Validate token with the Twitch API"""
        
        if not self.token:
            return False

        if self.expires_at is not None:
            return time.time() < self.expires_at

        try:
            response = APIRequest('GET',
                'https://id.twitch.tv/oauth2/validate',
                headers={'Authorization': f'Bearer {self.token}'}
            ).send()
            
            self.expires_at = time.time() + response['expires_in']
            
            # Keep username and user ID for external use
            self.login = response.get('login')
            self.user_id = response.get('user_id')

            return True

        except APIRequestError:
            return False

    def request_new(self) -> None:
        """Request a new user access token,
        and retrieve it through a temporary HTTP server
        """

        # Start an AuthorizationApp server
        auth_app = AuthorizationApp(self.host, self.port)

        # Create URL from parameters
        url = get_authorization_url(**self.query)

        # Open address in web browser
        subprocess.run(['python', '-m', 'webbrowser', '-n', url], capture_output=True)

        # Wait for the POST to be submitted
        # and the HTTP server to be closed
        auth_app.wait_for_shutdown()
        self.token = auth_app.get_token()

        # If the newly requested token is not valid, something is wrong
        if not self.is_valid():
            raise InvalidToken(
                'Something has gone wrong with retrieving a new valid token')

    def revoke(self) -> bool:
        """Revoke token"""
        response = APIRequest('POST',
            'https://id.twitch.tv/oauth2/revoke',
            data={'client_id': self.client_id, 'token': self.token}
        ).send()

        # Safety check to make sure token has been invalidated
        return not self.is_valid()



def get_authorization_url(**query) -> str:
    """Create a URL to the authentication endpoint from query"""

    # Join all parameters by &s and append to endpoint
    params = '&'.join(f'{key}={value}' for key, value in query.items())
    url = f'https://id.twitch.tv/oauth2/authorize?{params}'

    return url


def get_redirect_uri(host: str, port: int) -> str:
    """Create a URL for the redirect URI"""
    return f'http://{host}:{port}'