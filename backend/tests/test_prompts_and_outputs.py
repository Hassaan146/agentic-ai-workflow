from app.llm.prompts import agent_task_prompt, structure_request_prompt
from app.orchestration.outputs import build_agent_output
from app.orchestration.toon import to_toon
from app.schemas.workflow import StructuredRequest, WorkflowTask


def test_structure_request_prompt_names_agent_and_toon_contract() -> None:
    prompt = structure_request_prompt("Compare two AI workflow tools for a small team.")

    assert "Request Structuring Agent" in prompt
    assert "Return TOON" in prompt
    assert "Compare two AI workflow tools" in prompt


def test_agent_task_prompt_includes_goal_constraints_and_dependencies() -> None:
    structured = StructuredRequest(
        original_request="Compare two AI workflow tools for a small team.",
        goal="Compare two AI workflow tools for a small team.",
        constraints=["Team size constraint detected"],
    )
    task = WorkflowTask(
        id="task_comparison",
        title="Compare workflow tools",
        agent_type="comparison",
        depends_on=["task_research"],
        instructions="Compare candidate workflow tools.",
    )

    prompt = agent_task_prompt(task, structured, handoff_context="task_id: task_research\nsummary: source facts collected")

    assert "Comparison Agent" in prompt
    assert "Team size constraint detected" in prompt
    assert "task_research" in prompt
    assert "```toon" in prompt
    assert "source facts collected" in prompt


def test_build_agent_output_adds_stable_metadata() -> None:
    task = WorkflowTask(
        id="task_synthesis",
        title="Synthesize",
        agent_type="writing",
        instructions="Write final output.",
    )

    output = build_agent_output(
        task=task,
        agent_name="Writing Agent",
        summary="Completed summary.",
    )

    assert output.task_id == "task_synthesis"
    assert output.data["task_title"] == "Synthesize"
    assert output.data["output_format"] == "structured_summary"
    assert output.data["handoff_format"] == "toon"
    assert "task_id: task_synthesis" in output.data["toon_payload"]


def test_to_toon_encodes_uniform_rows_compactly() -> None:
    payload = {
        "agent": "Search Agent",
        "sources": [
            {"title": "A", "url": "https://a.test"},
            {"title": "B", "url": "https://b.test"},
        ],
    }

    encoded = to_toon(payload)

    assert "sources:" in encoded
    assert "[2]{title,url}:" in encoded
    assert "https://a.test" in encoded
