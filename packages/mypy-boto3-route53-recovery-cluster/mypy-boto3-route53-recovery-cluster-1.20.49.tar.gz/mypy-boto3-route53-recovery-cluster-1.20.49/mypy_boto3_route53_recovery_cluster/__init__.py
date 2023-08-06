"""
Main interface for route53-recovery-cluster service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53_recovery_cluster import (
        Client,
        Route53RecoveryClusterClient,
    )

    session = Session()
    client: Route53RecoveryClusterClient = session.client("route53-recovery-cluster")
    ```
"""
from .client import Route53RecoveryClusterClient

Client = Route53RecoveryClusterClient


__all__ = ("Client", "Route53RecoveryClusterClient")
