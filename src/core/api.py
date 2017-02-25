import requests
from utils.urls import get_api_url
from utils.exceptions import NotAuthorizedError, NotFoundError, UnknownError


class APIResource(object):
    """
    Used to retrieve objects from Terrene's API
    and perform certain operations on it
    """

    _namespace = None
    _auth = None
    _headers = {}
    object_id = None

    _data = {}

    def __init__(self, object_id, namespace, auth=None, headers=None):
        """
        Args:
            object_id: a unique identifier for the resource
            namespace: the namespace this resource resides in
            auth: an authentication object used to authorize
                access to this resource
            headers: a set of parameters to be added
                as custom headers when making an API request
                to this resource

        Returns:
            None

        Raises:
            None
        """
        # set the public attributes
        self.object_id = object_id

        # set the private attributes
        self._headers = headers
        self._auth = auth
        self._namespace = namespace

        # retrieve the object from the API
        self.retrieve()

    def retrieve(self):
        """
        Args:

        Returns:
            None

        Raises:
            NotAuthorizedError: if res.status_code is 403
            NotFoundError: if res.status_code is 404
            UnknownError: when res.status code is not in [200, 403, 404]
        """
        res = requests.get(
            '%s/%s/%s/' % (
                get_api_url(),
                self._namespace,
                self.object_id
            )
        )
        if res.status_code == 200:
            self._data = res.json()
        elif res.status_code == 403:
            raise NotAuthorizedError()
        elif res.status_code == 404:
            raise NotFoundError()
        else:
            raise UnknownError()

    def delete(self):
        return NotImplementedError()

    def update(self):
        return NotImplementedError()

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError


class APIResourceManagementClient(object):
    """
    """

    def __init__(self):
        pass
