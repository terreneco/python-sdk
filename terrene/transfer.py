from .apps import BaseApp, BaseAppManager
from .api import BaseModelManager
from .config import api
from coreapi.utils import File

import uuid
import json
import pandas
import io
import requests
import os


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
    namespace = ['transfer', 'input', 'file']
    _file = None

    def pre_create(self, **params):
        params['workspace'] = self.workspace.object_id
        params['parser'] = params['parser'].object_id
        params['file'].seek(0)
        params['file'] = File(str(uuid.uuid4()), params['file'].read())

        return params

    def pre_save(self):
        for param in ['workspace', 'parser']:
            if self._data.get(param, None) is not None and \
                    not isinstance(self._data[param], str):
                self._data[param] = self._data[param].object_id


class FileOutputManager(BaseModelManager):
    namespace = ['transfer', 'output', 'file']
    path = './batch-outputs/'
    batch_preds = []

    def __init__(self):
        self.batch_preds = self.query({})

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def save_all_content(self):
        for pred in self.batch_preds:
            content = requests.get(api() + '/transfer/output/file/{}/raw'.format(pred.object_id),
                                   headers=self.headers).content
            dataframe = pandas.read_csv(io.StringIO(content.decode('utf-8')))
            dataframe.to_csv(self.path + pred.object_id + '.csv')

    def save_single_content(self, obj_id):
        content = requests.get(api() + '/transfer/output/file/{}/raw'.format(obj_id),
                               headers=self.headers).content
        dataframe = pandas.read_csv(io.StringIO(content.decode('utf-8')))
        dataframe.to_csv(self.path + obj_id + '.csv')


class DataParserManager(BaseModelManager):
    namespace = ['transfer', 'parsers']
    filename = ''

    CSVParser = None
    JSONParser = None
    HTMLParser = None

    def __init__(self, **kwargs):
        self.filename = kwargs['filename']
        parsers = self.query({})

        parser_map = {'CSV Parser': 'CSVParser', 'HTML Parser': 'HTMLParser', 'JSON Parser': 'JSONParser'}
        for parser in parsers:
            try:
                setattr(self, parser_map[parser.name], parser)
            except KeyError:
                pass

    def set_default_parser(self):
        if self.filename.endswith('.csv'):
            return self.CSVParser
        elif self.filename.endswith('.json'):
            return self.JSONParser
        elif self.filename.endswith('.html'):
            return self.HTMLParser
        else:
            print('No default parser selected for this file type')
            return None


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
