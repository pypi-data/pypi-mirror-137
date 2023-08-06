"""
Main interface for finspace-data service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace_data import (
        Client,
        FinSpaceDataClient,
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
from .client import FinSpaceDataClient
from .paginator import ListChangesetsPaginator, ListDatasetsPaginator, ListDataViewsPaginator

Client = FinSpaceDataClient


__all__ = (
    "Client",
    "FinSpaceDataClient",
    "ListChangesetsPaginator",
    "ListDataViewsPaginator",
    "ListDatasetsPaginator",
)
