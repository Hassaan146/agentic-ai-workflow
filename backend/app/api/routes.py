import asyncio
import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.auth.local import AuthenticatedUser, AuthResponse, LoginRequest, SignupRequest, get_current_user, login_user, require_admin, signup_user
from app.orchestration.workflow import run_agentic_workflow
from app.schemas.workflow import AdminStats, AdminUser, NodeTrace, RunCreateRequest, RunResponse, UsageLog
from app.storage.repository import RunRepository, get_repository
from app.templates import TEMPLATES

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/auth/signup", response_model=AuthResponse)
def signup(request: SignupRequest) -> AuthResponse:
    return signup_user(request)


@router.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest) -> AuthResponse:
    return login_user(request)


@router.get("/me")
def me(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    return user


@router.get("/admin/stats", response_model=AdminStats)
def admin_stats(
    user: AuthenticatedUser = Depends(require_admin),
    repository: RunRepository = Depends(get_repository),
) -> AdminStats:
    return repository.admin_stats()


@router.get("/admin/users", response_model=list[AdminUser])
def admin_users(
    user: AuthenticatedUser = Depends(require_admin),
    repository: RunRepository = Depends(get_repository),
) -> list[AdminUser]:
    return repository.list_all_users()


@router.get("/admin/runs", response_model=list[RunResponse])
def admin_runs(
    user: AuthenticatedUser = Depends(require_admin),
    repository: RunRepository = Depends(get_repository),
) -> list[RunResponse]:
    return repository.list_all_runs()


@router.get("/admin/traces", response_model=list[NodeTrace])
def admin_traces(
    user: AuthenticatedUser = Depends(require_admin),
    repository: RunRepository = Depends(get_repository),
) -> list[NodeTrace]:
    return repository.list_all_node_traces()


@router.get("/admin/usage", response_model=list[UsageLog])
def admin_usage(
    user: AuthenticatedUser = Depends(require_admin),
    repository: RunRepository = Depends(get_repository),
) -> list[UsageLog]:
    return repository.list_all_usage_logs()


@router.get("/templates")
def list_templates():
    return TEMPLATES


@router.post("/runs", response_model=RunResponse)
async def create_run(
    request: RunCreateRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> RunResponse:
    run = repository.create_run(user.clerk_user_id, request)
    try:
        result = await run_agentic_workflow(
            run_id=run.id,
            user_request=request.user_request,
            template_key=request.template_key,
            repository=repository,
        )
        return repository.complete_run(run.id, result.final_output)
    except Exception as exc:
        repository.fail_run(run.id, str(exc))
        raise HTTPException(status_code=500, detail="Workflow run failed.") from exc


@router.post("/runs/stream")
async def stream_created_run(
    request: RunCreateRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> StreamingResponse:
    run = repository.create_run(user.clerk_user_id, request)

    async def event_stream():
        emitted_trace_ids: set[str] = set()
        task = asyncio.create_task(
            run_agentic_workflow(
                run_id=run.id,
                user_request=request.user_request,
                template_key=request.template_key,
                repository=repository,
            )
        )

        yield _sse("run", run.model_dump(mode="json"))

        while not task.done():
            for trace in repository.list_node_traces(run.id):
                trace_id = str(trace.id)
                if trace_id not in emitted_trace_ids:
                    emitted_trace_ids.add(trace_id)
                    yield _sse("trace", trace.model_dump(mode="json"))
            await asyncio.sleep(0.05)

        try:
            result = await task
            completed_run = repository.complete_run(run.id, result.final_output)
            for trace in repository.list_node_traces(run.id):
                trace_id = str(trace.id)
                if trace_id not in emitted_trace_ids:
                    emitted_trace_ids.add(trace_id)
                    yield _sse("trace", trace.model_dump(mode="json"))
            yield _sse("run", completed_run.model_dump(mode="json"))
            yield _sse("done", {"run_id": str(run.id)})
        except Exception as exc:
            failed_run = repository.fail_run(run.id, str(exc))
            yield _sse("run", failed_run.model_dump(mode="json"))
            yield _sse("error", {"message": "Workflow run failed.", "run_id": str(run.id)})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/runs", response_model=list[RunResponse])
def list_runs(
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> list[RunResponse]:
    return repository.list_runs(user.clerk_user_id)


@router.get("/runs/{run_id}", response_model=RunResponse)
def get_run(
    run_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> RunResponse:
    run = repository.get_run(run_id, user.clerk_user_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found.")
    return run


@router.get("/runs/{run_id}/traces", response_model=list[NodeTrace])
def list_run_traces(
    run_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> list[NodeTrace]:
    if repository.get_run(run_id, user.clerk_user_id) is None:
        raise HTTPException(status_code=404, detail="Run not found.")
    return repository.list_node_traces(run_id)


@router.get("/runs/{run_id}/usage", response_model=list[UsageLog])
def list_run_usage(
    run_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> list[UsageLog]:
    if repository.get_run(run_id, user.clerk_user_id) is None:
        raise HTTPException(status_code=404, detail="Run not found.")
    return repository.list_usage_logs(run_id)


@router.get("/runs/{run_id}/events")
async def stream_run_events(
    run_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    repository: RunRepository = Depends(get_repository),
) -> StreamingResponse:
    if repository.get_run(run_id, user.clerk_user_id) is None:
        raise HTTPException(status_code=404, detail="Run not found.")

    async def event_stream():
        for trace in repository.list_node_traces(run_id):
            yield f"data: {json.dumps(trace.model_dump(mode='json'))}\n\n"
            await asyncio.sleep(0.05)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def _sse(event: str, payload: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(payload)}\n\n"
