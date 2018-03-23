import unittest


class TransferTestCases(unittest.TestCase):
    def test_csv_dataset_creation_and_deletion(self):
        import os
        from terrene.auth import EmailPasswordCredentials, TokenCredential
        from terrene.apps import WorkspaceManager
        from terrene.transfer import FileInputManager, DataParserManager, FileOutputManager

        # EmailPasswordCredentials(
        #     email=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'))
        TokenCredential()

        workspace_manager = WorkspaceManager()

        # workspaces = workspace_manager.query({})
        # for workspace in workspaces:
        #     workspace.delete()

        workspace = workspace_manager.create(
            name="My Workspace", description="A workspace for Terrene's tutorial")

        file_input_manager = FileInputManager(workspace=workspace)
        with open('tests/dist/train.csv', 'r') as input_file:
            data_parser_manager = DataParserManager(filename=input_file.name)
            csv_file_input = file_input_manager.create(
                name="my file", description="training dataset", parser=data_parser_manager.set_default_parser(),
                workspace=workspace.object_id, file=input_file)

        FileOutputManager().save_all_content()

        csv_file_input.delete()
        workspace.delete()
