"""
Type annotations for s3outposts service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3outposts.client import S3OutpostsClient
    from types_aiobotocore_s3outposts.paginator import (
        ListEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("s3outposts") as client:
        client: S3OutpostsClient

        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListEndpointsResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListEndpointsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators.html#listendpointspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators.html#listendpointspaginator)
        """
