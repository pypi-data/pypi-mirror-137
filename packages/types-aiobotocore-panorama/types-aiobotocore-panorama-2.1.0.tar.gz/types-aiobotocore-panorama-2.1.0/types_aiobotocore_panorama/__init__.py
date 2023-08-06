"""
Main interface for panorama service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_panorama import (
        Client,
        PanoramaClient,
    )

    session = get_session()
    with async session.create_client("panorama") as client:
        client: PanoramaClient
        ...

    ```
"""
from .client import PanoramaClient

Client = PanoramaClient


__all__ = ("Client", "PanoramaClient")
