"""
Type annotations for elb service client waiters.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elb.client import ElasticLoadBalancingClient
    from types_aiobotocore_elb.waiter import (
        AnyInstanceInServiceWaiter,
        InstanceDeregisteredWaiter,
        InstanceInServiceWaiter,
    )

    session = get_session()
    async with session.create_client("elb") as client:
        client: ElasticLoadBalancingClient

        any_instance_in_service_waiter: AnyInstanceInServiceWaiter = client.get_waiter("any_instance_in_service")
        instance_deregistered_waiter: InstanceDeregisteredWaiter = client.get_waiter("instance_deregistered")
        instance_in_service_waiter: InstanceInServiceWaiter = client.get_waiter("instance_in_service")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import InstanceTypeDef, WaiterConfigTypeDef

__all__ = ("AnyInstanceInServiceWaiter", "InstanceDeregisteredWaiter", "InstanceInServiceWaiter")


class AnyInstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.AnyInstanceInService)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html#anyinstanceinservicewaiter)
    """

    async def wait(
        self,
        *,
        LoadBalancerName: str,
        Instances: Sequence["InstanceTypeDef"] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.AnyInstanceInService.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html#anyinstanceinservicewaiter)
        """


class InstanceDeregisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceDeregistered)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html#instancederegisteredwaiter)
    """

    async def wait(
        self,
        *,
        LoadBalancerName: str,
        Instances: Sequence["InstanceTypeDef"] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceDeregistered.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html#instancederegisteredwaiter)
        """


class InstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceInService)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html#instanceinservicewaiter)
    """

    async def wait(
        self,
        *,
        LoadBalancerName: str,
        Instances: Sequence["InstanceTypeDef"] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Waiter.InstanceInService.wait)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters.html#instanceinservicewaiter)
        """
