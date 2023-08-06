"""
Main interface for outposts service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_outposts import (
        Client,
        OutpostsClient,
    )

    session = get_session()
    with async session.create_client("outposts") as client:
        client: OutpostsClient
        ...

    ```
"""
from .client import OutpostsClient

Client = OutpostsClient


__all__ = ("Client", "OutpostsClient")
