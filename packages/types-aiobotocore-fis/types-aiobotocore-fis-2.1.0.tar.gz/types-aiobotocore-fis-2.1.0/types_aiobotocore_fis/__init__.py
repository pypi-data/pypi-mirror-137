"""
Main interface for fis service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_fis import (
        Client,
        FISClient,
    )

    session = get_session()
    with async session.create_client("fis") as client:
        client: FISClient
        ...

    ```
"""
from .client import FISClient

Client = FISClient


__all__ = ("Client", "FISClient")
