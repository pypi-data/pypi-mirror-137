"""
A pipeline on aidkit consists of analyses and evaluations. Pipelines must be
configured using the web GUI. After a pipeline has been configured, it can be
run on a data subset and a machine learning model version of choice using the
python client.

Running a pipeline on a machine learning model and a data subset creates
a pipeline run. Finishing a pipeline run creates a report, which
contains information about the evaluations and can be used to download
artifacts.
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from time import time
from typing import Any, Generator, List, Optional, Tuple, Type, Union

from pandas import DataFrame
from PIL import Image
from tabulate import tabulate
from tqdm import tqdm

from aidkit_client._endpoints.models import (
    IdentifierInput,
    PipelineRunResponse,
    PipelineRunState,
    RequiredContextDescription,
    TabularReport,
    TargetClassInput,
    UserProvidedContext,
)
from aidkit_client._endpoints.pipeline_runs import PipelineRunsAPI
from aidkit_client._endpoints.pipelines import PipelineResponse, PipelinesAPI
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.exceptions import (
    AidkitClientError,
    PipelineRunError,
    ResourceWithNameNotFoundError,
    RunTimeoutError,
    TargetClassNotPassedError,
)
from aidkit_client.resources.dataset import Observation, Subset
from aidkit_client.resources.ml_model import MLModelVersion


class PipelineRun:
    """
    A run of a pipeline.

    An instance of this class references a pipeline run on the server
    which has been created by running a pipeline.
    """

    def __init__(
        self, api_service: HTTPService, pipeline_run_response: PipelineRunResponse
    ) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communcation with the
            server.
        :param pipeline_run_response: Server response describing the pipeline
            run to be created.
        """
        self._data = pipeline_run_response
        self._api_service = api_service

    @classmethod
    async def get_by_id(cls, pipeline_run_id: int) -> "PipelineRun":
        """
        Get a pipeline run by its reference id on the aidkit server.

        :param pipeline_run_id: Reference ID of the pipeline run to fetch.
        :return: Instance of the pipeline with the given id.
        """
        api_service = get_api_client()
        response = await PipelineRunsAPI(api_service).get(pipeline_run_id)
        return PipelineRun(api_service, response)

    async def get_progress(self) -> Tuple[int, int]:
        """
        Get the progress of a pipeline run.

        :raises PipelineRunError: If the pipeline run has either failed or was
            stopped.
        :return: A tuple `(total_number, finished_number)`. `total_number` is
            the total number of tasks in the pipeline run, whereas
            `finished_number` is the number of tasks in the pipeline run which
            are finished.
        """
        response = await PipelineRunsAPI(self._api_service).get(self._data.id)
        states = [node.state for node in response.nodes]
        if PipelineRunState.FAILED in states:
            raise PipelineRunError("Pipeline failed.")
        if PipelineRunState.STOPPED in states:
            raise PipelineRunError("Pipeline stopped.")
        n_of_finished_nodes = sum(1 for state in states if state == PipelineRunState.SUCCESS)
        return len(states), n_of_finished_nodes

    async def get_state(self) -> PipelineRunState:
        """
        Get the state of the pipeline run. A pipeline can be either.

        * Stopped, if it got stopped by manual user intervention
        * Failed, if an analysis or evaluation failed
        * Running, if it is still running and not finished yet
        * Success, if it finished successfully

        :return: State of the pipeline run
        """
        # if one node is stopped, the whole run is stopped
        # else, if any node is running, the whole pipeline is running
        # otherwise, it's either pending or finished
        response = await PipelineRunsAPI(self._api_service).get(self._data.id)
        states = [node.state for node in response.nodes]
        if PipelineRunState.FAILED in states:
            return PipelineRunState.FAILED
        if PipelineRunState.STOPPED in states:
            return PipelineRunState.STOPPED
        if all(state == PipelineRunState.SUCCESS for state in states):
            return PipelineRunState.SUCCESS
        if all(state == PipelineRunState.PENDING for state in states):
            return PipelineRunState.PENDING
        return PipelineRunState.RUNNING

    async def report(
        self, pipeline_finish_timeout: Optional[int] = None, progress_bar: bool = False
    ) -> "Report":
        """
        Wait for the pipeline run to finish and return the report corresponding
        to the pipeline run after it is finished.

        :param pipeline_finish_timeout: Number of seconds to wait for the
            pipeline run to finish. If the pipeline run is not finished after
            `pipeline_finish_timeout` number of seconds, a `RunTimeoutError` is
            raised.
        :param progress_bar: Whether to display a progress bar informing about
            the pipeline run's update when waiting for the pipeline to finish.
        :raises RunTimeoutError: If `pipeline_finish_timeout` seconds have
            passed, but the pipeline run is not finished yet.
        :return: Instance of the report generated by the pipeline run.
        """
        starting_time = time()
        current_time = starting_time
        n_of_nodes, _ = await self.get_progress()
        last_finished_nodes = 0
        # the below is not missing an f-prefix, but is a format string for tqdm
        status_bar_format = (
            "{desc}: {percentage:3.0f}%|{bar}| "  # noqa: FS003
            "{n_fmt}/{total_fmt} [{elapsed}]"  # noqa: FS003
        )
        with tqdm(
            total=n_of_nodes,
            disable=not progress_bar,
            desc="Pipeline Run progress",
            miniters=1,
            mininterval=0,
            bar_format=status_bar_format,
        ) as pbar:
            while (
                pipeline_finish_timeout is None
                or current_time - starting_time < pipeline_finish_timeout
            ):
                n_of_nodes, finished_nodes = await self.get_progress()
                # keep the elapsed time at x.5 for consistent tqdm "elapsed time" updates
                await asyncio.sleep((starting_time - time()) % 1 + 0.5)
                pbar.update(finished_nodes - last_finished_nodes)
                # without refreshing, tqdm will not update the elapsed time unless there is progress
                pbar.refresh()
                last_finished_nodes = finished_nodes
                if n_of_nodes == finished_nodes:
                    return await Report.get_by_pipeline_run_id(self._data.id)
                current_time = time()
        raise RunTimeoutError(
            f"Pipeline has not finished after the timeout of {pipeline_finish_timeout} seconds."
        )

    @property
    def id(self) -> int:
        """
        Get the ID the instance is referenced by on the server.

        :return: ID of the instance
        """
        return self._data.id


class _ContextNames(Enum):
    ML_MODEL_VERSION = "ml_model_version_identifier"
    SUBSET = "subset_identifier"


_TARGET_CLASS_NAME = "TargetClassInput"


class Pipeline:
    """
    A pipeline.

    An instance of this class references a pipeline on the server which
    has been created in the web GUI.
    """

    def __init__(self, api_service: HTTPService, pipeline_response: PipelineResponse) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communcation with the
            server.
        :param pipeline_response: Server response describing the pipeline
            to be created.
        """
        self._data = pipeline_response
        self._api_service = api_service

    @classmethod
    async def get_by_id(cls, pipeline_id: int) -> "Pipeline":
        """
        Get a pipeline by its reference ID on the aidkit server.

        :param pipeline_id: Reference ID of the pipeline to fetch
        :return: Instance of the pipeline with the given ID.
        """
        api_service = get_api_client()
        pipeline_response = await PipelinesAPI(api_service).get_by_id(pipeline_id)
        return Pipeline(api_service, pipeline_response)

    @property
    def id(self) -> int:
        """
        Get the ID the instance is referenced by on the server.

        :return: ID of the instance
        """
        return self._data.id

    @property
    def name(self) -> str:
        """
        Get the name the instance.

        :return: Name of the instance
        """
        return self._data.name

    async def run(
        self,
        model_version: Union[int, MLModelVersion],
        subset: Union[int, Subset],
        target_class: Optional[int] = None,
    ) -> PipelineRun:
        """
        Run the pipeline with a specific model version and a specific subset.

        :param model_version: Model version to run the pipeline with.
            If an integer is passed, it is interpreted as the model version id.
        :param subset: Subset to run the pipeline with.
            If an integer is passed, it is interpreted as the subset id.
        :param target_class: Index of the target class to run the pipeline with.
            Some analyses need to be given a target class to run them. If such
            an analysis is contained in the pipeline, the index of the target
            class to run the analysis with must be passed. If the pipeline
            requires a target class index but `None` is passed, this method
            raises a `TargetClassNotPassedError`.
        :return: The pipeline run created by running the pipeline.
        """
        if isinstance(model_version, MLModelVersion):
            model_version_id = model_version.id
        else:
            model_version_id = model_version
        if isinstance(subset, Subset):
            subset_id = subset.id
        else:
            subset_id = subset
        required_context = self._data.context

        def required_context_to_context_mapper(
            required_context: RequiredContextDescription,
        ) -> UserProvidedContext:
            required_context_name = required_context.context_name
            context_value: Union[IdentifierInput, TargetClassInput]
            if required_context_name == _ContextNames.ML_MODEL_VERSION.value:
                context_value = IdentifierInput(value=model_version_id)
            elif required_context_name == _ContextNames.SUBSET.value:
                context_value = IdentifierInput(value=subset_id)
            elif required_context.context_type["title"] == _TARGET_CLASS_NAME:
                if target_class is None:
                    raise TargetClassNotPassedError("Pipeline requires a target class to be set")
                context_value = TargetClassInput(value=target_class)
            else:
                raise AidkitClientError(
                    f"Unknown context type '{required_context.context_type['title']}' required "
                    f"under context name {required_context_name}"
                )
            return UserProvidedContext(
                pipeline_node_id=required_context.pipeline_node_id,
                context_name=required_context.context_name,
                value=context_value,
            )

        context = map(required_context_to_context_mapper, required_context)
        pipeline_response = await PipelineRunsAPI(self._api_service).run_pipeline(
            self.id, context=list(context)
        )
        return PipelineRun(self._api_service, pipeline_response)

    @classmethod
    async def get_by_name(cls, name: str) -> "Pipeline":
        """
        Get a pipeline by its name.

        :param name: Name of the pipeline to create an instance for.
        :raises ResourceWithNameNotFoundError: If no pipeline with the given name
            exists.
        :return: Instance of the pipeline with the given name.
        """
        api_service = get_api_client()
        pipeline_response_list = await PipelinesAPI(api_service).get_all()
        try:
            (pipeline_response,) = [
                pipeline_response
                for pipeline_response in pipeline_response_list
                if pipeline_response.name == name
            ]
        except ValueError as wrong_entry_number:
            available_names = ", ".join(
                pipeline_response.name for pipeline_response in pipeline_response_list
            )
            raise ResourceWithNameNotFoundError(
                f"Pipeline with name '{name}' not found."
                f"Existing pipeline names: '[{available_names}]'."
            ) from wrong_entry_number
        # This refetch is required since get_all call returns only partial results.
        # Specifically, the required_context returned on the GET /pipelines/ endpoint is [].
        return await cls.get_by_id(pipeline_response.id)


@dataclass
class Artifact:
    """
    Wrapper class for an artifact url providing a method to fetch the artifact.
    """

    url: str

    async def fetch_artifact(self) -> Union[str, Image.Image]:
        """
        Fetch the artifact from the url.

        :raises AidkitClientError: If the response of the aidkit server is invalid.
        :return: artifact
        """
        api_service = get_api_client()
        response = await api_service.get_from_cdn(self.url)
        artifact_file_type = self.url.rsplit(".", maxsplit=1)[-1]
        if not isinstance(response.body, dict):
            raise AidkitClientError(
                f"Response body-content must be bytes but was type {type(response.body)}"
            )
        content = response.body["content"]
        if not isinstance(content, bytes):
            raise AidkitClientError(
                f"Response body-content must be bytes but was type {type(content)}"
            )
        if artifact_file_type == "txt":
            return content.decode("utf-8")

        if artifact_file_type == "png":
            return Image.open(BytesIO(content))

        raise AidkitClientError(
            f"Unknown artifact type received. "
            f"Valid are 'png' and 'txt' but received '{artifact_file_type}'."
        )


class Report:
    """
    A Report which is created by a finished pipeline run.

    An instance of this class references a report on the server which
    has been created by a pipeline run.
    """

    def __init__(
        self,
        api_service: HTTPService,
        tabular_report: TabularReport,
        pipeline_run_id: int,
    ) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communication with the
            server.
        :param tabular_report: Server response describing the report
            to be created.
        :param pipeline_run_id: id of the pipeline run the report is describing
        """
        self._api_service = api_service
        self._tabular_report = tabular_report
        self.pipeline_run_id = pipeline_run_id

    # pylint: disable=too-many-branches
    async def get_artifact_plots(
        self,
        method_name: Optional[str] = None,
        observation: Optional[Union[Observation, int]] = None,
        param_string: Optional[str] = None,
    ) -> DataFrame:
        """
        Return all artifacts matching the specified criteria.

        :param method_name: if provided, filter by method_name
        :param observation: if provided, filter by observation
        :param param_string: if provided, filter by param_string
        :return: filtered artifacts
        """
        api_service = get_api_client()

        if observation is not None:
            observation_id = observation if isinstance(observation, int) else observation.id
            artifacts = await PipelineRunsAPI(api_service).get_artifacts_by_observation_id(
                self.pipeline_run_id, observation_id
            )
        elif method_name is not None:
            # if we get artifacts by node id, the `param_string` is not set by the aidkit server
            pipeline_run_nodes: List[Tuple[int, str]] = []
            for method in self._tabular_report.methods:
                if method.method_name == method_name and (
                    param_string is None or method.param_string == param_string
                ):
                    pipeline_run_nodes.append((method.pipeline_node_id, method.param_string))
            artifacts = []
            for pipeline_run_node_id, method_param_string in pipeline_run_nodes:
                artifact_list = await PipelineRunsAPI(
                    api_service
                ).get_artifacts_by_pipeline_node_id(self.pipeline_run_id, pipeline_run_node_id)
                for artifact in artifact_list:
                    artifact.param_string = method_param_string
                artifacts.extend(artifact_list)

        elif param_string is not None:
            pipeline_run_nodes = []
            for method in self._tabular_report.methods:
                if method.param_string == param_string:
                    pipeline_run_nodes.append((method.pipeline_node_id, method.param_string))
            artifacts = []
            for pipeline_run_node_id, method_param_string in pipeline_run_nodes:
                artifact_list = await PipelineRunsAPI(
                    api_service
                ).get_artifacts_by_pipeline_node_id(self.pipeline_run_id, pipeline_run_node_id)
                for artifact in artifact_list:
                    artifact.param_string = method_param_string
                artifacts.extend(artifact_list)
        else:  # get all
            artifacts = []
            for observation_from_report in self._tabular_report.observations:
                artifacts.extend(
                    await PipelineRunsAPI(api_service).get_artifacts_by_observation_id(
                        self.pipeline_run_id, observation_from_report.id
                    )
                )

        filtered_artifacts = []
        for artifact in artifacts:
            if method_name is not None and artifact.method_name != method_name:
                continue
            if param_string is not None and artifact.param_string != param_string:
                continue
            if observation is not None:
                observation_id = observation if isinstance(observation, int) else observation.id
                if artifact.observation.id != observation_id:
                    continue

            filtered_artifacts.append(artifact)

        rows = []
        for artifact in filtered_artifacts:
            rows.append(
                [
                    artifact.method_name,
                    artifact.param_string,
                    artifact.observation.id,
                    Artifact(url=artifact.plot_url),
                ]
            )

        return DataFrame(rows, columns=["Method", "Param String", "Observation ID", "Artifact"])

    @classmethod
    async def get_by_pipeline_run_id(cls: Type["Report"], report_id: int) -> "Report":
        """
        Get a report by its reference ID on the aidkit server.

        :param report_id: Reference ID of the report to fetch
        :return: instance of the report with the given ID
        """
        api_service = get_api_client()
        tabular_report = await PipelineRunsAPI(api_service).get_report(report_id)
        return cls(
            api_service=api_service,
            tabular_report=tabular_report,
            pipeline_run_id=report_id,
        )

    @property
    def _data_generator(self) -> Generator[List[Union[str, float]], Any, None]:
        return (
            [
                row.method.method_name,
                row.metric.method_name,
                row.metric.param_string,
                row.metric_value,
            ]
            for row in self._tabular_report.rows
        )

    @property
    def table_string(self) -> str:
        """
        Create a table from the report.

        :return: Table as string form
        """
        return tabulate(self._data_generator, headers=["Method", "Metric", "Parameters", "Value"])

    @property
    def table(self) -> DataFrame:
        """
        Return the tabular report as a pandas DataFrame.

        :return: Pandas DataFrame containing the tabular report.
        """
        result_df = DataFrame(
            list(self._data_generator),
            columns=["Method", "Metric", "Parameters", "Value"],
        )
        return result_df

    @property
    def id(self) -> int:
        """
        Get the ID the instance is referenced by on the server.

        :return: ID of the pipeline run
        """
        return self.pipeline_run_id
