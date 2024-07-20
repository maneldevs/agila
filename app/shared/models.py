from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T", bound=BaseModel)


class DirectionEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class PageParams(BaseModel):
    page: int | None = Field(ge=1, default=1)
    size: int | None = Field(ge=1, default=10)
    order_field: str | None = "id"
    direction: DirectionEnum | None = DirectionEnum.asc


class PageResponse(GenericModel, Generic[T]):
    page: int
    size: int
    total: int
    content: list[T]
