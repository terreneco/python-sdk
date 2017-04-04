import requests
from core.apps import ServiceManagementClient, Service
from utils.exceptions import NotAuthorizedError, NotFoundError, UnknownError
from azure.servicebus import ServiceBusService


class Collector(Service):

    _access_key_value = None
    _access_key_name = None
    _access_namespace = None
    _hub = None

    _service_bus = None

    def write(self, data, hub=None):
        """
        Args:
            data: a dictionary of data to write to
                the collector
            hub: the hub to write to

        Returns:
            None

        Raises:
            NotAuthorizedError: if the write operation
                wasn't authorized
            NotFoundError: if the collector's endpoint
                could not be found
            UnknownError: if an unexpected error happened
        """
        if hub is None:
            hub = self._hub

        if self._service_bus:
            self._service_bus.send_event(
                hub_name=hub,
                message=data
            )
        else:
            raise NotFoundError()

    def _setup(self):
        """
        Returns: None
        """
        if None in [
            self._access_namespace,
            self._access_key_name,
            self._access_key_value,
            self._hub
        ]:
            self._retrieve_keys()

        if self._service_bus is None:
            self._service_bus = ServiceBusService(
                service_namespace=self._access_namespace,
                shared_access_key_name=self._access_key_name,
                shared_access_key_value=self._access_key_value
            )

    def _retrieve_keys(self):
        """
        Returns: None
        """
        res = requests.get(
            self._path + "keys/",
            headers=self._headers
        )
        if res.status_code == 200:
            self._access_key_name = res.json().get('key_name')
            self._access_key_value = res.json().get('key_value')

            self._access_namespace = res.json().get('namespace')

            self._hub = res.json().get('hub')


class CollectorManagementClient(ServiceManagementClient):

    _namespace = "collectors"
    _resource_class = Collector
