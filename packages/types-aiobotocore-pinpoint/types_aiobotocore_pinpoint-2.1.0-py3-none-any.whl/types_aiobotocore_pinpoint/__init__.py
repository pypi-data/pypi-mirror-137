"""
Main interface for pinpoint service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pinpoint import (
        Client,
        PinpointClient,
    )

    session = get_session()
    with async session.create_client("pinpoint") as client:
        client: PinpointClient
        ...

    ```
"""
from .client import PinpointClient

Client = PinpointClient


__all__ = ("Client", "PinpointClient")
