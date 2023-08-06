"""
Type annotations for mgh service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mgh.client import MigrationHubClient
    from types_aiobotocore_mgh.paginator import (
        ListApplicationStatesPaginator,
        ListCreatedArtifactsPaginator,
        ListDiscoveredResourcesPaginator,
        ListMigrationTasksPaginator,
        ListProgressUpdateStreamsPaginator,
    )

    session = get_session()
    with session.create_client("mgh") as client:
        client: MigrationHubClient

        list_application_states_paginator: ListApplicationStatesPaginator = client.get_paginator("list_application_states")
        list_created_artifacts_paginator: ListCreatedArtifactsPaginator = client.get_paginator("list_created_artifacts")
        list_discovered_resources_paginator: ListDiscoveredResourcesPaginator = client.get_paginator("list_discovered_resources")
        list_migration_tasks_paginator: ListMigrationTasksPaginator = client.get_paginator("list_migration_tasks")
        list_progress_update_streams_paginator: ListProgressUpdateStreamsPaginator = client.get_paginator("list_progress_update_streams")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationStatesResultTypeDef,
    ListCreatedArtifactsResultTypeDef,
    ListDiscoveredResourcesResultTypeDef,
    ListMigrationTasksResultTypeDef,
    ListProgressUpdateStreamsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListApplicationStatesPaginator",
    "ListCreatedArtifactsPaginator",
    "ListDiscoveredResourcesPaginator",
    "ListMigrationTasksPaginator",
    "ListProgressUpdateStreamsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationStatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListApplicationStates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listapplicationstatespaginator)
    """

    async def paginate(
        self, *, ApplicationIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListApplicationStates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listapplicationstatespaginator)
        """


class ListCreatedArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListCreatedArtifacts)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listcreatedartifactspaginator)
    """

    async def paginate(
        self,
        *,
        ProgressUpdateStream: str,
        MigrationTaskName: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCreatedArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListCreatedArtifacts.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listcreatedartifactspaginator)
        """


class ListDiscoveredResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListDiscoveredResources)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listdiscoveredresourcespaginator)
    """

    async def paginate(
        self,
        *,
        ProgressUpdateStream: str,
        MigrationTaskName: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDiscoveredResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListDiscoveredResources.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listdiscoveredresourcespaginator)
        """


class ListMigrationTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListMigrationTasks)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listmigrationtaskspaginator)
    """

    async def paginate(
        self, *, ResourceName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMigrationTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListMigrationTasks.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listmigrationtaskspaginator)
        """


class ListProgressUpdateStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListProgressUpdateStreams)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listprogressupdatestreamspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProgressUpdateStreamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub.Paginator.ListProgressUpdateStreams.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators.html#listprogressupdatestreamspaginator)
        """
