from terrene.core.api import APIResourceManagementClient, APIResource


class Service(APIResource):
    pass


class ServiceManagementClient(APIResourceManagementClient):

    _resource_class = Service
