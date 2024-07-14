from fastapi import Query
from sqlalchemy import text

from app.core.models import PageParams

# T = TypeVar("T", bound=BaseModel)

# class Paginator:

def paginate_query(query: Query, page_params: PageParams) -> Query:
    query = query.order_by(text(f"{page_params.order_field} {page_params.direction.value}"))
    query = query.offset((page_params.page - 1) * page_params.size).limit(page_params.size)
    return query
