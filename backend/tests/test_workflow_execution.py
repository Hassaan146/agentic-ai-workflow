import pytest

from app.orchestration.workflow import run_agentic_workflow
from app.schemas.workflow import RunCreateRequest
from app.storage.repository import InMemoryRunRepository


@pytest.mark.asyncio
async def test_agentic_workflow_completes_with_trace() -> None:
    repository = InMemoryRunRepository()
    run = repository.create_run(
        "user_123",
        RunCreateRequest(
            user_request="Compare two AI workflow tools for a small team.",
            template_key="generic",
        ),
    )

    result = await run_agentic_workflow(
        run_id=run.id,
        user_request=run.user_request,
        template_key=run.template_key,
        repository=repository,
    )

    traces = repository.list_node_traces(run.id)
    usage_logs = repository.list_usage_logs(run.id)
    completed_nodes = {trace.node_key for trace in traces if trace.status == "completed"}

    assert result.final_output.title
    assert result.final_output.trace_summary
    assert any("Comparison Agent" in item for item in result.final_output.trace_summary)
    agent_outputs = [trace.output_payload for trace in traces if trace.node_key == "execute_agents" and trace.status == "completed"]
    assert agent_outputs
    assert agent_outputs[-1]["handoff_format"] == "gcf"
    assert usage_logs
    assert {log.purpose for log in usage_logs}.issuperset({"structure", "reasoning", "comparison", "writing"})
    assert "structure_request" in completed_nodes
    assert "verify_output" in completed_nodes
    assert "final_response" in completed_nodes
