"""
Type annotations for importexport service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_importexport.client import ImportExportClient
    from types_aiobotocore_importexport.paginator import (
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("importexport") as client:
        client: ImportExportClient

        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListJobsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListJobsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators.html#listjobspaginator)
    """

    async def paginate(
        self, *, APIVersion: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators.html#listjobspaginator)
        """
