"""
Main interface for ce service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ce import (
        Client,
        CostExplorerClient,
    )

    session = get_session()
    with async session.create_client("ce") as client:
        client: CostExplorerClient
        ...

    ```
"""
from .client import CostExplorerClient

Client = CostExplorerClient


__all__ = ("Client", "CostExplorerClient")
