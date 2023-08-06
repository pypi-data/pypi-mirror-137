"""
Type annotations for iotthingsgraph service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotthingsgraph.client import IoTThingsGraphClient
    from types_aiobotocore_iotthingsgraph.paginator import (
        GetFlowTemplateRevisionsPaginator,
        GetSystemTemplateRevisionsPaginator,
        ListFlowExecutionMessagesPaginator,
        ListTagsForResourcePaginator,
        SearchEntitiesPaginator,
        SearchFlowExecutionsPaginator,
        SearchFlowTemplatesPaginator,
        SearchSystemInstancesPaginator,
        SearchSystemTemplatesPaginator,
        SearchThingsPaginator,
    )

    session = get_session()
    with session.create_client("iotthingsgraph") as client:
        client: IoTThingsGraphClient

        get_flow_template_revisions_paginator: GetFlowTemplateRevisionsPaginator = client.get_paginator("get_flow_template_revisions")
        get_system_template_revisions_paginator: GetSystemTemplateRevisionsPaginator = client.get_paginator("get_system_template_revisions")
        list_flow_execution_messages_paginator: ListFlowExecutionMessagesPaginator = client.get_paginator("list_flow_execution_messages")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        search_entities_paginator: SearchEntitiesPaginator = client.get_paginator("search_entities")
        search_flow_executions_paginator: SearchFlowExecutionsPaginator = client.get_paginator("search_flow_executions")
        search_flow_templates_paginator: SearchFlowTemplatesPaginator = client.get_paginator("search_flow_templates")
        search_system_instances_paginator: SearchSystemInstancesPaginator = client.get_paginator("search_system_instances")
        search_system_templates_paginator: SearchSystemTemplatesPaginator = client.get_paginator("search_system_templates")
        search_things_paginator: SearchThingsPaginator = client.get_paginator("search_things")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import EntityTypeType
from .type_defs import (
    EntityFilterTypeDef,
    FlowTemplateFilterTypeDef,
    GetFlowTemplateRevisionsResponseTypeDef,
    GetSystemTemplateRevisionsResponseTypeDef,
    ListFlowExecutionMessagesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PaginatorConfigTypeDef,
    SearchEntitiesResponseTypeDef,
    SearchFlowExecutionsResponseTypeDef,
    SearchFlowTemplatesResponseTypeDef,
    SearchSystemInstancesResponseTypeDef,
    SearchSystemTemplatesResponseTypeDef,
    SearchThingsResponseTypeDef,
    SystemInstanceFilterTypeDef,
    SystemTemplateFilterTypeDef,
)

__all__ = (
    "GetFlowTemplateRevisionsPaginator",
    "GetSystemTemplateRevisionsPaginator",
    "ListFlowExecutionMessagesPaginator",
    "ListTagsForResourcePaginator",
    "SearchEntitiesPaginator",
    "SearchFlowExecutionsPaginator",
    "SearchFlowTemplatesPaginator",
    "SearchSystemInstancesPaginator",
    "SearchSystemTemplatesPaginator",
    "SearchThingsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetFlowTemplateRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#getflowtemplaterevisionspaginator)
    """

    async def paginate(
        self, *, id: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetFlowTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#getflowtemplaterevisionspaginator)
        """


class GetSystemTemplateRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#getsystemtemplaterevisionspaginator)
    """

    async def paginate(
        self, *, id: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSystemTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#getsystemtemplaterevisionspaginator)
        """


class ListFlowExecutionMessagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#listflowexecutionmessagespaginator)
    """

    async def paginate(
        self, *, flowExecutionId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFlowExecutionMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#listflowexecutionmessagespaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#listtagsforresourcepaginator)
    """

    async def paginate(
        self, *, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#listtagsforresourcepaginator)
        """


class SearchEntitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchEntities)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchentitiespaginator)
    """

    async def paginate(
        self,
        *,
        entityTypes: Sequence[EntityTypeType],
        filters: Sequence["EntityFilterTypeDef"] = ...,
        namespaceVersion: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchEntities.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchentitiespaginator)
        """


class SearchFlowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchFlowExecutions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchflowexecutionspaginator)
    """

    async def paginate(
        self,
        *,
        systemInstanceId: str,
        flowExecutionId: str = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchFlowExecutions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchflowexecutionspaginator)
        """


class SearchFlowTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchFlowTemplates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchflowtemplatespaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["FlowTemplateFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchFlowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchFlowTemplates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchflowtemplatespaginator)
        """


class SearchSystemInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchSystemInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchsysteminstancespaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["SystemInstanceFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchSystemInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchSystemInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchsysteminstancespaginator)
        """


class SearchSystemTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchSystemTemplates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchsystemtemplatespaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["SystemTemplateFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchSystemTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchSystemTemplates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchsystemtemplatespaginator)
        """


class SearchThingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchThings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchthingspaginator)
    """

    async def paginate(
        self,
        *,
        entityId: str,
        namespaceVersion: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Paginator.SearchThings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators.html#searchthingspaginator)
        """
