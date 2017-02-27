import requests
from core.apps import ServiceManagementClient, Service
from utils.exceptions import NotAuthorizedError, NotFoundError, UnknownError


class Collector(Service):

    _access_key = None
    _connection_string = None

    def write(self, data):
        """
        Args:
            data: a dictionary of data to write to
                the collector

        Returns:
            None

        Raises:
            NotAuthorizedError: if the write operation
                wasn't authorized
            NotFoundError: if the collector's endpoint
                could not be found
            UnknownError: if an unexpected error happened
        """
        pass

    def _setup(self):
        """
        Returns: None
        """
        if self._access_key is None or self._connection_string is None:
            self._retrieve_keys()

    def _retrieve_keys(self):
        """
        Returns: None
        """
        res = requests.get(
            self._path + "/keys/",
            headers=self._headers
        )
        if res.status_code == 200:
            self._connection_string = res.json().get('connection_string')
            self._access_key = res.json().get('key')


class CollectorManagementClient(ServiceManagementClient):

    _namespace = "collectors"
    _resource_class = Collector
