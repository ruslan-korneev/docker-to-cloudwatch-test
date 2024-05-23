import sys
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()
    DEBUG: bool = False

    MAIN_COMMAND_NAME: str = "Docker container logs to CloudWatch"
    LOG_EVENTS_PER_BATCH: int = 10
    DOCKER_HOST: str = ""

    model_config = SettingsConfigDict(
        env_file=f"{ROOT_DIR}/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        extra="ignore",  # ignores extra keys from env file
    )


settings = Settings()

# Logging Configuration
logger.remove(0)
logger.add(
    sys.stderr,
    format="<red>[{level}]</red> Message : <green>{message}</green> @ {time:YYYY-MM-DD HH:mm:ss}",
    colorize=True,
    level=("DEBUG" if settings.DEBUG else "INFO"),
    backtrace=True,
    diagnose=True,
)
