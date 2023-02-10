setup:
	pip install poetry

generate-proto:
	poetry run python -m grpc_tools.protoc -I proto/mldeploy/v1 --python_out=mldeploy/api/ --pyi_out=mldeploy/api/ --grpc_python_out=mldeploy/api/ mldeploy.proto
	protoc --go_out=. --go-grpc_out=. proto/mldeploy/v1/mldeploy.proto

run:
	poetry run python -m mldeploy.main