"""
Type annotations for apprunner service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apprunner.client import AppRunnerClient

    session = get_session()
    with async session.create_client("apprunner") as client:
        client: AppRunnerClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AssociateCustomDomainResponseTypeDef,
    CreateAutoScalingConfigurationResponseTypeDef,
    CreateConnectionResponseTypeDef,
    CreateServiceResponseTypeDef,
    DeleteAutoScalingConfigurationResponseTypeDef,
    DeleteConnectionResponseTypeDef,
    DeleteServiceResponseTypeDef,
    DescribeAutoScalingConfigurationResponseTypeDef,
    DescribeCustomDomainsResponseTypeDef,
    DescribeServiceResponseTypeDef,
    DisassociateCustomDomainResponseTypeDef,
    EncryptionConfigurationTypeDef,
    HealthCheckConfigurationTypeDef,
    InstanceConfigurationTypeDef,
    ListAutoScalingConfigurationsResponseTypeDef,
    ListConnectionsResponseTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PauseServiceResponseTypeDef,
    ResumeServiceResponseTypeDef,
    SourceConfigurationTypeDef,
    StartDeploymentResponseTypeDef,
    TagTypeDef,
    UpdateServiceResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppRunnerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]


class AppRunnerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppRunnerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#exceptions)
        """

    async def associate_custom_domain(
        self, *, ServiceArn: str, DomainName: str, EnableWWWSubdomain: bool = ...
    ) -> AssociateCustomDomainResponseTypeDef:
        """
        Associate your own domain name with the App Runner subdomain URL of your App
        Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.associate_custom_domain)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#associate_custom_domain)
        """

    async def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#can_paginate)
        """

    async def create_auto_scaling_configuration(
        self,
        *,
        AutoScalingConfigurationName: str,
        MaxConcurrency: int = ...,
        MinSize: int = ...,
        MaxSize: int = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAutoScalingConfigurationResponseTypeDef:
        """
        Create an App Runner automatic scaling configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.create_auto_scaling_configuration)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#create_auto_scaling_configuration)
        """

    async def create_connection(
        self,
        *,
        ConnectionName: str,
        ProviderType: Literal["GITHUB"],
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateConnectionResponseTypeDef:
        """
        Create an App Runner connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.create_connection)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#create_connection)
        """

    async def create_service(
        self,
        *,
        ServiceName: str,
        SourceConfiguration: "SourceConfigurationTypeDef",
        InstanceConfiguration: "InstanceConfigurationTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        EncryptionConfiguration: "EncryptionConfigurationTypeDef" = ...,
        HealthCheckConfiguration: "HealthCheckConfigurationTypeDef" = ...,
        AutoScalingConfigurationArn: str = ...
    ) -> CreateServiceResponseTypeDef:
        """
        Create an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.create_service)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#create_service)
        """

    async def delete_auto_scaling_configuration(
        self, *, AutoScalingConfigurationArn: str
    ) -> DeleteAutoScalingConfigurationResponseTypeDef:
        """
        Delete an App Runner automatic scaling configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.delete_auto_scaling_configuration)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#delete_auto_scaling_configuration)
        """

    async def delete_connection(self, *, ConnectionArn: str) -> DeleteConnectionResponseTypeDef:
        """
        Delete an App Runner connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.delete_connection)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#delete_connection)
        """

    async def delete_service(self, *, ServiceArn: str) -> DeleteServiceResponseTypeDef:
        """
        Delete an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.delete_service)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#delete_service)
        """

    async def describe_auto_scaling_configuration(
        self, *, AutoScalingConfigurationArn: str
    ) -> DescribeAutoScalingConfigurationResponseTypeDef:
        """
        Return a full description of an App Runner automatic scaling configuration
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.describe_auto_scaling_configuration)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#describe_auto_scaling_configuration)
        """

    async def describe_custom_domains(
        self, *, ServiceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeCustomDomainsResponseTypeDef:
        """
        Return a description of custom domain names that are associated with an App
        Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.describe_custom_domains)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#describe_custom_domains)
        """

    async def describe_service(self, *, ServiceArn: str) -> DescribeServiceResponseTypeDef:
        """
        Return a full description of an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.describe_service)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#describe_service)
        """

    async def disassociate_custom_domain(
        self, *, ServiceArn: str, DomainName: str
    ) -> DisassociateCustomDomainResponseTypeDef:
        """
        Disassociate a custom domain name from an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.disassociate_custom_domain)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#disassociate_custom_domain)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#generate_presigned_url)
        """

    async def list_auto_scaling_configurations(
        self,
        *,
        AutoScalingConfigurationName: str = ...,
        LatestOnly: bool = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAutoScalingConfigurationsResponseTypeDef:
        """
        Returns a list of App Runner automatic scaling configurations in your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.list_auto_scaling_configurations)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#list_auto_scaling_configurations)
        """

    async def list_connections(
        self, *, ConnectionName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListConnectionsResponseTypeDef:
        """
        Returns a list of App Runner connections that are associated with your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.list_connections)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#list_connections)
        """

    async def list_operations(
        self, *, ServiceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListOperationsResponseTypeDef:
        """
        Return a list of operations that occurred on an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.list_operations)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#list_operations)
        """

    async def list_services(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListServicesResponseTypeDef:
        """
        Returns a list of running App Runner services in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.list_services)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#list_services)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags that are associated with for an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#list_tags_for_resource)
        """

    async def pause_service(self, *, ServiceArn: str) -> PauseServiceResponseTypeDef:
        """
        Pause an active App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.pause_service)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#pause_service)
        """

    async def resume_service(self, *, ServiceArn: str) -> ResumeServiceResponseTypeDef:
        """
        Resume an active App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.resume_service)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#resume_service)
        """

    async def start_deployment(self, *, ServiceArn: str) -> StartDeploymentResponseTypeDef:
        """
        Initiate a manual deployment of the latest commit in a source code repository or
        the latest image in a source image repository to an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.start_deployment)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#start_deployment)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Add tags to, or update the tag values of, an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.tag_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove tags from an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.untag_resource)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#untag_resource)
        """

    async def update_service(
        self,
        *,
        ServiceArn: str,
        SourceConfiguration: "SourceConfigurationTypeDef" = ...,
        InstanceConfiguration: "InstanceConfigurationTypeDef" = ...,
        AutoScalingConfigurationArn: str = ...,
        HealthCheckConfiguration: "HealthCheckConfigurationTypeDef" = ...
    ) -> UpdateServiceResponseTypeDef:
        """
        Update an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client.update_service)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client.html#update_service)
        """
