# db-contrib-tool

The `db-contrib-tool` - MongoDB's tools for contributors.

## Table of contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributor's Guide](#contributors-guide-local-development)
    - [Install dependencies](#install-project-dependencies)
    - [Run command line tool](#run-command-line-tool-local-development)
    - [Run linters](#run-linters)
    - [Run tests](#run-tests)
    - [Pre-commit](#pre-commit)
    - [Test pipx package](#test-pipx-package)

## Description

The command line tool with various subcommands:
- `bisect` - performs an evergreen-aware git-bisect to find the 'last passing version' and 'first failing version' of mongo
- `setup-repro-env` - downloads and installs:
  - particular MongoDB versions
  - debug symbols
  - artifacts (including resmoke, python scripts etc)
  - python venv for resmoke, python scripts etc
- `symbolize` - takes stacktraces as input and generates symbolized output of it.

## Dependencies

- Python 3.7 or later (python3 from the [MongoDB Toolchain](https://github.com/10gen/toolchain-builder/blob/master/INSTALL.md) is highly recommended)

## Installation

Make sure [dependencies](#dependencies) are installed.
Use [pipx](https://pypa.github.io/pipx/) to install db-contrib-tool that will be available globally on your machine:
```bash
$ python3 -m pip install pipx
$ python3 -m pipx ensurepath
```

Installing db-contrib-tool:
```bash
$ python3 -m pipx install db-contrib-tool
```

Upgrading db-contrib-tool:
```bash
$ python3 -m pipx upgrade db-contrib-tool
```

## Usage

Print out help message:
```bash
$ db-contrib-tool -h
```
More information on the usage of `setup-repro-env` can be found [here](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md).

## Contributor's Guide (local development)

### Install project dependencies

This project uses [poetry](https://python-poetry.org/) for dependency management.
```bash
$ poetry install
```

### Run command line tool (local development)

```bash
$ ENV=DEV poetry run db-contrib-tool -h
```

### Run linters

```bash
$ poetry run isort src tests
$ poetry run black src tests
```

### Run tests

```bash
$ poetry run pytest
```

### Pre-commit

This project has [pre-commit](https://pre-commit.com/) configured. Pre-commit will run
configured checks at git commit time.<br>
To enable pre-commit on your local repository run:
```bash
$ poetry run pre-commit install
```

To run pre-commit manually:
```bash
$ poetry run pre-commit run
```

### Test pipx package

Pipx installation recommendations can be found in [installation](#installation) section.<br>
The tool can be installed via pipx from your local repo:
```bash
$ python3 -m pipx install /path/to/db-contrib-tool
```
