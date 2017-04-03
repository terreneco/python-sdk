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
    _headers_dict = {}
    object_id = None

    _data = {}

    @property
    def _headers(self):

        headers = self._headers_dict

        if self._auth is not None:
            headers["Authorization"] = self._auth.authorization_header

        return headers

    def __init__(self, object_id, namespace, auth=None, headers={}):
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
        self._headers_dict = headers
        self._auth = auth
        self._namespace = namespace

        # retrieve the object from the API
        self._retrieve()

        # setup hook
        self._setup()

    def _setup(self):
        """
        Returns: None
        """
        pass

    @property
    def _path(self):
        return '%s/%s/%s/' % (
            get_api_url(),
            self._namespace,
            self.object_id
        )

    def _retrieve(self):
        """
        Args:

        Returns:
            None

        Raises:
            NotAuthorizedError: if res.status_code is 401
            NotFoundError: if res.status_code is 404
            UnknownError: when res.status code is not in [200, 401, 404]
        """
        res = requests.get(
            self._path,
            headers=self._headers
        )
        if res.status_code == 200:
            self._data = res.json()
        elif res.status_code == 401:
            raise NotAuthorizedError()
        elif res.status_code == 404:
            raise NotFoundError()
        else:
            raise UnknownError()

    def delete(self):
        """
        Args:

        Returns:
            None

        Raises:
            NotAuthorizedError: if the delete is not authorized
            NotFoundError: if the resource was not found
            UnknownError: an unexpected error happened
        """
        res = requests.delete(
            self._path,
            headers=self._headers
        )
        if res.status_code in [403, 401]:
            raise NotAuthorizedError()
        elif res.status_code == 404:
            raise NotFoundError()
        elif res.status_code == 204:
            return None
        else:
            raise UnknownError()

    def update(self, parameters):
        """
        Args:
            parameters: a dictionary of parameters to be updated

        Returns:
            None

        Raises:
            NotAuthorizedError: if the update is not authorized
            NotFoundError: if the resource was not found
            UnknownError: an unexpected error happened
        """
        res = requests.put(
            self._path,
            data=parameters,
            headers=self._headers
        )
        if res.status_code in [403, 401]:
            raise NotAuthorizedError()
        elif res.status_code == 404:
            raise NotFoundError()
        elif res.status_code == 200:
            # update the object again
            self._retrieve()
        else:
            raise UnknownError()

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError

    def __str__(self):
        from beeprint import pp
        return pp(vars(self), output=False)


class APIResourceManagementClient(object):
    """
    Used to interact with a certain type
    of resource
    """

    _namespace = None
    _auth = None
    _resource_class = None

    @property
    def _headers(self):

        headers = {}

        if self._auth is not None:
            headers["Authorization"] = self._auth.authorization_header

        return headers

    def __init__(self, auth=None):
        """
        Args:
            auth: a credentials object

        Returns:
            None

        Raises:
            NotImplementedError: if the _namespace attribute is not
                set by the child class
        """
        if None in [self._namespace, self._resource_class]:
            raise NotImplementedError()
        self._auth = auth

    def create(self, parameters):
        """
        Args:
            parameters: a list of parameters for this resource
             to be created according to

        Returns:
            self._resource_class instance
        
        Raises:
            None
        """
        res = requests.post(
            "%s/%s/" % (
                get_api_url(),
                self._namespace
            ),
            data=parameters,
            headers=self._headers
        )
        if res.status_code == 201:
            return self.get(res.json().get('object_id'))
        raise UnknownError

    def get(self, object_id):
        """
        Args:
            object_id: the unique identifier of the object
                to be retrieved

        Returns:
            self._resource_class instance

        Raises:
            None
        """
        return self._resource_class(
            object_id=object_id,
            namespace=self._namespace,
            auth=self._auth
        )

    def delete(self, object_id):
        return self.get(object_id).delete()

    def list(self, parameters={}):
        """
        Args:
            parameters: a dictionary to filter the resources
                within _namespace based on

        Returns:
            List[APIResource]

        Raises:
            NotAuthorizedError: if the _auth is not authorized
                to access the _namespace
            NotFoundError: if the _namespace was not found
            UnknownError: an unexpected error happened
        """
        res = requests.get(
            "%s/%s" % (
                get_api_url(),
                self._namespace
            ),
            params=parameters,
            headers=self._headers
        )
        if res.status_code == 200:
            resources = []
            for resource in res.json().get('results'):
                resources.append(
                    self._resource_class(
                        object_id=resource.get('object_id'),
                        namespace=self._namespace,
                        auth=self._auth
                    )
                )
            return resources
        elif res.status_code == 401:
            raise NotAuthorizedError()
        elif res.status_code == 404:
            raise NotFoundError()
        else:
            raise UnknownError()

    def __str__(self):
        from beeprint import pp
        return pp(vars(self), output=False)
