"""
Type annotations for rbin service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rbin.client import RecycleBinClient

    session = get_session()
    with async session.create_client("rbin") as client:
        client: RecycleBinClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListRulesPaginator
from .type_defs import (
    CreateRuleResponseTypeDef,
    GetRuleResponseTypeDef,
    ListRulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResourceTagTypeDef,
    RetentionPeriodTypeDef,
    TagTypeDef,
    UpdateRuleResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("RecycleBinClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class RecycleBinClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RecycleBinClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#exceptions)
        """

    async def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#can_paginate)
        """

    async def create_rule(
        self,
        *,
        RetentionPeriod: "RetentionPeriodTypeDef",
        ResourceType: Literal["EBS_SNAPSHOT"],
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        ResourceTags: Sequence["ResourceTagTypeDef"] = ...
    ) -> CreateRuleResponseTypeDef:
        """
        Creates a Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.create_rule)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#create_rule)
        """

    async def delete_rule(self, *, Identifier: str) -> Dict[str, Any]:
        """
        Deletes a Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.delete_rule)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#delete_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#generate_presigned_url)
        """

    async def get_rule(self, *, Identifier: str) -> GetRuleResponseTypeDef:
        """
        Gets information about a Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.get_rule)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#get_rule)
        """

    async def list_rules(
        self,
        *,
        ResourceType: Literal["EBS_SNAPSHOT"],
        MaxResults: int = ...,
        NextToken: str = ...,
        ResourceTags: Sequence["ResourceTagTypeDef"] = ...
    ) -> ListRulesResponseTypeDef:
        """
        Lists the Recycle Bin retention rules in the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.list_rules)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#list_rules)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned a specific resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#list_tags_for_resource)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Assigns tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.tag_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Unassigns a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.untag_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#untag_resource)
        """

    async def update_rule(
        self,
        *,
        Identifier: str,
        RetentionPeriod: "RetentionPeriodTypeDef" = ...,
        Description: str = ...,
        ResourceType: Literal["EBS_SNAPSHOT"] = ...,
        ResourceTags: Sequence["ResourceTagTypeDef"] = ...
    ) -> UpdateRuleResponseTypeDef:
        """
        Updates an existing Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.update_rule)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#update_rule)
        """

    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/client.html#get_paginator)
        """
