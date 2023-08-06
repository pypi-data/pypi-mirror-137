"""
Type annotations for fms service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_fms.client import FMSClient
    from types_aiobotocore_fms.paginator import (
        ListAppsListsPaginator,
        ListComplianceStatusPaginator,
        ListMemberAccountsPaginator,
        ListPoliciesPaginator,
        ListProtocolsListsPaginator,
    )

    session = get_session()
    with session.create_client("fms") as client:
        client: FMSClient

        list_apps_lists_paginator: ListAppsListsPaginator = client.get_paginator("list_apps_lists")
        list_compliance_status_paginator: ListComplianceStatusPaginator = client.get_paginator("list_compliance_status")
        list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_protocols_lists_paginator: ListProtocolsListsPaginator = client.get_paginator("list_protocols_lists")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAppsListsResponseTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAppsListsPaginator",
    "ListComplianceStatusPaginator",
    "ListMemberAccountsPaginator",
    "ListPoliciesPaginator",
    "ListProtocolsListsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppsListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListAppsLists)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listappslistspaginator)
    """

    async def paginate(
        self, *, DefaultLists: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListAppsLists.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listappslistspaginator)
        """


class ListComplianceStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListComplianceStatus)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listcompliancestatuspaginator)
    """

    async def paginate(
        self, *, PolicyId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComplianceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListComplianceStatus.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listcompliancestatuspaginator)
        """


class ListMemberAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListMemberAccounts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listmemberaccountspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMemberAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListMemberAccounts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listmemberaccountspaginator)
        """


class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listpoliciespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listpoliciespaginator)
        """


class ListProtocolsListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListProtocolsLists)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listprotocolslistspaginator)
    """

    async def paginate(
        self, *, DefaultLists: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProtocolsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListProtocolsLists.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators.html#listprotocolslistspaginator)
        """
