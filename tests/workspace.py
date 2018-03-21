import unittest


class WorkspaceTestCases(unittest.TestCase):
    def test_workspace_creation_and_deletion(self):

        import os
        from terrene.auth import EmailPasswordCredentials
        from terrene.apps import WorkspaceManager

        EmailPasswordCredentials(
            email=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'))

        workspace_manager = WorkspaceManager()
        workspace = workspace_manager.create(
            name="My Workspace", description="A workspace for Terrene's tutorial")

        workspace.delete()
