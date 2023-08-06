"""
Type annotations for redshift service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_redshift.client import RedshiftClient
    from types_aiobotocore_redshift.paginator import (
        DescribeClusterDbRevisionsPaginator,
        DescribeClusterParameterGroupsPaginator,
        DescribeClusterParametersPaginator,
        DescribeClusterSecurityGroupsPaginator,
        DescribeClusterSnapshotsPaginator,
        DescribeClusterSubnetGroupsPaginator,
        DescribeClusterTracksPaginator,
        DescribeClusterVersionsPaginator,
        DescribeClustersPaginator,
        DescribeDataSharesPaginator,
        DescribeDataSharesForConsumerPaginator,
        DescribeDataSharesForProducerPaginator,
        DescribeDefaultClusterParametersPaginator,
        DescribeEndpointAccessPaginator,
        DescribeEndpointAuthorizationPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeHsmClientCertificatesPaginator,
        DescribeHsmConfigurationsPaginator,
        DescribeNodeConfigurationOptionsPaginator,
        DescribeOrderableClusterOptionsPaginator,
        DescribeReservedNodeExchangeStatusPaginator,
        DescribeReservedNodeOfferingsPaginator,
        DescribeReservedNodesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeSnapshotCopyGrantsPaginator,
        DescribeSnapshotSchedulesPaginator,
        DescribeTableRestoreStatusPaginator,
        DescribeTagsPaginator,
        DescribeUsageLimitsPaginator,
        GetReservedNodeExchangeConfigurationOptionsPaginator,
        GetReservedNodeExchangeOfferingsPaginator,
    )

    session = get_session()
    with session.create_client("redshift") as client:
        client: RedshiftClient

        describe_cluster_db_revisions_paginator: DescribeClusterDbRevisionsPaginator = client.get_paginator("describe_cluster_db_revisions")
        describe_cluster_parameter_groups_paginator: DescribeClusterParameterGroupsPaginator = client.get_paginator("describe_cluster_parameter_groups")
        describe_cluster_parameters_paginator: DescribeClusterParametersPaginator = client.get_paginator("describe_cluster_parameters")
        describe_cluster_security_groups_paginator: DescribeClusterSecurityGroupsPaginator = client.get_paginator("describe_cluster_security_groups")
        describe_cluster_snapshots_paginator: DescribeClusterSnapshotsPaginator = client.get_paginator("describe_cluster_snapshots")
        describe_cluster_subnet_groups_paginator: DescribeClusterSubnetGroupsPaginator = client.get_paginator("describe_cluster_subnet_groups")
        describe_cluster_tracks_paginator: DescribeClusterTracksPaginator = client.get_paginator("describe_cluster_tracks")
        describe_cluster_versions_paginator: DescribeClusterVersionsPaginator = client.get_paginator("describe_cluster_versions")
        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        describe_data_shares_paginator: DescribeDataSharesPaginator = client.get_paginator("describe_data_shares")
        describe_data_shares_for_consumer_paginator: DescribeDataSharesForConsumerPaginator = client.get_paginator("describe_data_shares_for_consumer")
        describe_data_shares_for_producer_paginator: DescribeDataSharesForProducerPaginator = client.get_paginator("describe_data_shares_for_producer")
        describe_default_cluster_parameters_paginator: DescribeDefaultClusterParametersPaginator = client.get_paginator("describe_default_cluster_parameters")
        describe_endpoint_access_paginator: DescribeEndpointAccessPaginator = client.get_paginator("describe_endpoint_access")
        describe_endpoint_authorization_paginator: DescribeEndpointAuthorizationPaginator = client.get_paginator("describe_endpoint_authorization")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_hsm_client_certificates_paginator: DescribeHsmClientCertificatesPaginator = client.get_paginator("describe_hsm_client_certificates")
        describe_hsm_configurations_paginator: DescribeHsmConfigurationsPaginator = client.get_paginator("describe_hsm_configurations")
        describe_node_configuration_options_paginator: DescribeNodeConfigurationOptionsPaginator = client.get_paginator("describe_node_configuration_options")
        describe_orderable_cluster_options_paginator: DescribeOrderableClusterOptionsPaginator = client.get_paginator("describe_orderable_cluster_options")
        describe_reserved_node_exchange_status_paginator: DescribeReservedNodeExchangeStatusPaginator = client.get_paginator("describe_reserved_node_exchange_status")
        describe_reserved_node_offerings_paginator: DescribeReservedNodeOfferingsPaginator = client.get_paginator("describe_reserved_node_offerings")
        describe_reserved_nodes_paginator: DescribeReservedNodesPaginator = client.get_paginator("describe_reserved_nodes")
        describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
        describe_snapshot_copy_grants_paginator: DescribeSnapshotCopyGrantsPaginator = client.get_paginator("describe_snapshot_copy_grants")
        describe_snapshot_schedules_paginator: DescribeSnapshotSchedulesPaginator = client.get_paginator("describe_snapshot_schedules")
        describe_table_restore_status_paginator: DescribeTableRestoreStatusPaginator = client.get_paginator("describe_table_restore_status")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
        describe_usage_limits_paginator: DescribeUsageLimitsPaginator = client.get_paginator("describe_usage_limits")
        get_reserved_node_exchange_configuration_options_paginator: GetReservedNodeExchangeConfigurationOptionsPaginator = client.get_paginator("get_reserved_node_exchange_configuration_options")
        get_reserved_node_exchange_offerings_paginator: GetReservedNodeExchangeOfferingsPaginator = client.get_paginator("get_reserved_node_exchange_offerings")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    ActionTypeType,
    DataShareStatusForConsumerType,
    DataShareStatusForProducerType,
    ReservedNodeExchangeActionTypeType,
    ScheduledActionTypeValuesType,
    SourceTypeType,
    UsageLimitFeatureTypeType,
)
from .type_defs import (
    ClusterDbRevisionsMessageTypeDef,
    ClusterParameterGroupDetailsTypeDef,
    ClusterParameterGroupsMessageTypeDef,
    ClusterSecurityGroupMessageTypeDef,
    ClustersMessageTypeDef,
    ClusterSubnetGroupMessageTypeDef,
    ClusterVersionsMessageTypeDef,
    DescribeDataSharesForConsumerResultTypeDef,
    DescribeDataSharesForProducerResultTypeDef,
    DescribeDataSharesResultTypeDef,
    DescribeDefaultClusterParametersResultTypeDef,
    DescribeReservedNodeExchangeStatusOutputMessageTypeDef,
    DescribeSnapshotSchedulesOutputMessageTypeDef,
    EndpointAccessListTypeDef,
    EndpointAuthorizationListTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef,
    GetReservedNodeExchangeOfferingsOutputMessageTypeDef,
    HsmClientCertificateMessageTypeDef,
    HsmConfigurationMessageTypeDef,
    NodeConfigurationOptionsFilterTypeDef,
    NodeConfigurationOptionsMessageTypeDef,
    OrderableClusterOptionsMessageTypeDef,
    PaginatorConfigTypeDef,
    ReservedNodeOfferingsMessageTypeDef,
    ReservedNodesMessageTypeDef,
    ScheduledActionFilterTypeDef,
    ScheduledActionsMessageTypeDef,
    SnapshotCopyGrantMessageTypeDef,
    SnapshotMessageTypeDef,
    SnapshotSortingEntityTypeDef,
    TableRestoreStatusMessageTypeDef,
    TaggedResourceListMessageTypeDef,
    TrackListMessageTypeDef,
    UsageLimitListTypeDef,
)

__all__ = (
    "DescribeClusterDbRevisionsPaginator",
    "DescribeClusterParameterGroupsPaginator",
    "DescribeClusterParametersPaginator",
    "DescribeClusterSecurityGroupsPaginator",
    "DescribeClusterSnapshotsPaginator",
    "DescribeClusterSubnetGroupsPaginator",
    "DescribeClusterTracksPaginator",
    "DescribeClusterVersionsPaginator",
    "DescribeClustersPaginator",
    "DescribeDataSharesPaginator",
    "DescribeDataSharesForConsumerPaginator",
    "DescribeDataSharesForProducerPaginator",
    "DescribeDefaultClusterParametersPaginator",
    "DescribeEndpointAccessPaginator",
    "DescribeEndpointAuthorizationPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeHsmClientCertificatesPaginator",
    "DescribeHsmConfigurationsPaginator",
    "DescribeNodeConfigurationOptionsPaginator",
    "DescribeOrderableClusterOptionsPaginator",
    "DescribeReservedNodeExchangeStatusPaginator",
    "DescribeReservedNodeOfferingsPaginator",
    "DescribeReservedNodesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeSnapshotCopyGrantsPaginator",
    "DescribeSnapshotSchedulesPaginator",
    "DescribeTableRestoreStatusPaginator",
    "DescribeTagsPaginator",
    "DescribeUsageLimitsPaginator",
    "GetReservedNodeExchangeConfigurationOptionsPaginator",
    "GetReservedNodeExchangeOfferingsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeClusterDbRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterDbRevisions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterdbrevisionspaginator)
    """

    async def paginate(
        self, *, ClusterIdentifier: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClusterDbRevisionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterDbRevisions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterdbrevisionspaginator)
        """


class DescribeClusterParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterParameterGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterparametergroupspaginator)
    """

    async def paginate(
        self,
        *,
        ParameterGroupName: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterparametergroupspaginator)
        """


class DescribeClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterParameters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterparameterspaginator)
    """

    async def paginate(
        self,
        *,
        ParameterGroupName: str,
        Source: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterParameters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterparameterspaginator)
        """


class DescribeClusterSecurityGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterSecurityGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustersecuritygroupspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterSecurityGroupName: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClusterSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterSecurityGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustersecuritygroupspaginator)
        """


class DescribeClusterSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterSnapshots)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustersnapshotspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterIdentifier: str = ...,
        SnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        OwnerAccount: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        ClusterExists: bool = ...,
        SortingEntities: Sequence["SnapshotSortingEntityTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterSnapshots.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustersnapshotspaginator)
        """


class DescribeClusterSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterSubnetGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustersubnetgroupspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterSubnetGroupName: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClusterSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterSubnetGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustersubnetgroupspaginator)
        """


class DescribeClusterTracksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterTracks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustertrackspaginator)
    """

    async def paginate(
        self, *, MaintenanceTrackName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[TrackListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterTracks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclustertrackspaginator)
        """


class DescribeClusterVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterversionspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterVersion: str = ...,
        ClusterParameterGroupFamily: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClusterVersionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusterVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterversionspaginator)
        """


class DescribeClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterIdentifier: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeclusterspaginator)
        """


class DescribeDataSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDataShares)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedatasharespaginator)
    """

    async def paginate(
        self, *, DataShareArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDataSharesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDataShares.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedatasharespaginator)
        """


class DescribeDataSharesForConsumerPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDataSharesForConsumer)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedatasharesforconsumerpaginator)
    """

    async def paginate(
        self,
        *,
        ConsumerArn: str = ...,
        Status: DataShareStatusForConsumerType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDataSharesForConsumerResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDataSharesForConsumer.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedatasharesforconsumerpaginator)
        """


class DescribeDataSharesForProducerPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDataSharesForProducer)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedatasharesforproducerpaginator)
    """

    async def paginate(
        self,
        *,
        ProducerArn: str = ...,
        Status: DataShareStatusForProducerType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDataSharesForProducerResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDataSharesForProducer.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedatasharesforproducerpaginator)
        """


class DescribeDefaultClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDefaultClusterParameters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedefaultclusterparameterspaginator)
    """

    async def paginate(
        self, *, ParameterGroupFamily: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDefaultClusterParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeDefaultClusterParameters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describedefaultclusterparameterspaginator)
        """


class DescribeEndpointAccessPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEndpointAccess)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeendpointaccesspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterIdentifier: str = ...,
        ResourceOwner: str = ...,
        EndpointName: str = ...,
        VpcId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EndpointAccessListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEndpointAccess.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeendpointaccesspaginator)
        """


class DescribeEndpointAuthorizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEndpointAuthorization)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeendpointauthorizationpaginator)
    """

    async def paginate(
        self,
        *,
        ClusterIdentifier: str = ...,
        Account: str = ...,
        Grantee: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EndpointAuthorizationListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEndpointAuthorization.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeendpointauthorizationpaginator)
        """


class DescribeEventSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeeventsubscriptionspaginator)
    """

    async def paginate(
        self,
        *,
        SubscriptionName: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeeventsubscriptionspaginator)
        """


class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeeventspaginator)
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
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeeventspaginator)
        """


class DescribeHsmClientCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeHsmClientCertificates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describehsmclientcertificatespaginator)
    """

    async def paginate(
        self,
        *,
        HsmClientCertificateIdentifier: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[HsmClientCertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeHsmClientCertificates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describehsmclientcertificatespaginator)
        """


class DescribeHsmConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeHsmConfigurations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describehsmconfigurationspaginator)
    """

    async def paginate(
        self,
        *,
        HsmConfigurationIdentifier: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[HsmConfigurationMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeHsmConfigurations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describehsmconfigurationspaginator)
        """


class DescribeNodeConfigurationOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeNodeConfigurationOptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describenodeconfigurationoptionspaginator)
    """

    async def paginate(
        self,
        *,
        ActionType: ActionTypeType,
        ClusterIdentifier: str = ...,
        SnapshotIdentifier: str = ...,
        OwnerAccount: str = ...,
        Filters: Sequence["NodeConfigurationOptionsFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[NodeConfigurationOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeNodeConfigurationOptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describenodeconfigurationoptionspaginator)
        """


class DescribeOrderableClusterOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeOrderableClusterOptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeorderableclusteroptionspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterVersion: str = ...,
        NodeType: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[OrderableClusterOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeOrderableClusterOptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeorderableclusteroptionspaginator)
        """


class DescribeReservedNodeExchangeStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeReservedNodeExchangeStatus)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describereservednodeexchangestatuspaginator)
    """

    async def paginate(
        self,
        *,
        ReservedNodeId: str = ...,
        ReservedNodeExchangeRequestId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeReservedNodeExchangeStatusOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeReservedNodeExchangeStatus.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describereservednodeexchangestatuspaginator)
        """


class DescribeReservedNodeOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeReservedNodeOfferings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describereservednodeofferingspaginator)
    """

    async def paginate(
        self, *, ReservedNodeOfferingId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ReservedNodeOfferingsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeReservedNodeOfferings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describereservednodeofferingspaginator)
        """


class DescribeReservedNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeReservedNodes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describereservednodespaginator)
    """

    async def paginate(
        self, *, ReservedNodeId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ReservedNodesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeReservedNodes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describereservednodespaginator)
        """


class DescribeScheduledActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeScheduledActions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describescheduledactionspaginator)
    """

    async def paginate(
        self,
        *,
        ScheduledActionName: str = ...,
        TargetActionType: ScheduledActionTypeValuesType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Active: bool = ...,
        Filters: Sequence["ScheduledActionFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ScheduledActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeScheduledActions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describescheduledactionspaginator)
        """


class DescribeSnapshotCopyGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeSnapshotCopyGrants)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describesnapshotcopygrantspaginator)
    """

    async def paginate(
        self,
        *,
        SnapshotCopyGrantName: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SnapshotCopyGrantMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeSnapshotCopyGrants.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describesnapshotcopygrantspaginator)
        """


class DescribeSnapshotSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeSnapshotSchedules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describesnapshotschedulespaginator)
    """

    async def paginate(
        self,
        *,
        ClusterIdentifier: str = ...,
        ScheduleIdentifier: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSnapshotSchedulesOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeSnapshotSchedules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describesnapshotschedulespaginator)
        """


class DescribeTableRestoreStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeTableRestoreStatus)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describetablerestorestatuspaginator)
    """

    async def paginate(
        self,
        *,
        ClusterIdentifier: str = ...,
        TableRestoreRequestId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[TableRestoreStatusMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeTableRestoreStatus.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describetablerestorestatuspaginator)
        """


class DescribeTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeTags)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describetagspaginator)
    """

    async def paginate(
        self,
        *,
        ResourceName: str = ...,
        ResourceType: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[TaggedResourceListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describetagspaginator)
        """


class DescribeUsageLimitsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeUsageLimits)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeusagelimitspaginator)
    """

    async def paginate(
        self,
        *,
        UsageLimitId: str = ...,
        ClusterIdentifier: str = ...,
        FeatureType: UsageLimitFeatureTypeType = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[UsageLimitListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.DescribeUsageLimits.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#describeusagelimitspaginator)
        """


class GetReservedNodeExchangeConfigurationOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.GetReservedNodeExchangeConfigurationOptions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#getreservednodeexchangeconfigurationoptionspaginator)
    """

    async def paginate(
        self,
        *,
        ActionType: ReservedNodeExchangeActionTypeType,
        ClusterIdentifier: str = ...,
        SnapshotIdentifier: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.GetReservedNodeExchangeConfigurationOptions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#getreservednodeexchangeconfigurationoptionspaginator)
        """


class GetReservedNodeExchangeOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.GetReservedNodeExchangeOfferings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#getreservednodeexchangeofferingspaginator)
    """

    async def paginate(
        self, *, ReservedNodeId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetReservedNodeExchangeOfferingsOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Paginator.GetReservedNodeExchangeOfferings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators.html#getreservednodeexchangeofferingspaginator)
        """
