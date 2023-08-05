from typing import List

from aidkit_client._endpoints.constants import Constants
from aidkit_client._endpoints.models import (
    SubsetCreateRequest,
    SubsetResponse,
    SubsetUpdateRequest,
)
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.exceptions import ResourceWithIdNotFoundError


class SubsetAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get(self, name: str) -> SubsetResponse:
        result = await self.api.get(path=f"{Constants.SUBSETS_PATH}/{name}", parameters=None)
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(f"Subset with name {name} not found")
        return SubsetResponse(
            **result.body_dict_or_error(f"Error fetching Subset with name {name}.")
        )

    async def create(
        self, subset_name: str, dataset_name: str, observation_ids: List[int]
    ) -> SubsetResponse:
        body = SubsetCreateRequest(
            name=subset_name, dataset_name=dataset_name, observation_ids=observation_ids
        ).dict()
        return SubsetResponse(
            **(
                await self.api.post_json(
                    path=f"{Constants.SUBSETS_PATH}",
                    parameters=None,
                    body=body,
                )
            ).body_dict_or_error(f"Failed to create subset '{subset_name}'.")
        )

    async def update(self, subset_name: str, observation_ids: List[int]) -> SubsetResponse:
        body = SubsetUpdateRequest(name=subset_name, observation_ids=observation_ids).dict()
        return SubsetResponse(
            **(
                await self.api.patch(
                    path=f"{Constants.SUBSETS_PATH}/{subset_name}",
                    parameters=None,
                    body=body,
                )
            ).body_dict_or_error(
                f"Failed to update subset '{subset_name}'."  # noqa: S608
            )
        )
