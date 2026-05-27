from app.schemas.workflow import FinalOutput, NodeTrace, RunCreateRequest, UsageLog
from app.storage.repository import InMemoryRunRepository


def test_repository_run_lifecycle() -> None:
    repository = InMemoryRunRepository()
    run = repository.create_run(
        "user_123",
        RunCreateRequest(user_request="Validate my startup idea.", template_key="generic"),
    )

    repository.add_node_trace(
        NodeTrace(
            run_id=run.id,
            node_key="structure_request",
            agent_name="Request Structuring Agent",
            status="completed",
        )
    )
    completed = repository.complete_run(
        run.id,
        FinalOutput(title="Done", answer="Workflow completed."),
    )

    assert completed.status == "completed"
    assert completed.final_output is not None
    assert len(repository.list_node_traces(run.id)) == 1


def test_repository_tracks_usage_logs() -> None:
    repository = InMemoryRunRepository()
    run = repository.create_run(
        "user_123",
        RunCreateRequest(user_request="Research AI agents.", template_key="generic"),
    )

    repository.add_usage_log(
        UsageLog(
            run_id=run.id,
            provider="deterministic",
            model="local-dev-fallback",
            purpose="structure",
            prompt_tokens=4,
            completion_tokens=8,
        )
    )

    usage_logs = repository.list_usage_logs(run.id)

    assert len(usage_logs) == 1
    assert usage_logs[0].purpose == "structure"
