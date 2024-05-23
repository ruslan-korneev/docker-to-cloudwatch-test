from typing import Any, TYPE_CHECKING

from docker import from_env as docker_from_env
from docker.errors import ImageNotFound as DockerImageNotFound
from loguru import logger

from src.modules.docker.exceptions import ImageNotFoundError
from src.modules.general.dto import InputConfigDTO

if TYPE_CHECKING:
    from docker.models.containers import Container


class DockerClient:
    """Docker client wrapper for starting and stopping containers as context manager."""

    def __init__(self, input_config: InputConfigDTO) -> None:
        logger.info("Initializing DockerClient ...")
        self._docker_image = input_config.docker_image
        self._bash_command = input_config.bash_command

    def __enter__(self) -> "Container":
        try:
            self._container = self._create_container()
        except DockerImageNotFound as e:
            raise ImageNotFoundError(self._docker_image) from e

        logger.info("Container started.")
        return self._container

    def __exit__(self, *args: object, **kwargs: Any) -> None:
        self._container.remove(force=True)
        logger.info("Container removed.")

    def _create_container(self) -> "Container":
        return docker_from_env().containers.run(
            self._docker_image,
            ["/bin/bash", "-c", self._bash_command],
            detach=True,
            tty=True,
            stdout=True,
            stderr=True,
        )
