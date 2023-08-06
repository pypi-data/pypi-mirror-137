"""
Main interface for apigatewaymanagementapi service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigatewaymanagementapi import (
        ApiGatewayManagementApiClient,
        Client,
    )

    session = get_session()
    with async session.create_client("apigatewaymanagementapi") as client:
        client: ApiGatewayManagementApiClient
        ...

    ```
"""
from .client import ApiGatewayManagementApiClient

Client = ApiGatewayManagementApiClient


__all__ = ("ApiGatewayManagementApiClient", "Client")
