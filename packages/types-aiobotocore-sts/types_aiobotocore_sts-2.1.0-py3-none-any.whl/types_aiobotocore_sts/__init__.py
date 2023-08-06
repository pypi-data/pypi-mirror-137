"""
Main interface for sts service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sts import (
        Client,
        STSClient,
    )

    session = get_session()
    with async session.create_client("sts") as client:
        client: STSClient
        ...

    ```
"""
from .client import STSClient

Client = STSClient


__all__ = ("Client", "STSClient")
