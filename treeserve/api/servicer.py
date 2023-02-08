import grpc

from treeserve.api import treeserve_pb2_grpc, treeserve_pb2
from treeserve.model_manager import manager


class DeploymentServiceServicer(treeserve_pb2_grpc.DeploymentServiceServicer):

    def __init__(self, model_manager: manager.Manager):
        self.manager = model_manager

    async def Deploy(self, request: treeserve_pb2.DeployRequest, context: grpc.ServicerContext) -> \
            treeserve_pb2.DeployResponse:
        try:
            self.manager.add_or_update_model(request.model_name)
            context.set_code(grpc.StatusCode.OK)
            context.set_details(f'model name: {request.model_name}')
            return treeserve_pb2.DeployResponse(model_name=request.model_name)
        except FileNotFoundError:
            self.manager.logger.critical('failed to add model', **{'name': request.model_name})
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'model name: {request.model_name}')
            return treeserve_pb2.DeployResponse()

    async def Info(self, request: treeserve_pb2.InfoRequest, context: grpc.ServicerContext) \
            -> treeserve_pb2.InfoResponse:
        try:
            metadata = self.manager.get_info(request.model_name)
            context.set_code(grpc.StatusCode.OK)
            context.set_details(f'model name: {request.model_name}')
            return treeserve_pb2.InfoResponse(model_name=metadata['name'], model_version=metadata['version'],
                                              created_ts=metadata['timestamp'])
        except KeyError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'failed to get info for model: {request.model_name}')
            return treeserve_pb2.InfoResponse()

    async def Predict(self, request: treeserve_pb2.PredictRequest, context: grpc.ServicerContext) \
            -> treeserve_pb2.PredictResponse:
        try:
            predictions = await self.manager.get_predictions(request.model_name, request.input_data)
            context.set_code(grpc.StatusCode.OK)
            return treeserve_pb2.PredictResponse(model_name=request.model_name, predictions=predictions)
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'failed to get predictions for model: {request.model_name}')
            return treeserve_pb2.PredictResponse()
