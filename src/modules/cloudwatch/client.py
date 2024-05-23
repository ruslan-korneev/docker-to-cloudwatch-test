import contextlib
from collections.abc import Callable
from functools import wraps
from typing import cast, Concatenate, ParamSpec, Self, TypeVar

import boto3
from loguru import logger
from mypy_boto3_logs.client import CloudWatchLogsClient as BotoCloudWatchLogsClient

from src.modules.cloudwatch.dto import LogEvents
from src.modules.general.dto import InputConfigDTO

_S = TypeVar("_S", bound="AWSCloudWatchLogsClient")
_R = TypeVar("_R")
_P = ParamSpec("_P")


def _require_client(
    func: Callable[Concatenate[_S, _P], _R],
) -> Callable[Concatenate[_S, _P], _R]:
    @wraps(func)
    def wrapper(self: _S, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        assert self._client is not None, "AWS client is not initialized."
        return func(self, *args, **kwargs)

    return wrapper


class AWSCloudWatchLogsClient:
    """AWS CloudWatch Logs client wrapper."""

    _client: BotoCloudWatchLogsClient | None = None
    _sequence_token: str | None = None

    def __init__(self, input_config: InputConfigDTO) -> None:
        logger.debug("Initializing AWSCloudWatchLogsClient ...")
        self._aws_region = input_config.aws_region
        self._aws_cloudwatch_stream = input_config.aws_cloudwatch_stream
        self._aws_cloudwatch_group = input_config.aws_cloudwatch_group
        self._aws_access_key_id = input_config.aws_access_key_id
        self._aws_secret_access_key = input_config.aws_secret_access_key

    def prepare_logs(self) -> None:
        self._create_cloudwatch_log_group()
        self._create_cloudwatch_log_stream()

    def __enter__(self) -> Self:
        logger.info("Initializing AWS CloudWatch Logs client ...")
        self._client = boto3.client(
            service_name="logs",
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            region_name=self._aws_region,
        )
        return self

    def __exit__(self, *args: object, **kwargs: object) -> None:
        _client = cast(BotoCloudWatchLogsClient, self._client)
        _client.close()

    @_require_client
    def _create_cloudwatch_log_group(self) -> None:
        _client = cast(BotoCloudWatchLogsClient, self._client)
        with contextlib.suppress(
            _client.exceptions.ResourceAlreadyExistsException,
        ):
            _client.create_log_group(logGroupName=self._aws_cloudwatch_group)

    @_require_client
    def _create_cloudwatch_log_stream(self) -> None:
        _client = cast(BotoCloudWatchLogsClient, self._client)
        with contextlib.suppress(
            _client.exceptions.ResourceAlreadyExistsException,
        ):
            _client.create_log_stream(
                logGroupName=self._aws_cloudwatch_group,
                logStreamName=self._aws_cloudwatch_stream,
            )

    @_require_client
    def stream_logs_to_cloudwatch(self, log_events: LogEvents) -> None:
        logger.info(f"Sending log events: {log_events}")
        _client = cast(BotoCloudWatchLogsClient, self._client)

        while True:
            try:
                params = {
                    "logGroupName": self._aws_cloudwatch_group,
                    "logStreamName": self._aws_cloudwatch_stream,
                    "logEvents": log_events.model_dump(),
                }
                if self._sequence_token:
                    params["sequenceToken"] = self._sequence_token

                logger.debug(f"Sending log events: {params}")
                response = _client.put_log_events(**params)
                logger.debug(f"Log events sent. Response: {response}")
                self._sequence_token: str = response["nextSequenceToken"]
                break
            except _client.exceptions.InvalidSequenceTokenException as e:
                self._sequence_token: str = e.response["expectedSequenceToken"]

        logger.info("Log events sent.")
