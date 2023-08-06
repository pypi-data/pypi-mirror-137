import threading
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Value
from ctypes import c_wchar_p



class AuthorizationApp:
    """A temporary HTTP server to host a page for the redirect URI from Twitch,
    and on that, send a POST request to another internally hosted route
    with the requested user access token which would otherwise only be accessible
    from the web browser and the user
    """

    def __init__(self, host: str = 'localhost', port: int = 6319):
        self.host = host
        self.port = port

        self.server = None

        # Start the authorization process
        self.start(self.host, self.port)

    def start(self, host: str, port: int) -> None:
        """Start HTTP server to begin the authorization process"""

        TemporaryServer.status = True
        self.server = HTTPServer((self.host, self.port), TemporaryServer)

        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def wait_for_shutdown(self) -> None:
        """Wait for a cue to shut down server"""

        while TemporaryServer.status:
            time.sleep(0.02)

        self.server.shutdown()
        self.thread.join()

    def get_token(self) -> str:
        """Get the user access token"""
        
        # Get the token
        token = TemporaryServer.token
        # Reset token field
        TemporaryServer.token = ""

        return token


class TemporaryServer(BaseHTTPRequestHandler):
    status = Value('b', False)
    token = Value(c_wchar_p, "")

    def _set_headers(self):
        """Set Content-Type of headers"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Redirect the user to send the only locally accessible user access token
        in a POST request to another route which will receive and extract it
        """

        self._set_headers()
        self.wfile.write(b"""
            <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>mytwitch Authentication</title>
                        
                        <style>
                            body {
                                background-color: #9146FF;

                                color: white;
                                font-family: 'Ubuntu', sans-serif;
                                font-size: 2em;
                            }
                            
                            .centered {
                                margin: 0;

                                position: absolute;
                                top: 50%;
                                left: 50%;
                                transform: translate(-50%, -50%);

                                text-align: center;
                            }

                            h1, h4 { margin: 1rem; }
                            h1 { font-size: 4em; } 

                            a[href] {
                                color: white;
                                text-decoration: none;
                            }
                        </style>
                    </head>

                    <body>
                        <span class="centered">
                            <h1><a href="https://gitlab.com/thedisruptproject/mytwitch">mytwitch</a></h1>

                            <noscript>
                                <h4>
                                    Please enable JavaScript! I need to redirect
                                    the user&nbsp;access&nbsp;token back to the application.
                                </h4>
                            </noscript>
                        </span>

                        <script lang="javascript">
                            let xmlhttp = new XMLHttpRequest()
                            
                            xmlhttp.open('POST', '/', true)

                            xmlhttp.onreadystatechange = () => {
                                window.close()
                            }

                            xmlhttp.setRequestHeader('Content-Type', 'application/json')
                            xmlhttp.send(document.location.hash)
                        </script>
                    </body>
                </html>
        """)

    def do_POST(self):
        """Receive and extract the user access token
        from the pound sign section of the redirect URL
        """

        # Get body from request
        self._set_headers()
        content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len).decode(encoding='UTF-8')

        # Remove # from the start
        body = body[1:]

        # Read parameters from string
        # by splitting at &s and =s

        params = {}

        for segment in body.split('&'):
            try:
                key, value = segment.split('=')
                params[key] = value
            
            except ValueError:
                # Ignore if segment could not be parsed
                # into exactly two strings, key and value
                continue

        if 'access_token' not in params:
            raise KeyError('`access_token` could not be found')

        # Save the received user access token
        type(self).token = params['access_token']

        # Send cue that server may be shut down
        type(self).status = False

    def log_message(self, format, *args):
        # Do not log anything
        return