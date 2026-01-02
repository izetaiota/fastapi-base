from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    code: str = "OK"
    data: T | None = None


class PageModel(BaseModel, Generic[T]):
    items: list[T]
    total: int
