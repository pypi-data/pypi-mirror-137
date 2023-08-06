"""
Type annotations for lookoutvision service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lookoutvision.client import LookoutforVisionClient
    from types_aiobotocore_lookoutvision.paginator import (
        ListDatasetEntriesPaginator,
        ListModelPackagingJobsPaginator,
        ListModelsPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    with session.create_client("lookoutvision") as client:
        client: LookoutforVisionClient

        list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
        list_model_packaging_jobs_paginator: ListModelPackagingJobsPaginator = client.get_paginator("list_model_packaging_jobs")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDatasetEntriesResponseTypeDef,
    ListModelPackagingJobsResponseTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDatasetEntriesPaginator",
    "ListModelPackagingJobsPaginator",
    "ListModelsPaginator",
    "ListProjectsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDatasetEntriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listdatasetentriespaginator)
    """

    async def paginate(
        self,
        *,
        ProjectName: str,
        DatasetType: str,
        Labeled: bool = ...,
        AnomalyClass: str = ...,
        BeforeCreationDate: Union[datetime, str] = ...,
        AfterCreationDate: Union[datetime, str] = ...,
        SourceRefContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listdatasetentriespaginator)
        """


class ListModelPackagingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModelPackagingJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listmodelpackagingjobspaginator)
    """

    async def paginate(
        self, *, ProjectName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelPackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModelPackagingJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listmodelpackagingjobspaginator)
        """


class ListModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listmodelspaginator)
    """

    async def paginate(
        self, *, ProjectName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listmodelspaginator)
        """


class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listprojectspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators.html#listprojectspaginator)
        """
