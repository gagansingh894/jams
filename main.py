import asyncio
import argparse
import grpc
import structlog

from treeserve.api import treeserve_pb2_grpc
from treeserve.model_manager.manager import Manager
from treeserve.api.servicer import DeploymentServiceServicer
from grpc_health.v1 import health

from grpc_health.v1 import health_pb2_grpc

logger = structlog.getLogger('server')


async def serve(port: int, model_artefact_path: str) -> None:
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
    await server.start()
    logger.info('starting server..', **{'port': 8000})
    await server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='treeserve',
        description='set port number and artefact path',
        add_help=True
    )
    parser.add_argument('-port', default=8000, help='set the gRPC port', required=False)
    parser.add_argument('-path', default='/artefacts', help='set the artefacts path', required=False)
    args = parser.parse_args()
    asyncio.run(serve(int(args.port), args.path))
