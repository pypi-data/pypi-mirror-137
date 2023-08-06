"""
Main interface for fsx service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_fsx import (
        Client,
        DescribeBackupsPaginator,
        DescribeFileSystemsPaginator,
        FSxClient,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: FSxClient = session.client("fsx")

    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from .client import FSxClient
from .paginator import (
    DescribeBackupsPaginator,
    DescribeFileSystemsPaginator,
    ListTagsForResourcePaginator,
)

Client = FSxClient


__all__ = (
    "Client",
    "DescribeBackupsPaginator",
    "DescribeFileSystemsPaginator",
    "FSxClient",
    "ListTagsForResourcePaginator",
)
