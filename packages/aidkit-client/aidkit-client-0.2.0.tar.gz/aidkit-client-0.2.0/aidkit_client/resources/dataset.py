"""
A dataset is a collection of observations of the same type.

A subset is a set of observations. Observations of a Dataset can be part
of multiple overlapping subsets.
"""
from typing import List, Optional, Union

from aidkit_client._endpoints.datasets import DatasetAPI
from aidkit_client._endpoints.models import (
    DatasetResponse,
    ObservationResponse,
    ObservationType,
    SubsetResponse,
)
from aidkit_client._endpoints.observations import ObservationAPI
from aidkit_client._endpoints.subsets import SubsetAPI
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client


class Observation:
    """
    An observation.

    An instance of this class references an observation.
    """

    def __init__(self, api_service: HTTPService, observation_response: ObservationResponse) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param observation_response: Server response describing the observation
            to be created.
        """
        self._data = observation_response
        self._api_service = api_service

    @classmethod
    async def create(
        cls,
        dataset: Union["Dataset", str],
        file_name: str,
        observation_type: ObservationType,
        subsets: List[Union["Subset", str]],
    ) -> "Observation":
        """
        Create and upload a single observation.

        :param dataset: parent dataset
        :param file_name: path to the observation
        :param observation_type: type of the observation
        :param subsets: list of subsets this observation belongs to
        :return: created observation
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.name
        subset_names = [subset if isinstance(subset, str) else subset.name for subset in subsets]

        with open(file_name, "rb") as file_pointer:
            api_service = get_api_client()
            observation_response = await ObservationAPI(api_service).create(
                dataset_name=dataset,
                observation_type=observation_type,
                subset_names=subset_names,
                obs_name=file_name,
                obs_data=file_pointer,
            )
        return Observation(api_service=api_service, observation_response=observation_response)

    @classmethod
    async def get_by_id(cls, observation_id: int) -> "Observation":
        """
        Get an observation by its ID.

        :param observation_id: ID of the observation to fetch.
        :return: Instance of the observation with the given ID.
        """
        api_service = get_api_client()
        pipeline_response = await ObservationAPI(api_service).get_by_id(observation_id)
        return Observation(api_service, pipeline_response)

    @property
    def id(self) -> int:
        """
        Get the ID of the instance.

        :return: ID of the instance.
        """
        return self._data.id

    @property
    def name(self) -> str:
        """
        Get the name the instance.

        :return: Name of the instance.
        """
        return self._data.file_name


class Subset:
    """
    A dataset subset.

    An instance of this class references a subset.
    """

    def __init__(self, api_service: HTTPService, subset_response: SubsetResponse) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param subset_response: response describing the subset
            to be created.
        """
        self._data = subset_response
        self._api_service = api_service

    @classmethod
    async def create(
        cls,
        name: str,
        dataset: Union["Dataset", str],
        observations: List[Union[Observation, int]],
    ) -> "Subset":
        """
        Create a subset of a dataset.

        :param name: Name of the subset.
        :param dataset: Name of the parent dataset.
        :param observations: Observations to be in the subset.
        :return: Created subset.
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.name

        api_service = get_api_client()
        observation_ids = [obs if isinstance(obs, int) else obs.id for obs in observations]
        subset_response = await SubsetAPI(api_service).create(
            subset_name=name, dataset_name=dataset, observation_ids=observation_ids
        )
        return Subset(api_service=api_service, subset_response=subset_response)

    async def update(self, observations: List[Union[Observation, int]]) -> "Subset":
        """
        Update the observations within a subset.

        :param observations: observations to add to the dataset
        :return: new updated subset instance
        """
        api_service = get_api_client()
        observation_ids = [obs if isinstance(obs, int) else obs.id for obs in observations]
        subset_response = await SubsetAPI(api_service).update(
            subset_name=self.name, observation_ids=observation_ids
        )
        return Subset(api_service=api_service, subset_response=subset_response)

    @classmethod
    async def get_by_name(cls, name: str) -> "Subset":
        """
        Get a subset by its name.

        :param name: Name of the subset to create an instance of.
        :return: Instance of the pipeline with the given name.
        """
        api_service = get_api_client()
        response = await SubsetAPI(api_service).get(name)
        return Subset(api_service, response)

    @property
    def id(self) -> int:
        """
        Get the ID of the instance.

        :return: ID of the instance.
        """
        return self._data.id

    @property
    def name(self) -> str:
        """
        Get the name the instance.

        :return: Name of the instance.
        """
        return self._data.name

    @property
    def observation_ids(self) -> List[int]:
        """
        Get the observation ids contained in the subset.

        :return: List of observation ids in the subset.
        """
        return self._data.observation_ids


class Dataset:
    """
    A dataset.

    An instance of this class references a dataset.
    """

    def __init__(self, api_service: HTTPService, dataset_response: DatasetResponse) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param dataset_response: Server response describing the dataset
            to be created.
        """
        self._data = dataset_response
        self._api_service = api_service

    @classmethod
    async def create(
        cls,
        dataset_name: str,
        dataset_type: ObservationType,
        file_names: Optional[List[str]] = None,
        subsets: Optional[List[Union[Subset, str]]] = None,
    ) -> "Dataset":
        """
        Create a dataset.

        :param dataset_name: Name of the dataset.
        :param dataset_type: Type of the dataset.
        :param file_names: List of paths to files to upload.
        :param subsets: List of subsets the observations are in.
        :return: Created dataset.
        """
        api_service = get_api_client()
        dataset_response = await DatasetAPI(api_service).create(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
        )
        dataset = Dataset(api_service=api_service, dataset_response=dataset_response)
        if file_names is not None:
            if subsets is None:
                subsets = []
            else:
                for subset in subsets:
                    subset_name = subset if isinstance(subset, str) else subset.name
                    await dataset.create_subset(subset_name, [])
            await dataset.upload_data(file_names, subsets)
            dataset = await Dataset.get_by_name(dataset.name)

        return dataset

    async def create_subset(self, name: str, observations: List[Union[Observation, int]]) -> Subset:
        """
        Create a subset of the dataset.

        :param name: Name of the subset to create.
        :param observations: Observations (or ids) to be part of the subset.
        :return: Created subsets.
        """
        return await Subset.create(name=name, dataset=self.name, observations=observations)

    async def upload_data(
        self, file_names: List[str], subsets: List[Union[Subset, str]]
    ) -> List[Observation]:
        """
        Upload data to the dataset.

        :param file_names: List of paths to files to upload.
        :param subsets: List of subsets the observations are in.
        :return: Created observations.
        """
        observations = []
        for observation in file_names:
            uploaded_observation = await Observation.create(
                dataset=self.name,
                file_name=observation,
                observation_type=ObservationType(self._data.type),
                subsets=subsets,
            )
            observations.append(uploaded_observation)

        return observations

    @classmethod
    async def get_by_name(cls, name: str) -> "Dataset":
        """
        Get a subset by its name.

        :param name: Name of the subset to create an instance of.
        :return: Instance of the pipeline with the given name.
        """
        api_service = get_api_client()
        pipeline_response = await DatasetAPI(api_service).get(name)
        return Dataset(api_service, pipeline_response)

    @property
    def id(self) -> int:
        """
        Get the ID of the instance.

        :return: ID of the instance.
        """
        return self._data.id

    @property
    def name(self) -> str:
        """
        Get the name the instance.

        :return: Name of the instance.
        """
        return self._data.name
