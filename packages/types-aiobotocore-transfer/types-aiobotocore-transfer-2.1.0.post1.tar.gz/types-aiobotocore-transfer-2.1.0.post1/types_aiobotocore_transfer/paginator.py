"""
Type annotations for transfer service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_transfer.client import TransferClient
    from types_aiobotocore_transfer.paginator import (
        ListServersPaginator,
    )

    session = get_session()
    with session.create_client("transfer") as client:
        client: TransferClient

        list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListServersResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListServersPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Paginator.ListServers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators.html#listserverspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Paginator.ListServers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators.html#listserverspaginator)
        """
