"""
Type annotations for pi service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pi.client import PIClient

    session = get_session()
    with async session.create_client("pi") as client:
        client: PIClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    DescribeDimensionKeysResponseTypeDef,
    DimensionGroupTypeDef,
    GetDimensionKeyDetailsResponseTypeDef,
    GetResourceMetricsResponseTypeDef,
    MetricQueryTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("PIClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]


class PIClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html#exceptions)
        """

    async def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html#can_paginate)
        """

    async def describe_dimension_keys(
        self,
        *,
        ServiceType: Literal["RDS"],
        Identifier: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        Metric: str,
        GroupBy: "DimensionGroupTypeDef",
        PeriodInSeconds: int = ...,
        PartitionBy: "DimensionGroupTypeDef" = ...,
        Filter: Mapping[str, str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeDimensionKeysResponseTypeDef:
        """
        For a specific time period, retrieve the top `N` dimension keys for a metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.describe_dimension_keys)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html#describe_dimension_keys)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html#generate_presigned_url)
        """

    async def get_dimension_key_details(
        self,
        *,
        ServiceType: Literal["RDS"],
        Identifier: str,
        Group: str,
        GroupIdentifier: str,
        RequestedDimensions: Sequence[str] = ...
    ) -> GetDimensionKeyDetailsResponseTypeDef:
        """
        Get the attributes of the specified dimension group for a DB instance or data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_dimension_key_details)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html#get_dimension_key_details)
        """

    async def get_resource_metrics(
        self,
        *,
        ServiceType: Literal["RDS"],
        Identifier: str,
        MetricQueries: Sequence["MetricQueryTypeDef"],
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        PeriodInSeconds: int = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> GetResourceMetricsResponseTypeDef:
        """
        Retrieve Performance Insights metrics for a set of data sources, over a time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_resource_metrics)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client.html#get_resource_metrics)
        """
