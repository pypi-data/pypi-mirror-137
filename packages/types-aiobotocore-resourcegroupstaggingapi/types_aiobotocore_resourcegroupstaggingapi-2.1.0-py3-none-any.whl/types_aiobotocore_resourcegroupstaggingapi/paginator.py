"""
Type annotations for resourcegroupstaggingapi service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient
    from types_aiobotocore_resourcegroupstaggingapi.paginator import (
        GetComplianceSummaryPaginator,
        GetResourcesPaginator,
        GetTagKeysPaginator,
        GetTagValuesPaginator,
    )

    session = get_session()
    with session.create_client("resourcegroupstaggingapi") as client:
        client: ResourceGroupsTaggingAPIClient

        get_compliance_summary_paginator: GetComplianceSummaryPaginator = client.get_paginator("get_compliance_summary")
        get_resources_paginator: GetResourcesPaginator = client.get_paginator("get_resources")
        get_tag_keys_paginator: GetTagKeysPaginator = client.get_paginator("get_tag_keys")
        get_tag_values_paginator: GetTagValuesPaginator = client.get_paginator("get_tag_values")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import GroupByAttributeType
from .type_defs import (
    GetComplianceSummaryOutputTypeDef,
    GetResourcesOutputTypeDef,
    GetTagKeysOutputTypeDef,
    GetTagValuesOutputTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
)

__all__ = (
    "GetComplianceSummaryPaginator",
    "GetResourcesPaginator",
    "GetTagKeysPaginator",
    "GetTagValuesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetComplianceSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetComplianceSummary)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#getcompliancesummarypaginator)
    """

    async def paginate(
        self,
        *,
        TargetIdFilters: Sequence[str] = ...,
        RegionFilters: Sequence[str] = ...,
        ResourceTypeFilters: Sequence[str] = ...,
        TagKeyFilters: Sequence[str] = ...,
        GroupBy: Sequence[GroupByAttributeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetComplianceSummaryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetComplianceSummary.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#getcompliancesummarypaginator)
        """


class GetResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#getresourcespaginator)
    """

    async def paginate(
        self,
        *,
        TagFilters: Sequence["TagFilterTypeDef"] = ...,
        TagsPerPage: int = ...,
        ResourceTypeFilters: Sequence[str] = ...,
        IncludeComplianceDetails: bool = ...,
        ExcludeCompliantResources: bool = ...,
        ResourceARNList: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#getresourcespaginator)
        """


class GetTagKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetTagKeys)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#gettagkeyspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTagKeysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetTagKeys.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#gettagkeyspaginator)
        """


class GetTagValuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetTagValues)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#gettagvaluespaginator)
    """

    async def paginate(
        self, *, Key: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTagValuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Paginator.GetTagValues.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators.html#gettagvaluespaginator)
        """
