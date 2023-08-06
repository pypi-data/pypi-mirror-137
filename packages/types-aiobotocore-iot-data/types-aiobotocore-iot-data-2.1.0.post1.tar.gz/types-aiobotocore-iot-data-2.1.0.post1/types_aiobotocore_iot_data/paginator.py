"""
Type annotations for iot-data service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot_data.client import IoTDataPlaneClient
    from types_aiobotocore_iot_data.paginator import (
        ListRetainedMessagesPaginator,
    )

    session = get_session()
    with session.create_client("iot-data") as client:
        client: IoTDataPlaneClient

        list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListRetainedMessagesResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListRetainedMessagesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRetainedMessagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Paginator.ListRetainedMessages)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/paginators.html#listretainedmessagespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRetainedMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Paginator.ListRetainedMessages.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/paginators.html#listretainedmessagespaginator)
        """
