"""
Type annotations for kinesisvideo service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesisvideo.client import KinesisVideoClient
    from types_aiobotocore_kinesisvideo.paginator import (
        ListSignalingChannelsPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    with session.create_client("kinesisvideo") as client:
        client: KinesisVideoClient

        list_signaling_channels_paginator: ListSignalingChannelsPaginator = client.get_paginator("list_signaling_channels")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ChannelNameConditionTypeDef,
    ListSignalingChannelsOutputTypeDef,
    ListStreamsOutputTypeDef,
    PaginatorConfigTypeDef,
    StreamNameConditionTypeDef,
)

__all__ = ("ListSignalingChannelsPaginator", "ListStreamsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSignalingChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListSignalingChannels)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators.html#listsignalingchannelspaginator)
    """

    async def paginate(
        self,
        *,
        ChannelNameCondition: "ChannelNameConditionTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSignalingChannelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListSignalingChannels.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators.html#listsignalingchannelspaginator)
        """


class ListStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListStreams)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators.html#liststreamspaginator)
    """

    async def paginate(
        self,
        *,
        StreamNameCondition: "StreamNameConditionTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListStreams.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators.html#liststreamspaginator)
        """
