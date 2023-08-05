"""
Service class to handle low-level communication.
"""

import json
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from posixpath import join as join_url  # both urls and posix paths use `/` as seperator
from types import TracebackType
from typing import Any, Dict, Optional, Union

import httpx

from aidkit_client.exceptions import AidkitClientError, AuthenticationError

API_VERSION = "1.0"


@dataclass
class Response:
    """
    Response of an aidkit server.
    """

    status_code: int
    body: Union[Dict[str, Any], str]

    @property
    def is_success(self) -> bool:
        """
        Return whether the request prompting the response was handled
        successfully.

        :return: True if the aidkit server indicated success, False otherwise.
        """
        return self.status_code in (200, 201)

    @property
    def is_not_found(self) -> bool:
        """
        Return whether a resource was not found.

        :return: True if the aidkit server indicated that a resource was not
            found, False otherwise.
        """
        return self.status_code == 404

    @property
    def is_bad(self) -> bool:
        """
        Return whether the request prompting the response was deemed a bad
        request by the server.

        :return: True if the server returned a "bad request" error code, False
            otherwise.
        """
        return self.status_code == 400

    def body_dict_or_error(self, error_message: str) -> dict:
        """
        Return the body dictionary if the response indicates success and is a
        dictionary, raise the appropriate error otherwise.

        :param error_message: Error message to prepend to the raised error if
            an error is raised. Must contain relevant context.
        :raises AuthenticationError: If the server returned a 401 status code.
        :raises AidkitClientError: If some other error occured or if the server did
            not return a dictionary.
        :return: Body of the response.
        """
        if self.status_code == 401:
            if self.body == "Invalid audience" or (
                isinstance(self.body, str)
                and self.body.startswith("Unable to find a signing key that matches: ")
            ):
                raise AuthenticationError("JWT token is not usable for this domain.")
            if self.body == "Signature has expired":
                raise AuthenticationError("Used JWT token is expired.")
            raise AuthenticationError(f"Server response: '{self.body}'")

        if not self.is_success:
            raise AidkitClientError(
                error_message,
                f"Server responded with error code {self.status_code} and message '{self.body}'",
            )
        if not isinstance(self.body, dict):
            raise AidkitClientError(
                "Server did not respond with a dictionary, " f"but with the string '{self.body}'"
            )
        return self.body


class HTTPService(ABC):
    """
    Abstract HTTP service to use REST methods.
    """

    @abstractmethod
    async def get(self, path: str, parameters: Optional[Dict[str, Any]]) -> Response:
        """
        Get a resource on the server.

        :param path: Path of the resource to get.
        :param parameters: Parameters to pass to the server.
        :returns: Response of the server.
        """

    @abstractmethod
    async def post_json(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]],
        body: Optional[dict],
    ) -> Response:
        """
        Post JSON data to the server.

        :param path: Path of the resource to be posted.
        :param parameters: Parameters to be passed to the server.
        :param parameters: Parameters to be passed to the server.
        :param body: JSON body to be posted to the server.
        :returns: Response of the server.
        """

    @abstractmethod
    async def post_multipart_data(
        self,
        path: str,
        data: Optional[dict],
        files: Optional[dict],
    ) -> Response:
        """
        Post multipart data to the server.

        :param path: Path of the resource to be posted.
        :param data: Data to be uploaded to the server.
        :param files: Files to be uploaded to the server.
        :returns: Response of the server.
        """

    @abstractmethod
    async def patch(
        self, path: str, parameters: Optional[Dict[str, Any]], body: Optional[dict]
    ) -> Response:
        """
        Patch a resource on the server.

        :param path: Path of the resource to be patched.
        :param parameters: Parameters to pass to the server.
        :param body: JSON body of the patch request.
        :returns: Response of the server.
        """

    @abstractmethod
    async def delete(self, path: str, parameters: Optional[Dict[str, Any]] = None) -> Response:
        """
        Delete a resource on the server.

        :param path: Path of the resource to be deleted.
        :param parameters: Parameters to pass to the server.
        :returns: Response of the server.
        """

    @abstractmethod
    async def get_from_cdn(self, url) -> Response:
        """
        Get a file from the content delivery network.

        :param url: url to access
        :returns: Response of the server.
        """


class AidkitApi(HTTPService):
    """
    HTTP Service to be used to communicate with an aidkit server.
    """

    def __init__(self, base_url: str, auth_token: str, timeout: int = 300) -> None:
        """
        Create a new instance configured with a base URL and a JWT auth token.

        :param base_url: Base URL of the aidkit server to communicate with.
        :param auth_token: JWT token to use for authentication.
        :param timeout: timeout for httpx requests
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.auth_token}",
                "api_version": API_VERSION,
            },
            timeout=timeout,
        )

    async def __aenter__(self) -> "AidkitApi":
        """
        Enter the context to use the aidkit api within.

        :return: AidkitApi this method is called on.
        """
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[typing.Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        """
        Exit the context of the underlying HTTPX client.

        :param exc_type: Exception type, if an exception is the reason to exit
            the context.
        :param exc_value: Exception value, if an exception is the reason to exit
            the context.
        :param traceback: Traceback, if an exception is the reason to exit
            the context.
            the context
        :param exc_value: Exception value, if an exception is the reason to exit
            the context
        :param traceback: Traceback, if an exception is the reason to exit
            the context
        """
        await self.client.__aexit__(exc_type=exc_type, exc_value=exc_value, traceback=traceback)

    async def get(self, path: str, parameters: Optional[Dict[str, Any]]) -> Response:
        """
        Get a resource on the server.

        :param path: Path of the resource to get.
        :param parameters: Parameters to pass to the server.
        :returns: Response of the server.
        """
        response = await self.client.get(url=self._with_base_url(path), params=parameters)
        return self._to_aidkit_response(response)

    async def get_from_cdn(self, url) -> Response:
        """
        Get a file from the content delivery network.

        :param url: url to access
        :returns: Response of the server.
        """
        res = await self.client.get(url=url)

        return Response(
            status_code=res.status_code,
            body={"content": res.content},
        )

    async def post_json(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]],
        body: Optional[Dict[str, Any]],
    ) -> Response:
        """
        Post JSON data to the server.

        :param path: Path of the resource to be posted.
        :param parameters: Parameters to be passed to the server.
        :param body: JSON body to be posted to the server.
        :returns: Response of the server.
        """
        response = await self.client.post(
            url=self._with_base_url(path), params=parameters, json=body
        )
        return self._to_aidkit_response(response)

    async def post_multipart_data(
        self,
        path: str,
        data: Optional[dict],
        files: Optional[dict],
    ) -> Response:
        """
        Post multipart data to the server.

        :param path: Path of the resource to be posted.
        :param data: Data to be uploaded to the server.
        :param files: Files to be uploaded to the server.
        :returns: Response of the server.
        """
        response = await self.client.post(url=self._with_base_url(path), data=data, files=files)
        return self._to_aidkit_response(response)

    async def patch(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]],
        body: Optional[Dict[str, Any]],
    ) -> Response:
        """
        Patch a resource on the server.

        :param path: Path of the resource to be patched.
        :param parameters: Parameters to pass to the server.
        :param body: JSON body of the patch request.
        :returns: Response of the server.
        """
        response = await self.client.patch(
            url=self._with_base_url(path), params=parameters, json=body
        )
        return self._to_aidkit_response(response)

    async def delete(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """
        Delete a resource on the server.

        :param path: Path of the resource to be deleted.
        :param parameters: Parameters to pass to the server.
        :returns: Response of the server.
        """
        response = await self.client.delete(url=self._with_base_url(path), params=parameters)
        return self._to_aidkit_response(response)

    def _with_base_url(self, path: str) -> str:
        return join_url(self.base_url, path)

    @classmethod
    def _to_aidkit_response(cls, res: httpx.Response) -> Response:
        try:
            return Response(status_code=res.status_code, body=res.json())
        except json.decoder.JSONDecodeError:
            return Response(status_code=res.status_code, body={"not_json_decodable": res.content})
