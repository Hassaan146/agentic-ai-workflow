# Phase Testing Log

This log records what each phase currently verifies. Keep it updated whenever the product grows.

## Phase 1: Design Foundation

Verified by:

- Design docs exist in `docs/`.
- Mermaid diagrams are present in `docs/diagrams.md`.
- Decision Maker project memory exists in `docs/project-memory.md`.

## Phase 2: Stack And Environment

Verified by:

- `.venv` exists for backend Python isolation.
- `backend/requirements.txt` installs backend dependencies.
- `frontend/package-lock.json` locks frontend dependencies.
- `backend/tests/test_config.py` checks dev/production config behavior.
- `scripts/verify-all.ps1` runs the local verification gate.
- `.github/workflows/ci.yml` runs the same checks on GitHub.

## Phase 3: Core Agentic Workflow

Verified by:

- `backend/tests/test_planner.py` checks dependency ordering.
- `backend/tests/test_workflow_execution.py` checks LangGraph execution.
- `backend/tests/test_prompts_and_outputs.py` checks prompt and output contracts.
- `backend/tests/test_search_tool.py` checks controlled search limits.

## Phase 4: MVP Interface

Verified by:

- `frontend` production build.
- `backend/tests/test_api_routes.py` checks templates, runs, and trace endpoints.
- Dashboard exposes final output, sources, node traces, and usage logs for selected runs.
- Dashboard streams run and trace events while a workflow executes.
- Live local endpoint checks against `http://127.0.0.1:8000`.

## Phase 5: Release Skeleton

Verified by:

- `backend/Dockerfile` exists for backend packaging.
- `render.yaml` exists for Render deployment.
- `frontend/vercel.json` exists for Vercel deployment.
- `npm audit --audit-level=high` blocks high-severity frontend issues.

Known note:

- Next.js currently reports moderate PostCSS advisories through `npm audit`, but the suggested force fix would downgrade Next. We track the issue but do not apply the breaking downgrade.
