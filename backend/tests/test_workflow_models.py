from app.schemas.workflow import RunCreateRequest, StructuredRequest, WorkflowTask


def test_run_create_request_accepts_template() -> None:
    request = RunCreateRequest(
        user_request="Compare two AI research tools.",
        template_key="product_comparison",
    )

    assert request.template_key == "product_comparison"
    assert "Compare" in request.user_request


def test_structured_request_defaults_expected_output() -> None:
    structured = StructuredRequest(original_request="Find a car", goal="Find a car")

    assert structured.constraints == []
    assert structured.expected_output


def test_workflow_task_supports_dependencies() -> None:
    task = WorkflowTask(
        id="task_research",
        title="Research options",
        agent_type="search",
        depends_on=["task_constraints"],
        instructions="Find valid options.",
    )

    assert task.depends_on == ["task_constraints"]

