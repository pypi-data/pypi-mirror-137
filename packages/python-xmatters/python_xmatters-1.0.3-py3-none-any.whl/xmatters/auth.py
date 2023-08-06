import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from xmatters import errors as err
from xmatters.connection import Connection


class OAuth2Auth(Connection):
    _endpoints = {'token': '/oauth2/token'}

    def __init__(self, base_url, client_id, token=None, username=None, password=None, token_storage=None, **kwargs):
        """
        Class used to authentication requests using OAuth2 authentication.

        The method used to obtain a token are used in the following order:  token, username & password, token_storage.

        :param base_url: xMatters instance url or xMatters instance base url
        :type base_url: str
        :param client_id: xMatters instance client id
        :type client_id: str
        :param token: Authentication token. Can be just a refresh token (as a str) or a token object (as a dict)
        :type token: str or dict, optional
         :param username: xMatters username
        :type username: str, optional
        :param password: xMatters password
        :type password: str, optional
        :param token_storage: Class instance used to store token returned during a refresh.
            Any class instance will be accepted as long as it has "read_token" and "write_token" methods.
        :type token_storage: :class:`xmatters.utils.TokenFileStorage`, optional
        """
        self.client_id = client_id
        self.token_storage = token_storage
        self.username = username
        self.password = password
        self._token = token
        self.session = None
        token_url = '{}{}'.format(base_url, self._endpoints.get('token'))
        client = LegacyApplicationClient(client_id=self.client_id)
        auto_refresh_kwargs = {'client_id': self.client_id}
        token_updater = self.token_storage.write_token if self.token_storage else None
        self.session = OAuth2Session(client=client, auto_refresh_url=token_url,
                                     auto_refresh_kwargs=auto_refresh_kwargs,
                                     token_updater=token_updater)
        self.session.token = self.get_token()

        # update storage token if differs from self.token
        if self.token_storage and self.token_storage.read_token() != self.token:
            self.token_storage.write_token(self.token)

        super(OAuth2Auth, self).__init__(base_url, self.session, **kwargs)

    def get_token(self):
        if self._token and isinstance(self._token, dict):
            return self._token
        elif self._token and isinstance(self._token, str):
            return self.session.refresh_token(token_url=self.session.auto_refresh_url, refresh_token=self._token,
                                              timeout=3,
                                              kwargs=self.session.auto_refresh_kwargs)
        elif None not in (self.username, self.password):
            return self.session.fetch_token(token_url=self.session.auto_refresh_url, username=self.username,
                                            password=self.password, include_client_id=True, timeout=3)
        elif self.token_storage and self.token_storage.read_token():
            return self.token_storage.read_token()
        else:
            raise err.XMSessionError('Unable to obtain token with provided arguments')

    @property
    def token(self):
        return self.session.token if self.session else self._token

    @token.setter
    def token(self, token):
        if self.session:
            self.session.token = token
        else:
            self._token = token

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class BasicAuth(Connection):
    def __init__(self, base_url, username, password, **kwargs):
        """
        Class used to authentication requests using basic authentication

        :param base_url: xMatters instance url or xMatters instance base url
        :type base_url: str
        :param username: xMatters username
        :type username: str
        :param password: xMatters password
        :type password: str
        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        super(BasicAuth, self).__init__(base_url, self.session, **kwargs)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
