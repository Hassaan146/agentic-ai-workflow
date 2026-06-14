# Resume Brief

This file captures the recovered execution context for Agentic AI Workflow.

## Project

Agentic AI Workflow is a multi-agent workflow platform where users enter an unstructured request and the system:

- structures the request,
- decomposes it into tasks,
- detects prerequisites,
- routes tasks through specialized agents,
- verifies completion,
- stores the trace,
- returns a final answer with sources and execution history.

## Locked First Five Phases

1. Design and LinkedIn foundation.
2. Tech stack and tool responsibilities.
3. Core product flow.
4. MVP execution order.
5. First release features and testing.

## Confirmed Stack

- Frontend: Next.js and React.
- Backend: FastAPI and Pydantic.
- Orchestration: LangGraph.
- LLM/tool layer: LangChain.
- Auth: FastAPI auth.
- Database: Supabase Postgres.
- Model providers: Groq and Google AI Studio/Gemini.
- Deployment: Vercel frontend and Render backend.
- Source control: GitHub.
- Docker: backend packaging and local reproducibility, not production database hosting.

## Current Status

The phase 1-5 skeleton exists in this repository.

Verification on 2026-05-28:

- Backend compile passed.
- Backend tests passed: 29 tests.
- Frontend production build passed.
- High-severity frontend audit gate passed.
- Browser check passed for the dev dashboard workflow run at `http://127.0.0.1:3000/dashboard`.

Known note:

- `npm audit` reports moderate PostCSS advisories through Next.js. The suggested force fix would downgrade Next, so it is tracked but not applied.
- Next.js logs a Windows SWC native package warning, but the production build still completes successfully.

## Next Execution Steps

1. Connect real FastAPI auth, Supabase, Groq, and Gemini environment variables.
2. Replace the temporary frontend styling with the user's final frontend form/design.
3. Switch `SEARCH_PROVIDER` from `mock` to `duckduckgo` when real public source fetching is desired.
4. Start deployment to Vercel and Render after keys are configured.
