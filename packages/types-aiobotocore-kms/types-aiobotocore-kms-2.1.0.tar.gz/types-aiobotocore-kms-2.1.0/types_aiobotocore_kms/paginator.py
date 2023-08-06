"""
Type annotations for kms service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kms.client import KMSClient
    from types_aiobotocore_kms.paginator import (
        ListAliasesPaginator,
        ListGrantsPaginator,
        ListKeyPoliciesPaginator,
        ListKeysPaginator,
    )

    session = get_session()
    with session.create_client("kms") as client:
        client: KMSClient

        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_grants_paginator: ListGrantsPaginator = client.get_paginator("list_grants")
        list_key_policies_paginator: ListKeyPoliciesPaginator = client.get_paginator("list_key_policies")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAliasesResponseTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeysResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAliasesPaginator",
    "ListGrantsPaginator",
    "ListKeyPoliciesPaginator",
    "ListKeysPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listaliasespaginator)
    """

    async def paginate(
        self, *, KeyId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listaliasespaginator)
        """


class ListGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListGrants)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listgrantspaginator)
    """

    async def paginate(
        self,
        *,
        KeyId: str,
        GrantId: str = ...,
        GranteePrincipal: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListGrants.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listgrantspaginator)
        """


class ListKeyPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListKeyPolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listkeypoliciespaginator)
    """

    async def paginate(
        self, *, KeyId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListKeyPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListKeyPolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listkeypoliciespaginator)
        """


class ListKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListKeys)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listkeyspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListKeys.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators.html#listkeyspaginator)
        """
