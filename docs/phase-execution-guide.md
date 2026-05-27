# Phase Execution Guide

This project is being built like a product, not only like a code demo. Each phase has a clear purpose, a skeleton, and a testing checkpoint.

## Phase 1: Design And LinkedIn Foundation

Status: skeleton complete.

What was created:

- Product story in `docs/phase-1-design.md`.
- LinkedIn journey in `docs/linkedin-journey.md`.
- Mermaid diagrams in `docs/diagrams.md`.
- Testing strategy in `docs/testing-strategy.md`.
- Deployment notes in `docs/deployment.md`.

Testing/checking:

- Documentation files exist.
- Diagrams are written in Mermaid format.
- The README points to the project purpose and structure.

## Phase 2: Stack And Tool Responsibilities

Status: skeleton complete.

What was created:

- Python virtual environment: `.venv`.
- Explicit backend environment mode: `APP_ENV=dev` or `APP_ENV=production`.
- Production readiness guard for Clerk and Supabase settings.
- Local development auth mode through `dev-token`.
- Backend dependency file: `backend/requirements.txt`.
- Frontend dependency file: `frontend/package.json`.
- FastAPI app entrypoint: `backend/app/main.py`.
- Clerk auth boundary: `backend/app/auth/clerk.py`.
- Supabase repository boundary: `backend/app/storage/repository.py`.
- LangChain provider boundary: `backend/app/llm/providers.py`.
- LangGraph orchestration boundary: `backend/app/orchestration/workflow.py`.
- Next.js app shell: `frontend/app`.

Testing/checking:

- Backend dependencies install into `.venv`.
- Frontend dependencies install into `node_modules`.
- Backend imports compile.
- Frontend production build succeeds.
- Production config tests prove missing required services are caught before deployment.

## Phase 3: Core Product Flow

Status: skeleton complete.

What was created:

- User request schema.
- Structured request schema.
- Workflow task schema.
- Reusable task planner module.
- Reusable prompt template module.
- Structured agent output helper.
- Prerequisite-aware task ordering.
- Dependency cycle and missing dependency detection.
- Agent output schema.
- Final output schema.
- Run creation endpoint.
- LangGraph workflow:
  - structure request
  - decompose tasks
  - analyze prerequisites
  - execute agents
  - verify output
  - final response
- Simple controlled search tool.
- In-memory development repository.

Testing/checking:

- Unit tests validate schemas and repository lifecycle.
- Workflow execution test validates LangGraph flow.
- Planner tests validate prerequisite ordering, missing dependency rejection, and cycle rejection.
- Prompt/output tests validate agent prompt contracts and structured output metadata.
- API tests validate run creation and event trace behavior.

## Phase 4: MVP Execution Order

Status: skeleton complete.

What was created:

- `frontend/` for Next.js.
- `backend/` for FastAPI.
- `supabase/schema.sql` for hosted database setup.
- Local dev auth mode using `dev-token`.
- Simple dashboard GUI.
- Request form.
- Generic workflow request form.
- Backend template endpoint.
- Recent run history panel.
- Final output panel.
- Agent trace panel.

Testing/checking:

- Backend API can run without Clerk/Supabase keys in dev mode.
- Frontend can build without real Clerk keys in dev mode.
- The dashboard can call the backend when both dev servers are running.

## Phase 5: First Release Features And Testing

Status: skeleton complete.

What was created:

- One generic workflow entry point.
- Saved run support through repository abstraction.
- Node trace support.
- Final output support.
- Usage log schema.
- Usage logging repository methods.
- Model-call retry wrapper.
- Backend Dockerfile.
- Render deployment blueprint.
- Vercel frontend config.
- Deployment notes for Vercel, Render, and Supabase.

Testing/checking:

- Backend route tests cover auth, run creation, run listing, and trace streaming.
- Usage logging tests cover repository storage and workflow model-call tracking.
- Frontend build checks page compilation and TypeScript validity.
- Audit gate checks for high-severity frontend dependency issues.

## Next Product-Building Order

1. Connect real Clerk, Supabase, Groq, and Gemini keys.
2. Run the hosted Supabase schema.
3. Deploy backend to Render and frontend to Vercel.
4. Replace the temporary frontend styling with the user's final frontend form/design.
5. Switch `SEARCH_PROVIDER` from `mock` to `duckduckgo` when real public source fetching is desired.
