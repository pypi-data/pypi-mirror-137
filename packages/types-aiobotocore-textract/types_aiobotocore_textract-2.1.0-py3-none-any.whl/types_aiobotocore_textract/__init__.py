"""
Main interface for textract service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_textract import (
        Client,
        TextractClient,
    )

    session = get_session()
    with async session.create_client("textract") as client:
        client: TextractClient
        ...

    ```
"""
from .client import TextractClient

Client = TextractClient


__all__ = ("Client", "TextractClient")
