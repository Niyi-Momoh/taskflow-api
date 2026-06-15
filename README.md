# TaskFlow API

A RESTful task management API built with **FastAPI** and **PostgreSQL**, featuring JWT authentication, Alembic database migrations, and a Docker Compose development environment.

[![CI](https://github.com/Niyi-Momoh/taskflow-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Niyi-Momoh/taskflow-api/actions/workflows/ci.yml)

## Features

- **JWT Authentication** — register, login, token-protected endpoints
- **Full CRUD** on tasks with filtering (priority, completion status) and pagination
- **User isolation** — users can only access their own tasks
- **Pydantic v2** schemas with strict validation
- **SQLAlchemy 2.0** ORM with typed mapped columns
- **Alembic** migrations — schema versioned and reproducible
- **Docker Compose** — one command to run the full stack locally
- **13 integration tests** covering auth flows, CRUD, filters, and cross-user isolation

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.111 |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Containerisation | Docker + Docker Compose |

## Quick Start

### With Docker (recommended)

```bash
git clone https://github.com/Niyi-Momoh/taskflow-api.git
cd taskflow-api
docker compose up --build
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### Local development

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL connection string

# 4. Run migrations
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | — | Create account |
| POST | `/auth/login` | — | Get JWT token |
| GET | `/auth/me` | ✓ | Current user profile |
| GET | `/tasks/` | ✓ | List tasks (filterable) |
| POST | `/tasks/` | ✓ | Create task |
| GET | `/tasks/{id}` | ✓ | Get single task |
| PATCH | `/tasks/{id}` | ✓ | Update task |
| DELETE | `/tasks/{id}` | ✓ | Delete task |

**Filter params:** `?completed=true`, `?priority=high`, `?skip=0&limit=20`

## Running Tests

Tests use SQLite in-memory so no database setup is needed:

```bash
pytest tests/ -v
```

## Project Structure

```
taskflow-api/
├── app/
│   ├── main.py          # FastAPI app + router registration
│   ├── config.py        # Settings via pydantic-settings
│   ├── database.py      # SQLAlchemy engine + session
│   ├── dependencies.py  # JWT auth dependency
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── routers/         # FastAPI route handlers
│   └── services/        # Business logic (auth, tasks)
├── alembic/             # Database migrations
├── tests/               # pytest integration tests
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
