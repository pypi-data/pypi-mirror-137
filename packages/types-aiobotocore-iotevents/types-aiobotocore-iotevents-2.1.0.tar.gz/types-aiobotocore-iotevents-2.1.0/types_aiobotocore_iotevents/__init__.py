"""
Main interface for iotevents service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotevents import (
        Client,
        IoTEventsClient,
    )

    session = get_session()
    with async session.create_client("iotevents") as client:
        client: IoTEventsClient
        ...

    ```
"""
from .client import IoTEventsClient

Client = IoTEventsClient


__all__ = ("Client", "IoTEventsClient")
