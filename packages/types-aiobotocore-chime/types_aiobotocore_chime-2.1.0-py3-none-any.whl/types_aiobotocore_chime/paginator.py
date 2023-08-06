"""
Type annotations for chime service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_chime/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_chime.client import ChimeClient
    from types_aiobotocore_chime.paginator import (
        ListAccountsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("chime") as client:
        client: ChimeClient

        list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import UserTypeType
from .type_defs import ListAccountsResponseTypeDef, ListUsersResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListAccountsPaginator", "ListUsersPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Paginator.ListAccounts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_chime/paginators.html#listaccountspaginator)
    """

    async def paginate(
        self,
        *,
        Name: str = ...,
        UserEmail: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Paginator.ListAccounts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_chime/paginators.html#listaccountspaginator)
        """


class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_chime/paginators.html#listuserspaginator)
    """

    async def paginate(
        self,
        *,
        AccountId: str,
        UserEmail: str = ...,
        UserType: UserTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_chime/paginators.html#listuserspaginator)
        """
