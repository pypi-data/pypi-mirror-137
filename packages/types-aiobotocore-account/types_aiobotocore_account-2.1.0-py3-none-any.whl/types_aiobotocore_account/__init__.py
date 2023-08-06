"""
Main interface for account service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_account import (
        AccountClient,
        Client,
    )

    session = get_session()
    with async session.create_client("account") as client:
        client: AccountClient
        ...

    ```
"""
from .client import AccountClient

Client = AccountClient


__all__ = ("AccountClient", "Client")
