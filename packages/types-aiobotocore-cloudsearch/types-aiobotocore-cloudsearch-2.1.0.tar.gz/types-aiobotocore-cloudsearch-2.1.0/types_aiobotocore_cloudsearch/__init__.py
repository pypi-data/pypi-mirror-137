"""
Main interface for cloudsearch service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearch import (
        Client,
        CloudSearchClient,
    )

    session = get_session()
    with async session.create_client("cloudsearch") as client:
        client: CloudSearchClient
        ...

    ```
"""
from .client import CloudSearchClient

Client = CloudSearchClient


__all__ = ("Client", "CloudSearchClient")
