from loguru import logger

from src.config.settings import settings
from src.modules.cloudwatch.client import AWSCloudWatchLogsClient
from src.modules.cloudwatch.dto import LogEvent, LogEvents
from src.modules.docker.client import DockerClient
from src.modules.general.dto import InputConfigDTO


def start_docker_to_cloudwatch(input_config: InputConfigDTO) -> None:
    """Starts a Docker container and streams logs to CloudWatch."""
    with (
        DockerClient(input_config) as container,
        AWSCloudWatchLogsClient(input_config) as cloudwatch_client,
    ):
        cloudwatch_client.prepare_logs()
        log_events: list[LogEvent] = []

        current_line = ""
        for char in container.logs(follow=True, stream=True):
            try:
                decoded_char = char.decode("utf-8")
            except UnicodeDecodeError:
                continue

            # processing the current line
            current_line += decoded_char
            if decoded_char != "\n":
                continue

            logger.debug(f"Current Line: {current_line}")
            log_event = LogEvent(message=current_line.strip())
            log_events.append(log_event)

            current_line = ""

            # sending logs in batches
            if len(log_events) >= settings.LOG_EVENTS_PER_BATCH:
                cloudwatch_client.stream_logs_to_cloudwatch(LogEvents(log_events))
                log_events = []

        # sending the last batch
        if len(log_events) > 0:
            cloudwatch_client.stream_logs_to_cloudwatch(LogEvents(log_events))
