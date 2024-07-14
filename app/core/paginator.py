from typing import Generic, TypeVar
from fastapi import Query
from app.core.database import Base

from app.core.models import DirectionEnum, PageParams

T = TypeVar("T", bound=Base)


class Paginator(Generic[T]):

    def __init__(self, entity: T) -> None:
        self.entity = entity

    def paginate_query(self, query: Query, page_params: PageParams) -> Query:
        query = self.__apply_order_by(query, page_params.order_field, page_params.direction)
        query = self.__apply_page(query, page_params.page, page_params.size)
        return query

    def __apply_order_by(self, query: Query, order_field: str, direction: DirectionEnum) -> Query:
        order_column = getattr(self.entity, order_field)
        if direction is DirectionEnum.desc:
            order_column = order_column.desc()
        return query.order_by(order_column)

    def __apply_page(self, query: Query, page: int, size: int) -> Query:
        return query.offset((page - 1) * size).limit(size)
