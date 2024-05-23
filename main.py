import click
from botocore.exceptions import ClientError as AWSClientError
from botocore.exceptions import EndpointConnectionError as AWSEndpointConnectionError
from docker.errors import APIError as DockerAPIError
from loguru import logger
from pydanclick import from_pydantic

from src.config.settings import settings
from src.core.utils import exception_handler_decorator
from src.modules.cloudwatch.exception_handlers import (
    aws_client_error_handler,
    aws_endpoint_connection_error_handler,
)
from src.modules.docker.exception_handlers import (
    docker_api_error_handler,
    docker_image_not_found_error_handler,
)
from src.modules.docker.exceptions import ImageNotFoundError
from src.modules.general.dto import InputConfigDTO
from src.modules.general.services import start_docker_to_cloudwatch


@click.command(name=settings.MAIN_COMMAND_NAME)
@from_pydantic("input_config", model=InputConfigDTO)  # type: ignore
@exception_handler_decorator(
    {
        AWSClientError: aws_client_error_handler,
        AWSEndpointConnectionError: aws_endpoint_connection_error_handler,
        DockerAPIError: docker_api_error_handler,
        ImageNotFoundError: docker_image_not_found_error_handler,
    },
)
def main(input_config: InputConfigDTO) -> None:
    """CLI tool that streams logs from a Docker container to CloudWatch."""
    logger.info(f"Starting with config: {input_config}")
    start_docker_to_cloudwatch(input_config)
    logger.info("Container finished his job.")


if __name__ == "__main__":
    main()
