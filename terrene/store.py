from .apps import BaseAppManager


class AbstractWarehouseManager(BaseAppManager):
    namespace = ['store', 'all']


class StandardWarehouseManager(AbstractWarehouseManager):
    namespace = ['store', 'azure']
