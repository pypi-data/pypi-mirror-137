"""
Type annotations for opsworks service client waiters.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opsworks.client import OpsWorksClient
    from mypy_boto3_opsworks.waiter import (
        AppExistsWaiter,
        DeploymentSuccessfulWaiter,
        InstanceOnlineWaiter,
        InstanceRegisteredWaiter,
        InstanceStoppedWaiter,
        InstanceTerminatedWaiter,
    )

    session = Session()
    client: OpsWorksClient = session.client("opsworks")

    app_exists_waiter: AppExistsWaiter = client.get_waiter("app_exists")
    deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
    instance_online_waiter: InstanceOnlineWaiter = client.get_waiter("instance_online")
    instance_registered_waiter: InstanceRegisteredWaiter = client.get_waiter("instance_registered")
    instance_stopped_waiter: InstanceStoppedWaiter = client.get_waiter("instance_stopped")
    instance_terminated_waiter: InstanceTerminatedWaiter = client.get_waiter("instance_terminated")
    ```
"""
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "AppExistsWaiter",
    "DeploymentSuccessfulWaiter",
    "InstanceOnlineWaiter",
    "InstanceRegisteredWaiter",
    "InstanceStoppedWaiter",
    "InstanceTerminatedWaiter",
)


class AppExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.AppExists)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#appexistswaiter)
    """

    def wait(
        self,
        *,
        StackId: str = ...,
        AppIds: Sequence[str] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.AppExists.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#appexistswaiter)
        """


class DeploymentSuccessfulWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.DeploymentSuccessful)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#deploymentsuccessfulwaiter)
    """

    def wait(
        self,
        *,
        StackId: str = ...,
        AppId: str = ...,
        DeploymentIds: Sequence[str] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.DeploymentSuccessful.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#deploymentsuccessfulwaiter)
        """


class InstanceOnlineWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceOnline)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instanceonlinewaiter)
    """

    def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceOnline.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instanceonlinewaiter)
        """


class InstanceRegisteredWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceRegistered)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instanceregisteredwaiter)
    """

    def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceRegistered.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instanceregisteredwaiter)
        """


class InstanceStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceStopped)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instancestoppedwaiter)
    """

    def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceStopped.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instancestoppedwaiter)
        """


class InstanceTerminatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceTerminated)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instanceterminatedwaiter)
    """

    def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceTerminated.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_opsworks/waiters.html#instanceterminatedwaiter)
        """
