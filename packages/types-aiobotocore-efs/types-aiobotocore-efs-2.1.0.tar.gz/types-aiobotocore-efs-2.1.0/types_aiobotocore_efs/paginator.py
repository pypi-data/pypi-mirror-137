"""
Type annotations for efs service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_efs.client import EFSClient
    from types_aiobotocore_efs.paginator import (
        DescribeFileSystemsPaginator,
        DescribeMountTargetsPaginator,
        DescribeTagsPaginator,
    )

    session = get_session()
    with session.create_client("efs") as client:
        client: EFSClient

        describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
        describe_mount_targets_paginator: DescribeMountTargetsPaginator = client.get_paginator("describe_mount_targets")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeFileSystemsResponseTypeDef,
    DescribeMountTargetsResponseTypeDef,
    DescribeTagsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeFileSystemsPaginator", "DescribeMountTargetsPaginator", "DescribeTagsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeFileSystemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Paginator.DescribeFileSystems)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html#describefilesystemspaginator)
    """

    async def paginate(
        self,
        *,
        CreationToken: str = ...,
        FileSystemId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeFileSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Paginator.DescribeFileSystems.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html#describefilesystemspaginator)
        """


class DescribeMountTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Paginator.DescribeMountTargets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html#describemounttargetspaginator)
    """

    async def paginate(
        self,
        *,
        FileSystemId: str = ...,
        MountTargetId: str = ...,
        AccessPointId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMountTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Paginator.DescribeMountTargets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html#describemounttargetspaginator)
        """


class DescribeTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Paginator.DescribeTags)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html#describetagspaginator)
    """

    async def paginate(
        self, *, FileSystemId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators.html#describetagspaginator)
        """
