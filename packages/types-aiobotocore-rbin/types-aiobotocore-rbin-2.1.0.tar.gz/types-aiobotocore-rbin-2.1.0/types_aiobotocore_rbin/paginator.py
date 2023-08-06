"""
Type annotations for rbin service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rbin.client import RecycleBinClient
    from types_aiobotocore_rbin.paginator import (
        ListRulesPaginator,
    )

    session = get_session()
    with session.create_client("rbin") as client:
        client: RecycleBinClient

        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListRulesResponseTypeDef, PaginatorConfigTypeDef, ResourceTagTypeDef

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ListRulesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Paginator.ListRules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/paginators.html#listrulespaginator)
    """

    async def paginate(
        self,
        *,
        ResourceType: Literal["EBS_SNAPSHOT"],
        ResourceTags: Sequence["ResourceTagTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Paginator.ListRules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/paginators.html#listrulespaginator)
        """
