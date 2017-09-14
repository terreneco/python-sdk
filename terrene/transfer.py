from .apps import BaseApp, BaseAppManager
from coreapi.utils import File


class InputDataset(BaseApp):
    pass


class InputDatasetManager(BaseAppManager):
    model = InputDataset
    namespace = ['transfer', 'input', 'all']


class FileInput(InputDataset):
    def upload(self, file):
        file.seek(0)
        return self.act(['upload', 'create'], {
            'object_id': self.object_id,
            'file': File(self.object_id, file.read())})


class FileInputManager(InputDatasetManager):
    model = FileInput
    namespace = ['transfer', 'input', 'file', 'all']
    _file = None

    def pre_create(self, **params):
        params['workspace'] = self.workspace.object_id
        params['store'] = params['store'].object_id
        params['file'].seek(0)
        params['file'] = File(params['store'], params['file'].read())
        return params


class CSVInputManager(FileInputManager):
    namespace = ['transfer', 'input', 'file', 'csv']
