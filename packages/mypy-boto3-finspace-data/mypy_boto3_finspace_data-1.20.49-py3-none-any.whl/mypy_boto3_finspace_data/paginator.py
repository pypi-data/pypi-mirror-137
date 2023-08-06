"""
Type annotations for finspace-data service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_finspace_data.client import FinSpaceDataClient
    from mypy_boto3_finspace_data.paginator import (
        ListChangesetsPaginator,
        ListDataViewsPaginator,
        ListDatasetsPaginator,
    )

    session = Session()
    client: FinSpaceDataClient = session.client("finspace-data")

    list_changesets_paginator: ListChangesetsPaginator = client.get_paginator("list_changesets")
    list_data_views_paginator: ListDataViewsPaginator = client.get_paginator("list_data_views")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListChangesetsResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListChangesetsPaginator", "ListDataViewsPaginator", "ListDatasetsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChangesetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Paginator.ListChangesets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html#listchangesetspaginator)
    """

    def paginate(
        self, *, datasetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListChangesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Paginator.ListChangesets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html#listchangesetspaginator)
        """


class ListDataViewsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Paginator.ListDataViews)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html#listdataviewspaginator)
    """

    def paginate(
        self, *, datasetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Paginator.ListDataViews.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html#listdataviewspaginator)
        """


class ListDatasetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Paginator.ListDatasets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html#listdatasetspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Paginator.ListDatasets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/paginators.html#listdatasetspaginator)
        """
