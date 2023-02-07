from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional

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
    __slots__ = []
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ["info"]
    class InfoEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INFO_FIELD_NUMBER: _ClassVar[int]
    info: _containers.ScalarMap[str, str]
    def __init__(self, info: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PredictRequest(_message.Message):
    __slots__ = ["input_data", "model_name"]
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    input_data: str
    model_name: str
    def __init__(self, model_name: _Optional[str] = ..., input_data: _Optional[str] = ...) -> None: ...

class PredictResponse(_message.Message):
    __slots__ = ["model_name", "predictions"]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    predictions: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, model_name: _Optional[str] = ..., predictions: _Optional[_Iterable[float]] = ...) -> None: ...
