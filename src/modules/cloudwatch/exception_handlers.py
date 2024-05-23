from botocore.exceptions import ClientError as AWSClientError
from botocore.exceptions import EndpointConnectionError as AWSEndpointConnectionError
from loguru import logger


def aws_client_error_handler(e: AWSClientError) -> None:
    logger.error(f"Error initializing AWS CloudWatch Logs client: {e}")


def aws_endpoint_connection_error_handler(e: AWSEndpointConnectionError) -> None:
    logger.error(f"Error connecting to AWS CloudWatch Logs: {e}")
