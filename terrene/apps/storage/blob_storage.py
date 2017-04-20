from .storage import Storage, StorageManagementClient
from azure.storage.blob import BlockBlobService
from terrene.utils.exceptions import UnsupportedOperationError


class BlobStorage(Storage):

    _service_class = BlockBlobService

    def insert_record(self, data, table_name):
        raise UnsupportedOperationError()

    def delete_record(self, data, table_name):
        raise UnsupportedOperationError()

    def update_record(self, updated_record, table_name):
        """
        Raises: UnsupportedOperationError
        """
        raise UnsupportedOperationError()


class BlobStorageManagementClient(StorageManagementClient):
    _namespace = "warehouses/blob-storage"
    _resource_class = BlobStorage

