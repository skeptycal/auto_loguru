#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    from log import logger
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

__version__ = '0.1.0'

import atexit as _atexit
import sys as _sys
from loguru import _Logger, _Core

try:
    _debug_
except NameError:
    _debug_: bool = True

# original class init method:
# _Logger.__init__(self, core, exception, depth, record, lazy, colors, raw, capture, patcher, extra)

# TODO - pass in list of handlers instead of just one flag
class AutoSysLogger(_Logger):
    """ Extra Features ...

        If level is set to "NONE", the logger will still load but no handlers
        will be added. """

    LOGURU_LEVEL: str = ""
    DEFAULT_PROD_VALUE: str = "SUCCESS"  # for no logging, use NONE
    DEFAULT_DEV_VALUE: str = "TRACE"
    LOGGING: bool = False

    def __init__(
        self,
        core=_Core(),
        exception=None,
        depth=0,
        record=False,
        lazy=False,
        colors=True,
        raw=False,
        capture=True,
        patcher=None,
        extra={},
        debug=False,
        # handlers = {}
    ):
        super().__init__(_Core(), None, 0, False, False, False, False, True, None, {})
        self._autosys_defaults(debug=debug)

    def _autosys_defaults(self, debug: bool = False):
        """ Run once from self.__init__. """

        # set default severity
        try:
            if debug:
                self.LOGURU_LEVEL = self.DEFAULT_DEV_VALUE
            else:
                self.LOGURU_LEVEL = self.DEFAULT_PROD_VALUE
        except:
            self.LOGURU_LEVEL = self.DEFAULT_PROD_VALUE

        if self.LOGURU_LEVEL != "NONE":
            # set LOGGING flag if self.LOGURU_LEVEL is specified
            self.LOGGING = True

            from os import environ as _env

            # check for environment variable that overrides default value
            self.LOGURU_LEVEL = _env.get("LOGURU_LEVEL", self.LOGURU_LEVEL)

            # remove default handler
            try:
                self.remove(0)
            except ValueError:
                pass

            # setup new handler with correct severity
            self.add(_sys.stderr, level=self.LOGURU_LEVEL)
            # self.info(f"Logging is on. Severity level set to {self.LOGURU_LEVEL}")
            del _env


__all__ = ["logger"]


logger = AutoSysLogger(
    core=_Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=True,
    raw=False,
    capture=True,
    patcher=None,
    extra={},
    debug=_debug_,
)


logger.info(f"Logging is on. Severity level set to '{logger.LOGURU_LEVEL}'")

# this was the original default handler
# if _defaults.LOGURU_AUTOINIT and _sys.stderr:
#     logger.add(_sys.stderr)

_atexit.register(logger.remove)
