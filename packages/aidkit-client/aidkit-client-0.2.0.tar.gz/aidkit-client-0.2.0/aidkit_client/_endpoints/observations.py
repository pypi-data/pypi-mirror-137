from typing import BinaryIO

from aidkit_client._endpoints.constants import Constants
from aidkit_client._endpoints.models import ObservationResponse, ObservationType
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.exceptions import ResourceWithIdNotFoundError


class ObservationAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def create(
        self,
        dataset_name: str,
        observation_type: ObservationType,
        subset_names: list,
        obs_name: str,
        obs_data: BinaryIO,
    ) -> ObservationResponse:
        return ObservationResponse(
            **(
                await self.api.post_multipart_data(
                    f"observations?dataset_name={dataset_name}",
                    data={
                        "observation_type": observation_type.value,
                        "subset_names": subset_names,
                    },
                    files={"observation": (obs_name, obs_data)},
                )
            ).body_dict_or_error(f"Failed to create Observation {obs_name}.")
        )

    async def get_by_id(self, observation_id: int) -> ObservationResponse:
        result = await self.api.get(
            path=f"{Constants.DATASETS_PATH}/{observation_id}", parameters=None
        )
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(f"Observation with id {observation_id} not found")
        return ObservationResponse(
            **result.body_dict_or_error(f"Error fetching Observation with id {observation_id}.")
        )
