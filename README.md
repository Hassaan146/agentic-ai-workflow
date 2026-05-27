# Agentic AI Workflow

Agentic AI Workflow is a cloud-first multi-agent orchestration product. It turns messy user requests into structured, dependency-aware workflows, routes tasks through specialized agents, verifies the result, and shows the full execution trace.

## Stack

- Frontend: Next.js, React, Clerk
- Backend: FastAPI, Pydantic
- Orchestration: LangGraph
- LLM/tool layer: LangChain
- Database: Supabase Postgres
- Model providers: Groq and Google AI Studio/Gemini
- Deployment: Vercel frontend, Render backend

## Project Structure

```text
agentic-ai-workflow/
|-- backend/
|-- frontend/
|-- docs/
|-- scripts/
`-- supabase/
```

## Current Phase

Phase 1 design artifacts are in `docs/`. Phase 2 starts with the backend/frontend foundations and environment setup.

## Local Development

Backend:

```powershell
cd "H:\Skills\Agentic AI\agentic-ai-workflow"
.\scripts\run-backend.ps1
```

Frontend:

```powershell
cd "H:\Skills\Agentic AI\agentic-ai-workflow"
.\scripts\run-frontend.ps1
```

Open `http://localhost:3000`.

## Phase Verification

```powershell
cd "H:\Skills\Agentic AI\agentic-ai-workflow"
.\scripts\verify-all.ps1
```

The same verification gate is also encoded in `.github/workflows/ci.yml` for GitHub Actions.

## Learning Docs

- `docs/phase-execution-guide.md`
- `docs/environment-and-api-keys.md`
- `docs/diagrams.md`
- `docs/testing-strategy.md`
- `docs/phase-testing-log.md`
