import asyncio
import argparse

from mldeploy.server import server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='mldeploy',
        description='set port number and artefact path',
        add_help=True
    )
    parser.add_argument('-port', default=8000, help='set the gRPC port', required=False)
    parser.add_argument('-path', default='artefacts/', help='set the artefacts path', required=False)
    args = parser.parse_args()
    asyncio.run(server.serve(int(args.port), args.path))
