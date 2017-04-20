from .exceptions import NotFoundError


def get_client(str_reference):

    """
    Args:
        str_reference: a refrence to a management client
            i.e. apps.storage.BlobStorage

    Returns: a subclass of apps.core.service.ServiceManagementClient
    Raises:
        NotFoundError: if the str_reference doesn't exist

    """

    if str_reference == "apps.storage.BlobStorage":
        from terrene.apps.storage import BlobStorageManagementClient
        return BlobStorageManagementClient

    elif str_reference == "apps.storage.TableStorage":
        from terrene.apps.storage import TableStorageManagementClient
        return TableStorageManagementClient

    elif str_reference == "apps.collectors.EventIngress":
        from terrene.apps.collectors import CollectorManagementClient
        return CollectorManagementClient

    raise NotFoundError
