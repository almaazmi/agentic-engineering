# Backend — FastAPI

Reference API for the agentic SDLC pipeline. In-memory Tasks domain kept
deliberately small so tests, builds, and deploys have real behaviour.

## Local development

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload    # http://localhost:8000/docs
```

## Quality gates (run by CI)

```bash
ruff check .          # lint
ruff format --check . # formatting
mypy app              # static types (strict)
pytest                # tests + coverage (>=85%)
```

## Endpoints

| Method | Path                          | Description            |
| ------ | ----------------------------- | ---------------------- |
| GET    | `/health`                     | Liveness/readiness     |
| GET    | `/api/tasks`                  | List tasks             |
| POST   | `/api/tasks`                  | Create a task          |
| GET    | `/api/tasks/{id}`             | Get a task             |
| POST   | `/api/tasks/{id}/complete`    | Mark a task complete   |
| DELETE | `/api/tasks/{id}`             | Delete a task          |
