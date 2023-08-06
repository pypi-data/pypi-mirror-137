"""
Type annotations for datapipeline service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_datapipeline.client import DataPipelineClient
    from types_aiobotocore_datapipeline.paginator import (
        DescribeObjectsPaginator,
        ListPipelinesPaginator,
        QueryObjectsPaginator,
    )

    session = get_session()
    with session.create_client("datapipeline") as client:
        client: DataPipelineClient

        describe_objects_paginator: DescribeObjectsPaginator = client.get_paginator("describe_objects")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        query_objects_paginator: QueryObjectsPaginator = client.get_paginator("query_objects")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeObjectsOutputTypeDef,
    ListPipelinesOutputTypeDef,
    PaginatorConfigTypeDef,
    QueryObjectsOutputTypeDef,
    QueryTypeDef,
)

__all__ = ("DescribeObjectsPaginator", "ListPipelinesPaginator", "QueryObjectsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeObjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Paginator.DescribeObjects)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html#describeobjectspaginator)
    """

    async def paginate(
        self,
        *,
        pipelineId: str,
        objectIds: Sequence[str],
        evaluateExpressions: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Paginator.DescribeObjects.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html#describeobjectspaginator)
        """


class ListPipelinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Paginator.ListPipelines)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html#listpipelinespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html#listpipelinespaginator)
        """


class QueryObjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Paginator.QueryObjects)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html#queryobjectspaginator)
    """

    async def paginate(
        self,
        *,
        pipelineId: str,
        sphere: str,
        query: "QueryTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[QueryObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Paginator.QueryObjects.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators.html#queryobjectspaginator)
        """
