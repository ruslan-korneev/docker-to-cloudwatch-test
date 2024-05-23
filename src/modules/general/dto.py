from typing import Annotated

from pydantic import Field

from src.core.dto import BaseDTO


class InputConfigDTO(BaseDTO):
    docker_image: Annotated[
        str,
        Field(description="Name of docker image to build a container"),
    ]
    bash_command: Annotated[
        str,
        Field(description="Bash command to execute on container startup"),
    ]
    aws_cloudwatch_group: Annotated[
        str,
        Field(description="AWS CloudWatch Log Group name"),
    ]
    aws_cloudwatch_stream: Annotated[
        str,
        Field(description="AWS CloudWatch Log Stream name"),
    ]
    aws_access_key_id: Annotated[str, Field(description="AWS Access Key ID")]
    aws_secret_access_key: Annotated[str, Field(description="AWS Secret Access Key")]
    aws_region: Annotated[str, Field(description="AWS Region")]
