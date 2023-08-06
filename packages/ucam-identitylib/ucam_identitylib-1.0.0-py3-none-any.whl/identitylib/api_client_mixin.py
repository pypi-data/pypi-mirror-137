import requests
from logging import getLogger

LOG = getLogger(__name__)


class ClientCredentialsConfigurationMixin(object):

    """ mixin to support client_credentials authentication flow """

    def __init__(self, client_key, client_secret, access_token_url):

        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token_url = access_token_url

        self.access_token = None
        self.refresh_api_key_hook = self._refresh_access_token()

    def _refresh_access_token(self):
        """ refresh the access token """

        LOG.debug("Refreshing API access token")

        auth = requests.auth.HTTPBasicAuth(self.client_key, self.client_secret)
        data = {"grant_type": "client_credentials"}

        response = requests.post(self.access_token_url, data=data, auth=auth)

        if response.status_code != 200 or not response.json().get('access_token'):
            raise RuntimeError(
                f'Access token request failed: {response.status_code}, {response.text}'
            )

        self.access_token = response.json()['access_token']
