"""
Type annotations for cognito-idp service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cognito_idp.client import CognitoIdentityProviderClient
    from types_aiobotocore_cognito_idp.paginator import (
        AdminListGroupsForUserPaginator,
        AdminListUserAuthEventsPaginator,
        ListGroupsPaginator,
        ListIdentityProvidersPaginator,
        ListResourceServersPaginator,
        ListUserPoolClientsPaginator,
        ListUserPoolsPaginator,
        ListUsersPaginator,
        ListUsersInGroupPaginator,
    )

    session = get_session()
    with session.create_client("cognito-idp") as client:
        client: CognitoIdentityProviderClient

        admin_list_groups_for_user_paginator: AdminListGroupsForUserPaginator = client.get_paginator("admin_list_groups_for_user")
        admin_list_user_auth_events_paginator: AdminListUserAuthEventsPaginator = client.get_paginator("admin_list_user_auth_events")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
        list_resource_servers_paginator: ListResourceServersPaginator = client.get_paginator("list_resource_servers")
        list_user_pool_clients_paginator: ListUserPoolClientsPaginator = client.get_paginator("list_user_pool_clients")
        list_user_pools_paginator: ListUserPoolsPaginator = client.get_paginator("list_user_pools")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_users_in_group_paginator: ListUsersInGroupPaginator = client.get_paginator("list_users_in_group")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    AdminListGroupsForUserResponseTypeDef,
    AdminListUserAuthEventsResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListResourceServersResponseTypeDef,
    ListUserPoolClientsResponseTypeDef,
    ListUserPoolsResponseTypeDef,
    ListUsersInGroupResponseTypeDef,
    ListUsersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "AdminListGroupsForUserPaginator",
    "AdminListUserAuthEventsPaginator",
    "ListGroupsPaginator",
    "ListIdentityProvidersPaginator",
    "ListResourceServersPaginator",
    "ListUserPoolClientsPaginator",
    "ListUserPoolsPaginator",
    "ListUsersPaginator",
    "ListUsersInGroupPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class AdminListGroupsForUserPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.AdminListGroupsForUser)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#adminlistgroupsforuserpaginator)
    """

    async def paginate(
        self, *, Username: str, UserPoolId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[AdminListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.AdminListGroupsForUser.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#adminlistgroupsforuserpaginator)
        """


class AdminListUserAuthEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.AdminListUserAuthEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#adminlistuserautheventspaginator)
    """

    async def paginate(
        self, *, UserPoolId: str, Username: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[AdminListUserAuthEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.AdminListUserAuthEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#adminlistuserautheventspaginator)
        """


class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listgroupspaginator)
    """

    async def paginate(
        self, *, UserPoolId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listgroupspaginator)
        """


class ListIdentityProvidersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListIdentityProviders)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listidentityproviderspaginator)
    """

    async def paginate(
        self, *, UserPoolId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIdentityProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListIdentityProviders.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listidentityproviderspaginator)
        """


class ListResourceServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListResourceServers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listresourceserverspaginator)
    """

    async def paginate(
        self, *, UserPoolId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListResourceServers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listresourceserverspaginator)
        """


class ListUserPoolClientsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUserPoolClients)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listuserpoolclientspaginator)
    """

    async def paginate(
        self, *, UserPoolId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUserPoolClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUserPoolClients.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listuserpoolclientspaginator)
        """


class ListUserPoolsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUserPools)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listuserpoolspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUserPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUserPools.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listuserpoolspaginator)
        """


class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listuserspaginator)
    """

    async def paginate(
        self,
        *,
        UserPoolId: str,
        AttributesToGet: Sequence[str] = ...,
        Filter: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listuserspaginator)
        """


class ListUsersInGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUsersInGroup)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listusersingrouppaginator)
    """

    async def paginate(
        self, *, UserPoolId: str, GroupName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsersInGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Paginator.ListUsersInGroup.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators.html#listusersingrouppaginator)
        """
