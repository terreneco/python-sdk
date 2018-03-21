import unittest


class TransferTestCases(unittest.TestCase):
    def test_csv_dataset_creation_and_deletion(self):
        import os
        from terrene.auth import EmailPasswordCredentials
        from terrene.apps import WorkspaceManager
        from terrene.transfer import FileInputManager, DataParserManager

        credentials = EmailPasswordCredentials(
            email=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'))

        workspace_manager = WorkspaceManager(credentials=credentials)

        data_parser_manager = DataParserManager(credentials=credentials)
        workspace = workspace_manager.create(
            name="My Workspace", description="A workspace for Terrene's tutorial")

        file_input_manager = FileInputManager(
            credentials=credentials, workspace=workspace)
        with open('tests/dist/train.csv', 'r') as input_file:
            csv_file_input = file_input_manager.create(
                name="my file", description="training dataset", parser=data_parser_manager.CSVParser,
                workspace=workspace.object_id, file=input_file)

        # csv_file_input.delete()
        # workspace.delete()
