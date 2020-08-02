# AS_Loguru Changelog

## UNRELEASED

-   Finalize Python 3.9 support
-   Remove support for python < 3.8
-   Add default values
-   Add environment variables
-   Test all settings
-   Add settings and config options to Template Repo
-   Reinstalled poetry from custom installer (getting pip corruption on Big Sur install)
-   Update mypy
    -   settings in pyproject.toml now
-   Update isort
    -   settings in pyproject.toml now

## AS_Loguru 0.3.0

> Poetry is much better than wranggling the myriad config files and utilities that come with `pipenv`, `pytest`, `mypy`, `flake8`, `pre-commit`, `isort`, `autopep8`, `semver`, `twine`, and `setup.py`.

-   Use poetry semver to bump versions (major, minor, patch)
-   -   `poetry version minor` (e.g. 0.2.0 => 0.3.0)
-   Update pre-commit
-   -   Using hooks from pre-commit, flake8, mypy, and custom
-   Update tox environment
-   -   py3.6, py3.7, pypy, coverage, pytest
-   Installed pyenv to manage 3.6, 3.7, pypy envs
-   Set poetry to use pypi api token:

    ```sh
    poetry config pypi-token.pypi my-token
    export POETRY_PYPI_TOKEN_PYPI=my-token >>.zshrc
    ```

-   Set Poetry to create venv's in repo's

    ```sh
    export POETRY_CACHE_DIR=~/Library/Caches/pypoetry
    export POETRY_VIRTUALENVS_PATH=${POETRY_CACHE_DIR}/virtualenvs
    ```

-   Remove Twine ... using Poetry to publish versions

## AS_Loguru 0.2.0

-   Refactor Setup to include sphinx and package_metadata
-   Add poetry semver, build, and publish tools
-   (https://github.com/python-poetry)
-   streamline CI path (add Azure and Github hooks)
-   added twine_setup script file to run twine outside of setup.py

## AS_Loguru 0.1.0

-   supporting python 3.6+
-   Dev Release. Not Stable
