from docker.errors import APIError as DockerAPIError
from loguru import logger

from src.modules.docker.exceptions import ImageNotFoundError


def docker_api_error_handler(e: DockerAPIError) -> None:
    logger.error(f"DockerAPIError: Container has been removed: {e}")


def docker_image_not_found_error_handler(e: ImageNotFoundError) -> None:
    logger.error(f"Docker image not found: {e.docker_image}")
