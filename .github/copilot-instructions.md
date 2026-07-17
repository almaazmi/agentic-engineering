# Copilot instructions — agentic-engineering

Repository custom instructions for the GitHub Copilot cloud agent. Mirrors the
root `CLAUDE.md`; keep them in sync.

## Project

A reference agentic SDLC. `backend/` is a FastAPI (Python 3.12) Tasks API,
`frontend/` is a Next.js 15 (App Router, React 19, TypeScript) UI that proxies
`/api/*` to the backend, and `infra/` is Terraform that deploys both to Azure
Container Apps (staging + production).

## Expectations for every change

- Keep the change **small and focused**; one logical change per PR.
- Do **not** modify unrelated files or reformat untouched code.
- Add or update **tests** for any behaviour change (backend coverage gate: 85%).
- All quality gates below must pass before opening or updating a PR.
- Never commit secrets; the pipeline authenticates to Azure via OIDC.

## Validate your work

Backend (`cd backend`, then `pip install -e ".[dev]"`):

```bash
ruff check . && ruff format --check . && mypy app && pytest
```

Frontend (`cd frontend`, then `npm ci`):

```bash
npm run lint && npm run typecheck && npm run test && npm run build
```

Infra (`cd infra`):

```bash
terraform fmt -check -recursive && terraform init -backend=false && terraform validate
```

## Conventions

- Backend business logic goes in `app/services.py`; keep `app/main.py` thin.
  Type-hint everything (mypy strict). Translate domain errors to HTTP status
  codes in the route layer.
- Frontend talks to the backend only through the same-origin proxy route
  (`app/api/[...path]/route.ts`) using the runtime `BACKEND_URL`. Do not add
  `NEXT_PUBLIC_*` backend URLs.
- In Terraform, the container app `image` is under `ignore_changes`; the deploy
  workflow rolls images. Don't remove that lifecycle rule.
