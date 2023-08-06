"""
Main interface for meteringmarketplace service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_meteringmarketplace import (
        Client,
        MarketplaceMeteringClient,
    )

    session = get_session()
    with async session.create_client("meteringmarketplace") as client:
        client: MarketplaceMeteringClient
        ...

    ```
"""
from .client import MarketplaceMeteringClient

Client = MarketplaceMeteringClient


__all__ = ("Client", "MarketplaceMeteringClient")
