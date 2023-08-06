"""
Type annotations for appconfigdata service type definitions.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/type_defs.html)

Usage::

    ```python
    from types_aiobotocore_appconfigdata.type_defs import GetLatestConfigurationRequestRequestTypeDef

    data: GetLatestConfigurationRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "GetLatestConfigurationRequestRequestTypeDef",
    "GetLatestConfigurationResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartConfigurationSessionRequestRequestTypeDef",
    "StartConfigurationSessionResponseTypeDef",
)

GetLatestConfigurationRequestRequestTypeDef = TypedDict(
    "GetLatestConfigurationRequestRequestTypeDef",
    {
        "ConfigurationToken": str,
    },
)

GetLatestConfigurationResponseTypeDef = TypedDict(
    "GetLatestConfigurationResponseTypeDef",
    {
        "Configuration": StreamingBody,
        "ContentType": str,
        "NextPollConfigurationToken": str,
        "NextPollIntervalInSeconds": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredStartConfigurationSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStartConfigurationSessionRequestRequestTypeDef",
    {
        "ApplicationIdentifier": str,
        "ConfigurationProfileIdentifier": str,
        "EnvironmentIdentifier": str,
    },
)
_OptionalStartConfigurationSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStartConfigurationSessionRequestRequestTypeDef",
    {
        "RequiredMinimumPollIntervalInSeconds": int,
    },
    total=False,
)


class StartConfigurationSessionRequestRequestTypeDef(
    _RequiredStartConfigurationSessionRequestRequestTypeDef,
    _OptionalStartConfigurationSessionRequestRequestTypeDef,
):
    pass


StartConfigurationSessionResponseTypeDef = TypedDict(
    "StartConfigurationSessionResponseTypeDef",
    {
        "InitialConfigurationToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
