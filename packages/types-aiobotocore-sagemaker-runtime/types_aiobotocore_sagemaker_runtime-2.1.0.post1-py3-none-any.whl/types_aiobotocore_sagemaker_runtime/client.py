"""
Type annotations for sagemaker-runtime service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_runtime.client import SageMakerRuntimeClient

    session = get_session()
    async with session.create_client("sagemaker-runtime") as client:
        client: SageMakerRuntimeClient
    ```
"""
from typing import IO, Any, Dict, Mapping, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .type_defs import InvokeEndpointAsyncOutputTypeDef, InvokeEndpointOutputTypeDef

__all__ = ("SageMakerRuntimeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalDependencyException: Type[BotocoreClientError]
    InternalFailure: Type[BotocoreClientError]
    ModelError: Type[BotocoreClientError]
    ModelNotReadyException: Type[BotocoreClientError]
    ServiceUnavailable: Type[BotocoreClientError]
    ValidationError: Type[BotocoreClientError]


class SageMakerRuntimeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html#generate_presigned_url)
        """

    async def invoke_endpoint(
        self,
        *,
        EndpointName: str,
        Body: Union[bytes, IO[bytes], StreamingBody],
        ContentType: str = ...,
        Accept: str = ...,
        CustomAttributes: str = ...,
        TargetModel: str = ...,
        TargetVariant: str = ...,
        TargetContainerHostname: str = ...,
        InferenceId: str = ...
    ) -> InvokeEndpointOutputTypeDef:
        """
        After you deploy a model into production using Amazon SageMaker hosting
        services, your client applications use this API to get inferences from the model
        hosted at the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html#invoke_endpoint)
        """

    async def invoke_endpoint_async(
        self,
        *,
        EndpointName: str,
        InputLocation: str,
        ContentType: str = ...,
        Accept: str = ...,
        CustomAttributes: str = ...,
        InferenceId: str = ...,
        RequestTTLSeconds: int = ...
    ) -> InvokeEndpointAsyncOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint_async)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html#invoke_endpoint_async)
        """

    async def __aenter__(self) -> "SageMakerRuntimeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/client.html)
        """
