from identitylib.photo_client.configuration import Configuration
from identitylib.api_client_mixin import ClientCredentialsConfigurationMixin


class PhotoClientConfiguration(Configuration, ClientCredentialsConfigurationMixin):

    def __init__(self, client_key, client_secret, access_token_url, *args, **kwargs):

        Configuration.__init__(self, *args, **kwargs)
        ClientCredentialsConfigurationMixin.__init__(
            self, client_key, client_secret, access_token_url
        )
