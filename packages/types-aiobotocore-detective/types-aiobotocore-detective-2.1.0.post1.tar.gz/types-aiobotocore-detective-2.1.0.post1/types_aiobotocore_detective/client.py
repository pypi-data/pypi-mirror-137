"""
Type annotations for detective service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_detective.client import DetectiveClient

    session = get_session()
    async with session.create_client("detective") as client:
        client: DetectiveClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AccountTypeDef,
    CreateGraphResponseTypeDef,
    CreateMembersResponseTypeDef,
    DeleteMembersResponseTypeDef,
    GetMembersResponseTypeDef,
    ListGraphsResponseTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
)

__all__ = ("DetectiveClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DetectiveClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DetectiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#exceptions)
        """

    async def accept_invitation(self, *, GraphArn: str) -> None:
        """
        Accepts an invitation for the member account to contribute data to a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.accept_invitation)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#accept_invitation)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#can_paginate)
        """

    async def create_graph(self, *, Tags: Mapping[str, str] = ...) -> CreateGraphResponseTypeDef:
        """
        Creates a new behavior graph for the calling account, and sets that account as
        the administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.create_graph)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#create_graph)
        """

    async def create_members(
        self,
        *,
        GraphArn: str,
        Accounts: Sequence["AccountTypeDef"],
        Message: str = ...,
        DisableEmailNotification: bool = ...
    ) -> CreateMembersResponseTypeDef:
        """
        Sends a request to invite the specified AWS accounts to be member accounts in
        the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.create_members)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#create_members)
        """

    async def delete_graph(self, *, GraphArn: str) -> None:
        """
        Disables the specified behavior graph and queues it to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.delete_graph)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#delete_graph)
        """

    async def delete_members(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> DeleteMembersResponseTypeDef:
        """
        Deletes one or more member accounts from the administrator account's behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.delete_members)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#delete_members)
        """

    async def disassociate_membership(self, *, GraphArn: str) -> None:
        """
        Removes the member account from the specified behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.disassociate_membership)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#disassociate_membership)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#generate_presigned_url)
        """

    async def get_members(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> GetMembersResponseTypeDef:
        """
        Returns the membership details for specified member accounts for a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.get_members)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#get_members)
        """

    async def list_graphs(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGraphsResponseTypeDef:
        """
        Returns the list of behavior graphs that the calling account is an administrator
        account of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_graphs)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#list_graphs)
        """

    async def list_invitations(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves the list of open and accepted behavior graph invitations for the
        member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_invitations)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#list_invitations)
        """

    async def list_members(
        self, *, GraphArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves the list of member accounts for a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_members)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#list_members)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tag values that are assigned to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#list_tags_for_resource)
        """

    async def reject_invitation(self, *, GraphArn: str) -> None:
        """
        Rejects an invitation to contribute the account data to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.reject_invitation)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#reject_invitation)
        """

    async def start_monitoring_member(self, *, GraphArn: str, AccountId: str) -> None:
        """
        Sends a request to enable data ingest for a member account that has a status of
        `ACCEPTED_BUT_DISABLED` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.start_monitoring_member)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#start_monitoring_member)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Applies tag values to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.tag_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.untag_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html#untag_resource)
        """

    async def __aenter__(self) -> "DetectiveClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client.html)
        """
