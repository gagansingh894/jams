import concurrent.futures
import json
import os
import typing

import catboost
import joblib
import lightgbm
import pandas as pd
import sklearn.pipeline
import xgboost

num_worker = os.getenv("NUM_WORKERS") if os.getenv("NUM_WORKERS") else 1
worker_pool = concurrent.futures.ProcessPoolExecutor(num_worker)

_not_implemented_error = NotImplementedError('only regression/classification models are supported')


def loader(path: str, framework: str, task: str) -> typing.Union[catboost.CatBoost, lightgbm.Booster, xgboost.Booster,
                                                                 sklearn.pipeline.Pipeline]:
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
        m = xgboost.Booster()
        m.load_model(fname=path)
        return m
    else:
        try:
            obj = joblib.load(filename=path)
            if isinstance(obj, sklearn.pipeline.Pipeline):
                return obj
            else:
                raise ValueError("Only sklearn pipeline object deserialization is supported")
        except Exception as e:
            raise ValueError(e)


def predict(input_data: str, model: typing.Union[catboost.CatBoost, lightgbm.Booster, xgboost.Booster,
                                                 sklearn.pipeline.Pipeline]):
    # convert string to json, json to dataframe, dataframe to numpy and then predict
    model_input = pd.DataFrame(json.loads(input_data)).values
    return model.predict(model_input)
