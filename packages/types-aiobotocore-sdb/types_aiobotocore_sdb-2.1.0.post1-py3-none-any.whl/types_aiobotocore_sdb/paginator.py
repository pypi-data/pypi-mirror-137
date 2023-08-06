"""
Type annotations for sdb service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sdb.client import SimpleDBClient
    from types_aiobotocore_sdb.paginator import (
        ListDomainsPaginator,
        SelectPaginator,
    )

    session = get_session()
    with session.create_client("sdb") as client:
        client: SimpleDBClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        select_paginator: SelectPaginator = client.get_paginator("select")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListDomainsResultTypeDef, PaginatorConfigTypeDef, SelectResultTypeDef

__all__ = ("ListDomainsPaginator", "SelectPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators.html#listdomainspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators.html#listdomainspaginator)
        """


class SelectPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Paginator.Select)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators.html#selectpaginator)
    """

    async def paginate(
        self,
        *,
        SelectExpression: str,
        ConsistentRead: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SelectResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Paginator.Select.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators.html#selectpaginator)
        """
