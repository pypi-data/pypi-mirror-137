"""
Type annotations for firehose service client.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_firehose.client import FirehoseClient

    session = get_session()
    async with session.create_client("firehose") as client:
        client: FirehoseClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import DeliveryStreamTypeType
from .type_defs import (
    AmazonopensearchserviceDestinationConfigurationTypeDef,
    AmazonopensearchserviceDestinationUpdateTypeDef,
    CreateDeliveryStreamOutputTypeDef,
    DeliveryStreamEncryptionConfigurationInputTypeDef,
    DescribeDeliveryStreamOutputTypeDef,
    ElasticsearchDestinationConfigurationTypeDef,
    ElasticsearchDestinationUpdateTypeDef,
    ExtendedS3DestinationConfigurationTypeDef,
    ExtendedS3DestinationUpdateTypeDef,
    HttpEndpointDestinationConfigurationTypeDef,
    HttpEndpointDestinationUpdateTypeDef,
    KinesisStreamSourceConfigurationTypeDef,
    ListDeliveryStreamsOutputTypeDef,
    ListTagsForDeliveryStreamOutputTypeDef,
    PutRecordBatchOutputTypeDef,
    PutRecordOutputTypeDef,
    RecordTypeDef,
    RedshiftDestinationConfigurationTypeDef,
    RedshiftDestinationUpdateTypeDef,
    S3DestinationConfigurationTypeDef,
    S3DestinationUpdateTypeDef,
    SplunkDestinationConfigurationTypeDef,
    SplunkDestinationUpdateTypeDef,
    TagTypeDef,
)

__all__ = ("FirehoseClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidKMSResourceException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]


class FirehoseClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FirehoseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.exceptions)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.can_paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#can_paginate)
        """

    async def create_delivery_stream(
        self,
        *,
        DeliveryStreamName: str,
        DeliveryStreamType: DeliveryStreamTypeType = ...,
        KinesisStreamSourceConfiguration: "KinesisStreamSourceConfigurationTypeDef" = ...,
        DeliveryStreamEncryptionConfigurationInput: "DeliveryStreamEncryptionConfigurationInputTypeDef" = ...,
        S3DestinationConfiguration: "S3DestinationConfigurationTypeDef" = ...,
        ExtendedS3DestinationConfiguration: "ExtendedS3DestinationConfigurationTypeDef" = ...,
        RedshiftDestinationConfiguration: "RedshiftDestinationConfigurationTypeDef" = ...,
        ElasticsearchDestinationConfiguration: "ElasticsearchDestinationConfigurationTypeDef" = ...,
        AmazonopensearchserviceDestinationConfiguration: "AmazonopensearchserviceDestinationConfigurationTypeDef" = ...,
        SplunkDestinationConfiguration: "SplunkDestinationConfigurationTypeDef" = ...,
        HttpEndpointDestinationConfiguration: "HttpEndpointDestinationConfigurationTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDeliveryStreamOutputTypeDef:
        """
        Creates a Kinesis Data Firehose delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.create_delivery_stream)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#create_delivery_stream)
        """

    async def delete_delivery_stream(
        self, *, DeliveryStreamName: str, AllowForceDelete: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes a delivery stream and its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.delete_delivery_stream)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#delete_delivery_stream)
        """

    async def describe_delivery_stream(
        self, *, DeliveryStreamName: str, Limit: int = ..., ExclusiveStartDestinationId: str = ...
    ) -> DescribeDeliveryStreamOutputTypeDef:
        """
        Describes the specified delivery stream and its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.describe_delivery_stream)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#describe_delivery_stream)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#generate_presigned_url)
        """

    async def list_delivery_streams(
        self,
        *,
        Limit: int = ...,
        DeliveryStreamType: DeliveryStreamTypeType = ...,
        ExclusiveStartDeliveryStreamName: str = ...
    ) -> ListDeliveryStreamsOutputTypeDef:
        """
        Lists your delivery streams in alphabetical order of their names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.list_delivery_streams)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#list_delivery_streams)
        """

    async def list_tags_for_delivery_stream(
        self, *, DeliveryStreamName: str, ExclusiveStartTagKey: str = ..., Limit: int = ...
    ) -> ListTagsForDeliveryStreamOutputTypeDef:
        """
        Lists the tags for the specified delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.list_tags_for_delivery_stream)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#list_tags_for_delivery_stream)
        """

    async def put_record(
        self, *, DeliveryStreamName: str, Record: "RecordTypeDef"
    ) -> PutRecordOutputTypeDef:
        """
        Writes a single data record into an Amazon Kinesis Data Firehose delivery
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.put_record)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#put_record)
        """

    async def put_record_batch(
        self, *, DeliveryStreamName: str, Records: Sequence["RecordTypeDef"]
    ) -> PutRecordBatchOutputTypeDef:
        """
        Writes multiple data records into a delivery stream in a single call, which can
        achieve higher throughput per producer than when writing single records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.put_record_batch)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#put_record_batch)
        """

    async def start_delivery_stream_encryption(
        self,
        *,
        DeliveryStreamName: str,
        DeliveryStreamEncryptionConfigurationInput: "DeliveryStreamEncryptionConfigurationInputTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Enables server-side encryption (SSE) for the delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.start_delivery_stream_encryption)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#start_delivery_stream_encryption)
        """

    async def stop_delivery_stream_encryption(self, *, DeliveryStreamName: str) -> Dict[str, Any]:
        """
        Disables server-side encryption (SSE) for the delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.stop_delivery_stream_encryption)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#stop_delivery_stream_encryption)
        """

    async def tag_delivery_stream(
        self, *, DeliveryStreamName: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds or updates tags for the specified delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.tag_delivery_stream)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#tag_delivery_stream)
        """

    async def untag_delivery_stream(
        self, *, DeliveryStreamName: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Removes tags from the specified delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.untag_delivery_stream)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#untag_delivery_stream)
        """

    async def update_destination(
        self,
        *,
        DeliveryStreamName: str,
        CurrentDeliveryStreamVersionId: str,
        DestinationId: str,
        S3DestinationUpdate: "S3DestinationUpdateTypeDef" = ...,
        ExtendedS3DestinationUpdate: "ExtendedS3DestinationUpdateTypeDef" = ...,
        RedshiftDestinationUpdate: "RedshiftDestinationUpdateTypeDef" = ...,
        ElasticsearchDestinationUpdate: "ElasticsearchDestinationUpdateTypeDef" = ...,
        AmazonopensearchserviceDestinationUpdate: "AmazonopensearchserviceDestinationUpdateTypeDef" = ...,
        SplunkDestinationUpdate: "SplunkDestinationUpdateTypeDef" = ...,
        HttpEndpointDestinationUpdate: "HttpEndpointDestinationUpdateTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the specified destination of the specified delivery stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.update_destination)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html#update_destination)
        """

    async def __aenter__(self) -> "FirehoseClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/client.html)
        """
