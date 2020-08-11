# AutoSysLoguru

> A wrapper for the awesome Loguru logger package. Allows simpler configuration of the default logger level and handlers.

## Simple Configuration:

### _Problem: The default options based on environment variables are limited and tedious._

> To simply turn off the default logger handler (stderr), set the environment variable:

    LOGURU_AUTOINIT=False

> No logging will occur until another handler is added. There are many other options, but environment variables can be a pain. A better option is to set defaults per project:

---

To specify configuration options, it would be handy to do it in a config file or in pyproject.toml. You only have to set it up once. Config files can easily be copied, pasted, and tweaked.

1.  Set environment variables (e.g. in .bashprofile, .profile, .zshrc, or virtual environment):

        LOGURU_LEVEL=TRACE
        LOGURU_CONFIG_FILENAME=~/path/to/some_file.py

2.  Use a configuration section in `pyproject.toml`:

    ```toml
    [autosysloguru]
    dev_level = "DEBUG"
    dev_handlers = [
        { sink = "sys.stdout", colorize = "True", format = "<green>{time}</green> <level>{message}</level>" },
        { sink = "output.json", serialize = "True" },
        # Set 'False' to not leak sensitive data in production
        { sink = "output.log", backtrace = "True", diagnose = "True", rotation = "500 MB" }
    ]
    prod_level = "SUCCESS"
    prod_handlers = [
        { sink = "sys.stdout", colorize = "True", format = "<green>{time}</green> <level>{message}</level>" },
        { sink = "output.log", rotation = "500 MB", retention = "10 days" }
    ]
    ```

3.  Use a custom python configuration script:

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

---

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
[autosys]: https://www.github.com/skeptycal/as_loguru
