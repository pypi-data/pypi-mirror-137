"""
Type annotations for rum service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rum.client import CloudWatchRUMClient
    from types_aiobotocore_rum.paginator import (
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
    )

    session = get_session()
    with session.create_client("rum") as client:
        client: CloudWatchRUMClient

        get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
        list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetAppMonitorDataResponseTypeDef,
    ListAppMonitorsResponseTypeDef,
    PaginatorConfigTypeDef,
    QueryFilterTypeDef,
    TimeRangeTypeDef,
)

__all__ = ("GetAppMonitorDataPaginator", "ListAppMonitorsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetAppMonitorDataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.GetAppMonitorData)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators.html#getappmonitordatapaginator)
    """

    async def paginate(
        self,
        *,
        Name: str,
        TimeRange: "TimeRangeTypeDef",
        Filters: Sequence["QueryFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAppMonitorDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.GetAppMonitorData.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators.html#getappmonitordatapaginator)
        """


class ListAppMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.ListAppMonitors)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators.html#listappmonitorspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.ListAppMonitors.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators.html#listappmonitorspaginator)
        """
