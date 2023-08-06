"""
Type annotations for devops-guru service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devops_guru.client import DevOpsGuruClient
    from types_aiobotocore_devops_guru.paginator import (
        DescribeOrganizationResourceCollectionHealthPaginator,
        DescribeResourceCollectionHealthPaginator,
        GetCostEstimationPaginator,
        GetResourceCollectionPaginator,
        ListAnomaliesForInsightPaginator,
        ListEventsPaginator,
        ListInsightsPaginator,
        ListNotificationChannelsPaginator,
        ListOrganizationInsightsPaginator,
        ListRecommendationsPaginator,
        SearchInsightsPaginator,
        SearchOrganizationInsightsPaginator,
    )

    session = get_session()
    with session.create_client("devops-guru") as client:
        client: DevOpsGuruClient

        describe_organization_resource_collection_health_paginator: DescribeOrganizationResourceCollectionHealthPaginator = client.get_paginator("describe_organization_resource_collection_health")
        describe_resource_collection_health_paginator: DescribeResourceCollectionHealthPaginator = client.get_paginator("describe_resource_collection_health")
        get_cost_estimation_paginator: GetCostEstimationPaginator = client.get_paginator("get_cost_estimation")
        get_resource_collection_paginator: GetResourceCollectionPaginator = client.get_paginator("get_resource_collection")
        list_anomalies_for_insight_paginator: ListAnomaliesForInsightPaginator = client.get_paginator("list_anomalies_for_insight")
        list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
        list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
        list_notification_channels_paginator: ListNotificationChannelsPaginator = client.get_paginator("list_notification_channels")
        list_organization_insights_paginator: ListOrganizationInsightsPaginator = client.get_paginator("list_organization_insights")
        list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
        search_insights_paginator: SearchInsightsPaginator = client.get_paginator("search_insights")
        search_organization_insights_paginator: SearchOrganizationInsightsPaginator = client.get_paginator("search_organization_insights")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    InsightTypeType,
    LocaleType,
    OrganizationResourceCollectionTypeType,
    ResourceCollectionTypeType,
)
from .type_defs import (
    DescribeOrganizationResourceCollectionHealthResponseTypeDef,
    DescribeResourceCollectionHealthResponseTypeDef,
    GetCostEstimationResponseTypeDef,
    GetResourceCollectionResponseTypeDef,
    ListAnomaliesForInsightResponseTypeDef,
    ListEventsFiltersTypeDef,
    ListEventsResponseTypeDef,
    ListInsightsResponseTypeDef,
    ListInsightsStatusFilterTypeDef,
    ListNotificationChannelsResponseTypeDef,
    ListOrganizationInsightsResponseTypeDef,
    ListRecommendationsResponseTypeDef,
    PaginatorConfigTypeDef,
    SearchInsightsFiltersTypeDef,
    SearchInsightsResponseTypeDef,
    SearchOrganizationInsightsFiltersTypeDef,
    SearchOrganizationInsightsResponseTypeDef,
    StartTimeRangeTypeDef,
)

__all__ = (
    "DescribeOrganizationResourceCollectionHealthPaginator",
    "DescribeResourceCollectionHealthPaginator",
    "GetCostEstimationPaginator",
    "GetResourceCollectionPaginator",
    "ListAnomaliesForInsightPaginator",
    "ListEventsPaginator",
    "ListInsightsPaginator",
    "ListNotificationChannelsPaginator",
    "ListOrganizationInsightsPaginator",
    "ListRecommendationsPaginator",
    "SearchInsightsPaginator",
    "SearchOrganizationInsightsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeOrganizationResourceCollectionHealthPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#describeorganizationresourcecollectionhealthpaginator)
    """

    async def paginate(
        self,
        *,
        OrganizationResourceCollectionType: OrganizationResourceCollectionTypeType,
        AccountIds: Sequence[str] = ...,
        OrganizationalUnitIds: Sequence[str] = ...,
        MaxResults: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOrganizationResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#describeorganizationresourcecollectionhealthpaginator)
        """


class DescribeResourceCollectionHealthPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#describeresourcecollectionhealthpaginator)
    """

    async def paginate(
        self,
        *,
        ResourceCollectionType: ResourceCollectionTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#describeresourcecollectionhealthpaginator)
        """


class GetCostEstimationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.GetCostEstimation)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#getcostestimationpaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetCostEstimationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.GetCostEstimation.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#getcostestimationpaginator)
        """


class GetResourceCollectionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.GetResourceCollection)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#getresourcecollectionpaginator)
    """

    async def paginate(
        self,
        *,
        ResourceCollectionType: ResourceCollectionTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetResourceCollectionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.GetResourceCollection.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#getresourcecollectionpaginator)
        """


class ListAnomaliesForInsightPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListAnomaliesForInsight)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listanomaliesforinsightpaginator)
    """

    async def paginate(
        self,
        *,
        InsightId: str,
        StartTimeRange: "StartTimeRangeTypeDef" = ...,
        AccountId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAnomaliesForInsightResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListAnomaliesForInsight.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listanomaliesforinsightpaginator)
        """


class ListEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listeventspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: "ListEventsFiltersTypeDef",
        AccountId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listeventspaginator)
        """


class ListInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListInsights)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listinsightspaginator)
    """

    async def paginate(
        self,
        *,
        StatusFilter: "ListInsightsStatusFilterTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListInsights.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listinsightspaginator)
        """


class ListNotificationChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListNotificationChannels)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listnotificationchannelspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNotificationChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListNotificationChannels.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listnotificationchannelspaginator)
        """


class ListOrganizationInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListOrganizationInsights)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listorganizationinsightspaginator)
    """

    async def paginate(
        self,
        *,
        StatusFilter: "ListInsightsStatusFilterTypeDef",
        AccountIds: Sequence[str] = ...,
        OrganizationalUnitIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListOrganizationInsights.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listorganizationinsightspaginator)
        """


class ListRecommendationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListRecommendations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listrecommendationspaginator)
    """

    async def paginate(
        self,
        *,
        InsightId: str,
        Locale: LocaleType = ...,
        AccountId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.ListRecommendations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#listrecommendationspaginator)
        """


class SearchInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.SearchInsights)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#searchinsightspaginator)
    """

    async def paginate(
        self,
        *,
        StartTimeRange: "StartTimeRangeTypeDef",
        Type: InsightTypeType,
        Filters: "SearchInsightsFiltersTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.SearchInsights.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#searchinsightspaginator)
        """


class SearchOrganizationInsightsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.SearchOrganizationInsights)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#searchorganizationinsightspaginator)
    """

    async def paginate(
        self,
        *,
        AccountIds: Sequence[str],
        StartTimeRange: "StartTimeRangeTypeDef",
        Type: InsightTypeType,
        Filters: "SearchOrganizationInsightsFiltersTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Paginator.SearchOrganizationInsights.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators.html#searchorganizationinsightspaginator)
        """
