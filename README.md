# Boardify

Boardify is a simple application for managing boards and tasks with priorities and statuses, built on **FastAPI**.

## Features

* JWT Authentication (PyJWT).
* Layered structure: routes, schemas, models, repositories (FastAPI, Pydantic, SQLAlchemy).
* Automated tests (Pytest).
* Containerization (Docker, Docker Compose).
* Migrations (Alembic).
* Linter (Ruff).
* Continuous Integration (GitHub Actions).

## Getting Started

#### 1. Clone the repository:

```shell
$ git clone git@github.com:NazariiKuntsevych/boardify.git
$ cd boardify/
```

#### 2. Create ```.env``` file similar to ```.env.example``` with your own creds.

#### 3. Start API and DB for development:

```shell
$ docker compose --file docker-compose.dev.yml up
```

#### 4. To create new migration:

```shell
$ alembic revision --autogenerate
```

#### 5. To apply migrations:

```shell
$ alembic upgrade head
```

#### 6. To run linter:

```shell
$ ruff check .
```

#### 7. To run tests:

```shell
$ python3 -m pytest
```

#### 8. Stop API and DB for development:

```shell
$ docker compose --file docker-compose.dev.yml down
```

For production you can use ```docker-compose.prod.yml```.

## Code structure

```
boardify/
|-- migrations/        # Alembic environment and migration files
|-- tests/             # Automated tests
|-- src/               # Main code
|---- api/             # Routers, routes and dependencies
|---- models/          # Data models
|---- repositories/    # Data access layer
|---- schemas/         # Pydantic schemas
|---- config.py        # Settings
|---- database.py      # Database utils
|---- main.py          # Application
|---- security.py      # Security utils
```

## ER Diagram

![ER Diagram](images/er_diagram.svg)

## Endpoints

| Endpoints                          | Methods          | Requires token |
|------------------------------------|------------------|----------------|
| /login                             | POST             | No             |
| /users                             | POST             | No             |
| /users/me                          | GET, PUT, DELETE | Yes            |
| /boards                            | POST, GET        | Yes            |
| /boards/{board_id}                 | GET, PUT, DELETE | Yes            |
| /boards/{board_id}/tasks           | POST, GET        | Yes            |
| /boards/{board_id}/tasks/{task_id} | GET, PUT, DELETE | Yes            |
| /priorities                        | GET              | No             |
| /statuses                          | GET              | No             |

## Licensing

The code in this project is licensed under MIT license.
