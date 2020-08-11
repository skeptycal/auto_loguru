__all__ = ["AutoSysLoggerError", "AutoSysLoggerKeyError",
           "AutoSysLoggerTypeError", "AutoSysLoggerValueError"]


class AutoSysLoggerError(Exception):
    """ A problem occurred while configuring the logger. """


class AutoSysLoggerKeyError(KeyError):
    """ An invalid key was encountered during logging. """


class AutoSysLoggerTypeError(TypeError):
    """ An invalid type was encountered during logging. """


class AutoSysLoggerValueError(ValueError):
    """ An invalid value was encountered during logging. """
