from app.schemas.workflow import RunCreateRequest, StructuredRequest, WorkflowTask


def test_run_create_request_accepts_generic_workflow_key() -> None:
    request = RunCreateRequest(
        user_request="Compare two AI research tools.",
        template_key="generic",
    )

    assert request.template_key == "generic"
    assert "Compare" in request.user_request


def test_structured_request_defaults_expected_output() -> None:
    structured = StructuredRequest(original_request="Compare AI tools", goal="Compare AI tools")

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
