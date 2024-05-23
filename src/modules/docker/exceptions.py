class ImageNotFoundError(Exception):
    docker_image: str

    def __init__(self, docker_image: str) -> None:
        self.docker_image = docker_image
        super().__init__(f"Docker image not found: {docker_image}")

    def __str__(self) -> str:
        return f"Docker image not found: {self.docker_image}"
