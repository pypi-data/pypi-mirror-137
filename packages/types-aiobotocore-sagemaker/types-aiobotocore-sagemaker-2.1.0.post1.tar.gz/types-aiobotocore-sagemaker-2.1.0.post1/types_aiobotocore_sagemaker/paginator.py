"""
Type annotations for sagemaker service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker.client import SageMakerClient
    from types_aiobotocore_sagemaker.paginator import (
        ListActionsPaginator,
        ListAlgorithmsPaginator,
        ListAppImageConfigsPaginator,
        ListAppsPaginator,
        ListArtifactsPaginator,
        ListAssociationsPaginator,
        ListAutoMLJobsPaginator,
        ListCandidatesForAutoMLJobPaginator,
        ListCodeRepositoriesPaginator,
        ListCompilationJobsPaginator,
        ListContextsPaginator,
        ListDataQualityJobDefinitionsPaginator,
        ListDeviceFleetsPaginator,
        ListDevicesPaginator,
        ListDomainsPaginator,
        ListEdgePackagingJobsPaginator,
        ListEndpointConfigsPaginator,
        ListEndpointsPaginator,
        ListExperimentsPaginator,
        ListFeatureGroupsPaginator,
        ListFlowDefinitionsPaginator,
        ListHumanTaskUisPaginator,
        ListHyperParameterTuningJobsPaginator,
        ListImageVersionsPaginator,
        ListImagesPaginator,
        ListInferenceRecommendationsJobsPaginator,
        ListLabelingJobsPaginator,
        ListLabelingJobsForWorkteamPaginator,
        ListLineageGroupsPaginator,
        ListModelBiasJobDefinitionsPaginator,
        ListModelExplainabilityJobDefinitionsPaginator,
        ListModelMetadataPaginator,
        ListModelPackageGroupsPaginator,
        ListModelPackagesPaginator,
        ListModelQualityJobDefinitionsPaginator,
        ListModelsPaginator,
        ListMonitoringExecutionsPaginator,
        ListMonitoringSchedulesPaginator,
        ListNotebookInstanceLifecycleConfigsPaginator,
        ListNotebookInstancesPaginator,
        ListPipelineExecutionStepsPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelineParametersForExecutionPaginator,
        ListPipelinesPaginator,
        ListProcessingJobsPaginator,
        ListStudioLifecycleConfigsPaginator,
        ListSubscribedWorkteamsPaginator,
        ListTagsPaginator,
        ListTrainingJobsPaginator,
        ListTrainingJobsForHyperParameterTuningJobPaginator,
        ListTransformJobsPaginator,
        ListTrialComponentsPaginator,
        ListTrialsPaginator,
        ListUserProfilesPaginator,
        ListWorkforcesPaginator,
        ListWorkteamsPaginator,
        SearchPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker") as client:
        client: SageMakerClient

        list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
        list_algorithms_paginator: ListAlgorithmsPaginator = client.get_paginator("list_algorithms")
        list_app_image_configs_paginator: ListAppImageConfigsPaginator = client.get_paginator("list_app_image_configs")
        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_auto_ml_jobs_paginator: ListAutoMLJobsPaginator = client.get_paginator("list_auto_ml_jobs")
        list_candidates_for_auto_ml_job_paginator: ListCandidatesForAutoMLJobPaginator = client.get_paginator("list_candidates_for_auto_ml_job")
        list_code_repositories_paginator: ListCodeRepositoriesPaginator = client.get_paginator("list_code_repositories")
        list_compilation_jobs_paginator: ListCompilationJobsPaginator = client.get_paginator("list_compilation_jobs")
        list_contexts_paginator: ListContextsPaginator = client.get_paginator("list_contexts")
        list_data_quality_job_definitions_paginator: ListDataQualityJobDefinitionsPaginator = client.get_paginator("list_data_quality_job_definitions")
        list_device_fleets_paginator: ListDeviceFleetsPaginator = client.get_paginator("list_device_fleets")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_edge_packaging_jobs_paginator: ListEdgePackagingJobsPaginator = client.get_paginator("list_edge_packaging_jobs")
        list_endpoint_configs_paginator: ListEndpointConfigsPaginator = client.get_paginator("list_endpoint_configs")
        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_feature_groups_paginator: ListFeatureGroupsPaginator = client.get_paginator("list_feature_groups")
        list_flow_definitions_paginator: ListFlowDefinitionsPaginator = client.get_paginator("list_flow_definitions")
        list_human_task_uis_paginator: ListHumanTaskUisPaginator = client.get_paginator("list_human_task_uis")
        list_hyper_parameter_tuning_jobs_paginator: ListHyperParameterTuningJobsPaginator = client.get_paginator("list_hyper_parameter_tuning_jobs")
        list_image_versions_paginator: ListImageVersionsPaginator = client.get_paginator("list_image_versions")
        list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
        list_inference_recommendations_jobs_paginator: ListInferenceRecommendationsJobsPaginator = client.get_paginator("list_inference_recommendations_jobs")
        list_labeling_jobs_paginator: ListLabelingJobsPaginator = client.get_paginator("list_labeling_jobs")
        list_labeling_jobs_for_workteam_paginator: ListLabelingJobsForWorkteamPaginator = client.get_paginator("list_labeling_jobs_for_workteam")
        list_lineage_groups_paginator: ListLineageGroupsPaginator = client.get_paginator("list_lineage_groups")
        list_model_bias_job_definitions_paginator: ListModelBiasJobDefinitionsPaginator = client.get_paginator("list_model_bias_job_definitions")
        list_model_explainability_job_definitions_paginator: ListModelExplainabilityJobDefinitionsPaginator = client.get_paginator("list_model_explainability_job_definitions")
        list_model_metadata_paginator: ListModelMetadataPaginator = client.get_paginator("list_model_metadata")
        list_model_package_groups_paginator: ListModelPackageGroupsPaginator = client.get_paginator("list_model_package_groups")
        list_model_packages_paginator: ListModelPackagesPaginator = client.get_paginator("list_model_packages")
        list_model_quality_job_definitions_paginator: ListModelQualityJobDefinitionsPaginator = client.get_paginator("list_model_quality_job_definitions")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_monitoring_executions_paginator: ListMonitoringExecutionsPaginator = client.get_paginator("list_monitoring_executions")
        list_monitoring_schedules_paginator: ListMonitoringSchedulesPaginator = client.get_paginator("list_monitoring_schedules")
        list_notebook_instance_lifecycle_configs_paginator: ListNotebookInstanceLifecycleConfigsPaginator = client.get_paginator("list_notebook_instance_lifecycle_configs")
        list_notebook_instances_paginator: ListNotebookInstancesPaginator = client.get_paginator("list_notebook_instances")
        list_pipeline_execution_steps_paginator: ListPipelineExecutionStepsPaginator = client.get_paginator("list_pipeline_execution_steps")
        list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
        list_pipeline_parameters_for_execution_paginator: ListPipelineParametersForExecutionPaginator = client.get_paginator("list_pipeline_parameters_for_execution")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_processing_jobs_paginator: ListProcessingJobsPaginator = client.get_paginator("list_processing_jobs")
        list_studio_lifecycle_configs_paginator: ListStudioLifecycleConfigsPaginator = client.get_paginator("list_studio_lifecycle_configs")
        list_subscribed_workteams_paginator: ListSubscribedWorkteamsPaginator = client.get_paginator("list_subscribed_workteams")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_training_jobs_paginator: ListTrainingJobsPaginator = client.get_paginator("list_training_jobs")
        list_training_jobs_for_hyper_parameter_tuning_job_paginator: ListTrainingJobsForHyperParameterTuningJobPaginator = client.get_paginator("list_training_jobs_for_hyper_parameter_tuning_job")
        list_transform_jobs_paginator: ListTransformJobsPaginator = client.get_paginator("list_transform_jobs")
        list_trial_components_paginator: ListTrialComponentsPaginator = client.get_paginator("list_trial_components")
        list_trials_paginator: ListTrialsPaginator = client.get_paginator("list_trials")
        list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
        list_workforces_paginator: ListWorkforcesPaginator = client.get_paginator("list_workforces")
        list_workteams_paginator: ListWorkteamsPaginator = client.get_paginator("list_workteams")
        search_paginator: SearchPaginator = client.get_paginator("search")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    AlgorithmSortByType,
    AppImageConfigSortKeyType,
    AssociationEdgeTypeType,
    AutoMLJobStatusType,
    AutoMLSortByType,
    AutoMLSortOrderType,
    CandidateSortByType,
    CandidateStatusType,
    CodeRepositorySortByType,
    CodeRepositorySortOrderType,
    CompilationJobStatusType,
    EdgePackagingJobStatusType,
    EndpointConfigSortKeyType,
    EndpointSortKeyType,
    EndpointStatusType,
    ExecutionStatusType,
    FeatureGroupSortByType,
    FeatureGroupSortOrderType,
    FeatureGroupStatusType,
    HyperParameterTuningJobSortByOptionsType,
    HyperParameterTuningJobStatusType,
    ImageSortByType,
    ImageSortOrderType,
    ImageVersionSortByType,
    ImageVersionSortOrderType,
    LabelingJobStatusType,
    ListCompilationJobsSortByType,
    ListDeviceFleetsSortByType,
    ListEdgePackagingJobsSortByType,
    ListInferenceRecommendationsJobsSortByType,
    ListWorkforcesSortByOptionsType,
    ListWorkteamsSortByOptionsType,
    ModelApprovalStatusType,
    ModelPackageGroupSortByType,
    ModelPackageSortByType,
    ModelPackageTypeType,
    ModelSortKeyType,
    MonitoringExecutionSortKeyType,
    MonitoringJobDefinitionSortKeyType,
    MonitoringScheduleSortKeyType,
    MonitoringTypeType,
    NotebookInstanceLifecycleConfigSortKeyType,
    NotebookInstanceLifecycleConfigSortOrderType,
    NotebookInstanceSortKeyType,
    NotebookInstanceSortOrderType,
    NotebookInstanceStatusType,
    OfflineStoreStatusValueType,
    OrderKeyType,
    ProcessingJobStatusType,
    RecommendationJobStatusType,
    ResourceTypeType,
    ScheduleStatusType,
    SearchSortOrderType,
    SortActionsByType,
    SortAssociationsByType,
    SortByType,
    SortContextsByType,
    SortExperimentsByType,
    SortLineageGroupsByType,
    SortOrderType,
    SortPipelineExecutionsByType,
    SortPipelinesByType,
    SortTrialComponentsByType,
    SortTrialsByType,
    StudioLifecycleConfigAppTypeType,
    StudioLifecycleConfigSortKeyType,
    TrainingJobSortByOptionsType,
    TrainingJobStatusType,
    TransformJobStatusType,
    UserProfileSortKeyType,
)
from .type_defs import (
    ListActionsResponseTypeDef,
    ListAlgorithmsOutputTypeDef,
    ListAppImageConfigsResponseTypeDef,
    ListAppsResponseTypeDef,
    ListArtifactsResponseTypeDef,
    ListAssociationsResponseTypeDef,
    ListAutoMLJobsResponseTypeDef,
    ListCandidatesForAutoMLJobResponseTypeDef,
    ListCodeRepositoriesOutputTypeDef,
    ListCompilationJobsResponseTypeDef,
    ListContextsResponseTypeDef,
    ListDataQualityJobDefinitionsResponseTypeDef,
    ListDeviceFleetsResponseTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsResponseTypeDef,
    ListEdgePackagingJobsResponseTypeDef,
    ListEndpointConfigsOutputTypeDef,
    ListEndpointsOutputTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeatureGroupsResponseTypeDef,
    ListFlowDefinitionsResponseTypeDef,
    ListHumanTaskUisResponseTypeDef,
    ListHyperParameterTuningJobsResponseTypeDef,
    ListImagesResponseTypeDef,
    ListImageVersionsResponseTypeDef,
    ListInferenceRecommendationsJobsResponseTypeDef,
    ListLabelingJobsForWorkteamResponseTypeDef,
    ListLabelingJobsResponseTypeDef,
    ListLineageGroupsResponseTypeDef,
    ListModelBiasJobDefinitionsResponseTypeDef,
    ListModelExplainabilityJobDefinitionsResponseTypeDef,
    ListModelMetadataResponseTypeDef,
    ListModelPackageGroupsOutputTypeDef,
    ListModelPackagesOutputTypeDef,
    ListModelQualityJobDefinitionsResponseTypeDef,
    ListModelsOutputTypeDef,
    ListMonitoringExecutionsResponseTypeDef,
    ListMonitoringSchedulesResponseTypeDef,
    ListNotebookInstanceLifecycleConfigsOutputTypeDef,
    ListNotebookInstancesOutputTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelineExecutionStepsResponseTypeDef,
    ListPipelineParametersForExecutionResponseTypeDef,
    ListPipelinesResponseTypeDef,
    ListProcessingJobsResponseTypeDef,
    ListStudioLifecycleConfigsResponseTypeDef,
    ListSubscribedWorkteamsResponseTypeDef,
    ListTagsOutputTypeDef,
    ListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    ListTrainingJobsResponseTypeDef,
    ListTransformJobsResponseTypeDef,
    ListTrialComponentsResponseTypeDef,
    ListTrialsResponseTypeDef,
    ListUserProfilesResponseTypeDef,
    ListWorkforcesResponseTypeDef,
    ListWorkteamsResponseTypeDef,
    ModelMetadataSearchExpressionTypeDef,
    PaginatorConfigTypeDef,
    SearchExpressionTypeDef,
    SearchResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListActionsPaginator",
    "ListAlgorithmsPaginator",
    "ListAppImageConfigsPaginator",
    "ListAppsPaginator",
    "ListArtifactsPaginator",
    "ListAssociationsPaginator",
    "ListAutoMLJobsPaginator",
    "ListCandidatesForAutoMLJobPaginator",
    "ListCodeRepositoriesPaginator",
    "ListCompilationJobsPaginator",
    "ListContextsPaginator",
    "ListDataQualityJobDefinitionsPaginator",
    "ListDeviceFleetsPaginator",
    "ListDevicesPaginator",
    "ListDomainsPaginator",
    "ListEdgePackagingJobsPaginator",
    "ListEndpointConfigsPaginator",
    "ListEndpointsPaginator",
    "ListExperimentsPaginator",
    "ListFeatureGroupsPaginator",
    "ListFlowDefinitionsPaginator",
    "ListHumanTaskUisPaginator",
    "ListHyperParameterTuningJobsPaginator",
    "ListImageVersionsPaginator",
    "ListImagesPaginator",
    "ListInferenceRecommendationsJobsPaginator",
    "ListLabelingJobsPaginator",
    "ListLabelingJobsForWorkteamPaginator",
    "ListLineageGroupsPaginator",
    "ListModelBiasJobDefinitionsPaginator",
    "ListModelExplainabilityJobDefinitionsPaginator",
    "ListModelMetadataPaginator",
    "ListModelPackageGroupsPaginator",
    "ListModelPackagesPaginator",
    "ListModelQualityJobDefinitionsPaginator",
    "ListModelsPaginator",
    "ListMonitoringExecutionsPaginator",
    "ListMonitoringSchedulesPaginator",
    "ListNotebookInstanceLifecycleConfigsPaginator",
    "ListNotebookInstancesPaginator",
    "ListPipelineExecutionStepsPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelineParametersForExecutionPaginator",
    "ListPipelinesPaginator",
    "ListProcessingJobsPaginator",
    "ListStudioLifecycleConfigsPaginator",
    "ListSubscribedWorkteamsPaginator",
    "ListTagsPaginator",
    "ListTrainingJobsPaginator",
    "ListTrainingJobsForHyperParameterTuningJobPaginator",
    "ListTransformJobsPaginator",
    "ListTrialComponentsPaginator",
    "ListTrialsPaginator",
    "ListUserProfilesPaginator",
    "ListWorkforcesPaginator",
    "ListWorkteamsPaginator",
    "SearchPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListActions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listactionspaginator)
    """

    async def paginate(
        self,
        *,
        SourceUri: str = ...,
        ActionType: str = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortActionsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListActions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listactionspaginator)
        """


class ListAlgorithmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAlgorithms)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listalgorithmspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        SortBy: AlgorithmSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAlgorithmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAlgorithms.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listalgorithmspaginator)
        """


class ListAppImageConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAppImageConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listappimageconfigspaginator)
    """

    async def paginate(
        self,
        *,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        ModifiedTimeBefore: Union[datetime, str] = ...,
        ModifiedTimeAfter: Union[datetime, str] = ...,
        SortBy: AppImageConfigSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppImageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAppImageConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listappimageconfigspaginator)
        """


class ListAppsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListApps)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listappspaginator)
    """

    async def paginate(
        self,
        *,
        SortOrder: SortOrderType = ...,
        SortBy: Literal["CreationTime"] = ...,
        DomainIdEquals: str = ...,
        UserProfileNameEquals: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListApps.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listappspaginator)
        """


class ListArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListArtifacts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listartifactspaginator)
    """

    async def paginate(
        self,
        *,
        SourceUri: str = ...,
        ArtifactType: str = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: Literal["CreationTime"] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listartifactspaginator)
        """


class ListAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAssociations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listassociationspaginator)
    """

    async def paginate(
        self,
        *,
        SourceArn: str = ...,
        DestinationArn: str = ...,
        SourceType: str = ...,
        DestinationType: str = ...,
        AssociationType: AssociationEdgeTypeType = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortAssociationsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listassociationspaginator)
        """


class ListAutoMLJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAutoMLJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listautomljobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        StatusEquals: AutoMLJobStatusType = ...,
        SortOrder: AutoMLSortOrderType = ...,
        SortBy: AutoMLSortByType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAutoMLJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAutoMLJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listautomljobspaginator)
        """


class ListCandidatesForAutoMLJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCandidatesForAutoMLJob)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcandidatesforautomljobpaginator)
    """

    async def paginate(
        self,
        *,
        AutoMLJobName: str,
        StatusEquals: CandidateStatusType = ...,
        CandidateNameEquals: str = ...,
        SortOrder: AutoMLSortOrderType = ...,
        SortBy: CandidateSortByType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCandidatesForAutoMLJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCandidatesForAutoMLJob.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcandidatesforautomljobpaginator)
        """


class ListCodeRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCodeRepositories)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcoderepositoriespaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        SortBy: CodeRepositorySortByType = ...,
        SortOrder: CodeRepositorySortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCodeRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCodeRepositories.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcoderepositoriespaginator)
        """


class ListCompilationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCompilationJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcompilationjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        StatusEquals: CompilationJobStatusType = ...,
        SortBy: ListCompilationJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCompilationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCompilationJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcompilationjobspaginator)
        """


class ListContextsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListContexts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcontextspaginator)
    """

    async def paginate(
        self,
        *,
        SourceUri: str = ...,
        ContextType: str = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortContextsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListContexts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listcontextspaginator)
        """


class ListDataQualityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDataQualityJobDefinitions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdataqualityjobdefinitionspaginator)
    """

    async def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDataQualityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdataqualityjobdefinitionspaginator)
        """


class ListDeviceFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDeviceFleets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdevicefleetspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        SortBy: ListDeviceFleetsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeviceFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDeviceFleets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdevicefleetspaginator)
        """


class ListDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdevicespaginator)
    """

    async def paginate(
        self,
        *,
        LatestHeartbeatAfter: Union[datetime, str] = ...,
        ModelName: str = ...,
        DeviceFleetName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdevicespaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdomainspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listdomainspaginator)
        """


class ListEdgePackagingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEdgePackagingJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listedgepackagingjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        ModelNameContains: str = ...,
        StatusEquals: EdgePackagingJobStatusType = ...,
        SortBy: ListEdgePackagingJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEdgePackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEdgePackagingJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listedgepackagingjobspaginator)
        """


class ListEndpointConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpointConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listendpointconfigspaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: EndpointConfigSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEndpointConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpointConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listendpointconfigspaginator)
        """


class ListEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpoints)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listendpointspaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: EndpointSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        StatusEquals: EndpointStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listendpointspaginator)
        """


class ListExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListExperiments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listexperimentspaginator)
    """

    async def paginate(
        self,
        *,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortExperimentsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listexperimentspaginator)
        """


class ListFeatureGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFeatureGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listfeaturegroupspaginator)
    """

    async def paginate(
        self,
        *,
        NameContains: str = ...,
        FeatureGroupStatusEquals: FeatureGroupStatusType = ...,
        OfflineStoreStatusEquals: OfflineStoreStatusValueType = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        SortOrder: FeatureGroupSortOrderType = ...,
        SortBy: FeatureGroupSortByType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFeatureGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFeatureGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listfeaturegroupspaginator)
        """


class ListFlowDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFlowDefinitions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listflowdefinitionspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFlowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFlowDefinitions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listflowdefinitionspaginator)
        """


class ListHumanTaskUisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHumanTaskUis)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listhumantaskuispaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListHumanTaskUisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHumanTaskUis.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listhumantaskuispaginator)
        """


class ListHyperParameterTuningJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHyperParameterTuningJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listhyperparametertuningjobspaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: HyperParameterTuningJobSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        StatusEquals: HyperParameterTuningJobStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListHyperParameterTuningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHyperParameterTuningJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listhyperparametertuningjobspaginator)
        """


class ListImageVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImageVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listimageversionspaginator)
    """

    async def paginate(
        self,
        *,
        ImageName: str,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        SortBy: ImageVersionSortByType = ...,
        SortOrder: ImageVersionSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListImageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImageVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listimageversionspaginator)
        """


class ListImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listimagespaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        SortBy: ImageSortByType = ...,
        SortOrder: ImageSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listimagespaginator)
        """


class ListInferenceRecommendationsJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceRecommendationsJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listinferencerecommendationsjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        StatusEquals: RecommendationJobStatusType = ...,
        SortBy: ListInferenceRecommendationsJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInferenceRecommendationsJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceRecommendationsJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listinferencerecommendationsjobspaginator)
        """


class ListLabelingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listlabelingjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        StatusEquals: LabelingJobStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLabelingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listlabelingjobspaginator)
        """


class ListLabelingJobsForWorkteamPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobsForWorkteam)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listlabelingjobsforworkteampaginator)
    """

    async def paginate(
        self,
        *,
        WorkteamArn: str,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        JobReferenceCodeContains: str = ...,
        SortBy: Literal["CreationTime"] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLabelingJobsForWorkteamResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobsForWorkteam.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listlabelingjobsforworkteampaginator)
        """


class ListLineageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLineageGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listlineagegroupspaginator)
    """

    async def paginate(
        self,
        *,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortLineageGroupsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLineageGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLineageGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listlineagegroupspaginator)
        """


class ListModelBiasJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelBiasJobDefinitions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelbiasjobdefinitionspaginator)
    """

    async def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelBiasJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelBiasJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelbiasjobdefinitionspaginator)
        """


class ListModelExplainabilityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelexplainabilityjobdefinitionspaginator)
    """

    async def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelExplainabilityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelexplainabilityjobdefinitionspaginator)
        """


class ListModelMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelMetadata)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelmetadatapaginator)
    """

    async def paginate(
        self,
        *,
        SearchExpression: "ModelMetadataSearchExpressionTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelMetadata.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelmetadatapaginator)
        """


class ListModelPackageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackageGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelpackagegroupspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        SortBy: ModelPackageGroupSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelPackageGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackageGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelpackagegroupspaginator)
        """


class ListModelPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelpackagespaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        ModelApprovalStatus: ModelApprovalStatusType = ...,
        ModelPackageGroupName: str = ...,
        ModelPackageType: ModelPackageTypeType = ...,
        SortBy: ModelPackageSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelpackagespaginator)
        """


class ListModelQualityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelQualityJobDefinitions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelqualityjobdefinitionspaginator)
    """

    async def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelQualityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelqualityjobdefinitionspaginator)
        """


class ListModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModels)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelspaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: ModelSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModels.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmodelspaginator)
        """


class ListMonitoringExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmonitoringexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        MonitoringScheduleName: str = ...,
        EndpointName: str = ...,
        SortBy: MonitoringExecutionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        ScheduledTimeBefore: Union[datetime, str] = ...,
        ScheduledTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        StatusEquals: ExecutionStatusType = ...,
        MonitoringJobDefinitionName: str = ...,
        MonitoringTypeEquals: MonitoringTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMonitoringExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmonitoringexecutionspaginator)
        """


class ListMonitoringSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringSchedules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmonitoringschedulespaginator)
    """

    async def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringScheduleSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        StatusEquals: ScheduleStatusType = ...,
        MonitoringJobDefinitionName: str = ...,
        MonitoringTypeEquals: MonitoringTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMonitoringSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringSchedules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listmonitoringschedulespaginator)
        """


class ListNotebookInstanceLifecycleConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listnotebookinstancelifecycleconfigspaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: NotebookInstanceLifecycleConfigSortKeyType = ...,
        SortOrder: NotebookInstanceLifecycleConfigSortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNotebookInstanceLifecycleConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listnotebookinstancelifecycleconfigspaginator)
        """


class ListNotebookInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listnotebookinstancespaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: NotebookInstanceSortKeyType = ...,
        SortOrder: NotebookInstanceSortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        StatusEquals: NotebookInstanceStatusType = ...,
        NotebookInstanceLifecycleConfigNameContains: str = ...,
        DefaultCodeRepositoryContains: str = ...,
        AdditionalCodeRepositoryEquals: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNotebookInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listnotebookinstancespaginator)
        """


class ListPipelineExecutionStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutionSteps)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelineexecutionstepspaginator)
    """

    async def paginate(
        self,
        *,
        PipelineExecutionArn: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelineExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutionSteps.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelineexecutionstepspaginator)
        """


class ListPipelineExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelineexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        PipelineName: str,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortPipelineExecutionsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelineExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelineexecutionspaginator)
        """


class ListPipelineParametersForExecutionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineParametersForExecution)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelineparametersforexecutionpaginator)
    """

    async def paginate(
        self, *, PipelineExecutionArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelineParametersForExecutionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineParametersForExecution.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelineparametersforexecutionpaginator)
        """


class ListPipelinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelines)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelinespaginator)
    """

    async def paginate(
        self,
        *,
        PipelineNamePrefix: str = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortPipelinesByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listpipelinespaginator)
        """


class ListProcessingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListProcessingJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listprocessingjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        StatusEquals: ProcessingJobStatusType = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProcessingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListProcessingJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listprocessingjobspaginator)
        """


class ListStudioLifecycleConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListStudioLifecycleConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#liststudiolifecycleconfigspaginator)
    """

    async def paginate(
        self,
        *,
        NameContains: str = ...,
        AppTypeEquals: StudioLifecycleConfigAppTypeType = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        CreationTimeAfter: Union[datetime, str] = ...,
        ModifiedTimeBefore: Union[datetime, str] = ...,
        ModifiedTimeAfter: Union[datetime, str] = ...,
        SortBy: StudioLifecycleConfigSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStudioLifecycleConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListStudioLifecycleConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#liststudiolifecycleconfigspaginator)
        """


class ListSubscribedWorkteamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListSubscribedWorkteams)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listsubscribedworkteamspaginator)
    """

    async def paginate(
        self, *, NameContains: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSubscribedWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListSubscribedWorkteams.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listsubscribedworkteamspaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtagspaginator)
    """

    async def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtagspaginator)
        """


class ListTrainingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrainingjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        StatusEquals: TrainingJobStatusType = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTrainingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrainingjobspaginator)
        """


class ListTrainingJobsForHyperParameterTuningJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrainingjobsforhyperparametertuningjobpaginator)
    """

    async def paginate(
        self,
        *,
        HyperParameterTuningJobName: str,
        StatusEquals: TrainingJobStatusType = ...,
        SortBy: TrainingJobSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTrainingJobsForHyperParameterTuningJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrainingjobsforhyperparametertuningjobpaginator)
        """


class ListTransformJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTransformJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtransformjobspaginator)
    """

    async def paginate(
        self,
        *,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        LastModifiedTimeAfter: Union[datetime, str] = ...,
        LastModifiedTimeBefore: Union[datetime, str] = ...,
        NameContains: str = ...,
        StatusEquals: TransformJobStatusType = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTransformJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTransformJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtransformjobspaginator)
        """


class ListTrialComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrialComponents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrialcomponentspaginator)
    """

    async def paginate(
        self,
        *,
        ExperimentName: str = ...,
        TrialName: str = ...,
        SourceArn: str = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortTrialComponentsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTrialComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrialComponents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrialcomponentspaginator)
        """


class ListTrialsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrials)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrialspaginator)
    """

    async def paginate(
        self,
        *,
        ExperimentName: str = ...,
        TrialComponentName: str = ...,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        SortBy: SortTrialsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTrialsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrials.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listtrialspaginator)
        """


class ListUserProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListUserProfiles)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listuserprofilespaginator)
    """

    async def paginate(
        self,
        *,
        SortOrder: SortOrderType = ...,
        SortBy: UserProfileSortKeyType = ...,
        DomainIdEquals: str = ...,
        UserProfileNameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListUserProfiles.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listuserprofilespaginator)
        """


class ListWorkforcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkforces)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listworkforcespaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: ListWorkforcesSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkforcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkforces.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listworkforcespaginator)
        """


class ListWorkteamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkteams)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listworkteamspaginator)
    """

    async def paginate(
        self,
        *,
        SortBy: ListWorkteamsSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkteams.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#listworkteamspaginator)
        """


class SearchPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.Search)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#searchpaginator)
    """

    async def paginate(
        self,
        *,
        Resource: ResourceTypeType,
        SearchExpression: "SearchExpressionTypeDef" = ...,
        SortBy: str = ...,
        SortOrder: SearchSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.Search.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators.html#searchpaginator)
        """
