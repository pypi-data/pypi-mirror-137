"""
Main interface for cognito-sync service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_sync import (
        Client,
        CognitoSyncClient,
    )

    session = get_session()
    with async session.create_client("cognito-sync") as client:
        client: CognitoSyncClient
        ...

    ```
"""
from .client import CognitoSyncClient

Client = CognitoSyncClient


__all__ = ("Client", "CognitoSyncClient")
