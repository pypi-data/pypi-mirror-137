"""
Type annotations for macie2 service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_macie2.client import Macie2Client
    from types_aiobotocore_macie2.paginator import (
        DescribeBucketsPaginator,
        GetUsageStatisticsPaginator,
        ListClassificationJobsPaginator,
        ListCustomDataIdentifiersPaginator,
        ListFindingsPaginator,
        ListFindingsFiltersPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("macie2") as client:
        client: Macie2Client

        describe_buckets_paginator: DescribeBucketsPaginator = client.get_paginator("describe_buckets")
        get_usage_statistics_paginator: GetUsageStatisticsPaginator = client.get_paginator("get_usage_statistics")
        list_classification_jobs_paginator: ListClassificationJobsPaginator = client.get_paginator("list_classification_jobs")
        list_custom_data_identifiers_paginator: ListCustomDataIdentifiersPaginator = client.get_paginator("list_custom_data_identifiers")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_findings_filters_paginator: ListFindingsFiltersPaginator = client.get_paginator("list_findings_filters")
        list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import TimeRangeType
from .type_defs import (
    BucketCriteriaAdditionalPropertiesTypeDef,
    BucketSortCriteriaTypeDef,
    DescribeBucketsResponseTypeDef,
    FindingCriteriaTypeDef,
    GetUsageStatisticsResponseTypeDef,
    ListClassificationJobsResponseTypeDef,
    ListCustomDataIdentifiersResponseTypeDef,
    ListFindingsFiltersResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsResponseTypeDef,
    ListJobsFilterCriteriaTypeDef,
    ListJobsSortCriteriaTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    PaginatorConfigTypeDef,
    SearchResourcesBucketCriteriaTypeDef,
    SearchResourcesResponseTypeDef,
    SearchResourcesSortCriteriaTypeDef,
    SortCriteriaTypeDef,
    UsageStatisticsFilterTypeDef,
    UsageStatisticsSortByTypeDef,
)

__all__ = (
    "DescribeBucketsPaginator",
    "GetUsageStatisticsPaginator",
    "ListClassificationJobsPaginator",
    "ListCustomDataIdentifiersPaginator",
    "ListFindingsPaginator",
    "ListFindingsFiltersPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "SearchResourcesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeBucketsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.DescribeBuckets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#describebucketspaginator)
    """

    async def paginate(
        self,
        *,
        criteria: Mapping[str, "BucketCriteriaAdditionalPropertiesTypeDef"] = ...,
        sortCriteria: "BucketSortCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBucketsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.DescribeBuckets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#describebucketspaginator)
        """


class GetUsageStatisticsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.GetUsageStatistics)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#getusagestatisticspaginator)
    """

    async def paginate(
        self,
        *,
        filterBy: Sequence["UsageStatisticsFilterTypeDef"] = ...,
        sortBy: "UsageStatisticsSortByTypeDef" = ...,
        timeRange: TimeRangeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetUsageStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.GetUsageStatistics.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#getusagestatisticspaginator)
        """


class ListClassificationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListClassificationJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listclassificationjobspaginator)
    """

    async def paginate(
        self,
        *,
        filterCriteria: "ListJobsFilterCriteriaTypeDef" = ...,
        sortCriteria: "ListJobsSortCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListClassificationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListClassificationJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listclassificationjobspaginator)
        """


class ListCustomDataIdentifiersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListCustomDataIdentifiers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listcustomdataidentifierspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomDataIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListCustomDataIdentifiers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listcustomdataidentifierspaginator)
        """


class ListFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListFindings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listfindingspaginator)
    """

    async def paginate(
        self,
        *,
        findingCriteria: "FindingCriteriaTypeDef" = ...,
        sortCriteria: "SortCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListFindings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listfindingspaginator)
        """


class ListFindingsFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListFindingsFilters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listfindingsfilterspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFindingsFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListFindingsFilters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listfindingsfilterspaginator)
        """


class ListInvitationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListInvitations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listinvitationspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListInvitations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listinvitationspaginator)
        """


class ListMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListMembers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listmemberspaginator)
    """

    async def paginate(
        self, *, onlyAssociated: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListMembers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listmemberspaginator)
        """


class ListOrganizationAdminAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListOrganizationAdminAccounts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listorganizationadminaccountspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#listorganizationadminaccountspaginator)
        """


class SearchResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.SearchResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#searchresourcespaginator)
    """

    async def paginate(
        self,
        *,
        bucketCriteria: "SearchResourcesBucketCriteriaTypeDef" = ...,
        sortCriteria: "SearchResourcesSortCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Paginator.SearchResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators.html#searchresourcespaginator)
        """
