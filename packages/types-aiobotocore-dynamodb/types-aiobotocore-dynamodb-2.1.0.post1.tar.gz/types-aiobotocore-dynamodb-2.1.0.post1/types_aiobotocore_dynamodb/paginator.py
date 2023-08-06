"""
Type annotations for dynamodb service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dynamodb.client import DynamoDBClient
    from types_aiobotocore_dynamodb.paginator import (
        ListBackupsPaginator,
        ListTablesPaginator,
        ListTagsOfResourcePaginator,
        QueryPaginator,
        ScanPaginator,
    )

    session = get_session()
    with session.create_client("dynamodb") as client:
        client: DynamoDBClient

        list_backups_paginator: ListBackupsPaginator = client.get_paginator("list_backups")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
        list_tags_of_resource_paginator: ListTagsOfResourcePaginator = client.get_paginator("list_tags_of_resource")
        query_paginator: QueryPaginator = client.get_paginator("query")
        scan_paginator: ScanPaginator = client.get_paginator("scan")
    ```
"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Generic, Iterator, Mapping, Sequence, Set, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    BackupTypeFilterType,
    ConditionalOperatorType,
    ReturnConsumedCapacityType,
    SelectType,
)
from .type_defs import (
    ConditionTypeDef,
    ListBackupsOutputTypeDef,
    ListTablesOutputTypeDef,
    ListTagsOfResourceOutputTypeDef,
    PaginatorConfigTypeDef,
    QueryOutputTypeDef,
    ScanOutputTypeDef,
)

__all__ = (
    "ListBackupsPaginator",
    "ListTablesPaginator",
    "ListTagsOfResourcePaginator",
    "QueryPaginator",
    "ScanPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBackupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListBackups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#listbackupspaginator)
    """

    async def paginate(
        self,
        *,
        TableName: str = ...,
        TimeRangeLowerBound: Union[datetime, str] = ...,
        TimeRangeUpperBound: Union[datetime, str] = ...,
        BackupType: BackupTypeFilterType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListBackups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#listbackupspaginator)
        """


class ListTablesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTables)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#listtablespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTables.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#listtablespaginator)
        """


class ListTagsOfResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTagsOfResource)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#listtagsofresourcepaginator)
    """

    async def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsOfResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTagsOfResource.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#listtagsofresourcepaginator)
        """


class QueryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Query)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#querypaginator)
    """

    async def paginate(
        self,
        *,
        TableName: str,
        IndexName: str = ...,
        Select: SelectType = ...,
        AttributesToGet: Sequence[str] = ...,
        ConsistentRead: bool = ...,
        KeyConditions: Mapping[str, "ConditionTypeDef"] = ...,
        QueryFilter: Mapping[str, "ConditionTypeDef"] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ScanIndexForward: bool = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ProjectionExpression: str = ...,
        FilterExpression: str = ...,
        KeyConditionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                Sequence[Any],
                Mapping[str, Any],
                None,
            ],
        ] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[QueryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Query.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#querypaginator)
        """


class ScanPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Scan)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#scanpaginator)
    """

    async def paginate(
        self,
        *,
        TableName: str,
        IndexName: str = ...,
        AttributesToGet: Sequence[str] = ...,
        Select: SelectType = ...,
        ScanFilter: Mapping[str, "ConditionTypeDef"] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        TotalSegments: int = ...,
        Segment: int = ...,
        ProjectionExpression: str = ...,
        FilterExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                Sequence[Any],
                Mapping[str, Any],
                None,
            ],
        ] = ...,
        ConsistentRead: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ScanOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Scan.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators.html#scanpaginator)
        """
