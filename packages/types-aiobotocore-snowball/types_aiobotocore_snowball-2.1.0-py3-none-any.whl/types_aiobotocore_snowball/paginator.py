"""
Type annotations for snowball service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_snowball.client import SnowballClient
    from types_aiobotocore_snowball.paginator import (
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("snowball") as client:
        client: SnowballClient

        describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
        list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAddressesResultTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAddressesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.DescribeAddresses)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#describeaddressespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.DescribeAddresses.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#describeaddressespaginator)
        """


class ListClusterJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusterJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listclusterjobspaginator)
    """

    async def paginate(
        self, *, ClusterId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListClusterJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusterJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listclusterjobspaginator)
        """


class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listclusterspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listclusterspaginator)
        """


class ListCompatibleImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListCompatibleImages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listcompatibleimagespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCompatibleImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListCompatibleImages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listcompatibleimagespaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listjobspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators.html#listjobspaginator)
        """
