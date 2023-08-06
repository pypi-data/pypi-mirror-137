"""
Type annotations for kinesis-video-archived-media service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient

    session = Session()
    client: KinesisVideoArchivedMediaClient = session.client("kinesis-video-archived-media")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ContainerFormatType,
    DASHDisplayFragmentNumberType,
    DASHDisplayFragmentTimestampType,
    DASHPlaybackModeType,
    HLSDiscontinuityModeType,
    HLSDisplayFragmentTimestampType,
    HLSPlaybackModeType,
)
from .paginator import ListFragmentsPaginator
from .type_defs import (
    ClipFragmentSelectorTypeDef,
    DASHFragmentSelectorTypeDef,
    FragmentSelectorTypeDef,
    GetClipOutputTypeDef,
    GetDASHStreamingSessionURLOutputTypeDef,
    GetHLSStreamingSessionURLOutputTypeDef,
    GetMediaForFragmentListOutputTypeDef,
    HLSFragmentSelectorTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KinesisVideoArchivedMediaClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidCodecPrivateDataException: Type[BotocoreClientError]
    InvalidMediaFrameException: Type[BotocoreClientError]
    MissingCodecPrivateDataException: Type[BotocoreClientError]
    NoDataRetentionException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnsupportedStreamMediaTypeException: Type[BotocoreClientError]


class KinesisVideoArchivedMediaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoArchivedMediaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.exceptions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#generate_presigned_url)
        """

    def get_clip(
        self,
        *,
        ClipFragmentSelector: "ClipFragmentSelectorTypeDef",
        StreamName: str = ...,
        StreamARN: str = ...
    ) -> GetClipOutputTypeDef:
        """
        Downloads an MP4 file (clip) containing the archived, on-demand media from the
        specified video stream over the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_clip)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#get_clip)
        """

    def get_dash_streaming_session_url(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        PlaybackMode: DASHPlaybackModeType = ...,
        DisplayFragmentTimestamp: DASHDisplayFragmentTimestampType = ...,
        DisplayFragmentNumber: DASHDisplayFragmentNumberType = ...,
        DASHFragmentSelector: "DASHFragmentSelectorTypeDef" = ...,
        Expires: int = ...,
        MaxManifestFragmentResults: int = ...
    ) -> GetDASHStreamingSessionURLOutputTypeDef:
        """
        Retrieves an MPEG Dynamic Adaptive Streaming over HTTP (DASH) URL for the
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_dash_streaming_session_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#get_dash_streaming_session_url)
        """

    def get_hls_streaming_session_url(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        PlaybackMode: HLSPlaybackModeType = ...,
        HLSFragmentSelector: "HLSFragmentSelectorTypeDef" = ...,
        ContainerFormat: ContainerFormatType = ...,
        DiscontinuityMode: HLSDiscontinuityModeType = ...,
        DisplayFragmentTimestamp: HLSDisplayFragmentTimestampType = ...,
        Expires: int = ...,
        MaxMediaPlaylistFragmentResults: int = ...
    ) -> GetHLSStreamingSessionURLOutputTypeDef:
        """
        Retrieves an HTTP Live Streaming (HLS) URL for the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_hls_streaming_session_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#get_hls_streaming_session_url)
        """

    def get_media_for_fragment_list(
        self, *, Fragments: Sequence[str], StreamName: str = ..., StreamARN: str = ...
    ) -> GetMediaForFragmentListOutputTypeDef:
        """
        Gets media for a list of fragments (specified by fragment number) from the
        archived data in an Amazon Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_media_for_fragment_list)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#get_media_for_fragment_list)
        """

    def list_fragments(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        FragmentSelector: "FragmentSelectorTypeDef" = ...
    ) -> ListFragmentsOutputTypeDef:
        """
        Returns a list of  Fragment objects from the specified stream and timestamp
        range within the archived data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.list_fragments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#list_fragments)
        """

    def get_paginator(self, operation_name: Literal["list_fragments"]) -> ListFragmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_paginator)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/client.html#get_paginator)
        """
