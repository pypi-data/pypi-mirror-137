"""
Type annotations for shield service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_shield.client import ShieldClient
    from types_aiobotocore_shield.paginator import (
        ListAttacksPaginator,
        ListProtectionsPaginator,
    )

    session = get_session()
    with session.create_client("shield") as client:
        client: ShieldClient

        list_attacks_paginator: ListAttacksPaginator = client.get_paginator("list_attacks")
        list_protections_paginator: ListProtectionsPaginator = client.get_paginator("list_protections")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAttacksResponseTypeDef,
    ListProtectionsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimeRangeTypeDef,
)

__all__ = ("ListAttacksPaginator", "ListProtectionsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAttacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListAttacks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators.html#listattackspaginator)
    """

    async def paginate(
        self,
        *,
        ResourceArns: Sequence[str] = ...,
        StartTime: "TimeRangeTypeDef" = ...,
        EndTime: "TimeRangeTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListAttacks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators.html#listattackspaginator)
        """


class ListProtectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListProtections)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators.html#listprotectionspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProtectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListProtections.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators.html#listprotectionspaginator)
        """
