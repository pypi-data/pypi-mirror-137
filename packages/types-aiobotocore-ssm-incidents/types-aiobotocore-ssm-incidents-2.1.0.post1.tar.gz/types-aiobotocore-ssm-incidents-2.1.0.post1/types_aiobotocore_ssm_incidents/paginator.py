"""
Type annotations for ssm-incidents service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient
    from types_aiobotocore_ssm_incidents.paginator import (
        GetResourcePoliciesPaginator,
        ListIncidentRecordsPaginator,
        ListRelatedItemsPaginator,
        ListReplicationSetsPaginator,
        ListResponsePlansPaginator,
        ListTimelineEventsPaginator,
    )

    session = get_session()
    with session.create_client("ssm-incidents") as client:
        client: SSMIncidentsClient

        get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
        list_incident_records_paginator: ListIncidentRecordsPaginator = client.get_paginator("list_incident_records")
        list_related_items_paginator: ListRelatedItemsPaginator = client.get_paginator("list_related_items")
        list_replication_sets_paginator: ListReplicationSetsPaginator = client.get_paginator("list_replication_sets")
        list_response_plans_paginator: ListResponsePlansPaginator = client.get_paginator("list_response_plans")
        list_timeline_events_paginator: ListTimelineEventsPaginator = client.get_paginator("list_timeline_events")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import SortOrderType
from .type_defs import (
    FilterTypeDef,
    GetResourcePoliciesOutputTypeDef,
    ListIncidentRecordsOutputTypeDef,
    ListRelatedItemsOutputTypeDef,
    ListReplicationSetsOutputTypeDef,
    ListResponsePlansOutputTypeDef,
    ListTimelineEventsOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "GetResourcePoliciesPaginator",
    "ListIncidentRecordsPaginator",
    "ListRelatedItemsPaginator",
    "ListReplicationSetsPaginator",
    "ListResponsePlansPaginator",
    "ListTimelineEventsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetResourcePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.GetResourcePolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#getresourcepoliciespaginator)
    """

    async def paginate(
        self, *, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetResourcePoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.GetResourcePolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#getresourcepoliciespaginator)
        """


class ListIncidentRecordsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListIncidentRecords)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listincidentrecordspaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIncidentRecordsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListIncidentRecords.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listincidentrecordspaginator)
        """


class ListRelatedItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListRelatedItems)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listrelateditemspaginator)
    """

    async def paginate(
        self, *, incidentRecordArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRelatedItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListRelatedItems.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listrelateditemspaginator)
        """


class ListReplicationSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListReplicationSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listreplicationsetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListReplicationSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListReplicationSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listreplicationsetspaginator)
        """


class ListResponsePlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListResponsePlans)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listresponseplanspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResponsePlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListResponsePlans.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listresponseplanspaginator)
        """


class ListTimelineEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListTimelineEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listtimelineeventspaginator)
    """

    async def paginate(
        self,
        *,
        incidentRecordArn: str,
        filters: Sequence["FilterTypeDef"] = ...,
        sortBy: Literal["EVENT_TIME"] = ...,
        sortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTimelineEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Paginator.ListTimelineEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/paginators.html#listtimelineeventspaginator)
        """
