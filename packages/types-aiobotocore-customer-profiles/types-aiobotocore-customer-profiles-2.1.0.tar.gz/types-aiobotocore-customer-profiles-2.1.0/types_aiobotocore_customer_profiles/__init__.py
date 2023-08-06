"""
Main interface for customer-profiles service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_customer_profiles import (
        Client,
        CustomerProfilesClient,
    )

    session = get_session()
    with async session.create_client("customer-profiles") as client:
        client: CustomerProfilesClient
        ...

    ```
"""
from .client import CustomerProfilesClient

Client = CustomerProfilesClient


__all__ = ("Client", "CustomerProfilesClient")
