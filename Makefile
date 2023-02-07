setup:
	pip install poetry

generate-proto:
	poetry run python -m grpc_tools.protoc -I proto/treeserve/v1 --python_out=treeserve/api/ --pyi_out=treeserve/api/ --grpc_python_out=treeserve/api/ treeserve.proto
	protoc --go_out=. --go-grpc_out=. proto/treeserve/v1/treeserve.proto

run:
	poetry run python -m treeserve.main