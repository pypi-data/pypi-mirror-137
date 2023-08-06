from unittest import TestCase, mock
from identitylib.api_client_mixin import ClientCredentialsConfigurationMixin


class TestApiClientConfigurationMixin(TestCase):
    class MockResponse:
        """ mock the api post response """

        def __init__(self, response_status_code, response_text, response_data):
            self.status_code = response_status_code
            self.text = response_text
            self.response_data = response_data

        def __iter__(self):
            return self

        def __next__(self):
            return self

        def json(self):
            return self.response_data

    @mock.patch('identitylib.api_client_mixin.requests.post', side_effect=MockResponse(
        200, "api responds 200", {'access_token': 'new_access_token'}
    ))
    def test_refresh_access_token(self, mock_post):
        """ check the mixin refreshes access token """

        configuration = ClientCredentialsConfigurationMixin(
            'client_key', 'client_secret', 'access_token_url'
        )
        configuration._refresh_access_token()

        self.assertEqual('new_access_token', configuration.access_token)

    @mock.patch('identitylib.api_client_mixin.requests.post', side_effect=MockResponse(
        401, "api responds 401",
        {"fault": {"faultstring": "Invalid access token",
                   "detail": {"errorcode": "oauth.v2.InvalidAccessToken"}}}
    ))
    def test_refresh_access_token_fails(self, mock_post):
        """ check the mixin correctly raises exception when server responds 401 """

        with self.assertRaises(RuntimeError):
            configuration = ClientCredentialsConfigurationMixin(
                'client_key', 'client_secret', 'access_token_url'
            )
            configuration._refresh_access_token()

    @mock.patch('identitylib.api_client_mixin.requests.post', side_effect=MockResponse(
        200, "no access_token", {'no_access_token': 'not_an_access_token'}
    ))
    def test_refresh_access_token_no_token(self, mock_post):
        """ check the mixin correctly raises exception when no access_token in response """

        with self.assertRaises(RuntimeError):
            configuration = ClientCredentialsConfigurationMixin(
                'client_key', 'client_secret', 'access_token_url'
            )
            configuration._refresh_access_token()
