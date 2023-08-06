"""
Type annotations for route53-recovery-control-config service client waiters.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_control_config.client import Route53RecoveryControlConfigClient
    from types_aiobotocore_route53_recovery_control_config.waiter import (
        ClusterCreatedWaiter,
        ClusterDeletedWaiter,
        ControlPanelCreatedWaiter,
        ControlPanelDeletedWaiter,
        RoutingControlCreatedWaiter,
        RoutingControlDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("route53-recovery-control-config") as client:
        client: Route53RecoveryControlConfigClient

        cluster_created_waiter: ClusterCreatedWaiter = client.get_waiter("cluster_created")
        cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
        control_panel_created_waiter: ControlPanelCreatedWaiter = client.get_waiter("control_panel_created")
        control_panel_deleted_waiter: ControlPanelDeletedWaiter = client.get_waiter("control_panel_deleted")
        routing_control_created_waiter: RoutingControlCreatedWaiter = client.get_waiter("routing_control_created")
        routing_control_deleted_waiter: RoutingControlDeletedWaiter = client.get_waiter("routing_control_deleted")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "ClusterCreatedWaiter",
    "ClusterDeletedWaiter",
    "ControlPanelCreatedWaiter",
    "ControlPanelDeletedWaiter",
    "RoutingControlCreatedWaiter",
    "RoutingControlDeletedWaiter",
)


class ClusterCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ClusterCreated)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#clustercreatedwaiter)
    """

    async def wait(self, *, ClusterArn: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ClusterCreated.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#clustercreatedwaiter)
        """


class ClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ClusterDeleted)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#clusterdeletedwaiter)
    """

    async def wait(self, *, ClusterArn: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ClusterDeleted.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#clusterdeletedwaiter)
        """


class ControlPanelCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ControlPanelCreated)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#controlpanelcreatedwaiter)
    """

    async def wait(self, *, ControlPanelArn: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ControlPanelCreated.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#controlpanelcreatedwaiter)
        """


class ControlPanelDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ControlPanelDeleted)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#controlpaneldeletedwaiter)
    """

    async def wait(self, *, ControlPanelArn: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.ControlPanelDeleted.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#controlpaneldeletedwaiter)
        """


class RoutingControlCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.RoutingControlCreated)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#routingcontrolcreatedwaiter)
    """

    async def wait(
        self, *, RoutingControlArn: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.RoutingControlCreated.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#routingcontrolcreatedwaiter)
        """


class RoutingControlDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.RoutingControlDeleted)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#routingcontroldeletedwaiter)
    """

    async def wait(
        self, *, RoutingControlArn: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Waiter.RoutingControlDeleted.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters.html#routingcontroldeletedwaiter)
        """
