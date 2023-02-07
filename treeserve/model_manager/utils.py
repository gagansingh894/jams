import concurrent.futures
import typing

import catboost
import lightgbm
import xgboost


worker_pool = concurrent.futures.ProcessPoolExecutor(2)
_not_implemented_error = NotImplementedError('only regression/classification models are supported')


def loader(path: str, framework: str, task: str) -> typing.Union[catboost.CatBoost, lightgbm.Booster, xgboost.Booster]:
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
