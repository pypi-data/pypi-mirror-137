"""
Custom errors for the aidkit python client.
"""


class AidkitClientError(Exception):
    """
    Base Error for all errors explicitely raised from the aidkit client.
    """


class ResourceWithIdNotFoundError(Exception):
    """
    No resource with the passed ID was found.
    """


class ResourceWithNameNotFoundError(Exception):
    """
    No resource with the passed name was found.
    """


class AidkitClientNotConfiguredError(AidkitClientError):
    """
    The client is used before being configured.
    """


class RunTimeoutError(AidkitClientError):
    """
    A pipeline run took too long to finish.
    """


class TargetClassNotPassedError(AidkitClientError):
    """
    No target class was passed when trying to run a pipeline which requires a
    target class.
    """


class PipelineRunError(AidkitClientError):
    """
    A pipeline run did not finish successfully, but was stopped or failed.
    """


class AuthenticationError(AidkitClientError):
    """
    The user is not authenticated properly.
    """

    def __init__(self, *args: object) -> None:
        """
        Create a new error with the appropriate error message.

        :param args: Context for the error.
        """
        super().__init__(
            *args, "For instructions on how to get a valid JWT token, consult the documentation."
        )
