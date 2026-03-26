from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Book(_message.Message):
    __slots__ = ("id", "title", "pub_year", "owner", "cover", "authors")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PUB_YEAR_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    COVER_FIELD_NUMBER: _ClassVar[int]
    AUTHORS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    pub_year: int
    owner: Owner
    cover: Cover
    authors: _containers.RepeatedCompositeFieldContainer[Author]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., pub_year: _Optional[int] = ..., owner: _Optional[_Union[Owner, _Mapping]] = ..., cover: _Optional[_Union[Cover, _Mapping]] = ..., authors: _Optional[_Iterable[_Union[Author, _Mapping]]] = ...) -> None: ...

class Owner(_message.Message):
    __slots__ = ("id", "username")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ...) -> None: ...

class Cover(_message.Message):
    __slots__ = ("type", "content")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    type: str
    content: bytes
    def __init__(self, type: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class Author(_message.Message):
    __slots__ = ("last_name", "first_name")
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    last_name: str
    first_name: str
    def __init__(self, last_name: _Optional[str] = ..., first_name: _Optional[str] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("error_msg",)
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    error_msg: str
    def __init__(self, error_msg: _Optional[str] = ...) -> None: ...

class Success(_message.Message):
    __slots__ = ("success_msg",)
    SUCCESS_MSG_FIELD_NUMBER: _ClassVar[int]
    success_msg: str
    def __init__(self, success_msg: _Optional[str] = ...) -> None: ...

class GetBooksRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBooksResponse(_message.Message):
    __slots__ = ("book",)
    BOOK_FIELD_NUMBER: _ClassVar[int]
    book: Book
    def __init__(self, book: _Optional[_Union[Book, _Mapping]] = ...) -> None: ...

class GetBookByIdRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetBookByIdResponse(_message.Message):
    __slots__ = ("error", "book")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BOOK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    book: Book
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., book: _Optional[_Union[Book, _Mapping]] = ...) -> None: ...

class GetBooksByOwnerRequest(_message.Message):
    __slots__ = ("owner_id",)
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    owner_id: int
    def __init__(self, owner_id: _Optional[int] = ...) -> None: ...

class GetBooksByOwnerResponse(_message.Message):
    __slots__ = ("error", "book")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BOOK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    book: Book
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., book: _Optional[_Union[Book, _Mapping]] = ...) -> None: ...

class AddBookRequest(_message.Message):
    __slots__ = ("book",)
    BOOK_FIELD_NUMBER: _ClassVar[int]
    book: Book
    def __init__(self, book: _Optional[_Union[Book, _Mapping]] = ...) -> None: ...

class AddBookResponse(_message.Message):
    __slots__ = ("book_id", "error")
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    book_id: int
    error: Error
    def __init__(self, book_id: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class UpdateBookRequest(_message.Message):
    __slots__ = ("id", "title", "pub_year", "owner", "cover", "clear_authors", "authors")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PUB_YEAR_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    COVER_FIELD_NUMBER: _ClassVar[int]
    CLEAR_AUTHORS_FIELD_NUMBER: _ClassVar[int]
    AUTHORS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    pub_year: int
    owner: Owner
    cover: Cover
    clear_authors: bool
    authors: _containers.RepeatedCompositeFieldContainer[Author]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., pub_year: _Optional[int] = ..., owner: _Optional[_Union[Owner, _Mapping]] = ..., cover: _Optional[_Union[Cover, _Mapping]] = ..., clear_authors: bool = ..., authors: _Optional[_Iterable[_Union[Author, _Mapping]]] = ...) -> None: ...

class UpdateBookResponse(_message.Message):
    __slots__ = ("error", "success")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    success: Success
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., success: _Optional[_Union[Success, _Mapping]] = ...) -> None: ...

class RemoveBookCoverRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RemoveBookCoverResponse(_message.Message):
    __slots__ = ("error", "success")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    success: Success
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., success: _Optional[_Union[Success, _Mapping]] = ...) -> None: ...

class RemoveBookRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RemoveBookResponse(_message.Message):
    __slots__ = ("error", "success")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    success: Success
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., success: _Optional[_Union[Success, _Mapping]] = ...) -> None: ...
