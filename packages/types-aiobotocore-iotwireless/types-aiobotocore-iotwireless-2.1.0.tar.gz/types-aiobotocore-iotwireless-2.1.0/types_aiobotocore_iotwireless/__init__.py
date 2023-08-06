"""
Main interface for iotwireless service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotwireless import (
        Client,
        IoTWirelessClient,
    )

    session = get_session()
    with async session.create_client("iotwireless") as client:
        client: IoTWirelessClient
        ...

    ```
"""
from .client import IoTWirelessClient

Client = IoTWirelessClient


__all__ = ("Client", "IoTWirelessClient")
