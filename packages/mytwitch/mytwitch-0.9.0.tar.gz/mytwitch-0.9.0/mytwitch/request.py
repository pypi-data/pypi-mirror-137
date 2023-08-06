import requests
import json
import lzon

from typing import Callable

from .exceptions import APIRequestError



class APIRequest:
    """An HTTP request to the Twitch API"""

    def __init__(self, method: Callable, *args, **kwargs):
        # Use the corresponding function from requests
        if method == 'GET':
            self.method = requests.get
        elif method == 'POST':
            self.method = requests.post
        elif method == 'DELETE':
            self.method = requests.delete
        else:
            raise ValueError('Method must be either GET, POST, or DELETE')

        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.send()

    def send(self):
        """Send the request and return the response"""

        # Send request and unpack JSON payload
        response = self.method(*self.args, **self.kwargs)

        # Try to parse content if body is returned
        try:
            content = json.loads(response.content)
        except json.JSONDecodeError:
            content = {}
        
        # Twitch API error
        if 'status' in content:
            raise APIRequestError(
                content['status'],
                content['message']
            )

        return lzon.loads(content)