"""
Main interface for transfer service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_transfer import (
        Client,
        ListServersPaginator,
        TransferClient,
    )

    session = Session()
    client: TransferClient = session.client("transfer")

    list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```
"""
from .client import TransferClient
from .paginator import ListServersPaginator

Client = TransferClient

__all__ = ("Client", "ListServersPaginator", "TransferClient")
