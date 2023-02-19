import grpc

from mldeploy.api import mldeploy_pb2_grpc, mldeploy_pb2
from mldeploy.model_manager import manager


class DeploymentServiceServicer(mldeploy_pb2_grpc.DeploymentServiceServicer):

    def __init__(self, model_manager: manager.Manager):
        self.manager = model_manager

    async def Deploy(self, request: mldeploy_pb2.DeployRequest, context: grpc.ServicerContext) -> \
            mldeploy_pb2.DeployResponse:
        try:
            self.manager.add_or_update_model(request.model_name)
            context.set_code(grpc.StatusCode.OK)
            context.set_details(f'model name: {request.model_name}')
            return mldeploy_pb2.DeployResponse(model_name=request.model_name)
        except FileNotFoundError:
            self.manager.logger.critical('failed to add model', **{'name': request.model_name})
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'model name: {request.model_name}')
            return mldeploy_pb2.DeployResponse()

    async def Info(self, request: mldeploy_pb2.InfoRequest, context: grpc.ServicerContext) \
            -> mldeploy_pb2.InfoResponse:
        try:
            info = self.manager.get_info(request.model_name)
            context.set_code(grpc.StatusCode.OK)
            context.set_details(f'model name: {request.model_name}')
            return mldeploy_pb2.InfoResponse(info=info)
        except KeyError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'failed to get info for model: {request.model_name}')
            return mldeploy_pb2.InfoResponse()

    async def Predict(self, request: mldeploy_pb2.PredictRequest, context: grpc.ServicerContext) \
            -> mldeploy_pb2.PredictResponse:
        try:
            if request.version == 0:
                predictions = await self.manager.get_predictions(request.model_name, request.input_data)
            else:
                predictions = await self.manager.get_predictions(request.model_name, request.input_data,
                                                                 request.version)
            context.set_code(grpc.StatusCode.OK)
            return mldeploy_pb2.PredictResponse(model_name=request.model_name, predictions=predictions)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'failed to get predictions for model: {request.model_name}. Error: {str(e)}')
            return mldeploy_pb2.PredictResponse()
