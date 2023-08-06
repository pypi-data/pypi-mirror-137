"""
Type annotations for evidently service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_evidently.client import CloudWatchEvidentlyClient
    from types_aiobotocore_evidently.paginator import (
        ListExperimentsPaginator,
        ListFeaturesPaginator,
        ListLaunchesPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    with session.create_client("evidently") as client:
        client: CloudWatchEvidentlyClient

        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_features_paginator: ListFeaturesPaginator = client.get_paginator("list_features")
        list_launches_paginator: ListLaunchesPaginator = client.get_paginator("list_launches")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListExperimentsResponseTypeDef,
    ListFeaturesResponseTypeDef,
    ListLaunchesResponseTypeDef,
    ListProjectsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListExperimentsPaginator",
    "ListFeaturesPaginator",
    "ListLaunchesPaginator",
    "ListProjectsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListExperiments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listexperimentspaginator)
    """

    async def paginate(
        self, *, project: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listexperimentspaginator)
        """


class ListFeaturesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListFeatures)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listfeaturespaginator)
    """

    async def paginate(
        self, *, project: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFeaturesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListFeatures.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listfeaturespaginator)
        """


class ListLaunchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListLaunches)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listlaunchespaginator)
    """

    async def paginate(
        self, *, project: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLaunchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListLaunches.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listlaunchespaginator)
        """


class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listprojectspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators.html#listprojectspaginator)
        """
