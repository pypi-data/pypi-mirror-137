"""
Type annotations for glacier service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_glacier.client import GlacierClient
    from types_aiobotocore_glacier.paginator import (
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
    )

    session = get_session()
    with session.create_client("glacier") as client:
        client: GlacierClient

        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
        list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
        list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListJobsOutputTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListPartsOutputTypeDef,
    ListVaultsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listjobspaginator)
    """

    async def paginate(
        self,
        *,
        accountId: str,
        vaultName: str,
        statuscode: str = ...,
        completed: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listjobspaginator)
        """


class ListMultipartUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListMultipartUploads)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listmultipartuploadspaginator)
    """

    async def paginate(
        self, *, accountId: str, vaultName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListMultipartUploads.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listmultipartuploadspaginator)
        """


class ListPartsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListParts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listpartspaginator)
    """

    async def paginate(
        self,
        *,
        accountId: str,
        vaultName: str,
        uploadId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListParts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listpartspaginator)
        """


class ListVaultsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListVaults)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listvaultspaginator)
    """

    async def paginate(
        self, *, accountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Paginator.ListVaults.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators.html#listvaultspaginator)
        """
