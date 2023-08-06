"""
Main interface for cloudsearchdomain service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearchdomain import (
        Client,
        CloudSearchDomainClient,
    )

    session = get_session()
    with async session.create_client("cloudsearchdomain") as client:
        client: CloudSearchDomainClient
        ...

    ```
"""
from .client import CloudSearchDomainClient

Client = CloudSearchDomainClient


__all__ = ("Client", "CloudSearchDomainClient")
