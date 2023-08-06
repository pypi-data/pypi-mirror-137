"""
Type annotations for kinesis-video-archived-media service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
    from types_aiobotocore_kinesis_video_archived_media.paginator import (
        ListFragmentsPaginator,
    )

    session = get_session()
    with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient

        list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import FragmentSelectorTypeDef, ListFragmentsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListFragmentsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListFragmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Paginator.ListFragments)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators.html#listfragmentspaginator)
    """

    async def paginate(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        FragmentSelector: "FragmentSelectorTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFragmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Paginator.ListFragments.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators.html#listfragmentspaginator)
        """
