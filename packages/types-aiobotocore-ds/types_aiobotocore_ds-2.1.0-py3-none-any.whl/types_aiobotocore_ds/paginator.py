"""
Type annotations for ds service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ds.client import DirectoryServiceClient
    from types_aiobotocore_ds.paginator import (
        DescribeDirectoriesPaginator,
        DescribeDomainControllersPaginator,
        DescribeSharedDirectoriesPaginator,
        DescribeSnapshotsPaginator,
        DescribeTrustsPaginator,
        ListIpRoutesPaginator,
        ListLogSubscriptionsPaginator,
        ListSchemaExtensionsPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("ds") as client:
        client: DirectoryServiceClient

        describe_directories_paginator: DescribeDirectoriesPaginator = client.get_paginator("describe_directories")
        describe_domain_controllers_paginator: DescribeDomainControllersPaginator = client.get_paginator("describe_domain_controllers")
        describe_shared_directories_paginator: DescribeSharedDirectoriesPaginator = client.get_paginator("describe_shared_directories")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_trusts_paginator: DescribeTrustsPaginator = client.get_paginator("describe_trusts")
        list_ip_routes_paginator: ListIpRoutesPaginator = client.get_paginator("list_ip_routes")
        list_log_subscriptions_paginator: ListLogSubscriptionsPaginator = client.get_paginator("list_log_subscriptions")
        list_schema_extensions_paginator: ListSchemaExtensionsPaginator = client.get_paginator("list_schema_extensions")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeDirectoriesResultTypeDef,
    DescribeDomainControllersResultTypeDef,
    DescribeSharedDirectoriesResultTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeTrustsResultTypeDef,
    ListIpRoutesResultTypeDef,
    ListLogSubscriptionsResultTypeDef,
    ListSchemaExtensionsResultTypeDef,
    ListTagsForResourceResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeDirectoriesPaginator",
    "DescribeDomainControllersPaginator",
    "DescribeSharedDirectoriesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeTrustsPaginator",
    "ListIpRoutesPaginator",
    "ListLogSubscriptionsPaginator",
    "ListSchemaExtensionsPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeDirectoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeDirectories)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describedirectoriespaginator)
    """

    async def paginate(
        self, *, DirectoryIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeDirectories.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describedirectoriespaginator)
        """


class DescribeDomainControllersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeDomainControllers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describedomaincontrollerspaginator)
    """

    async def paginate(
        self,
        *,
        DirectoryId: str,
        DomainControllerIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDomainControllersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeDomainControllers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describedomaincontrollerspaginator)
        """


class DescribeSharedDirectoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeSharedDirectories)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describeshareddirectoriespaginator)
    """

    async def paginate(
        self,
        *,
        OwnerDirectoryId: str,
        SharedDirectoryIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSharedDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeSharedDirectories.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describeshareddirectoriespaginator)
        """


class DescribeSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeSnapshots)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describesnapshotspaginator)
    """

    async def paginate(
        self,
        *,
        DirectoryId: str = ...,
        SnapshotIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describesnapshotspaginator)
        """


class DescribeTrustsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeTrusts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describetrustspaginator)
    """

    async def paginate(
        self,
        *,
        DirectoryId: str = ...,
        TrustIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTrustsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.DescribeTrusts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#describetrustspaginator)
        """


class ListIpRoutesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListIpRoutes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listiproutespaginator)
    """

    async def paginate(
        self, *, DirectoryId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIpRoutesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListIpRoutes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listiproutespaginator)
        """


class ListLogSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListLogSubscriptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listlogsubscriptionspaginator)
    """

    async def paginate(
        self, *, DirectoryId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLogSubscriptionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListLogSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listlogsubscriptionspaginator)
        """


class ListSchemaExtensionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListSchemaExtensions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listschemaextensionspaginator)
    """

    async def paginate(
        self, *, DirectoryId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSchemaExtensionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListSchemaExtensions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listschemaextensionspaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listtagsforresourcepaginator)
    """

    async def paginate(
        self, *, ResourceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators.html#listtagsforresourcepaginator)
        """
