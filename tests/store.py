import unittest


class StoreTestCases(unittest.TestCase):
    def test_standard_warehouse_creation_and_deletion(self):
        import os
        from terrene.auth import EmailPasswordCredentials
        from terrene.apps import WorkspaceManager
        from terrene.store import StandardWarehouseManager

        EmailPasswordCredentials(
            email=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'))

        workspace_manager = WorkspaceManager()
        workspace = workspace_manager.create(
            name="My Workspace", description="A workspace for Terrene's tutorial")

        standard_warehouse_manager = StandardWarehouseManager(
            workspace=workspace)
        store = standard_warehouse_manager.create(
            name="default storage", description="default warehouse for my workspace")

        store.delete()
        workspace.delete()
