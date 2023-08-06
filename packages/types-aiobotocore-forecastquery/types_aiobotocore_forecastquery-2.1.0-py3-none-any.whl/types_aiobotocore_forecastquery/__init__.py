"""
Main interface for forecastquery service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_forecastquery import (
        Client,
        ForecastQueryServiceClient,
    )

    session = get_session()
    with async session.create_client("forecastquery") as client:
        client: ForecastQueryServiceClient
        ...

    ```
"""
from .client import ForecastQueryServiceClient

Client = ForecastQueryServiceClient


__all__ = ("Client", "ForecastQueryServiceClient")
