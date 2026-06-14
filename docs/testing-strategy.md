# Testing Strategy

Testing will happen during every coding phase, not only before deployment.

## Backend

- FastAPI health and workflow route tests.
- FastAPI auth authentication verification tests.
- Supabase repository tests.
- Pydantic request and output validation tests.
- LangGraph route/order tests.
- Agent output format tests.
- Retry and failure-state tests.

## Frontend

- Dashboard render checks.
- Login/logout flow checks with FastAPI auth.
- Workflow request form checks.
- Agent trace and final output display checks.
- Empty, loading, success, and error state checks.

## Integration

- User signs in.
- User starts a workflow.
- Backend executes the graph.
- Node traces are saved.
- Frontend displays the final response.

## Deployment

- Vercel frontend reaches Render backend.
- Render backend reaches Supabase.
- FastAPI auth works in production.
- CORS and environment variables are correct.
- A full workflow run succeeds online.

