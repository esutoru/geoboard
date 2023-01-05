# Geoboard

![GitHub last commit](https://img.shields.io/github/last-commit/esutoru/geoboard)

Geoboard is a project where you can create a dashboard with various widgets containing weather 
information: temperature for seven next days, wind status, sunrise status, etc.

This repository contains backend part of this project

## Requirements

* [PostgreSQL](https://www.postgresql.org/)
* [Python 3.11](https://www.python.org/) (You can use [pyenv](https://github.com/pyenv/pyenv) 
to install it)
* [Poetry](https://python-poetry.org/) for Python package and environment management

## Installation

1. Create the PostgreSQL Database and User
2. Go to project directory and add `.env` file:
```
cp .env.template .env
```
3. Configure `.env`: add database info, generate jwt key and etc.
4. Install dependencies py `poetry`:
```
poetry install
```
5. Start a shell session with the new environment with:
```
poetry shell
```
6. Run database migrations:
```
alembic upgrade head
```
7. Install [pre-commit](https://pre-commit.com/):
```
pre-commit install
```

## Run project
```
cli run-server
```
You can get additional information about this command if you add `--help` flag

## API documentation

Run project and open http://127.0.0.1:8000/api/v1/docs to see list of available endpoints

## Commands

You can run special helper commands to create user, get users list, run server, etc:
```
# Create user:
cli user create

# Get more info about all available commands
cli --help
```
