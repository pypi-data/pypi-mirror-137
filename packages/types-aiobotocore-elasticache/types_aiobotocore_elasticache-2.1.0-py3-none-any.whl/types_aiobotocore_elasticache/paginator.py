"""
Type annotations for elasticache service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elasticache.client import ElastiCacheClient
    from types_aiobotocore_elasticache.paginator import (
        DescribeCacheClustersPaginator,
        DescribeCacheEngineVersionsPaginator,
        DescribeCacheParameterGroupsPaginator,
        DescribeCacheParametersPaginator,
        DescribeCacheSecurityGroupsPaginator,
        DescribeCacheSubnetGroupsPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeGlobalReplicationGroupsPaginator,
        DescribeReplicationGroupsPaginator,
        DescribeReservedCacheNodesPaginator,
        DescribeReservedCacheNodesOfferingsPaginator,
        DescribeServiceUpdatesPaginator,
        DescribeSnapshotsPaginator,
        DescribeUpdateActionsPaginator,
        DescribeUserGroupsPaginator,
        DescribeUsersPaginator,
    )

    session = get_session()
    with session.create_client("elasticache") as client:
        client: ElastiCacheClient

        describe_cache_clusters_paginator: DescribeCacheClustersPaginator = client.get_paginator("describe_cache_clusters")
        describe_cache_engine_versions_paginator: DescribeCacheEngineVersionsPaginator = client.get_paginator("describe_cache_engine_versions")
        describe_cache_parameter_groups_paginator: DescribeCacheParameterGroupsPaginator = client.get_paginator("describe_cache_parameter_groups")
        describe_cache_parameters_paginator: DescribeCacheParametersPaginator = client.get_paginator("describe_cache_parameters")
        describe_cache_security_groups_paginator: DescribeCacheSecurityGroupsPaginator = client.get_paginator("describe_cache_security_groups")
        describe_cache_subnet_groups_paginator: DescribeCacheSubnetGroupsPaginator = client.get_paginator("describe_cache_subnet_groups")
        describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_global_replication_groups_paginator: DescribeGlobalReplicationGroupsPaginator = client.get_paginator("describe_global_replication_groups")
        describe_replication_groups_paginator: DescribeReplicationGroupsPaginator = client.get_paginator("describe_replication_groups")
        describe_reserved_cache_nodes_paginator: DescribeReservedCacheNodesPaginator = client.get_paginator("describe_reserved_cache_nodes")
        describe_reserved_cache_nodes_offerings_paginator: DescribeReservedCacheNodesOfferingsPaginator = client.get_paginator("describe_reserved_cache_nodes_offerings")
        describe_service_updates_paginator: DescribeServiceUpdatesPaginator = client.get_paginator("describe_service_updates")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_update_actions_paginator: DescribeUpdateActionsPaginator = client.get_paginator("describe_update_actions")
        describe_user_groups_paginator: DescribeUserGroupsPaginator = client.get_paginator("describe_user_groups")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ServiceUpdateStatusType, SourceTypeType, UpdateActionStatusType
from .type_defs import (
    CacheClusterMessageTypeDef,
    CacheEngineVersionMessageTypeDef,
    CacheParameterGroupDetailsTypeDef,
    CacheParameterGroupsMessageTypeDef,
    CacheSecurityGroupMessageTypeDef,
    CacheSubnetGroupMessageTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeGlobalReplicationGroupsResultTypeDef,
    DescribeSnapshotsListMessageTypeDef,
    DescribeUserGroupsResultTypeDef,
    DescribeUsersResultTypeDef,
    EventsMessageTypeDef,
    FilterTypeDef,
    PaginatorConfigTypeDef,
    ReplicationGroupMessageTypeDef,
    ReservedCacheNodeMessageTypeDef,
    ReservedCacheNodesOfferingMessageTypeDef,
    ServiceUpdatesMessageTypeDef,
    TimeRangeFilterTypeDef,
    UpdateActionsMessageTypeDef,
)

__all__ = (
    "DescribeCacheClustersPaginator",
    "DescribeCacheEngineVersionsPaginator",
    "DescribeCacheParameterGroupsPaginator",
    "DescribeCacheParametersPaginator",
    "DescribeCacheSecurityGroupsPaginator",
    "DescribeCacheSubnetGroupsPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalReplicationGroupsPaginator",
    "DescribeReplicationGroupsPaginator",
    "DescribeReservedCacheNodesPaginator",
    "DescribeReservedCacheNodesOfferingsPaginator",
    "DescribeServiceUpdatesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeUpdateActionsPaginator",
    "DescribeUserGroupsPaginator",
    "DescribeUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCacheClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheClusters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheclusterspaginator)
    """

    async def paginate(
        self,
        *,
        CacheClusterId: str = ...,
        ShowCacheNodeInfo: bool = ...,
        ShowCacheClustersNotInReplicationGroups: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CacheClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheClusters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheclusterspaginator)
        """


class DescribeCacheEngineVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheEngineVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheengineversionspaginator)
    """

    async def paginate(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        CacheParameterGroupFamily: str = ...,
        DefaultOnly: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CacheEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheEngineVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheengineversionspaginator)
        """


class DescribeCacheParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheParameterGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheparametergroupspaginator)
    """

    async def paginate(
        self, *, CacheParameterGroupName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CacheParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheparametergroupspaginator)
        """


class DescribeCacheParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheParameters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheparameterspaginator)
    """

    async def paginate(
        self,
        *,
        CacheParameterGroupName: str,
        Source: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CacheParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheParameters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecacheparameterspaginator)
        """


class DescribeCacheSecurityGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheSecurityGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecachesecuritygroupspaginator)
    """

    async def paginate(
        self, *, CacheSecurityGroupName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CacheSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheSecurityGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecachesecuritygroupspaginator)
        """


class DescribeCacheSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheSubnetGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecachesubnetgroupspaginator)
    """

    async def paginate(
        self, *, CacheSubnetGroupName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CacheSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheSubnetGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describecachesubnetgroupspaginator)
        """


class DescribeEngineDefaultParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeEngineDefaultParameters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeenginedefaultparameterspaginator)
    """

    async def paginate(
        self, *, CacheParameterGroupFamily: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeenginedefaultparameterspaginator)
        """


class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeeventspaginator)
    """

    async def paginate(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeeventspaginator)
        """


class DescribeGlobalReplicationGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeglobalreplicationgroupspaginator)
    """

    async def paginate(
        self,
        *,
        GlobalReplicationGroupId: str = ...,
        ShowMemberInfo: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeGlobalReplicationGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeglobalreplicationgroupspaginator)
        """


class DescribeReplicationGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReplicationGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describereplicationgroupspaginator)
    """

    async def paginate(
        self, *, ReplicationGroupId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ReplicationGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReplicationGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describereplicationgroupspaginator)
        """


class DescribeReservedCacheNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReservedCacheNodes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describereservedcachenodespaginator)
    """

    async def paginate(
        self,
        *,
        ReservedCacheNodeId: str = ...,
        ReservedCacheNodesOfferingId: str = ...,
        CacheNodeType: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ReservedCacheNodeMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReservedCacheNodes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describereservedcachenodespaginator)
        """


class DescribeReservedCacheNodesOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describereservedcachenodesofferingspaginator)
    """

    async def paginate(
        self,
        *,
        ReservedCacheNodesOfferingId: str = ...,
        CacheNodeType: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ReservedCacheNodesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describereservedcachenodesofferingspaginator)
        """


class DescribeServiceUpdatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeServiceUpdates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeserviceupdatespaginator)
    """

    async def paginate(
        self,
        *,
        ServiceUpdateName: str = ...,
        ServiceUpdateStatus: Sequence[ServiceUpdateStatusType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ServiceUpdatesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeServiceUpdates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeserviceupdatespaginator)
        """


class DescribeSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeSnapshots)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describesnapshotspaginator)
    """

    async def paginate(
        self,
        *,
        ReplicationGroupId: str = ...,
        CacheClusterId: str = ...,
        SnapshotName: str = ...,
        SnapshotSource: str = ...,
        ShowNodeGroupConfig: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSnapshotsListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describesnapshotspaginator)
        """


class DescribeUpdateActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeUpdateActions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeupdateactionspaginator)
    """

    async def paginate(
        self,
        *,
        ServiceUpdateName: str = ...,
        ReplicationGroupIds: Sequence[str] = ...,
        CacheClusterIds: Sequence[str] = ...,
        Engine: str = ...,
        ServiceUpdateStatus: Sequence[ServiceUpdateStatusType] = ...,
        ServiceUpdateTimeRange: "TimeRangeFilterTypeDef" = ...,
        UpdateActionStatus: Sequence[UpdateActionStatusType] = ...,
        ShowNodeLevelUpdateStatus: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[UpdateActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeUpdateActions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeupdateactionspaginator)
        """


class DescribeUserGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeUserGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeusergroupspaginator)
    """

    async def paginate(
        self, *, UserGroupId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeUserGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeUserGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeusergroupspaginator)
        """


class DescribeUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeUsers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeuserspaginator)
    """

    async def paginate(
        self,
        *,
        Engine: str = ...,
        UserId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators.html#describeuserspaginator)
        """
