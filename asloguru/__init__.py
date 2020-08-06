#!/usr/bin/env python3
""" AutoSys loguru log wrapper used to set default log level
    of default log.

    Use an environment variable set in .bashprofile (or .zshrc, etc):

    ```sh
    LOGURU_LEVEL=TRACE
    ```

    or place a constant below in place of "TRACE":
    ```
    LOGURU_LEVEL: str = environ.get("LOGURU_LEVEL", "TRACE")
    ```

    then run this from the main script
    ```
    from asloguru import logger
    ```
    ---
    System utilities for Python.

    Part of the [AutoSys][1] package

    Copyright (c) 2018 [Michael Treanor][2]

    AutoSys is licensed under the [MIT License][3]

    [1]: https://www.github.com/skeptycal/autosys
    [2]: https://www.twitter.com/skeptycal
    [3]: https://opensource.org/licenses/MIT
    """


import atexit as _atexit
import sys as _sys

from loguru import _Core
from loguru import _Logger

from arepl_dump import dump


from typing import List, Dict

try:
    _debug_ == True
except NameError:
    _debug_: bool = True

# TODO - pass in list of handlers instead of just one flag

def get_current_logger():
    """ Returns the logger instance used in this module,
        or a new instance if none is available. """
    global logger
    logger = logger or AutoSysLogger(debug=_debug_)
    return logger

dump()
class AutoSysLogger(_Logger):
    """ Smoother defaults for the awesome Loguru logger.

        the logger is loaded with a level specified by:

        - environment variable LOGURU_LEVEL
            (e.g. LOGURU_LEVEL='INFO')
        - environment variable LOGURU_DEFAULT_LEVEL
        - dev or production default (based on _debug_ bool flag)
            _DEFAULT_PROD_VALUE: str = 'SUCCESS'
            _DEFAULT_DEV_VALUE: str = 'TRACE'

        If level is set to "NONE", the logger will still load but no handlers
        will be added. """

    LOGURU_LEVEL: str = ''

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
        handlers: Dict = {}
    ):
        # original class init method:
        # _Logger.__init__(self, core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)
        # super().__init__(_Core(), None, 0, False, False, False, False, True, None, {})
        super().__init__(core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)

        self.debug = debug
        if level:
            self.LOGURU_LEVEL = level
        self.handlers = handlers

        self._autosys_defaults(debug=debug)

    def _autosys_defaults(self, debug: bool = False):
        """ Run once from self.__init__. """

        if not self.LOGURU_LEVEL:
            if self.debug:
                self.LOGURU_LEVEL = self._DEFAULT_DEV_VALUE
            else:
                self.LOGURU_LEVEL = self._DEFAULT_PROD_VALUE



        self.LOGURU_LEVEL = _env.get('LOGURU_LEVEL', self.LOGURU_LEVEL)

        if self.LOGURU_LEVEL == 'NONE':
            self.LOGGING = False
        else:
            self.LOGGING = True

        # remove default handler
        try:
            self.remove(0)
        except ValueError:
            pass

        # setup new handler with correct severity
        if self.LOGGING:
            self.add(_sys.stderr, level=self.LOGURU_LEVEL)
            # self.info(f"Logging is on. Severity level set to {self.LOGURU_LEVEL}")
            del _env


__all__ = ['logger']

# if not get_current_logger():
#     logger = AutoSysLogger(
#         core=_Core(),
#         exception=None,
#         depth=0,
#         record=False,
#         lazy=False,
#         colors=True,
#         raw=False,
#         capture=True,
#         patcher=None,
#         extra={},
#         debug=_debug_,
#     )

logger=get_current_logger()

logger.info(f"Logging is on. Severity level set to '{logger.LOGURU_LEVEL}'")


# this was the original default handler
# if _defaults.LOGURU_AUTOINIT and _sys.stderr:
#     logger.add(_sys.stderr)


_atexit.register(logger.remove)
