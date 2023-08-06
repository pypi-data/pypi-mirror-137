"""
Main interface for chime-sdk-identity service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_identity import (
        ChimeSDKIdentityClient,
        Client,
    )

    session = get_session()
    with async session.create_client("chime-sdk-identity") as client:
        client: ChimeSDKIdentityClient
        ...

    ```
"""
from .client import ChimeSDKIdentityClient

Client = ChimeSDKIdentityClient


__all__ = ("ChimeSDKIdentityClient", "Client")
