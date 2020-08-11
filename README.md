<p style="float: right;">
    <img alt="Skeptycal logo" width=100 src="https://avatars0.githubusercontent.com/u/26148512?s=460&u=351b13d46c1b95745bad1a8efab23abd866c5a1a&v=4">
</p>

# AutoSysLoguru

### Fancy defaults for the awesome [Loguru][loguru] logger by [Delgan][delgan]!

## Install:

```sh
pip install autosysloguru
```

## Usage

The simplest thing ever invented for logging:

```py
from autosysloguru import logger
logger.info('This is a message!')
```

## _That's it! Nothing else! It just works._

---

## Options:

If you want any of these defaults, you only have to set it up once. Config files can easily be copied and pasted.

-   ### Set environment variables (e.g. in .bashprofile, .profile, or .zshrc):

    ```sh
    LOGURU_LEVEL=TRACE
    LOGURU_CONFIG_FILENAME=~/path/to/some_file.py
    ```

-   ### Use a configuration section in pyproject.toml

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

-   ### Use a custom python configuration script

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

    # load the configuration from AutoSysLoguru

    logger.config()
    ```

---

> ## Part of the [AutoSys][1] package

> _System utilities for Python on macOS._

> [![macOS Version](https://img.shields.io/badge/macOS-10.16%20Big%20Sur-orange?logo=apple)](https://www.apple.com) [![GitHub Pipenv locked Python version](https://img.shields.io/badge/Python-3.8-yellow?color=3776AB&logo=python&logoColor=yellow)](https://www.python.org/)

> _Copyright (c) 2018 [Michael Treanor][2]_

> [![Twitter Follow](https://img.shields.io/twitter/follow/skeptycal.svg?style=social)][link_twitter] [![GitHub followers](https://img.shields.io/github/followers/skeptycal.svg?label=GitHub&style=social)][link_github]

> _AutoSys is licensed under the [MIT License][3]_

> [![License](https://img.shields.io/badge/License-MIT-darkblue)](https://skeptycal.mit-license.org/1976/)

## Contributions Welcome!

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?logo=prettier)](https://github.com/prettier/prettier)

**Please feel free to offer suggestions and changes** (contribution instructions below). I have been coding for many years, but mostly as a side activity ... as a tool to assist me in other endeavors ... so I have not had the 'hard time' invested of constant coding that many of you have.

> Below is information from the original project repo.

---

<p align="center">
    <a href="#readme">
        <img alt="Loguru logo" src="https://raw.githubusercontent.com/Delgan/loguru/master/docs/_static/img/logo.png">
        <!-- Logo credits: Sambeet from Pixaday -->
        <!-- Logo fonts: Comfortaa + Raleway -->
    </a>
</p>
<p align="center">
    <a href="https://pypi.python.org/pypi/loguru"><img alt="Pypi version" src="https://img.shields.io/pypi/v/loguru.svg"></a>
    <a href="https://pypi.python.org/pypi/loguru"><img alt="Python versions" src="https://img.shields.io/badge/python-3.5%2B%20%7C%20PyPy-blue.svg"></a>
    <a href="https://loguru.readthedocs.io/en/stable/index.html"><img alt="Documentation" src="https://img.shields.io/readthedocs/loguru.svg"></a>
    <a href="https://travis-ci.com/Delgan/loguru"><img alt="Build status" src="https://img.shields.io/travis/Delgan/loguru/master.svg"></a>
    <a href="https://codecov.io/gh/delgan/loguru/branch/master"><img alt="Coverage" src="https://img.shields.io/codecov/c/github/delgan/loguru/master.svg"></a>
    <a href="https://www.codacy.com/app/delgan-py/loguru/dashboard"><img alt="Code quality" src="https://img.shields.io/codacy/grade/4d97edb1bb734a0d9a684a700a84f555.svg"></a>
    <a href="https://github.com/Delgan/loguru/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/delgan/loguru.svg"></a>
</p>
<p align="center">
    <a href="#readme">
        <img alt="Loguru logo" src="https://raw.githubusercontent.com/Delgan/loguru/master/docs/_static/img/demo.gif">
    </a>
</p>

---

**Loguru** is a library which aims to bring enjoyable logging in Python.

Did you ever feel lazy about configuring a logger and used `print()`
instead?... I did, yet logging is fundamental to every application and
eases the process of debugging. Using **Loguru** you have no excuse not
to use logging from the start.

Also, this library is intended to make Python logging less painful by
adding a bunch of useful functionalities that solve caveats of the
standard loggers. Using logs in your application should be an
automatism, **Loguru** tries to make it both pleasant and powerful.

# Features

-   [Entirely ready out of the box without boilerplate][ready]
-   [No Handler, no Formatter, no Filter: one function to rule them all][ready]
-   [Easier file logging with rotation / retention / compression][ready]
-   [Modern string formatting using braces style][ready]
-   [Exceptions catching within threads or main][ready]
-   [Pretty logging with colors][ready]
-   [Asynchronous, Thread-safe, Multiprocess-safe][ready]
-   [Fully descriptive exceptions][ready]
-   [Structured logging as needed][ready]
-   [Lazy evaluation of expensive functions][ready]
-   [Customizable levels][ready]
-   [Better datetime handling][ready]
-   [Suitable for scripts and libraries][ready]
-   [Entirely compatible with standard logging][ready]

[ready]: ()
[delgan]: (https://github.com/Delgan)
[loguru]: (https://loguru.readthedocs.io/en/stable/overview.html)
[1]: https://www.github.com/skeptycal/autosys
[2]: https://www.twitter.com/skeptycal
[3]: https://opensource.org/licenses/MIT
[link_netlify]: (https://app.netlify.com/sites/mystifying-keller-ab5658/deploys)
[link_travis]: (https://travis-ci.com/skeptycal/autosys)
[link_twitter]: (https://www.twitter.com/skeptycal)
[link_github]: (https://www.github.com/skeptycal)
