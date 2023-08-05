from typing import BinaryIO, List

from aidkit_client._endpoints.constants import Constants
from aidkit_client._endpoints.models import (
    ListMLModelResponse,
    MLModelResponse,
    MLModelVersionResponse,
)
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.exceptions import ResourceWithIdNotFoundError


class MLModelsAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get_all(self) -> List[MLModelResponse]:
        result = await self.api.get(path=Constants.ML_MODELS_PATH, parameters=None)
        return ListMLModelResponse(
            **result.body_dict_or_error("Failed to retrieve MLModels.")
        ).ml_models

    async def get(self, name: str) -> MLModelResponse:
        result = await self.api.get(path=f"{Constants.ML_MODELS_PATH}/{name}", parameters=None)
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(f"MLModel with name {name} not found")
        return MLModelResponse(
            **result.body_dict_or_error(f"Error fetching MLModel with name {name}. ")
        )

    async def update(self, name: str, new_name: str) -> MLModelResponse:
        result = await self.api.patch(
            path=f"{Constants.ML_MODELS_PATH}/{name}",
            parameters=None,
            body={"name": new_name},
        )
        if result.is_bad:
            raise ResourceWithIdNotFoundError(f"Could not update MLModel name with {name}")
        return MLModelResponse(
            **result.body_dict_or_error(f"Error patching MLModel with name {name}.")
        )

    async def upload_model_version(
        self, model_name: str, model_version: str, model_file_content: BinaryIO
    ) -> MLModelVersionResponse:

        result = await self.api.post_multipart_data(
            path=f"{Constants.ML_MODELS_PATH}/{model_name}/versions",
            data={"name": model_version},
            files={"model": model_file_content},
        )
        if result.is_bad:
            raise ResourceWithIdNotFoundError(
                f"Could not update MLModel '{model_name}' with version '{model_version}'"
            )
        return MLModelVersionResponse(
            **result.body_dict_or_error(
                f"Error updating MLModel '{model_name}' with version '{model_version}'."
            )
        )

    async def delete(self, name: str) -> bool:
        response = await self.api.delete(path=f"{Constants.ML_MODELS_PATH}/{name}")
        return response.is_success
