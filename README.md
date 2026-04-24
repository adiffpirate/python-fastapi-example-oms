# Order Management System API

A simple, modular FastAPI application for managing orders.
Built as a **modular monolith** with clean separation of concerns, PostgreSQL for persistence,
Alembic for migrations, and SQLite for fast unit tests.

## 📁 Project Structure

```
.
├── app/
│   ├── main.py
│   ├── api/
│   │   └── router.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── session.py
│   └── modules/
│       ├── orders/
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── repository.py
│       │   ├── service.py
│       │   └── routes.py
│       └── users/
│           ├── models.py
│           ├── schemas.py
│           ├── repository.py
│           ├── service.py
│           └── routes.py
├── alembic/
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```

## 🐍 Python Virtual Environment (venv)

It’s recommended to use a virtual environment to isolate dependencies.

### Create venv

```bash
python -m venv .venv
```

### Activate

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install --upgrade pip
pip install -e '.[dev]'
```

## 🐘 Running PostgreSQL (Docker)

Start a fresh local PostgreSQL instance:

```bash
docker stop postgres-dev || true
docker rm postgres-dev || true
docker run -d \
  --name postgres-dev \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=app \
  -p 5432:5432 \
  postgres:15
```

## ⚙️ Environment Variables

Set your database connection:

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
```

## 🗄️ Database Migrations (Alembic)

Create migration:

```bash
python -m alembic revision --autogenerate -m "init"
```

Apply migrations:

```bash
python -m alembic upgrade head
```

## ▶️ Run the API

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://localhost:8000
```

Interactive docs:

```
http://localhost:8000/docs
```

## 🧪 Running Tests

### Unit Tests

> Uses SQLite in-memory, so no database setup is required.

```bash
pytest tests/unit
```

### Integration Tests

> Fresh PostgreSQL instance with migrations applied is required.

```bash
pytest tests/integration
```

## 🔌 Example API Usage

### Create Order

```bash
curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -d '{"item": "laptop"}'
```

### Get Order

```bash
curl http://localhost:8000/orders/1
```

### List Orders

```bash
curl http://localhost:8000/orders/
```

## 🧠 Architecture

This project uses a **feature-based modular structure**:

* `modules/orders` contains everything related to orders
* `repository.py` → database access
* `service.py` → business logic
* `routes.py` → API layer

This keeps the codebase:

* easy to navigate
* easy to extend
* ready to evolve into microservices if needed

## 📌 Future Improvements

* Order state transitions (finite state machine)
* Update / delete endpoints
* Authorization
* Integration tests with PostgreSQL
* Docker support for full deployment
