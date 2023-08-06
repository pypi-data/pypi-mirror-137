"""
Main interface for route53-recovery-cluster service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53_recovery_cluster import (
        Client,
        Route53RecoveryClusterClient,
    )

    session = get_session()
    with async session.create_client("route53-recovery-cluster") as client:
        client: Route53RecoveryClusterClient
        ...

    ```
"""
from .client import Route53RecoveryClusterClient

Client = Route53RecoveryClusterClient


__all__ = ("Client", "Route53RecoveryClusterClient")
