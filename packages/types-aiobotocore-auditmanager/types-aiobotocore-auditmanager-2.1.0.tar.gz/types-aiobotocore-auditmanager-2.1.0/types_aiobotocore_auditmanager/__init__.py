"""
Main interface for auditmanager service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_auditmanager import (
        AuditManagerClient,
        Client,
    )

    session = get_session()
    with async session.create_client("auditmanager") as client:
        client: AuditManagerClient
        ...

    ```
"""
from .client import AuditManagerClient

Client = AuditManagerClient


__all__ = ("AuditManagerClient", "Client")
