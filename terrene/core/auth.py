import requests
from terrene.core.api import APIResourceManagementClient, APIResource
from terrene.utils.urls import get_api_url
from terrene.utils.exceptions import NotAuthorizedError, UnknownError


class _AbstractCredentials(object):

    @property
    def authorization_header(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args:
            **kwargs:

        """
        self._setup(*args, **kwargs)

    def _setup(self, *args, **kwargs):
        """
        Args:
            *args:
            **kwargs:

        Returns:
            None

        Raises:
            NotImplementedError: all the time
        """
        raise NotImplementedError()

    def is_authorized(self):
        """
        Returns:
            True: if authorized
            False: if not authorized

        Raises:
            NotImplementedError: all the time
        """
        raise NotImplementedError()

    def __str__(self):
        from beeprint import pp
        return pp(vars(self), output=False)


class UserPassCredentials(_AbstractCredentials):

    object_id = None
    username = None
    _token = None

    def _setup(self, username, password):
        """
        Args:
            username: username of the user
            password: password of the user

        Returns:
            None
        """
        self.username = username
        self._login(password)

    def _login(self, password):
        """
        Args:
            password: password of the user

        Returns:
            None

        Raises:
            NotAuthorizedError: when the username password
                combo didn't work
            UnknownError: when an unknown error happened
        """
        res = requests.post(
            "%s/users/actions/login/" % get_api_url(),
            data={
                "email": self.username,
                "password": password
            }
        )
        if res.status_code == 401:
            raise NotAuthorizedError
        elif res.status_code == 200:
            self._token = res.json().get('token')
            self.object_id = res.json().get('object_id')
        else:
            raise UnknownError

    def is_authorized(self):
        """
        Returns:
            True: if authorized
            False: if not authorized
        """
        res = requests.post(
            "%s/users/actions/login/verify-token/" % get_api_url(),
            data={
                "token": self._token
            }
        )
        if res.status_code == 200:
            return True
        return False

    @property
    def authorization_header(self):
        return "JWT " + self._token


class JWTCredentials(_AbstractCredentials):

    @property
    def authorization_header(self):
        return "JWT " + self._token

    def _setup(self, token):
        """
        Args:
            token: JWT token

        Returns:
            None
        """
        self._token = token

    def is_authorized(self):
        """
        Returns:
            True: if authorized
            False: if not authorized
        """
        res = requests.post(
            "%s/users/actions/login/verify-token/" % get_api_url(),
            data={
                "token": self._token
            }
        )
        if res.status_code == 200:
            return True
        return False
