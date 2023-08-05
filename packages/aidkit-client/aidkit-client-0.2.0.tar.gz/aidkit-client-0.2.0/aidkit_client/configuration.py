"""
Utilities to configure the aidkit python client.
"""

from typing import Optional

from aidkit_client.aidkit_api import AidkitApi, HTTPService
from aidkit_client.exceptions import AidkitClientNotConfiguredError


def configure(base_url: str, auth_token: str, timeout: int = 300) -> None:
    """
    Configure the client. Must be called before the client is used.

    :param base_url: Base URL of the API backend.
    :param auth_token: JWT token used for authentification.
    :param timeout: timeout for httpx requests
    """
    # we allow global setting of the configurations parameters
    global _GLOBAL_API_SERVICE  # pylint: disable=global-statement
    _GLOBAL_API_SERVICE = AidkitApi(base_url=base_url, auth_token=auth_token, timeout=timeout)


_GLOBAL_API_SERVICE: Optional[HTTPService] = None


def get_api_client() -> HTTPService:
    """
    Get an API client using the current global configuration options.

    :raises AidkitClientNotConfiguredError: If the client has not been
        configured before this function is called.
    :return: Service instance using the global configuration options set via
        `aidkit_client.configure`.
    """
    if _GLOBAL_API_SERVICE is None:
        raise AidkitClientNotConfiguredError(
            """aidkit must be configured first.
        Run `aidkit_client.configure(BASE_URL, AUTH_TOKEN)` before calling any other method."""
        )
    return _GLOBAL_API_SERVICE
