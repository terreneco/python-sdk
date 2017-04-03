import requests
from core.apps import ServiceManagementClient, Service
from utils.exceptions import NotAuthorizedError, NotFoundError, UnknownError
from azure.storage.table import TableService, Entity
import uuid


class StorageResource(object):

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

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError

    def __str__(self):
        from beeprint import pp
        return pp(vars(self), output=False)


class Storage(Service):

    _access_key = None
    _access_namespace = None

    _table_service = None

    def _setup(self):
        """
        Returns: None
        """
        if None in [
            self._access_key,
            self._access_namespace
        ]:
            self._retrieve_keys()

        if self._table_service is None:
            self._table_service = TableService(
                account_name=self._access_namespace,
                account_key=self._access_key
            )
            pass

    def update_record(self, updated_record, table_name):
        entity = Entity()
        for key, val in updated_record.items():
            entity[key] = val

        self._table_service.update_entity(
            table_name=table_name,
            entity=entity
        )

    def insert_record(self, data, table_name):
        entity = Entity()
        entity.PartitionKey = table_name
        entity.RowKey = str(uuid.uuid4())
        for key, val in data.items():
            entity[key] = val

        self._table_service.insert_entity(
            table_name=table_name,
            entity=entity
        )

    def delete_record(self, data, table_name):
        self._table_service.delete_entity(
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
        items = self._table_service.query_entities(
            table_name=table_name,
            filter=filter_str,
            select=select_str
        )
        for item in items:
            records.append(StorageResource(
                storage=self,
                table_name=table_name,
                data=item
            ))
        return records

    def create_table(self, table_name):
        """
        Args:
            table_name: the name of the table to be created
        Returns: None
        Raises:
            UnknownError: when the table could not be created
        """
        res = requests.post(
            self._path + 'create_table/',
            data={
                'table_name': table_name
            },
            headers=self._headers
        )
        if res.status_code is not 201:
            raise UnknownError

    def drop_table(self, table_name):
        """
        Args:
            table_name: the name of the table to be created
        Returns: None
        Raises:
            UnknownError: when the table could not be created
        """
        res = requests.post(
            self._path + 'drop_table/',
            data={
                'table_name': table_name
            },
            headers=self._headers
        )
        if res.status_code is not 200:
            raise UnknownError

    def _retrieve_keys(self):
        """
        Returns: None
        """
        res = requests.get(
            self._path + "keys/",
            headers=self._headers
        )

        if res.status_code == 200:
            self._access_namespace = self._data.get('storage_account_name')
            self._access_key = res.json().get('key')


class StorageManagementClient(ServiceManagementClient):

    _namespace = "warehouses"
    _resource_class = Storage
