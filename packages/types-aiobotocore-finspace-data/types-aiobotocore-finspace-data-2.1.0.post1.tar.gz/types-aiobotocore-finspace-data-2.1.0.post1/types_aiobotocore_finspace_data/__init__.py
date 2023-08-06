"""
Main interface for finspace-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace_data import (
        Client,
        FinSpaceDataClient,
        ListChangesetsPaginator,
        ListDataViewsPaginator,
        ListDatasetsPaginator,
    )

    session = get_session()
    async with session.create_client("finspace-data") as client:
        client: FinSpaceDataClient
        ...


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
