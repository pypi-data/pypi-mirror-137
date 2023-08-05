"""
A machine learning model on aidkit can cover multiple model versions.

Machine learning models must be configured using the web GUI. After a
model has been configured, model versions can be uploaded using the
python client.
"""

import io
import os
from typing import Any, BinaryIO

from tqdm import tqdm

from aidkit_client._endpoints.ml_models import MLModelsAPI
from aidkit_client._endpoints.models import MLModelVersionResponse
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client


def _model_to_file_object(model: Any) -> BinaryIO:
    if isinstance(model, str):
        return open(model, "rb")
    try:
        # we do not require tensorflow - which in turn requires
        # h5py. _But_ if a user has tensorflow installed and hands over a
        # tensorflow model, we want to be able to serialize it.
        import h5py  # pylint: disable=import-outside-toplevel
        import tensorflow as tf  # pylint: disable=import-outside-toplevel

        if isinstance(model, tf.keras.Model):
            bio = io.BytesIO()
            with h5py.File(bio, "w") as file:
                model.save(file)
            return bio
    except ImportError:
        pass
    try:
        import torch  # pylint: disable=import-outside-toplevel

        if isinstance(model, torch.jit.ScriptModule):
            bio = io.BytesIO()
            torch.jit.save(model, bio)
            return bio

        if isinstance(model, torch.nn.Module):
            ValueError(
                f"""ML Models of type {type(model)} are not supported.
            Please convert the torch model to a torch.jit.ScriptModule by
            calling torch.jit.trace(model, example_input), see
            https://pytorch.org/docs/stable/jit.html"""
            )
    except ImportError:
        pass
    raise ValueError(f"ML Model type {type(model)} not understood.")


class MLModelVersion:
    """
    Version of a machine learning model.

    An instance of this class references a model version which is
    uploaded to an aidkit server.
    """

    def __init__(
        self, api_service: HTTPService, model_version_response: MLModelVersionResponse
    ) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communcation with the
            server.
        :param model_version_response: Server response describing the model
            version to be created.
        """
        self._api_service = api_service
        self._model_version_response = model_version_response

    @classmethod
    async def upload(
        cls,
        model_name: str,
        model_version: str,
        model: Any,
        progress_bar: bool = False,
    ) -> "MLModelVersion":
        """
        Upload a new model version.

        :param model_name: Name of the model to upload a new version of.
        :param model_version: Name of the new model version.
        :param model: Model to upload. How this parameter is interpreted
            depends on the type of the parameter:
            * If the parameter is a string, it is interpreted as the path of the
            model file to be uploaded.
            * If the parameter is an instance of a keras model, the model is saved
            and the resulting file is uploaded.
            * If the parameter is a torch ScriptModule, the ScriptModule is saved
            and the resulting file is uploaded.
        :param progress_bar: Whether to display a progress bar while uploading.
        :return: Instance representing the newly uploaded model version.
        """
        api_service = get_api_client()
        model_file_object = _model_to_file_object(model)
        model_file_object.seek(0, os.SEEK_END)
        model_file_size = model_file_object.tell()
        model_file_object.seek(0, 0)
        with tqdm.wrapattr(
            model_file_object,
            "read",
            total=model_file_size,
            desc="Uploading ML Model Version",
            disable=not progress_bar,
        ) as wrapped_file_object:
            model_version_response = await MLModelsAPI(api_service).upload_model_version(
                model_name=model_name,
                model_version=model_version,
                model_file_content=wrapped_file_object,
            )
        return MLModelVersion(
            api_service=api_service, model_version_response=model_version_response
        )

    @property
    def id(self) -> int:
        """
        Get the ID the instance is referenced by on the server.

        :return: ID of the instance
        """
        return self._model_version_response.id

    @property
    def name(self) -> str:
        """
        Get the name the instance.

        :return: Name of the instance
        """
        return self._model_version_response.name
