"""
Type annotations for mediastore-data service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediastore_data.client import MediaStoreDataClient
    from types_aiobotocore_mediastore_data.paginator import (
        ListItemsPaginator,
    )

    session = get_session()
    with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient

        list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListItemsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListItemsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Paginator.ListItems)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators.html#listitemspaginator)
    """

    async def paginate(
        self, *, Path: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Paginator.ListItems.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators.html#listitemspaginator)
        """
