import json
import os
import typing

import catboost
import lightgbm
import pandas as pd
import structlog
import xgboost

from treeserve.api import treeserve_pb2

_not_implemented_error = NotImplementedError('only regression/classification models are supported')


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
                model = _loader(path, framework, task)
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


def _loader(path: str, framework: str, task: str) -> typing.Union[catboost.CatBoost, lightgbm.Booster, xgboost.Booster]:
    if framework == 'catboost':
        # todoL add support for different file formats. currently .cbm is supported
        if task == 'regression':
            return catboost.CatBoostRegressor().load_model(fname=path)
        elif task == 'classification':
            return catboost.CatBoostClassifier().load_model(fname=path)
        else:
            raise _not_implemented_error
    elif framework == 'lightgbm':
        return lightgbm.Booster(model_file=path)
    elif framework == 'xgboost':
        if task == 'regression':
            m = xgboost.XGBRegressor()
            m.load_model(fname=path)
            return m
        elif task == 'classification':
            m = xgboost.XGBClassifier()
            m.load_model(fname=path)
            return m
        else:
            raise _not_implemented_error
    else:
        raise ValueError('requested framework is not supported')
