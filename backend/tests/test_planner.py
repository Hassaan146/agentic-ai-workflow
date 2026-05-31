import pytest

from app.orchestration.planner import build_task_plan, order_tasks_by_prerequisites
from app.schemas.workflow import StructuredRequest, WorkflowTask


def test_car_budget_request_orders_budget_before_search_and_comparison() -> None:
    structured = StructuredRequest(
        original_request="Compare two AI workflow tools for a small team.",
        goal="Compare two AI workflow tools for a small team.",
        constraints=["Budget or price constraint detected"],
    )

    plan = build_task_plan(structured)

    assert plan.execution_order.index("task_constraints") < plan.execution_order.index("task_research")
    assert plan.execution_order.index("task_research") < plan.execution_order.index("task_comparison")
    assert plan.execution_order[-1] == "task_synthesis"


def test_unknown_dependency_is_rejected() -> None:
    tasks = [
        WorkflowTask(
            id="task_synthesis",
            title="Synthesize",
            agent_type="writing",
            depends_on=["missing_task"],
            instructions="Write final output.",
        )
    ]

    with pytest.raises(ValueError, match="Unknown dependency"):
        order_tasks_by_prerequisites(tasks)


def test_dependency_cycle_is_rejected() -> None:
    tasks = [
        WorkflowTask(
            id="task_a",
            title="A",
            agent_type="reasoning",
            depends_on=["task_b"],
            instructions="Do A.",
        ),
        WorkflowTask(
            id="task_b",
            title="B",
            agent_type="writing",
            depends_on=["task_a"],
            instructions="Do B.",
        ),
    ]

    with pytest.raises(ValueError, match="cycle"):
        order_tasks_by_prerequisites(tasks)


def test_factual_what_is_question_includes_research_before_synthesis() -> None:
    structured = StructuredRequest(
        original_request="what is toon, is it better than json",
        goal="what is toon, is it better than json",
    )

    plan = build_task_plan(structured)

    assert "task_research" in plan.execution_order
    assert plan.execution_order.index("task_research") < plan.execution_order.index("task_synthesis")
