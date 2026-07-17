# Frontend — Next.js

App Router UI for the agentic SDLC demo. Talks to the FastAPI backend and is
built as a `standalone` bundle for a small container image.

## Local development

```bash
cd frontend
npm install
cp .env.local.example .env.local   # point NEXT_PUBLIC_API_BASE_URL at the backend
npm run dev                        # http://localhost:3000
```

## Quality gates (run by CI)

```bash
npm run lint        # eslint (next/core-web-vitals)
npm run typecheck   # tsc --noEmit
npm run test        # vitest (unit + component)
npm run build       # next build (standalone)
```
