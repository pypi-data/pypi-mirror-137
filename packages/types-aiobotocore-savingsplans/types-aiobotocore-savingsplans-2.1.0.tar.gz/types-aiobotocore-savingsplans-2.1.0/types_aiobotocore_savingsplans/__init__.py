"""
Main interface for savingsplans service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_savingsplans import (
        Client,
        SavingsPlansClient,
    )

    session = get_session()
    with async session.create_client("savingsplans") as client:
        client: SavingsPlansClient
        ...

    ```
"""
from .client import SavingsPlansClient

Client = SavingsPlansClient


__all__ = ("Client", "SavingsPlansClient")
