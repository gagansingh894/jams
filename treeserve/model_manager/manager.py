import asyncio
import concurrent.futures
from datetime import datetime
import functools
import os
import typing

import structlog

from treeserve.model_manager import utils


class Manager:

    __slots__ = 'logger', 'worker_pool', 'num_versions', 'path', 'models'

    def __init__(self, path: str, num_worker: int = 2, num_versions: int = 5):
        self.logger = structlog.getLogger(self.__class__.__name__)
        self.worker_pool = concurrent.futures.ProcessPoolExecutor(num_worker)
        self.num_versions = num_versions
        self.path = path
        self.models = {}

    def _download_model(self):
        pass

    def add_or_update_model(self, model_name: str):
        for file_name in os.listdir(self.path):
            split_name = file_name.split('_')
            name, task, framework = split_name[0], split_name[1], split_name[-1].split('.')[0]
            path = f'{self.path}/{file_name}'
            if name == model_name:
                model = utils.loader(path, framework, task)
                version = len(self.models.get(name)) + 1 if self.models.get(name) else 1
                if version > self.num_versions:
                    oldest_version = min(self.models[name].keys())
                    del self.models[name][oldest_version]
                if model_name not in self.models:
                    self.models[name] = {version: {
                        'model': model,
                        'metadata': {
                            'name': name,
                            'version': 1,
                            'timestamp': str(datetime.now())
                        }
                    }}
                else:
                    self.models[name][version] = {
                        'model': model,
                        'metadata': {
                            'name': name,
                            'version': version,
                            'timestamp': str(datetime.now())
                        }
                    }

                self.logger.info('model added successfully', **{
                    'name': name,
                    'framework': framework,
                    'version': version
                })
                return
        raise FileNotFoundError('model does not exist')

    def get_info(self, model_name: str) -> typing.List:
        return [str(v['metadata']) for v in self.models[model_name].values()]

    async def get_predictions(self, model_name: str, input_data: str, version: int = None):
        loop = asyncio.get_event_loop()
        if version:
            model = self.models[model_name][version]['model']
        else:
            models = self.models[model_name]
            model = models[len(models)]['model']
        result = await loop.run_in_executor(self.worker_pool, functools.partial(utils.predict, input_data, model))
        return result
