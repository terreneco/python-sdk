from .apps import BaseApp, BaseAppManager
from coreapi.utils import File

import uuid
import json


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

    def initiate_file(self, **params):
        params['workspace'] = self.workspace.object_id
        params['file'].seek(0)
        params['file'] = File(str(uuid.uuid4()), params['file'].read())

        return params

    def pre_save(self):
        for param in ['workspace', 'parser']:
            if self._data.get(param, None) is not None and \
                    not isinstance(self._data[param], str):
                self._data[param] = self._data[param].object_id


class DataParserManager(FileInputManager):
    all_parsers = None
    selected_parser = None

    def pre_create(self, **params):
        params = self.initiate_file(**params)

        self.all_parsers = self.read_parsers().results
        params['parser'] = self.preset_parser(params['file'].name).object_id

        self.pre_save()

    def read_parsers(self):
        return self.act(['transfer', 'parsers'], None)  # fix this

    def preset_parser(self, filename):
        csv_index = 0
        json_index = 0
        html_index = 0

        for index, parser in enumerate(self.all_parsers):
            if parser.name == 'CSV Parser':
                csv_index = index
            elif parser.name == 'JSON Parser':
                json_index = index
            elif parser.name == 'HTML Parser':
                html_index = index

        if filename.endswith('.csv'):
            self.selected_parser = self.all_parsers[csv_index]
            return self.selected_parser
        elif filename.endswith('.json'):
            self.selected_parser = self.all_parsers[json_index]
            return self.selected_parser
        elif filename.endswith('.html'):
            self.selected_parser = self.all_parsers[html_index]
            return self.selected_parser
        else:
            return None

    def set_parser(self, **params):
        params['parser'] = self.selected_parser.object_id


class CSVInputManager(DataParserManager):
    namespace = []


class WarehouseQueryInputManager(InputDatasetManager):
    namespace = ['transfer', 'input', 'warehouse_query']

    def pre_create(self, **params):
        params['store'] = params['store'].object_id
        params['workspace'] = self.workspace.object_id
        return params

    def pre_save(self):
        for param in ['store', 'workspace']:
            if self._data.get(param, None) is not None and \
                    not isinstance(self._data[param], str):
                self._data[param] = self._data[param].object_id
