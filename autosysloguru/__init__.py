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


import atexit as _atexit
import sys as _sys
from sys import stdout, stderr

from loguru import _Core, _Logger
from loguru._defaults import env

if True:  # * ################## type definitions
    from io import TextIOWrapper
    from logging import Handler
    from typing import Dict, List


# use existing _debug_ else use default
try:
    _debug_
except NameError:
    _debug_: bool = True  # set default value (DEV = True, PROD = False)


class PropagateHandler(Handler):
    """ Handler used to pass messages directly from Loguru to the standard library logging module Logger. Just set it and forget it.

    logger = AutoSysLogger(propagate=True)
    """

    def emit(self, record):
        import logging
        logging.getLogger(record.name).handle(record)


class AutoSysLevelChangeFilter:
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
        levelno = logger.level(self.level).no
        return record['level'].no >= levelno


class AutoSysLoggerError(Exception):
    """ A problem occurred while configuring the logger. """


class LoguruConfig:
    """ Configuration data for AutoSysLoguru """

    def __init__(self, dev_level: str, prod_level: str, dev_handlers: List, prod_handlers: List):
        self.dev_level = dev_level
        self.prod_level = prod_level
        self.dev_handlers = dev_handlers
        self.prod_handlers = prod_handlers
        super().__init__()


def logger_wraps(*, entry=True, exit=True, level='DEBUG'):
    # https://loguru.readthedocs.io/en/stable/resources/recipes.html
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
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
        {'sink': stdout, 'colorize': True,
         'format': '<green>{time}</green> <level>{message}</level>'},
        # 1kb max size forces a new json file for each run
        {'sink': 'output.json', 'serialize': True, 'rotation': '1 KB', 'retention': '10 days'},
        # Set 'False' to not leak sensitive data in prod
        {'sink': 'output.log', 'backtrace': True, 'diagnose': True, 'rotation': '500 MB'}
    ]
    _DEFAULT_PROD_HANDLERS: List = [
        {'sink': stdout, 'colorize': True, 'format': '<green>{time}</green> <level>{message}</level>'},
        {'sink': 'output.log', 'rotation': '500 MB', 'retention': '10 days'}
    ],

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
        debug: bool = False,
        level: str = '',
        propagate: bool = True,
        json: bool = True,
        handlers: Dict = {}
    ):
        # original class init method:
        # _Logger.__init__(self, core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)
        # super().__init__(_Core(), None, 0, False, False, False, False, True, None, {})
        super().__init__(core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)

        self._debug: bool = debug
        self._propagate: bool = propagate
        self._json: bool = json
        self._handlers: List = handlers
        self._level: int
        self.level_filter = AutoSysLevelChangeFilter('WARNING')
        # must be added at handler creation:
        # logger.add(sys.stderr, filter=level_filter, level=0)
        # but can be adjusted dynamically:
        level_filter.level = self.level

        if level:
            self.level(level)
        else:
            _ = self.level

        # if True, logger messages will propagate to stdlib logging module

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
        return {'sink': filename, 'serialize': True, 'rotation': rotation, 'retention': retention},

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
    def __debug(self):
        if not self._debug:
            self._debug = _debug_
        return self._debug

    @__debug.setter
    def __debug(self, value: bool):
        self._debug = bool(value)

    @property
    def __level(self):
        if not self._level:
            from os import environ as _env
            if 'LOGURU_LEVEL' in _env:
                self._level = _env.get('LOGURU_LEVEL', self._level)
            else:  # or use environment default
                if 'LOGURU_DEFAULT_LEVEL' in _env:
                    self._level = _env.get('LOGURU_DEFAULT_LEVEL', self._level)
                else:  # or use hardcoded defaults based on debug boolean flag
                    if self.debug:
                        self._level = self._DEFAULT_DEV_LEVEL
                    else:
                        self._level = self._DEFAULT_PROD_LEVEL
            del _env
            self.LOGGING = self._level != 'NONE'
        return self._level

    @__level.setter
    def __level(self, value):
        if value in stuff:  # todo - find the loguru list of levels
            self._level = value
            self.LOGGING = self._level != 'NONE'

    def _level_name(self):
        self.level(self._level)

    def propagate(self, value):

        if self._propagate:
            logger.configure(handlers=[{'sink': SocketHandler('localhost', 9999)}])
            p_handler = {'sink': PropagateHandler(), filter = self.level_filter, format = '{message}'}
            self.add(PropagateHandler(), format='{message}')

    def _set_default_handler(self):
        """ Remove default (first) handler if one is attached
            Add a new handler based on level attribute
            Add handlers passed in 'handlers' variable."""
        try:
            self.remove(0)
        except ValueError:
            pass

        if self.LOGGING:
            if not self.handlers:
                # default handler
                self.add(stderr, filter=self.level_filter, level=self.level)
            else:
                for handler in self.handlers:
                    self.add(handler, filter=self.level_filter, level=self.level)

        if self.propagate:
            s

        # for name,handler in self.handlers.items():
        #     self.add(handler)

    def config(self, config=None):
        # todo - all this ...
        # check arguments first
        # read environment next
        #   LOGURU_CONFIG_FILENAME
        # read pyproject.toml next
        # read config file next
        # use defaults last
        if not config:
            if self.debug:
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
            raise LoggerError(e)


__all__ = ['logger']


# TODO - pass in list of handlers instead of just one flag

def _get_current_logger():
    """ Returns the current logger instance if one is running,
        else a new instance. """
    try:
        logger = logger or AutoSysLogger(debug=_debug_)
    except NameError:
        logger: AutoSysLogger = AutoSysLogger(debug=_debug_)
    return logger


logger: AutoSysLogger = _get_current_logger()

logger.info(f"Logging is on. Severity level set to '{logger.level}'")
logger.info(f'Current user is {logger.username}')


# this was the original default handler
# if _defaults.LOGURU_AUTOINIT and _sys.stderr:
#     logger.add(_sys.stderr)


_atexit.register(logger.remove)
