#!/usr/bin/env python3
""" AutoSysLoguru is a wrapper for the awesome Loguru logger package.

    Allows simpler configuration of default logger and handlers

    Options:
    - Use environment variables set in .bashprofile (or .zshrc, etc):

        ```sh
        LOGURU_LEVEL=TRACE
        LOGURU_CONFIG_FILENAME=~/path/to/some_file.py
        ```
    - Use a configuration section in pyproject.toml

    ```toml
    [autosysloguru]
    dev_level = 'DEBUG'
    prod_level = 'SUCCESS'
    dev_handlers = [
        {sink= "sys.stdout", colorize = "True", format = "<green>{time}</green> <level>{message}</level>"},
        {sink = "output.json", serialize = "True"},
        # Set 'False' to not leak sensitive data in prod
        {sink = "output.log", backtrace = "True", diagnose = "True", rotation = "500 MB"}
    ]
    prod_handlers = [
        {sink = "sys.stdout", colorize = "True", format = "<green>{time}</green> <level>{message}</level>"},
        {sink = "output.log", rotation = "500 MB", retention = "10 days"}
    ]
    ```

    - Use a custom python configuration script

    ```py
    dev_level: str = 'DEBUG'
    prod_level: str = 'SUCCESS'

    dev_handlers: List = [
        {"sink": sys.stdout, "colorize": True, "format": "<green>{time}</green> <level>{message}</level>"},
        {"sink": "output.json", "serialize": True},
        # Set 'False' to not leak sensitive data in prod
        {"sink": "output.log", "backtrace": True, "diagnose": True, "rotation": "500 MB"}
    ]

    prod_handlers: List = [
        {"sink": sys.stdout, "colorize": True, "format": "<green>{time}</green> <level>{message}</level>"},
        {"sink": "output.log", "rotation": "500 MB", "retention": "10 days"}
    ]
    ```

    Then just do the simplest thing ever invented for logging:

    ```py
    from autosysloguru import logger
    ```

    That's it! Nothing else! It just works.

    ---
    Part of the [AutoSys][1] package

    System utilities for Python.

    Copyright (c) 2018 [Michael Treanor][2]

    AutoSys is licensed under the [MIT License][3]

    [1]: https://www.github.com/skeptycal/autosys
    [2]: https://www.twitter.com/skeptycal
    [3]: https://opensource.org/licenses/MIT
    """

from __future__ import annotations

import atexit as _atexit
import sys as _sys

from _config import (
    AutoSysLoggerConfig, AutoSysLoggerError,
    AutoSysLoggerLevelChangeFilter, Highlander,
    PropagateHandler, env)

from loguru import _Core, _Logger

from typing import Dict, List


_debug_: bool = True  # set default value (DEV = True, PROD = False)

__version__: str = "0.5.0"


def logger_wraps(*, entry=True, exit=True, level='DEBUG'):
    # https://loguru.readthedocs.io/en/stable/resources/recipes.html
    def wrapper(func):
        name = func.__name__
        from functools import wraps

        @wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


@Highlander
class AutoSysLogger(_Logger):
    """ Smoother defaults for the awesome Loguru logger.

        the logger is loaded with a level specified by:

        - environment variable LOGURU_LEVEL
            (e.g. LOGURU_LEVEL='INFO')
        - environment variable LOGURU_DEFAULT_LEVEL
        - dev or production default (based on _debug_ bool flag)
            _DEFAULT_PROD_LEVEL: str = 'SUCCESS'
            _DEFAULT_DEV_LEVEL: str = 'TRACE'

        If level is set to "NONE", the logger will still load but no handlers
        will be added. """

    _user: str = ''
    _level: str = ''
    _propagate: bool = False

    _DEFAULT_PROD_LEVEL: str = 'SUCCESS'
    _DEFAULT_DEV_LEVEL: str = 'TRACE'
    _DEFAULT_DEV_HANDLERS: List = [
        {'sink': _sys.stdout, 'colorize': True,
         'format': '<green>{time}</green> <level>{message}</level>'},
        # 1kb max size forces a new json file for each run
        {'sink': 'output.json', 'serialize': True, 'rotation': '1 KB', 'retention': '10 days'},
        # Set 'False' to not leak sensitive data in prod
        {'sink': 'output.log', 'backtrace': True, 'diagnose': True, 'rotation': '500 MB'}
    ]
    _DEFAULT_PROD_HANDLERS: List = [
        {'sink': _sys.stdout, 'colorize': True, 'format': '<green>{time}</green> <level>{message}</level>'},
        {'sink': 'output.log', 'rotation': '500 MB', 'retention': '10 days'}
    ]

    LOGGING: bool = True

    def __init__(
        self,
        core: _Core = _Core(),
        exception: str = None,
        depth: int = 0,
        record: bool = False,
        lazy: bool = False,
        colors: bool = True,
        raw: bool = False,
        capture: bool = True,
        patcher: str = None,
        extra: Dict = {},
        debug: bool = _debug_,
        level: str = '',
        propagate: bool = True,
        json: bool = True,
        handlers: Dict = {}
    ):
        # original class init method:
        # _Logger.__init__(self, core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)
        # super().__init__(_Core(), None, 0, False, False, False, False, True, None, {})
        super().__init__(core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)

        # if True, logger will default to DEV mode (insecure, may contain secrets)
        self._debug: bool = debug
        # if True, logger messages will propagate to stdlib logging module
        self._propagate: bool = propagate
        # if True, a separate json file is generated
        self._json: bool = json

        self.configsettings: AutoSysLoggerConfig()
        # If True, contains a list of handlers to start with
        self._handlers: List = handlers
        # If True, this is the default starting level for the logger
        self._level: str = level
        if level:
            self.log_level(level)
        else:
            _ = self.log_level

        self._level_filter = AutoSysLoggerLevelChangeFilter('WARNING')
        self._level_filter.level = self.log_level

        self._set_default_handler()

    def get_handler(self, **args):
        retval: Dict = {}
        for name, value in args.items():
            retval[name] = value
        return retval

    def json_handler(self, filename='output.json', rotation='1 B', retention='10 days'):
        # 1 B max size forces a new json file for each run
        retval = {'sink': filename, 'serialize': True}
        if rotation:
            retval['rotation'] = rotation
        if retention:
            retval['retention'] = retention
        return retval

    @property
    def username(self):
        if not self._user:
            from os import getuid
            from pwd import getpwuid
            self._user = getpwuid(getuid())[0]
            del getuid
            del getpwuid
        return self._user

    @property
    def debug_flag(self):
        if not self._debug:
            self._debug = _debug_
        return self._debug

    @debug_flag.setter
    def debug_flag(self, value: bool):
        self._debug = bool(value)

    @property
    def log_level(self):
        if not self._level:  # if no parameter, use environment variable setting
            # def env(key, type_, default=None):
            self._level = env('LOGURU_LEVEL', '')
        if not self._level:  # or use hardcoded defaults based on debug boolean flag
            if self.debug_flag:
                self._level = self._DEFAULT_DEV_LEVEL
            else:
                self._level = self._DEFAULT_PROD_LEVEL
        self.LOGGING = self._level != 'NONE'
        return self._level

    @log_level.setter
    def log_level(self, value):
        if value in self._core.levels:
            self._level = value
            self.LOGGING = self._level != 'NONE'

    def _level_name(self):
        self.log_level(self._level)

    def propagate(self, value):
        if self._propagate:
            p_handler = {'sink': PropagateHandler(), 'filter': self._level_filter,
                         'format': '{message}'}
            self.add(p_handler)

    def _set_default_handler(self):
        """ Remove default (first) handler if one is attached
            Add a new handler based on level attribute
            Add handlers passed in 'handlers' variable."""
        try:
            # self.remove(0)
            pass
        except ValueError:
            pass

        if self.LOGGING:
            if not self._handlers:
                # default handler
                # logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
                pass
                # todo - some stupid error here ???
                # todo - ValueError: Tag "<stderr>" does not corespond to any known ansi directive, make sure you did not misspelled it (or prepend '\' to escape it)
                # self.add(_sys.stderr)
                self.add(sink=_sys.stderr, filter=self._level_filter, level=self.log_level)
            else:
                for handler in self.handlers:
                    self.add(handler, filter=self._level_filter, level=self.log_level)

        if self.propagate:
            pass

    def config(self, config=None):
        # todo - all this ...
        # check arguments first
        # read environment next
        #   LOGURU_CONFIG_FILENAME
        # read pyproject.toml next
        # read config file next
        # use defaults last
        if not config:
            if self.debug_flag:
                # DEV MODE OPTIONS
                new_handlers = self._DEFAULT_DEV_HANDLERS
                pass
            else:
                # PRODUCTION MODE OPTIONS
                new_handlers = self._DEFAULT_PROD_HANDLERS
                pass

            self.config = {
                'handlers': new_handlers,
                'extra': {'user': self.username}
            }

        try:
            self.configure(**config)
        except Exception as e:
            raise AutoSysLoggerError(e)


__all__ = ['logger']

logger: AutoSysLogger = AutoSysLogger()

# logger.add(_sys.stderr)

print(logger.log_level)
print(logger.debug_flag)
logger.debug(f'stuff')
logger.info(f"Logging is on. Severity level set to '{logger.level}'")
logger.info(f'Current user is {logger.username}')


# this was the original default handler
# if _defaults.LOGURU_AUTOINIT and _sys.stderr:
#     logger.add(_sys.stderr)


_atexit.register(logger.remove)
