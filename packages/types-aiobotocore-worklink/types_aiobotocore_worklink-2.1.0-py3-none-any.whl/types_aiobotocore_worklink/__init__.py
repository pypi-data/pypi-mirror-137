"""
Main interface for worklink service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_worklink import (
        Client,
        WorkLinkClient,
    )

    session = get_session()
    with async session.create_client("worklink") as client:
        client: WorkLinkClient
        ...

    ```
"""
from .client import WorkLinkClient

Client = WorkLinkClient


__all__ = ("Client", "WorkLinkClient")
