"""
Type annotations for route53-recovery-cluster service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53_recovery_cluster.client import Route53RecoveryClusterClient

    session = get_session()
    with async session.create_client("route53-recovery-cluster") as client:
        client: Route53RecoveryClusterClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import RoutingControlStateType
from .type_defs import GetRoutingControlStateResponseTypeDef, UpdateRoutingControlStateEntryTypeDef

__all__ = ("Route53RecoveryClusterClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EndpointTemporarilyUnavailableException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53RecoveryClusterClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53RecoveryClusterClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html#exceptions)
        """

    async def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html#generate_presigned_url)
        """

    async def get_routing_control_state(
        self, *, RoutingControlArn: str
    ) -> GetRoutingControlStateResponseTypeDef:
        """
        Get the state for a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.get_routing_control_state)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html#get_routing_control_state)
        """

    async def update_routing_control_state(
        self, *, RoutingControlArn: str, RoutingControlState: RoutingControlStateType
    ) -> Dict[str, Any]:
        """
        Set the state of the routing control to reroute traffic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.update_routing_control_state)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html#update_routing_control_state)
        """

    async def update_routing_control_states(
        self, *, UpdateRoutingControlStateEntries: Sequence["UpdateRoutingControlStateEntryTypeDef"]
    ) -> Dict[str, Any]:
        """
        Set multiple routing control states.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.update_routing_control_states)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client.html#update_routing_control_states)
        """
