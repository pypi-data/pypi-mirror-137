"""
Main interface for timestream-write service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_write import (
        Client,
        TimestreamWriteClient,
    )

    session = get_session()
    with async session.create_client("timestream-write") as client:
        client: TimestreamWriteClient
        ...

    ```
"""
from .client import TimestreamWriteClient

Client = TimestreamWriteClient


__all__ = ("Client", "TimestreamWriteClient")
