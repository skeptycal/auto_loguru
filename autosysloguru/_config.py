from logging import Handler
from os import environ

# from loguru._defaults import env
from loguru._logger import Level, Logger

from _exceptions import *

from typing import List, Union


__all__ = ["Handler", "env", "Level", "Logger", "AutoSysLoggerConfig",
           "AutoSysLoggerError", "AutoSysLoggerLevelChangeFilter", "Highlander", "PropagateHandler"]


def env(
        key: Union[str, bool, int],
        type_: Union[str, bool, int] = str,
        default: Union[str, bool, int] = None
) -> Union[str, bool, int]:
    """#### Environment variable reader from Loguru.

        by Delgan (https://github.com/Delgan)

        MIT License

        Reference: https://github.com/Delgan/loguru/blob/master/loguru/_defaults.py

        Args:
            key (str): name of environment variable
            type_ (Union[str, bool, int], optional): value type expected. Defaults to str.
            default (Union[str, bool, int], optional): default return value. Defaults to None.

        Raises:
            AutoSysLoggerValueError: Boolean value was expected but was not found.
            AutoSysLoggerValueError: Integer value was expected but was not found.

        Returns:
            Union[str, bool, int]: value of environment variable else default value
        """

    try:
        val = environ[key]
    except KeyError:
        return default

    if type_ == str:
        return val

    elif type_ == bool:
        if val.lower() in {"1", "true", "yes", "y", "ok", "on", "why not"}:
            return True
        if val.lower() in {"0", "false", "no", "n", "nok", "off", "no way"}:
            return False
        raise AutoSysLoggerValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )

    try:
        return int(val)
    except ValueError:
        raise AutoSysLoggerValueError(
            "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
        ) from None


class AutoSysLoggerConfig:
    """ Configuration data for AutoSysLoguru """

    def __init__(self, debug: bool, dev_level: str, prod_level: str, dev_handlers: List, prod_handlers: List):
        self.dev_level = dev_level
        self.prod_level = prod_level
        self.dev_handlers = dev_handlers
        self.prod_handlers = prod_handlers
        self.debug = debug

    def level(self):
        if self.debug:
            return self.dev_level
        return self.prod_level

    def handlers(self):
        if self.debug:
            return self.dev_handlers
        return self.prod_handlers


class AutoSysLoggerLevelChangeFilter:
    """
    # Dynamically change logger level.

    ```py
    level_filter = AutoSysLevelChangeFilter("WARNING")
    # must be added at handler creation:
    logger.add(sys.stderr, filter=level_filter, level=0)
    # but can be adjusted dynamically:
    level_filter.level = "DEBUG"
    ```

    from loguru documentation 'recipes'
    https://loguru.readthedocs.io/en/stable/resources/recipes.html
    """

    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        levelno = Logger.level(self.level).no
        return record['level'].no >= levelno


class Highlander:
    """ A generic singleton decorator.

        There can be only one ... """

    def __init__(self, cls):
        self._cls = cls

    def __call__(self):
        """ Return _instance if it exists else set and return _instance. """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Highlander
class PropagateHandler(Handler):
    """ Handler used to pass messages directly from Loguru to the standard library logging module Logger. Just set it and forget it.

    logger = AutoSysLogger(propagate=True)
    """

    def emit(self, record):
        import logging
        logging.getLogger(record.name).handle(record)


LOGURU_AUTOINIT = env("LOGURU_AUTOINIT", bool, True)

LOGURU_FORMAT = env(
    "LOGURU_FORMAT",
    str,
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
LOGURU_FILTER = env("LOGURU_FILTER", str, None)
LOGURU_LEVEL = env("LOGURU_LEVEL", str, "DEBUG")
LOGURU_COLORIZE = env("LOGURU_COLORIZE", bool, None)
LOGURU_SERIALIZE = env("LOGURU_SERIALIZE", bool, False)
LOGURU_BACKTRACE = env("LOGURU_BACKTRACE", bool, True)
LOGURU_DIAGNOSE = env("LOGURU_DIAGNOSE", bool, True)
LOGURU_ENQUEUE = env("LOGURU_ENQUEUE", bool, False)
LOGURU_CATCH = env("LOGURU_CATCH", bool, True)

LOGURU_TRACE_NO = env("LOGURU_TRACE_NO", int, 5)
LOGURU_TRACE_COLOR = env("LOGURU_TRACE_COLOR", str, "<cyan><bold>")
LOGURU_TRACE_ICON = env("LOGURU_TRACE_ICON", str, "✏️")  # Pencil

LOGURU_DEBUG_NO = env("LOGURU_DEBUG_NO", int, 10)
LOGURU_DEBUG_COLOR = env("LOGURU_DEBUG_COLOR", str, "<blue><bold>")
LOGURU_DEBUG_ICON = env("LOGURU_DEBUG_ICON", str, "🐞")  # Lady Beetle

LOGURU_INFO_NO = env("LOGURU_INFO_NO", int, 20)
LOGURU_INFO_COLOR = env("LOGURU_INFO_COLOR", str, "<bold>")
LOGURU_INFO_ICON = env("LOGURU_INFO_ICON", str, "ℹ️")  # Information

LOGURU_SUCCESS_NO = env("LOGURU_SUCCESS_NO", int, 25)
LOGURU_SUCCESS_COLOR = env("LOGURU_SUCCESS_COLOR", str, "<green><bold>")
LOGURU_SUCCESS_ICON = env("LOGURU_SUCCESS_ICON", str, "✔️")  # Heavy Check Mark

LOGURU_WARNING_NO = env("LOGURU_WARNING_NO", int, 30)
LOGURU_WARNING_COLOR = env("LOGURU_WARNING_COLOR", str, "<yellow><bold>")
LOGURU_WARNING_ICON = env("LOGURU_WARNING_ICON", str, "⚠️")  # Warning

LOGURU_ERROR_NO = env("LOGURU_ERROR_NO", int, 40)
LOGURU_ERROR_COLOR = env("LOGURU_ERROR_COLOR", str, "<red><bold>")
LOGURU_ERROR_ICON = env("LOGURU_ERROR_ICON", str, "❌")  # Cross Mark

LOGURU_CRITICAL_NO = env("LOGURU_CRITICAL_NO", int, 50)
LOGURU_CRITICAL_COLOR = env("LOGURU_CRITICAL_COLOR", str, "<RED><bold>")
LOGURU_CRITICAL_ICON = env("LOGURU_CRITICAL_ICON", str, "☠️")  # Skull and Crossbones
