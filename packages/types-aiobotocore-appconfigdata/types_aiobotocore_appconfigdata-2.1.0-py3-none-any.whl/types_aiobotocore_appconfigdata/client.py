"""
Type annotations for appconfigdata service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appconfigdata.client import AppConfigDataClient

    session = get_session()
    with async session.create_client("appconfigdata") as client:
        client: AppConfigDataClient
    ```
"""
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    GetLatestConfigurationResponseTypeDef,
    StartConfigurationSessionResponseTypeDef,
)

__all__ = ("AppConfigDataClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class AppConfigDataClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppConfigDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html#exceptions)
        """

    async def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html#generate_presigned_url)
        """

    async def get_latest_configuration(
        self, *, ConfigurationToken: str
    ) -> GetLatestConfigurationResponseTypeDef:
        """
        Retrieves the latest deployed configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.get_latest_configuration)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html#get_latest_configuration)
        """

    async def start_configuration_session(
        self,
        *,
        ApplicationIdentifier: str,
        ConfigurationProfileIdentifier: str,
        EnvironmentIdentifier: str,
        RequiredMinimumPollIntervalInSeconds: int = ...
    ) -> StartConfigurationSessionResponseTypeDef:
        """
        Starts a configuration session used to retrieve a deployed configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfigdata.html#AppConfigData.Client.start_configuration_session)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/client.html#start_configuration_session)
        """
