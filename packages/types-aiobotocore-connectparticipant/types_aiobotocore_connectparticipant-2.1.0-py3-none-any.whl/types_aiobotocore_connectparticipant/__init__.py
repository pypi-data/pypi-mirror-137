"""
Main interface for connectparticipant service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectparticipant import (
        Client,
        ConnectParticipantClient,
    )

    session = get_session()
    with async session.create_client("connectparticipant") as client:
        client: ConnectParticipantClient
        ...

    ```
"""
from .client import ConnectParticipantClient

Client = ConnectParticipantClient


__all__ = ("Client", "ConnectParticipantClient")
