"""
Main interface for backup service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_backup import (
        BackupClient,
        Client,
    )

    session = Session()
    client: BackupClient = session.client("backup")
    ```
"""
from .client import BackupClient

Client = BackupClient


__all__ = ("BackupClient", "Client")
