"""
Main interface for transfer service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transfer import (
        Client,
        ListServersPaginator,
        TransferClient,
    )

    session = get_session()
    async with session.create_client("transfer") as client:
        client: TransferClient
        ...


    list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```
"""
from .client import TransferClient
from .paginator import ListServersPaginator

Client = TransferClient


__all__ = ("Client", "ListServersPaginator", "TransferClient")
