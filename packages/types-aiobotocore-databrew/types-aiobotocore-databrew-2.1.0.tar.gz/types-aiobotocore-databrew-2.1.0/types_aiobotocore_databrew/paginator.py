"""
Type annotations for databrew service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_databrew.client import GlueDataBrewClient
    from types_aiobotocore_databrew.paginator import (
        ListDatasetsPaginator,
        ListJobRunsPaginator,
        ListJobsPaginator,
        ListProjectsPaginator,
        ListRecipeVersionsPaginator,
        ListRecipesPaginator,
        ListRulesetsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    with session.create_client("databrew") as client:
        client: GlueDataBrewClient

        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_recipe_versions_paginator: ListRecipeVersionsPaginator = client.get_paginator("list_recipe_versions")
        list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
        list_rulesets_paginator: ListRulesetsPaginator = client.get_paginator("list_rulesets")
        list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDatasetsResponseTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListRulesetsResponseTypeDef,
    ListSchedulesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDatasetsPaginator",
    "ListJobRunsPaginator",
    "ListJobsPaginator",
    "ListProjectsPaginator",
    "ListRecipeVersionsPaginator",
    "ListRecipesPaginator",
    "ListRulesetsPaginator",
    "ListSchedulesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDatasetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListDatasets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listdatasetspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listdatasetspaginator)
        """


class ListJobRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobRuns)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listjobrunspaginator)
    """

    async def paginate(
        self, *, Name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listjobrunspaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listjobspaginator)
    """

    async def paginate(
        self,
        *,
        DatasetName: str = ...,
        ProjectName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listjobspaginator)
        """


class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listprojectspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listprojectspaginator)
        """


class ListRecipeVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipeVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listrecipeversionspaginator)
    """

    async def paginate(
        self, *, Name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecipeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipeVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listrecipeversionspaginator)
        """


class ListRecipesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listrecipespaginator)
    """

    async def paginate(
        self, *, RecipeVersion: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listrecipespaginator)
        """


class ListRulesetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListRulesets)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listrulesetspaginator)
    """

    async def paginate(
        self, *, TargetArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListRulesets.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listrulesetspaginator)
        """


class ListSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListSchedules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listschedulespaginator)
    """

    async def paginate(
        self, *, JobName: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Paginator.ListSchedules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators.html#listschedulespaginator)
        """
