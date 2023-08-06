"""
Type annotations for timestream-query service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_timestream_query.client import TimestreamQueryClient
    from types_aiobotocore_timestream_query.paginator import (
        ListScheduledQueriesPaginator,
        ListTagsForResourcePaginator,
        QueryPaginator,
    )

    session = get_session()
    with session.create_client("timestream-query") as client:
        client: TimestreamQueryClient

        list_scheduled_queries_paginator: ListScheduledQueriesPaginator = client.get_paginator("list_scheduled_queries")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        query_paginator: QueryPaginator = client.get_paginator("query")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListScheduledQueriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PaginatorConfigTypeDef,
    QueryResponseTypeDef,
)

__all__ = ("ListScheduledQueriesPaginator", "ListTagsForResourcePaginator", "QueryPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListScheduledQueriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListScheduledQueries)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html#listscheduledqueriespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListScheduledQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListScheduledQueries.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html#listscheduledqueriespaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html#listtagsforresourcepaginator)
    """

    async def paginate(
        self, *, ResourceARN: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html#listtagsforresourcepaginator)
        """


class QueryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.Query)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html#querypaginator)
    """

    async def paginate(
        self,
        *,
        QueryString: str,
        ClientToken: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[QueryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.Query.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators.html#querypaginator)
        """
