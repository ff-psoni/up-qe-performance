from base.base_user import BaseTest
import time

import requests
from locust import events

class ConfigMicroservicesBaseHTTPUser(BaseTest):
    abstract = True
    _client_secret = ""  # _client_secret needs to be passed through command line argument
    _access_token = None
    _token_expires_at = 0

    def _get_headers(self):
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Accept": "application/json;version=v2"}
        return headers

    def get_access_token(self):
        if self._access_token is None or time.time() >= self._token_expires_at:
            token_url = "https://uplight-external-stg.us.auth0.com/oauth/token"
            client_id = "VyPLdyjDEZDeUsKfgmdYPiklqE2WCdkk"
            client_secret = self._client_secret
            payload = {"client_id": client_id,
                       "client_secret": client_secret,
                       "grant_type": "client_credentials"}
            self._access_token = requests.post(token_url, payload).json()['access_token']
            self._token_expires_at = time.time() + 3600 - 60  # Refresh 60 seconds before expiry
        return self._access_token

    def on_start(self):
        self._client_secret = self.environment.parsed_options.client_secret
        self._access_token = None
        self._token_expires_at = 0

    @events.init_command_line_parser.add_listener
    def _(parser):
        parser.add_argument("--client_secret", type=str, required=True)
