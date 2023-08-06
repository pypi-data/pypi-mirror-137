"""
Main interface for kinesis-video-archived-media service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_archived_media import (
        Client,
        KinesisVideoArchivedMediaClient,
        ListFragmentsPaginator,
    )

    session = Session()
    client: KinesisVideoArchivedMediaClient = session.client("kinesis-video-archived-media")

    list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```
"""
from .client import KinesisVideoArchivedMediaClient
from .paginator import ListFragmentsPaginator

Client = KinesisVideoArchivedMediaClient


__all__ = ("Client", "KinesisVideoArchivedMediaClient", "ListFragmentsPaginator")
