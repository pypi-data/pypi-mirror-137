"""
Type annotations for cognito-identity service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cognito_identity.client import CognitoIdentityClient
    from types_aiobotocore_cognito_identity.paginator import (
        ListIdentityPoolsPaginator,
    )

    session = get_session()
    with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient

        list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListIdentityPoolsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListIdentityPoolsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListIdentityPoolsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Paginator.ListIdentityPools)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators.html#listidentitypoolspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIdentityPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Paginator.ListIdentityPools.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators.html#listidentitypoolspaginator)
        """
