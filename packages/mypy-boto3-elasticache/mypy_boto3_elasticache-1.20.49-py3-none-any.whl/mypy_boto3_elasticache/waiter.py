"""
Type annotations for elasticache service client waiters.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elasticache.client import ElastiCacheClient
    from mypy_boto3_elasticache.waiter import (
        CacheClusterAvailableWaiter,
        CacheClusterDeletedWaiter,
        ReplicationGroupAvailableWaiter,
        ReplicationGroupDeletedWaiter,
    )

    session = Session()
    client: ElastiCacheClient = session.client("elasticache")

    cache_cluster_available_waiter: CacheClusterAvailableWaiter = client.get_waiter("cache_cluster_available")
    cache_cluster_deleted_waiter: CacheClusterDeletedWaiter = client.get_waiter("cache_cluster_deleted")
    replication_group_available_waiter: ReplicationGroupAvailableWaiter = client.get_waiter("replication_group_available")
    replication_group_deleted_waiter: ReplicationGroupDeletedWaiter = client.get_waiter("replication_group_deleted")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "CacheClusterAvailableWaiter",
    "CacheClusterDeletedWaiter",
    "ReplicationGroupAvailableWaiter",
    "ReplicationGroupDeletedWaiter",
)


class CacheClusterAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.CacheClusterAvailable)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#cacheclusteravailablewaiter)
    """

    def wait(
        self,
        *,
        CacheClusterId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        ShowCacheNodeInfo: bool = ...,
        ShowCacheClustersNotInReplicationGroups: bool = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.CacheClusterAvailable.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#cacheclusteravailablewaiter)
        """


class CacheClusterDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.CacheClusterDeleted)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#cacheclusterdeletedwaiter)
    """

    def wait(
        self,
        *,
        CacheClusterId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        ShowCacheNodeInfo: bool = ...,
        ShowCacheClustersNotInReplicationGroups: bool = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.CacheClusterDeleted.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#cacheclusterdeletedwaiter)
        """


class ReplicationGroupAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.ReplicationGroupAvailable)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#replicationgroupavailablewaiter)
    """

    def wait(
        self,
        *,
        ReplicationGroupId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.ReplicationGroupAvailable.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#replicationgroupavailablewaiter)
        """


class ReplicationGroupDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.ReplicationGroupDeleted)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#replicationgroupdeletedwaiter)
    """

    def wait(
        self,
        *,
        ReplicationGroupId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Waiter.ReplicationGroupDeleted.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elasticache/waiters.html#replicationgroupdeletedwaiter)
        """
