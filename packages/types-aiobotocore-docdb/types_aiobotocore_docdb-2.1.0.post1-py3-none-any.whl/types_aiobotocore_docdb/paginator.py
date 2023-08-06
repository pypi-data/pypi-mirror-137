"""
Type annotations for docdb service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_docdb.client import DocDBClient
    from types_aiobotocore_docdb.paginator import (
        DescribeCertificatesPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeGlobalClustersPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
    )

    session = get_session()
    with session.create_client("docdb") as client:
        client: DocDBClient

        describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
        describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
        describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
        describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
        describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
        describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
        describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
        describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
        describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
        describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import SourceTypeType
from .type_defs import (
    CertificateMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FilterTypeDef,
    GlobalClustersMessageTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PaginatorConfigTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
)

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeCertificates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describecertificatespaginator)
    """

    async def paginate(
        self,
        *,
        CertificateIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeCertificates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describecertificatespaginator)
        """


class DescribeDBClusterParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameterGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclusterparametergroupspaginator)
    """

    async def paginate(
        self,
        *,
        DBClusterParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclusterparametergroupspaginator)
        """


class DescribeDBClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclusterparameterspaginator)
    """

    async def paginate(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterParameters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclusterparameterspaginator)
        """


class DescribeDBClusterSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterSnapshots)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclustersnapshotspaginator)
    """

    async def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclustersnapshotspaginator)
        """


class DescribeDBClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclusterspaginator)
    """

    async def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBClusters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbclusterspaginator)
        """


class DescribeDBEngineVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBEngineVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbengineversionspaginator)
    """

    async def paginate(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        DBParameterGroupFamily: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        DefaultOnly: bool = ...,
        ListSupportedCharacterSets: bool = ...,
        ListSupportedTimezones: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBEngineVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbengineversionspaginator)
        """


class DescribeDBInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbinstancespaginator)
    """

    async def paginate(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbinstancespaginator)
        """


class DescribeDBSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBSubnetGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbsubnetgroupspaginator)
    """

    async def paginate(
        self,
        *,
        DBSubnetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeDBSubnetGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describedbsubnetgroupspaginator)
        """


class DescribeEventSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeeventsubscriptionspaginator)
    """

    async def paginate(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeeventsubscriptionspaginator)
        """


class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeeventspaginator)
    """

    async def paginate(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeeventspaginator)
        """


class DescribeGlobalClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeGlobalClusters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeglobalclusterspaginator)
    """

    async def paginate(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeGlobalClusters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeglobalclusterspaginator)
        """


class DescribeOrderableDBInstanceOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeorderabledbinstanceoptionspaginator)
    """

    async def paginate(
        self,
        *,
        Engine: str,
        EngineVersion: str = ...,
        DBInstanceClass: str = ...,
        LicenseModel: str = ...,
        Vpc: bool = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describeorderabledbinstanceoptionspaginator)
        """


class DescribePendingMaintenanceActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribePendingMaintenanceActions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describependingmaintenanceactionspaginator)
    """

    async def paginate(
        self,
        *,
        ResourceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators.html#describependingmaintenanceactionspaginator)
        """
