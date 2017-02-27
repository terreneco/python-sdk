import requests
from core.api import APIResourceManagementClient, APIResource
from utils.urls import get_api_url
from utils.exceptions import NotAuthorizedError, UnknownError


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
