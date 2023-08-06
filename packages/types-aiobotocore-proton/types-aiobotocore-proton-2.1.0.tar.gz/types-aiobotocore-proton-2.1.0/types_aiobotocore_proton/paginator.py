"""
Type annotations for proton service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_proton.client import ProtonClient
    from types_aiobotocore_proton.paginator import (
        ListEnvironmentAccountConnectionsPaginator,
        ListEnvironmentOutputsPaginator,
        ListEnvironmentProvisionedResourcesPaginator,
        ListEnvironmentTemplateVersionsPaginator,
        ListEnvironmentTemplatesPaginator,
        ListEnvironmentsPaginator,
        ListRepositoriesPaginator,
        ListRepositorySyncDefinitionsPaginator,
        ListServiceInstanceOutputsPaginator,
        ListServiceInstanceProvisionedResourcesPaginator,
        ListServiceInstancesPaginator,
        ListServicePipelineOutputsPaginator,
        ListServicePipelineProvisionedResourcesPaginator,
        ListServiceTemplateVersionsPaginator,
        ListServiceTemplatesPaginator,
        ListServicesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("proton") as client:
        client: ProtonClient

        list_environment_account_connections_paginator: ListEnvironmentAccountConnectionsPaginator = client.get_paginator("list_environment_account_connections")
        list_environment_outputs_paginator: ListEnvironmentOutputsPaginator = client.get_paginator("list_environment_outputs")
        list_environment_provisioned_resources_paginator: ListEnvironmentProvisionedResourcesPaginator = client.get_paginator("list_environment_provisioned_resources")
        list_environment_template_versions_paginator: ListEnvironmentTemplateVersionsPaginator = client.get_paginator("list_environment_template_versions")
        list_environment_templates_paginator: ListEnvironmentTemplatesPaginator = client.get_paginator("list_environment_templates")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
        list_repository_sync_definitions_paginator: ListRepositorySyncDefinitionsPaginator = client.get_paginator("list_repository_sync_definitions")
        list_service_instance_outputs_paginator: ListServiceInstanceOutputsPaginator = client.get_paginator("list_service_instance_outputs")
        list_service_instance_provisioned_resources_paginator: ListServiceInstanceProvisionedResourcesPaginator = client.get_paginator("list_service_instance_provisioned_resources")
        list_service_instances_paginator: ListServiceInstancesPaginator = client.get_paginator("list_service_instances")
        list_service_pipeline_outputs_paginator: ListServicePipelineOutputsPaginator = client.get_paginator("list_service_pipeline_outputs")
        list_service_pipeline_provisioned_resources_paginator: ListServicePipelineProvisionedResourcesPaginator = client.get_paginator("list_service_pipeline_provisioned_resources")
        list_service_template_versions_paginator: ListServiceTemplateVersionsPaginator = client.get_paginator("list_service_template_versions")
        list_service_templates_paginator: ListServiceTemplatesPaginator = client.get_paginator("list_service_templates")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    RepositoryProviderType,
)
from .type_defs import (
    EnvironmentTemplateFilterTypeDef,
    ListEnvironmentAccountConnectionsOutputTypeDef,
    ListEnvironmentOutputsOutputTypeDef,
    ListEnvironmentProvisionedResourcesOutputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListEnvironmentTemplatesOutputTypeDef,
    ListEnvironmentTemplateVersionsOutputTypeDef,
    ListRepositoriesOutputTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListServiceInstanceOutputsOutputTypeDef,
    ListServiceInstanceProvisionedResourcesOutputTypeDef,
    ListServiceInstancesOutputTypeDef,
    ListServicePipelineOutputsOutputTypeDef,
    ListServicePipelineProvisionedResourcesOutputTypeDef,
    ListServicesOutputTypeDef,
    ListServiceTemplatesOutputTypeDef,
    ListServiceTemplateVersionsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListEnvironmentAccountConnectionsPaginator",
    "ListEnvironmentOutputsPaginator",
    "ListEnvironmentProvisionedResourcesPaginator",
    "ListEnvironmentTemplateVersionsPaginator",
    "ListEnvironmentTemplatesPaginator",
    "ListEnvironmentsPaginator",
    "ListRepositoriesPaginator",
    "ListRepositorySyncDefinitionsPaginator",
    "ListServiceInstanceOutputsPaginator",
    "ListServiceInstanceProvisionedResourcesPaginator",
    "ListServiceInstancesPaginator",
    "ListServicePipelineOutputsPaginator",
    "ListServicePipelineProvisionedResourcesPaginator",
    "ListServiceTemplateVersionsPaginator",
    "ListServiceTemplatesPaginator",
    "ListServicesPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEnvironmentAccountConnectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentAccountConnections)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentaccountconnectionspaginator)
    """

    async def paginate(
        self,
        *,
        requestedBy: EnvironmentAccountConnectionRequesterAccountTypeType,
        environmentName: str = ...,
        statuses: Sequence[EnvironmentAccountConnectionStatusType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentAccountConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentAccountConnections.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentaccountconnectionspaginator)
        """


class ListEnvironmentOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentOutputs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentoutputspaginator)
    """

    async def paginate(
        self, *, environmentName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentOutputs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentoutputspaginator)
        """


class ListEnvironmentProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentProvisionedResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentprovisionedresourcespaginator)
    """

    async def paginate(
        self, *, environmentName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentprovisionedresourcespaginator)
        """


class ListEnvironmentTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentTemplateVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmenttemplateversionspaginator)
    """

    async def paginate(
        self,
        *,
        templateName: str,
        majorVersion: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentTemplateVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentTemplateVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmenttemplateversionspaginator)
        """


class ListEnvironmentTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentTemplates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmenttemplatespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironmentTemplates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmenttemplatespaginator)
        """


class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentspaginator)
    """

    async def paginate(
        self,
        *,
        environmentTemplates: Sequence["EnvironmentTemplateFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listenvironmentspaginator)
        """


class ListRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListRepositories)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listrepositoriespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listrepositoriespaginator)
        """


class ListRepositorySyncDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListRepositorySyncDefinitions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listrepositorysyncdefinitionspaginator)
    """

    async def paginate(
        self,
        *,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        syncType: Literal["TEMPLATE_SYNC"],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRepositorySyncDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListRepositorySyncDefinitions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listrepositorysyncdefinitionspaginator)
        """


class ListServiceInstanceOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceInstanceOutputs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listserviceinstanceoutputspaginator)
    """

    async def paginate(
        self,
        *,
        serviceInstanceName: str,
        serviceName: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceInstanceOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceInstanceOutputs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listserviceinstanceoutputspaginator)
        """


class ListServiceInstanceProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceInstanceProvisionedResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listserviceinstanceprovisionedresourcespaginator)
    """

    async def paginate(
        self,
        *,
        serviceInstanceName: str,
        serviceName: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceInstanceProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceInstanceProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listserviceinstanceprovisionedresourcespaginator)
        """


class ListServiceInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listserviceinstancespaginator)
    """

    async def paginate(
        self, *, serviceName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listserviceinstancespaginator)
        """


class ListServicePipelineOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServicePipelineOutputs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicepipelineoutputspaginator)
    """

    async def paginate(
        self, *, serviceName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServicePipelineOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServicePipelineOutputs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicepipelineoutputspaginator)
        """


class ListServicePipelineProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServicePipelineProvisionedResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicepipelineprovisionedresourcespaginator)
    """

    async def paginate(
        self, *, serviceName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServicePipelineProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServicePipelineProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicepipelineprovisionedresourcespaginator)
        """


class ListServiceTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceTemplateVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicetemplateversionspaginator)
    """

    async def paginate(
        self,
        *,
        templateName: str,
        majorVersion: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceTemplateVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceTemplateVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicetemplateversionspaginator)
        """


class ListServiceTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceTemplates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicetemplatespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServiceTemplates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicetemplatespaginator)
        """


class ListServicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServices)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListServices.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listservicespaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listtagsforresourcepaginator)
    """

    async def paginate(
        self, *, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators.html#listtagsforresourcepaginator)
        """
