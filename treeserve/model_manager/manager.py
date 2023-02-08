import asyncio
import concurrent.futures
import functools
import os

import structlog

from treeserve.model_manager import utils
from treeserve.api import treeserve_pb2


class Manager:

    def __init__(self, path: str, num_worker: int = 2):
        self.logger = structlog.getLogger(self.__class__.__name__)
        self.worker_pool = concurrent.futures.ProcessPoolExecutor(num_worker)
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

    async def get_predictions(self, request: treeserve_pb2.PredictRequest):
        loop = asyncio.get_event_loop()
        model = self.models[request.model_name]
        input_data = request.input_data
        result = await loop.run_in_executor(self.worker_pool, functools.partial(utils.predict, input_data, model))
        return result
