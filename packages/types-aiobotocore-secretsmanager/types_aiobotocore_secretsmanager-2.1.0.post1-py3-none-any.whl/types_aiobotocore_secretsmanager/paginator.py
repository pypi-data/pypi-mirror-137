"""
Type annotations for secretsmanager service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_secretsmanager.client import SecretsManagerClient
    from types_aiobotocore_secretsmanager.paginator import (
        ListSecretsPaginator,
    )

    session = get_session()
    with session.create_client("secretsmanager") as client:
        client: SecretsManagerClient

        list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import SortOrderTypeType
from .type_defs import FilterTypeDef, ListSecretsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListSecretsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSecretsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Paginator.ListSecrets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/paginators.html#listsecretspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortOrder: SortOrderTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Paginator.ListSecrets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/paginators.html#listsecretspaginator)
        """
