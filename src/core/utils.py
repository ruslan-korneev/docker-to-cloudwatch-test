from collections.abc import Callable
from datetime import datetime, UTC
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from loguru import logger

from src.modules.general.dto import InputConfigDTO

_P = ParamSpec("_P")
_R = TypeVar("_R")
_ET = TypeVar("_ET", Exception, BaseException)


def utcnow() -> datetime:
    return datetime.now(tz=UTC)


def exception_handler_decorator(
    exception_handlers: dict[type[_ET], Callable[[_ET], None]],
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    def decorator(
        func: Callable[_P, _R],
    ) -> Callable[_P, _R]:

        @wraps(func)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                logger.info("Program terminated by user.")
                exit(0)
            except Exception as e:
                exception_handlers.get(type(e), _default_handler(e))(e)
                exit(1)

        return wrapper

    def _default_handler(e: _ET) -> Callable[[_ET], None]:
        def default_handler(_: _ET) -> None:
            logger.exception(f"An unexpected error occurred: {e}")

        return default_handler

    return decorator


def input_config_decorator(
    func: Callable[Concatenate[InputConfigDTO, _P], _R],
) -> Callable[..., _R]:
    @wraps(func)
    def wrapper(*_: _P.args, **kwargs: _P.kwargs) -> _R:
        input_config = InputConfigDTO.model_validate(kwargs)
        return func(input_config)

    return wrapper
