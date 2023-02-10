from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeployRequest(_message.Message):
    __slots__ = ["model_name"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    def __init__(self, model_name: _Optional[str] = ...) -> None: ...

class DeployResponse(_message.Message):
    __slots__ = ["model_name"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    def __init__(self, model_name: _Optional[str] = ...) -> None: ...

class InfoRequest(_message.Message):
    __slots__ = ["model_name"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    def __init__(self, model_name: _Optional[str] = ...) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ["info"]
    INFO_FIELD_NUMBER: _ClassVar[int]
    info: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, info: _Optional[_Iterable[str]] = ...) -> None: ...

class PredictRequest(_message.Message):
    __slots__ = ["input_data", "model_name", "version"]
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    input_data: str
    model_name: str
    version: int
    def __init__(self, model_name: _Optional[str] = ..., input_data: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class PredictResponse(_message.Message):
    __slots__ = ["model_name", "predictions"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    predictions: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, model_name: _Optional[str] = ..., predictions: _Optional[_Iterable[float]] = ...) -> None: ...
