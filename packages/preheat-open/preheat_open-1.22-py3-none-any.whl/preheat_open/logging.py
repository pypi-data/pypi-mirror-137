import inspect
import logging
import sys
import warnings
from typing import Optional, Union

from .singleton import Singleton

LOG_FORMAT = "%(asctime)-23s  %(levelname)-8s  %(name)-32s  %(message)-160s  .(%(filename)s:%(lineno)d)"


class Logging(metaclass=Singleton):
    def __init__(self, stack_level: int = 0):
        self.stack_level = 2 + stack_level
        if sys.gettrace() is None:
            logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        else:
            logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    def _get_logger(self, failsafe: bool = True, stack_level: int = 0):
        try:
            frame = inspect.stack()[self.stack_level + stack_level]
            mod = inspect.getmodule(frame[0])
            # return logging.getLogger(mod.__package__)
            return logging.getLogger(mod.__name__.split('.')[-1])
        except Exception as e:
            if failsafe is True:
                warnings.warn(
                    "There was an issue in accessing the desired logger - defaulting to a failsafe one"
                )
                return logging.getLogger("Failsafe-log (preheat_open)")
            else:
                raise e

    def set_level(self, level: Union[str, int]) -> None:
        logging.basicConfig(level=level, force=True)

    def error(self, msg: str, exception: Optional[Exception], *args, **kwargs) -> None:
        if exception is None:
            for line in msg.split("\n"):
                self._get_logger().error(
                    line, stacklevel=self.stack_level, *args, **kwargs
                )
        else:
            try:
                raise exception
            except Exception as e:
                for line in msg.split("\n"):
                    self._get_logger().exception(
                        line, stacklevel=self.stack_level, *args, **kwargs
                    )

    def warning(self, msg: Union[str, Warning], *args, **kwargs) -> None:
        warnings.warn(msg)
        if isinstance(msg, Warning):
            msg = str(msg)
        for line in msg.split("\n"):
            self._get_logger().warning(
                line, stacklevel=self.stack_level, *args, **kwargs
            )

    def info(self, msg: str, *args, **kwargs) -> None:
        for line in msg.split("\n"):
            self._get_logger().info(line, stacklevel=self.stack_level, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        for line in msg.split("\n"):
            self._get_logger().debug(line, stacklevel=self.stack_level, *args, **kwargs)


def logging_level(level: str) -> int:
    """
    Converts a string to a logging level

    :param level: logging level (debug, info, warning, error, critical)
    :type level:
    :return: logging level identifier (in logging package)
    :rtype:
    """
    if isinstance(level, str):
        str_level = level.lower()
        if str_level == "debug":
            log_level = logging.DEBUG
        elif str_level == "info":
            log_level = logging.INFO
        elif str_level == "warning":
            log_level = logging.WARNING
        elif str_level == "error":
            log_level = logging.ERROR
        elif str_level == "critical":
            log_level = logging.CRITICAL
        else:
            raise Exception(f"Illegal logging level ({level})")

        return log_level

    else:
        raise Exception("Only logging levels in string format are supported for now")


def set_logging_level(level: str) -> None:
    """
    Sets the logging level

    :param level: logging level (debug, info, warning, error, critical)
    :type level:
    """
    Logging().set_level(logging_level(level))
