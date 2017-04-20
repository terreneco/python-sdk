import requests
from terrene.utils.exceptions import UnknownError
from terrene.core.apps import Service, ServiceManagementClient


class Storage(Service):

    _access_key = None
    _access_namespace = None
    _service = None
    _service_class = None

    def _setup(self):
        """
        Returns: None
        """
        if None in [
            self._access_key,
            self._access_namespace
        ]:
            self._retrieve_keys()

        if self._service is None:
            self._service = self._service_class(
                account_name=self._access_namespace,
                account_key=self._access_key
            )
            pass

    def update_record(self, updated_record, table_name):
        raise NotImplementedError()

    def insert_record(self, data, table_name):
        raise NotImplementedError()

    def delete_record(self, data, table_name):
        raise NotImplementedError()

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
    pass
