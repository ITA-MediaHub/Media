from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MediaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEDIA_TYPE_UNKNOWN: _ClassVar[MediaType]
    MEDIA_TYPE_MUSIC: _ClassVar[MediaType]
    MEDIA_TYPE_BOOK: _ClassVar[MediaType]
    MEDIA_TYPE_MOVIE: _ClassVar[MediaType]
    MEDIA_TYPE_TV: _ClassVar[MediaType]
    MEDIA_TYPE_GAME: _ClassVar[MediaType]
MEDIA_TYPE_UNKNOWN: MediaType
MEDIA_TYPE_MUSIC: MediaType
MEDIA_TYPE_BOOK: MediaType
MEDIA_TYPE_MOVIE: MediaType
MEDIA_TYPE_TV: MediaType
MEDIA_TYPE_GAME: MediaType

class GetMediaByIdRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class MediaResponse(_message.Message):
    __slots__ = ("id", "title", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    type: MediaType
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., type: _Optional[_Union[MediaType, str]] = ...) -> None: ...
