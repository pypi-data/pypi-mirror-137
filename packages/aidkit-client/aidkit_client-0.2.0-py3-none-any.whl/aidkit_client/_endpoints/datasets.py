import json

from aidkit_client._endpoints.constants import Constants
from aidkit_client._endpoints.models import (
    DatasetResponse,
    DatasetUploadRequest,
    ObservationType,
)
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.exceptions import ResourceWithIdNotFoundError


class DatasetAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get(self, name: str) -> DatasetResponse:
        result = await self.api.get(path=f"{Constants.DATASETS_PATH}/{name}", parameters=None)
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(f"Dataset with name {name} not found")
        return DatasetResponse(
            **result.body_dict_or_error(f"Error fetching Dataset with name {name}.")
        )

    async def create(self, dataset_name: str, dataset_type: ObservationType) -> DatasetResponse:
        # needs to go through json to convert the enums, otherwise httpx will throw an error
        body = json.loads(DatasetUploadRequest(name=dataset_name, type=dataset_type).json())
        return DatasetResponse(
            **(
                await self.api.post_json(
                    path=f"{Constants.DATASETS_PATH}",
                    parameters=None,
                    body=body,
                )
            ).body_dict_or_error(f"Failed to create dataset '{dataset_name}'.")
        )
