import asyncio
import grpc
import structlog

from treeserve.api import treeserve_pb2_grpc
from treeserve.model_manager.manager import Manager
from treeserve.api.servicer import DeploymentServiceServicer
from grpc_health.v1 import health

from grpc_health.v1 import health_pb2_grpc

logger = structlog.getLogger("server")


def create_server(port: int, model_artefact_path: str) -> grpc.aio.Server:
    # create manager
    manager = Manager(model_artefact_path)

    # create server
    server = grpc.aio.server()

    # add deployment service to server
    treeserve_pb2_grpc.add_DeploymentServiceServicer_to_server(
        DeploymentServiceServicer(manager), server)

    # add health service to server
    health_pb2_grpc.add_HealthServicer_to_server(
        health.HealthServicer(), server)

    server.add_insecure_port(f'[::]:{str(port)}')

    return server


async def serve():
    treeserve_server = create_server(8000, 'artefacts/')
    await treeserve_server.start()
    logger.info("starting server..", **{"port": 8000})
    await treeserve_server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
