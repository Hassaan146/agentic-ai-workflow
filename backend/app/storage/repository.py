from datetime import UTC, datetime
from threading import Lock
from uuid import UUID, uuid4

from app.core.config import settings
from app.schemas.workflow import AdminStats, AdminUser, FinalOutput, NodeTrace, RunCreateRequest, RunResponse, UsageLog


class RunRepository:
    def create_run(self, clerk_user_id: str, request: RunCreateRequest) -> RunResponse:
        raise NotImplementedError

    def complete_run(self, run_id: UUID, final_output: FinalOutput) -> RunResponse:
        raise NotImplementedError

    def fail_run(self, run_id: UUID, error_message: str) -> RunResponse:
        raise NotImplementedError

    def get_run(self, run_id: UUID, clerk_user_id: str) -> RunResponse | None:
        raise NotImplementedError

    def list_runs(self, clerk_user_id: str) -> list[RunResponse]:
        raise NotImplementedError

    def add_node_trace(self, trace: NodeTrace) -> NodeTrace:
        raise NotImplementedError

    def list_node_traces(self, run_id: UUID) -> list[NodeTrace]:
        raise NotImplementedError

    def add_usage_log(self, usage_log: UsageLog) -> UsageLog:
        raise NotImplementedError

    def list_usage_logs(self, run_id: UUID) -> list[UsageLog]:
        raise NotImplementedError

    def list_all_users(self) -> list[AdminUser]:
        raise NotImplementedError

    def list_all_runs(self) -> list[RunResponse]:
        raise NotImplementedError

    def list_all_node_traces(self) -> list[NodeTrace]:
        raise NotImplementedError

    def list_all_usage_logs(self) -> list[UsageLog]:
        raise NotImplementedError

    def admin_stats(self) -> AdminStats:
        raise NotImplementedError


class InMemoryRunRepository(RunRepository):
    def __init__(self) -> None:
        self._runs: dict[UUID, RunResponse] = {}
        self._traces: dict[UUID, list[NodeTrace]] = {}
        self._usage_logs: dict[UUID, list[UsageLog]] = {}
        self._lock = Lock()

    def create_run(self, clerk_user_id: str, request: RunCreateRequest) -> RunResponse:
        with self._lock:
            run = RunResponse(
                id=uuid4(),
                clerk_user_id=clerk_user_id,
                template_key=request.template_key,
                user_request=request.user_request,
                status="running",
            )
            self._runs[run.id] = run
            self._traces[run.id] = []
            self._usage_logs[run.id] = []
            return run

    def complete_run(self, run_id: UUID, final_output: FinalOutput) -> RunResponse:
        with self._lock:
            run = self._runs[run_id].model_copy(
                update={
                    "status": "completed",
                    "final_output": final_output,
                    "updated_at": datetime.now(UTC),
                }
            )
            self._runs[run_id] = run
            return run

    def fail_run(self, run_id: UUID, error_message: str) -> RunResponse:
        with self._lock:
            run = self._runs[run_id].model_copy(
                update={
                    "status": "failed",
                    "error_message": error_message,
                    "updated_at": datetime.now(UTC),
                }
            )
            self._runs[run_id] = run
            return run

    def get_run(self, run_id: UUID, clerk_user_id: str) -> RunResponse | None:
        run = self._runs.get(run_id)
        if run is None or run.clerk_user_id != clerk_user_id:
            return None
        return run

    def list_runs(self, clerk_user_id: str) -> list[RunResponse]:
        return [
            run
            for run in sorted(self._runs.values(), key=lambda item: item.created_at, reverse=True)
            if run.clerk_user_id == clerk_user_id
        ]

    def add_node_trace(self, trace: NodeTrace) -> NodeTrace:
        with self._lock:
            self._traces.setdefault(trace.run_id, []).append(trace)
            return trace

    def list_node_traces(self, run_id: UUID) -> list[NodeTrace]:
        return list(self._traces.get(run_id, []))

    def add_usage_log(self, usage_log: UsageLog) -> UsageLog:
        with self._lock:
            self._usage_logs.setdefault(usage_log.run_id, []).append(usage_log)
            return usage_log

    def list_usage_logs(self, run_id: UUID) -> list[UsageLog]:
        return list(self._usage_logs.get(run_id, []))

    def list_all_users(self) -> list[AdminUser]:
        from app.auth.local import _memory_users_by_email

        return [
            AdminUser(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_admin=user.is_admin,
                auth_provider="local",
            )
            for user in _memory_users_by_email.values()
        ]

    def list_all_runs(self) -> list[RunResponse]:
        return sorted(self._runs.values(), key=lambda item: item.created_at, reverse=True)

    def list_all_node_traces(self) -> list[NodeTrace]:
        traces: list[NodeTrace] = []
        for run_traces in self._traces.values():
            traces.extend(run_traces)
        return sorted(traces, key=lambda item: item.started_at, reverse=True)

    def list_all_usage_logs(self) -> list[UsageLog]:
        logs: list[UsageLog] = []
        for run_logs in self._usage_logs.values():
            logs.extend(run_logs)
        return sorted(logs, key=lambda item: item.created_at, reverse=True)

    def admin_stats(self) -> AdminStats:
        usage_logs = self.list_all_usage_logs()
        return AdminStats(
            users=len(self.list_all_users()),
            runs=len(self._runs),
            traces=sum(len(items) for items in self._traces.values()),
            usage_logs=len(usage_logs),
            estimated_tokens=sum(item.prompt_tokens + item.completion_tokens for item in usage_logs),
        )


class SupabaseRunRepository(RunRepository):
    def __init__(self) -> None:
        from supabase import create_client

        self.client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    def create_run(self, clerk_user_id: str, request: RunCreateRequest) -> RunResponse:
        payload = {
            "clerk_user_id": clerk_user_id,
            "template_key": request.template_key,
            "user_request": request.user_request,
            "status": "running",
        }
        data = self.client.table("workflow_runs").insert(payload).execute().data[0]
        return RunResponse(**data)

    def complete_run(self, run_id: UUID, final_output: FinalOutput) -> RunResponse:
        data = (
            self.client.table("workflow_runs")
            .update({"status": "completed", "final_output": final_output.model_dump(mode="json")})
            .eq("id", str(run_id))
            .execute()
            .data[0]
        )
        return RunResponse(**data)

    def fail_run(self, run_id: UUID, error_message: str) -> RunResponse:
        data = (
            self.client.table("workflow_runs")
            .update({"status": "failed", "error_message": error_message})
            .eq("id", str(run_id))
            .execute()
            .data[0]
        )
        return RunResponse(**data)

    def get_run(self, run_id: UUID, clerk_user_id: str) -> RunResponse | None:
        data = (
            self.client.table("workflow_runs")
            .select("*")
            .eq("id", str(run_id))
            .eq("clerk_user_id", clerk_user_id)
            .execute()
            .data
        )
        return RunResponse(**data[0]) if data else None

    def list_runs(self, clerk_user_id: str) -> list[RunResponse]:
        data = (
            self.client.table("workflow_runs")
            .select("*")
            .eq("clerk_user_id", clerk_user_id)
            .order("created_at", desc=True)
            .execute()
            .data
        )
        return [RunResponse(**item) for item in data]

    def add_node_trace(self, trace: NodeTrace) -> NodeTrace:
        self.client.table("node_traces").insert(trace.model_dump(mode="json")).execute()
        return trace

    def list_node_traces(self, run_id: UUID) -> list[NodeTrace]:
        data = (
            self.client.table("node_traces")
            .select("*")
            .eq("run_id", str(run_id))
            .order("started_at")
            .execute()
            .data
        )
        return [NodeTrace(**item) for item in data]

    def add_usage_log(self, usage_log: UsageLog) -> UsageLog:
        self.client.table("usage_logs").insert(usage_log.model_dump(mode="json")).execute()
        return usage_log

    def list_usage_logs(self, run_id: UUID) -> list[UsageLog]:
        data = (
            self.client.table("usage_logs")
            .select("*")
            .eq("run_id", str(run_id))
            .order("created_at")
            .execute()
            .data
        )
        return [UsageLog(**item) for item in data]

    def list_all_users(self) -> list[AdminUser]:
        data = self.client.table("user_profiles").select("id,email,full_name,is_admin,auth_provider,created_at,updated_at").order("created_at", desc=True).execute().data
        return [AdminUser(**item) for item in data]

    def list_all_runs(self) -> list[RunResponse]:
        data = self.client.table("workflow_runs").select("*").order("created_at", desc=True).execute().data
        return [RunResponse(**item) for item in data]

    def list_all_node_traces(self) -> list[NodeTrace]:
        data = self.client.table("node_traces").select("*").order("started_at", desc=True).limit(200).execute().data
        return [NodeTrace(**item) for item in data]

    def list_all_usage_logs(self) -> list[UsageLog]:
        data = self.client.table("usage_logs").select("*").order("created_at", desc=True).limit(200).execute().data
        return [UsageLog(**item) for item in data]

    def admin_stats(self) -> AdminStats:
        users = self.list_all_users()
        runs = self.list_all_runs()
        traces = self.list_all_node_traces()
        usage_logs = self.list_all_usage_logs()
        return AdminStats(
            users=len(users),
            runs=len(runs),
            traces=len(traces),
            usage_logs=len(usage_logs),
            estimated_tokens=sum(item.prompt_tokens + item.completion_tokens for item in usage_logs),
        )


_memory_repository = InMemoryRunRepository()


def get_repository() -> RunRepository:
    if settings.has_supabase_storage:
        return SupabaseRunRepository()
    return _memory_repository

