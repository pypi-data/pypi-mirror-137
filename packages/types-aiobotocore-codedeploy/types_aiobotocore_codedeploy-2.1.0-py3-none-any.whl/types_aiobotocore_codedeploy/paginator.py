"""
Type annotations for codedeploy service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codedeploy.client import CodeDeployClient
    from types_aiobotocore_codedeploy.paginator import (
        ListApplicationRevisionsPaginator,
        ListApplicationsPaginator,
        ListDeploymentConfigsPaginator,
        ListDeploymentGroupsPaginator,
        ListDeploymentInstancesPaginator,
        ListDeploymentTargetsPaginator,
        ListDeploymentsPaginator,
        ListGitHubAccountTokenNamesPaginator,
        ListOnPremisesInstancesPaginator,
    )

    session = get_session()
    with session.create_client("codedeploy") as client:
        client: CodeDeployClient

        list_application_revisions_paginator: ListApplicationRevisionsPaginator = client.get_paginator("list_application_revisions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_deployment_configs_paginator: ListDeploymentConfigsPaginator = client.get_paginator("list_deployment_configs")
        list_deployment_groups_paginator: ListDeploymentGroupsPaginator = client.get_paginator("list_deployment_groups")
        list_deployment_instances_paginator: ListDeploymentInstancesPaginator = client.get_paginator("list_deployment_instances")
        list_deployment_targets_paginator: ListDeploymentTargetsPaginator = client.get_paginator("list_deployment_targets")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_git_hub_account_token_names_paginator: ListGitHubAccountTokenNamesPaginator = client.get_paginator("list_git_hub_account_token_names")
        list_on_premises_instances_paginator: ListOnPremisesInstancesPaginator = client.get_paginator("list_on_premises_instances")
    ```
"""
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    ApplicationRevisionSortByType,
    DeploymentStatusType,
    InstanceStatusType,
    InstanceTypeType,
    ListStateFilterActionType,
    RegistrationStatusType,
    SortOrderType,
    TargetFilterNameType,
)
from .type_defs import (
    ListApplicationRevisionsOutputTypeDef,
    ListApplicationsOutputTypeDef,
    ListDeploymentConfigsOutputTypeDef,
    ListDeploymentGroupsOutputTypeDef,
    ListDeploymentInstancesOutputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListDeploymentTargetsOutputTypeDef,
    ListGitHubAccountTokenNamesOutputTypeDef,
    ListOnPremisesInstancesOutputTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
    TimeRangeTypeDef,
)

__all__ = (
    "ListApplicationRevisionsPaginator",
    "ListApplicationsPaginator",
    "ListDeploymentConfigsPaginator",
    "ListDeploymentGroupsPaginator",
    "ListDeploymentInstancesPaginator",
    "ListDeploymentTargetsPaginator",
    "ListDeploymentsPaginator",
    "ListGitHubAccountTokenNamesPaginator",
    "ListOnPremisesInstancesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplicationRevisions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listapplicationrevisionspaginator)
    """

    async def paginate(
        self,
        *,
        applicationName: str,
        sortBy: ApplicationRevisionSortByType = ...,
        sortOrder: SortOrderType = ...,
        s3Bucket: str = ...,
        s3KeyPrefix: str = ...,
        deployed: ListStateFilterActionType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplicationRevisions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listapplicationrevisionspaginator)
        """


class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listapplicationspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listapplicationspaginator)
        """


class ListDeploymentConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentConfigs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentconfigspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentConfigs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentconfigspaginator)
        """


class ListDeploymentGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentgroupspaginator)
    """

    async def paginate(
        self, *, applicationName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentgroupspaginator)
        """


class ListDeploymentInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentinstancespaginator)
    """

    async def paginate(
        self,
        *,
        deploymentId: str,
        instanceStatusFilter: Sequence[InstanceStatusType] = ...,
        instanceTypeFilter: Sequence[InstanceTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentinstancespaginator)
        """


class ListDeploymentTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentTargets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymenttargetspaginator)
    """

    async def paginate(
        self,
        *,
        deploymentId: str = ...,
        targetFilters: Mapping[TargetFilterNameType, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeploymentTargets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymenttargetspaginator)
        """


class ListDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeployments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentspaginator)
    """

    async def paginate(
        self,
        *,
        applicationName: str = ...,
        deploymentGroupName: str = ...,
        externalId: str = ...,
        includeOnlyStatuses: Sequence[DeploymentStatusType] = ...,
        createTimeRange: "TimeRangeTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listdeploymentspaginator)
        """


class ListGitHubAccountTokenNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listgithubaccounttokennamespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGitHubAccountTokenNamesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listgithubaccounttokennamespaginator)
        """


class ListOnPremisesInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListOnPremisesInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listonpremisesinstancespaginator)
    """

    async def paginate(
        self,
        *,
        registrationStatus: RegistrationStatusType = ...,
        tagFilters: Sequence["TagFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOnPremisesInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Paginator.ListOnPremisesInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators.html#listonpremisesinstancespaginator)
        """
