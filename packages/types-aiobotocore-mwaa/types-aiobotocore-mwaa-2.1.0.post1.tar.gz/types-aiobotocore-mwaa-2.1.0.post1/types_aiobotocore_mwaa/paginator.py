"""
Type annotations for mwaa service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mwaa.client import MWAAClient
    from types_aiobotocore_mwaa.paginator import (
        ListEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("mwaa") as client:
        client: MWAAClient

        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListEnvironmentsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListEnvironmentsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/paginators.html#listenvironmentspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/paginators.html#listenvironmentspaginator)
        """
