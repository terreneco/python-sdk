from terrene.core.api import APIResourceManagementClient, APIResource


class Service(APIResource):

    def serialize(self):
        return self._data


class ServiceManagementClient(APIResourceManagementClient):

    _resource_class = Service
