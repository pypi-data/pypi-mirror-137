"""
Type annotations for braket service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_braket.client import BraketClient
    from types_aiobotocore_braket.paginator import (
        SearchDevicesPaginator,
        SearchJobsPaginator,
        SearchQuantumTasksPaginator,
    )

    session = get_session()
    with session.create_client("braket") as client:
        client: BraketClient

        search_devices_paginator: SearchDevicesPaginator = client.get_paginator("search_devices")
        search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
        search_quantum_tasks_paginator: SearchQuantumTasksPaginator = client.get_paginator("search_quantum_tasks")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    PaginatorConfigTypeDef,
    SearchDevicesFilterTypeDef,
    SearchDevicesResponseTypeDef,
    SearchJobsFilterTypeDef,
    SearchJobsResponseTypeDef,
    SearchQuantumTasksFilterTypeDef,
    SearchQuantumTasksResponseTypeDef,
)

__all__ = ("SearchDevicesPaginator", "SearchJobsPaginator", "SearchQuantumTasksPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class SearchDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Paginator.SearchDevices)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html#searchdevicespaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["SearchDevicesFilterTypeDef"],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Paginator.SearchDevices.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html#searchdevicespaginator)
        """


class SearchJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Paginator.SearchJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html#searchjobspaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["SearchJobsFilterTypeDef"],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Paginator.SearchJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html#searchjobspaginator)
        """


class SearchQuantumTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Paginator.SearchQuantumTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html#searchquantumtaskspaginator)
    """

    async def paginate(
        self,
        *,
        filters: Sequence["SearchQuantumTasksFilterTypeDef"],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchQuantumTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Paginator.SearchQuantumTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators.html#searchquantumtaskspaginator)
        """
