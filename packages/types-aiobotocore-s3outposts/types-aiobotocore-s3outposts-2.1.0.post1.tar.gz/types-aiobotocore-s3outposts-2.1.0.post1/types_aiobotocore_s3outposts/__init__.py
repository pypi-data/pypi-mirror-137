"""
Main interface for s3outposts service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3outposts import (
        Client,
        ListEndpointsPaginator,
        S3OutpostsClient,
    )

    session = get_session()
    async with session.create_client("s3outposts") as client:
        client: S3OutpostsClient
        ...


    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    ```
"""
from .client import S3OutpostsClient
from .paginator import ListEndpointsPaginator

Client = S3OutpostsClient


__all__ = ("Client", "ListEndpointsPaginator", "S3OutpostsClient")
