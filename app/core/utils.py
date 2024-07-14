from fastapi import Query

from app.core.models import PageParams


def paginate_query(query: Query, page_params: PageParams) -> Query:
    query = query.offset((page_params.page - 1) * page_params.size).limit(page_params.size)
    return query
    # TODO mmr add orderby