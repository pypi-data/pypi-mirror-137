"""
Main interface for frauddetector service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_frauddetector import (
        Client,
        FraudDetectorClient,
    )

    session = get_session()
    with async session.create_client("frauddetector") as client:
        client: FraudDetectorClient
        ...

    ```
"""
from .client import FraudDetectorClient

Client = FraudDetectorClient


__all__ = ("Client", "FraudDetectorClient")
