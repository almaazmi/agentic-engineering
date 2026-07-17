# Agentic Engineering — agent guide

This file is read by Claude (Claude Code / `@claude`) and mirrors
`.github/copilot-instructions.md`. Keep them in sync.

## What this repo is

A reference **agentic SDLC**: an issue is picked up by an AI agent, which opens
a PR that flows through CI, security scanning, AI review, and gated deploys to
Azure. Two apps exercise the pipeline end to end.

## Layout

```
backend/   FastAPI (Python 3.12) — in-memory Tasks API
frontend/  Next.js 15 (App Router, React 19, TS) — proxies /api/* to the backend
infra/     Terraform — Azure Container Apps + ACR (staging & production)
.github/   Workflows, agent config, templates
```

## Golden rules

- Keep changes **small and focused** — one logical change per PR.
- **Never** touch unrelated files or reformat code you did not change.
- **Never** commit secrets. Use GitHub secrets / Azure OIDC.
- All quality gates must pass locally before you open/expand a PR.
- Add or update **tests** for any behaviour change. Backend coverage gate is 85%.
- Match existing style; the linters/formatters are the source of truth.

## Commands

Backend (`cd backend`, venv with `pip install -e ".[dev]"`):

```bash
ruff check .          # lint
ruff format --check . # formatting
mypy app              # strict types
pytest                # tests + coverage (fails under 85%)
```

Frontend (`cd frontend`, `npm ci`):

```bash
npm run lint          # eslint
npm run typecheck     # tsc --noEmit
npm run test          # vitest
npm run build         # next build (standalone)
npm audit --omit=dev --audit-level=high
```

Infra (`cd infra`):

```bash
terraform fmt -recursive
terraform init -backend=false && terraform validate
```

## Conventions

- **Backend**: type-hint everything (mypy strict). Business logic lives in
  `app/services.py`; HTTP wiring in `app/main.py`; models in `app/models.py`.
  Raise domain errors and translate them to HTTP in the route layer.
- **Frontend**: the browser only calls same-origin `/api/*`, which the route
  handler in `app/api/[...path]/route.ts` proxies to `BACKEND_URL` (a runtime
  env var). Do not introduce `NEXT_PUBLIC_*` backend URLs.
- **Infra**: Terraform owns infrastructure; container **images** are rolled by
  the deploy workflow (`az containerapp update`). The image field is under
  `ignore_changes` — do not remove that.

## Definition of done

CI green (backend + frontend + infra + docker build), no new high/critical
vulnerabilities, tests updated, and the PR description explains what and why.
