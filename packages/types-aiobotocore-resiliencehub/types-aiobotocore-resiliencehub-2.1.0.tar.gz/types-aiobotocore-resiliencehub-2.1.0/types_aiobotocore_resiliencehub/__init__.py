"""
Main interface for resiliencehub service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resiliencehub import (
        Client,
        ResilienceHubClient,
    )

    session = get_session()
    with async session.create_client("resiliencehub") as client:
        client: ResilienceHubClient
        ...

    ```
"""
from .client import ResilienceHubClient

Client = ResilienceHubClient


__all__ = ("Client", "ResilienceHubClient")
