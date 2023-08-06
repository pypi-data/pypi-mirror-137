"""
Type annotations for migrationhubstrategy service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient
    from types_aiobotocore_migrationhubstrategy.paginator import (
        GetServerDetailsPaginator,
        ListApplicationComponentsPaginator,
        ListCollectorsPaginator,
        ListImportFileTaskPaginator,
        ListServersPaginator,
    )

    session = get_session()
    with session.create_client("migrationhubstrategy") as client:
        client: MigrationHubStrategyRecommendationsClient

        get_server_details_paginator: GetServerDetailsPaginator = client.get_paginator("get_server_details")
        list_application_components_paginator: ListApplicationComponentsPaginator = client.get_paginator("list_application_components")
        list_collectors_paginator: ListCollectorsPaginator = client.get_paginator("list_collectors")
        list_import_file_task_paginator: ListImportFileTaskPaginator = client.get_paginator("list_import_file_task")
        list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ApplicationComponentCriteriaType, ServerCriteriaType, SortOrderType
from .type_defs import (
    GetServerDetailsResponseTypeDef,
    GroupTypeDef,
    ListApplicationComponentsResponseTypeDef,
    ListCollectorsResponseTypeDef,
    ListImportFileTaskResponseTypeDef,
    ListServersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetServerDetailsPaginator",
    "ListApplicationComponentsPaginator",
    "ListCollectorsPaginator",
    "ListImportFileTaskPaginator",
    "ListServersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetServerDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.GetServerDetails)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#getserverdetailspaginator)
    """

    async def paginate(
        self, *, serverId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetServerDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.GetServerDetails.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#getserverdetailspaginator)
        """


class ListApplicationComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListApplicationComponents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listapplicationcomponentspaginator)
    """

    async def paginate(
        self,
        *,
        applicationComponentCriteria: ApplicationComponentCriteriaType = ...,
        filterValue: str = ...,
        groupIdFilter: Sequence["GroupTypeDef"] = ...,
        sort: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListApplicationComponents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listapplicationcomponentspaginator)
        """


class ListCollectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListCollectors)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listcollectorspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCollectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListCollectors.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listcollectorspaginator)
        """


class ListImportFileTaskPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListImportFileTask)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listimportfiletaskpaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListImportFileTaskResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListImportFileTask.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listimportfiletaskpaginator)
        """


class ListServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListServers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listserverspaginator)
    """

    async def paginate(
        self,
        *,
        filterValue: str = ...,
        groupIdFilter: Sequence["GroupTypeDef"] = ...,
        serverCriteria: ServerCriteriaType = ...,
        sort: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Paginator.ListServers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators.html#listserverspaginator)
        """
