"""
Type annotations for sso service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sso.client import SSOClient
    from types_aiobotocore_sso.paginator import (
        ListAccountRolesPaginator,
        ListAccountsPaginator,
    )

    session = get_session()
    with session.create_client("sso") as client:
        client: SSOClient

        list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
        list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAccountRolesResponseTypeDef,
    ListAccountsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListAccountRolesPaginator", "ListAccountsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountRolesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccountRoles)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators.html#listaccountrolespaginator)
    """

    async def paginate(
        self, *, accessToken: str, accountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccountRoles.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators.html#listaccountrolespaginator)
        """


class ListAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccounts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators.html#listaccountspaginator)
    """

    async def paginate(
        self, *, accessToken: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccounts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators.html#listaccountspaginator)
        """
