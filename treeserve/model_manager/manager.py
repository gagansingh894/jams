import json
import os

import pandas as pd
import structlog

from treeserve.model_manager import utils
from treeserve.api import treeserve_pb2


class Manager:

    def __init__(self, path: str):
        self.logger = structlog.getLogger(self.__class__.__name__)
        self.path = path
        self.models = {}

    def _download_model(self):
        pass

    def add_or_update_model(self, model_name: str):
        for file_name in os.listdir(self.path):
            split_name = file_name.split('_')
            name, task, framework, version = split_name[0], split_name[1], split_name[-2], split_name[-1].split('.')[0]
            path = f'{self.path}/{file_name}'
            if name == model_name:
                model = utils.loader(path, framework, task)
                self.models[name] = model
                self.logger.info('model added successfully', **{
                    'name': name,
                    'framework': framework,
                    'version': version
                })
                return
        raise FileNotFoundError('model does not exist')

    def get_predictions(self, request: treeserve_pb2.PredictRequest):
        # convert string to json, json to dataframe, dataframe to numpy and then predict
        data = pd.DataFrame(json.loads(request.input_data)).values
        return self.models[request.model_name].predict(data)
