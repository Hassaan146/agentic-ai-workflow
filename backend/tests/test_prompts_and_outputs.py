from app.llm.prompts import agent_task_prompt, structure_request_prompt
from app.orchestration.outputs import build_agent_output
from app.schemas.workflow import StructuredRequest, WorkflowTask


def test_structure_request_prompt_names_agent_and_json_contract() -> None:
    prompt = structure_request_prompt("Find me a car under $500.")

    assert "Request Structuring Agent" in prompt
    assert "Return JSON" in prompt
    assert "Find me a car" in prompt


def test_agent_task_prompt_includes_goal_constraints_and_dependencies() -> None:
    structured = StructuredRequest(
        original_request="Find me a car under $500.",
        goal="Find me a car under $500.",
        constraints=["Budget or price constraint detected"],
    )
    task = WorkflowTask(
        id="task_comparison",
        title="Compare cars",
        agent_type="comparison",
        depends_on=["task_research"],
        instructions="Compare candidate cars.",
    )

    prompt = agent_task_prompt(task, structured)

    assert "Comparison Agent" in prompt
    assert "Budget or price constraint detected" in prompt
    assert "task_research" in prompt


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

