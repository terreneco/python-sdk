import requests
import uuid
from azure.storage.table import TableService, Entity, TableBatch
from .storage import Storage, StorageManagementClient


class TableStorageResource(object):

    _data = None
    _storage = None
    table_name = None

    def __init__(self, storage, table_name, data):
        self._data = data
        self._storage = storage
        self.table_name = table_name

    def partial_update(self, data):
        for key, val in data.items():
            if key in self._data:
                self._data[key] = val
        self._save()

    def _save(self):
        self._storage.update_record(self._data, self.table_name)

    def delete(self):
        self._storage.delete_record(self._data, self.table_name)

    def serialize(self):
        return self._data

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError

    def __str__(self):
        from beeprint import pp
        return pp(vars(self), output=False)


class TableStorage(Storage):

    _service_class = TableService

    def update_record(self, updated_record, table_name):
        entity = Entity()
        for key, val in updated_record.items():
            entity[key] = val

        self._service.update_entity(
            table_name=table_name,
            entity=entity
        )

    def insert_record(self, data, table_name):
        entity = Entity()
        entity.PartitionKey = table_name
        entity.RowKey = str(uuid.uuid4())
        for key, val in data.items():
            entity[key] = val

        self._service.insert_or_replace_entity(
            table_name=table_name,
            entity=entity
        )

    def insert_batch(self, data, table_name):
        batch = TableBatch()
        for entry in data:
            entity = Entity()
            entity.PartitionKey = table_name
            entity.RowKey = str(uuid.uuid4())
            for key, val in entry.items():
                entity[key] = val
            batch.insert_or_replace_entity(entry)
        self._service.commit_batch(table_name, batch)

    def delete_record(self, data, table_name):
        self._service.delete_entity(
            table_name,
            data.get('PartitionKey'),
            data.get('RowKey')
        )

    def query(self, filter_str, table_name, select_str=None):
        """
        Args:
            filter_str: a query string to filter for.
                e.g. "PartitionKey eq 'tasksSeattle'"
            table_name: the name of the table to run the query on
            select_str: the attributes to select from the table
                e.g. name, description
        Returns:
            list of StorageResource instances
    
        """

        records = []
        items = self._service.query_entities(
            table_name=table_name,
            filter=filter_str,
            select=select_str
        )
        for item in items:
            records.append(TableStorageResource(
                storage=self,
                table_name=table_name,
                data=item
            ))
        return records


class TableStorageManagementClient(StorageManagementClient):

    _namespace = "warehouses/table-storage"
    _resource_class = TableStorage
