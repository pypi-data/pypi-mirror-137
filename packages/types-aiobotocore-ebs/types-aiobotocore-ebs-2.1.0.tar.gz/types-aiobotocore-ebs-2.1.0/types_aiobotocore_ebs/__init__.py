"""
Main interface for ebs service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ebs import (
        Client,
        EBSClient,
    )

    session = get_session()
    with async session.create_client("ebs") as client:
        client: EBSClient
        ...

    ```
"""
from .client import EBSClient

Client = EBSClient


__all__ = ("Client", "EBSClient")
