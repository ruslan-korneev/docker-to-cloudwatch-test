from src.core.dto import BaseDTO


class InputConfigDTO(BaseDTO):
    docker_image: str
    bash_command: str
    aws_cloudwatch_group: str
    aws_cloudwatch_stream: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
