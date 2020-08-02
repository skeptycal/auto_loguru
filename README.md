# Auto-Loguru

> Fancy defaults for the awesome loguru logs!

Simple!

### Install:

`pip install as_loguru`

---

### Use in Python script:

`from as_loguru import logger`

---

> This is a wrapper for the marvlous `loguru` logging package. Below is the information from the original project repo.

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
to use logging from the start, this is as simple as

```py
from loguru import logger

logger.info("I'm logging now!")
```

Also, this library is intended to make Python logging less painful by
adding a bunch of useful functionalities that solve caveats of the
standard loggers. Using logs in your application should be an
automatism, **Loguru** tries to make it both pleasant and powerful.

# Installation

    pip install loguru

# Features

-   Ready to use out of the box without boilerplate
-   [No Handler, no Formatter, no Filter: one function to rule them
    all][ready to use out of the box without boilerplate]
-   [Easier file logging with rotation / retention /
    compression][ready to use out of the box without boilerplate]
-   [Modern string formatting using braces
    style][ready to use out of the box without boilerplate]
-   [Exceptions catching within threads or
    main][ready to use out of the box without boilerplate]
-   [Pretty logging with
    colors][ready to use out of the box without boilerplate]
-   [Asynchronous, Thread-safe,
    Multiprocess-safe][ready to use out of the box without boilerplate]
-   [Fully descriptive
    exceptions][ready to use out of the box without boilerplate]
-   [Structured logging as
    needed][ready to use out of the box without boilerplate]
-   [Lazy evaluation of expensive
    functions][ready to use out of the box without boilerplate]
-   [Customizable
    levels][ready to use out of the box without boilerplate]
-   [Better datetime
    handling][ready to use out of the box without boilerplate]
-   [Suitable for scripts and
    libraries][ready to use out of the box without boilerplate]
-   \`Entirely compatible with standard loggin

[Ready to use out of the box without boilerplate]:
