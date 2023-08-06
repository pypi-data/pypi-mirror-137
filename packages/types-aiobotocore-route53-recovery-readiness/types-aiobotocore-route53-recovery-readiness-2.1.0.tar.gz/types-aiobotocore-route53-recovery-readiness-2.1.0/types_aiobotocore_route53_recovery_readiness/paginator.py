"""
Type annotations for route53-recovery-readiness service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_readiness.client import Route53RecoveryReadinessClient
    from types_aiobotocore_route53_recovery_readiness.paginator import (
        GetCellReadinessSummaryPaginator,
        GetReadinessCheckResourceStatusPaginator,
        GetReadinessCheckStatusPaginator,
        GetRecoveryGroupReadinessSummaryPaginator,
        ListCellsPaginator,
        ListCrossAccountAuthorizationsPaginator,
        ListReadinessChecksPaginator,
        ListRecoveryGroupsPaginator,
        ListResourceSetsPaginator,
        ListRulesPaginator,
    )

    session = get_session()
    with session.create_client("route53-recovery-readiness") as client:
        client: Route53RecoveryReadinessClient

        get_cell_readiness_summary_paginator: GetCellReadinessSummaryPaginator = client.get_paginator("get_cell_readiness_summary")
        get_readiness_check_resource_status_paginator: GetReadinessCheckResourceStatusPaginator = client.get_paginator("get_readiness_check_resource_status")
        get_readiness_check_status_paginator: GetReadinessCheckStatusPaginator = client.get_paginator("get_readiness_check_status")
        get_recovery_group_readiness_summary_paginator: GetRecoveryGroupReadinessSummaryPaginator = client.get_paginator("get_recovery_group_readiness_summary")
        list_cells_paginator: ListCellsPaginator = client.get_paginator("list_cells")
        list_cross_account_authorizations_paginator: ListCrossAccountAuthorizationsPaginator = client.get_paginator("list_cross_account_authorizations")
        list_readiness_checks_paginator: ListReadinessChecksPaginator = client.get_paginator("list_readiness_checks")
        list_recovery_groups_paginator: ListRecoveryGroupsPaginator = client.get_paginator("list_recovery_groups")
        list_resource_sets_paginator: ListResourceSetsPaginator = client.get_paginator("list_resource_sets")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetCellReadinessSummaryResponseTypeDef,
    GetReadinessCheckResourceStatusResponseTypeDef,
    GetReadinessCheckStatusResponseTypeDef,
    GetRecoveryGroupReadinessSummaryResponseTypeDef,
    ListCellsResponseTypeDef,
    ListCrossAccountAuthorizationsResponseTypeDef,
    ListReadinessChecksResponseTypeDef,
    ListRecoveryGroupsResponseTypeDef,
    ListResourceSetsResponseTypeDef,
    ListRulesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetCellReadinessSummaryPaginator",
    "GetReadinessCheckResourceStatusPaginator",
    "GetReadinessCheckStatusPaginator",
    "GetRecoveryGroupReadinessSummaryPaginator",
    "ListCellsPaginator",
    "ListCrossAccountAuthorizationsPaginator",
    "ListReadinessChecksPaginator",
    "ListRecoveryGroupsPaginator",
    "ListResourceSetsPaginator",
    "ListRulesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetCellReadinessSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getcellreadinesssummarypaginator)
    """

    async def paginate(
        self, *, CellName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetCellReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getcellreadinesssummarypaginator)
        """


class GetReadinessCheckResourceStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getreadinesscheckresourcestatuspaginator)
    """

    async def paginate(
        self,
        *,
        ReadinessCheckName: str,
        ResourceIdentifier: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetReadinessCheckResourceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getreadinesscheckresourcestatuspaginator)
        """


class GetReadinessCheckStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getreadinesscheckstatuspaginator)
    """

    async def paginate(
        self, *, ReadinessCheckName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetReadinessCheckStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getreadinesscheckstatuspaginator)
        """


class GetRecoveryGroupReadinessSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getrecoverygroupreadinesssummarypaginator)
    """

    async def paginate(
        self, *, RecoveryGroupName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRecoveryGroupReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#getrecoverygroupreadinesssummarypaginator)
        """


class ListCellsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCells)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listcellspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCellsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCells.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listcellspaginator)
        """


class ListCrossAccountAuthorizationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listcrossaccountauthorizationspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCrossAccountAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listcrossaccountauthorizationspaginator)
        """


class ListReadinessChecksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listreadinesscheckspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListReadinessChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listreadinesscheckspaginator)
        """


class ListRecoveryGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listrecoverygroupspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecoveryGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listrecoverygroupspaginator)
        """


class ListResourceSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListResourceSets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listresourcesetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListResourceSets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listresourcesetspaginator)
        """


class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listrulespaginator)
    """

    async def paginate(
        self, *, ResourceType: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness.html#Route53RecoveryReadiness.Paginator.ListRules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_readiness/paginators.html#listrulespaginator)
        """
