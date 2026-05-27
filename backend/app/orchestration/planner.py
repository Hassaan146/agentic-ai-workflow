from collections import deque

from app.schemas.workflow import StructuredRequest, TaskPlan, WorkflowTask


def build_task_plan(structured: StructuredRequest) -> TaskPlan:
    tasks = [
        WorkflowTask(
            id="task_constraints",
            title="Identify important constraints",
            agent_type="reasoning",
            instructions=f"Analyze constraints for: {structured.goal}",
        )
    ]

    if _needs_research(structured):
        tasks.append(
            WorkflowTask(
                id="task_research",
                title="Research relevant information",
                agent_type="search",
                depends_on=["task_constraints"],
                instructions=f"Find relevant information for: {structured.goal}",
            )
        )

    if _needs_comparison(structured):
        comparison_dependencies = ["task_research"] if _has_task(tasks, "task_research") else ["task_constraints"]
        tasks.append(
            WorkflowTask(
                id="task_comparison",
                title="Compare valid options against constraints",
                agent_type="comparison",
                depends_on=comparison_dependencies,
                instructions=f"Compare options for: {structured.goal}",
            )
        )

    final_dependency = tasks[-1].id
    tasks.append(
        WorkflowTask(
            id="task_synthesis",
            title="Synthesize the final recommendation",
            agent_type="writing",
            depends_on=[final_dependency],
            instructions="Create a concise answer grounded in the completed tasks.",
        )
    )

    ordered_tasks = order_tasks_by_prerequisites(tasks)
    return TaskPlan(tasks=ordered_tasks, execution_order=[task.id for task in ordered_tasks])


def order_tasks_by_prerequisites(tasks: list[WorkflowTask]) -> list[WorkflowTask]:
    task_by_id = {task.id: task for task in tasks}
    dependency_count = {task.id: len(task.depends_on) for task in tasks}
    dependents: dict[str, list[str]] = {task.id: [] for task in tasks}

    for task in tasks:
        for dependency in task.depends_on:
            if dependency not in task_by_id:
                raise ValueError(f"Unknown dependency '{dependency}' for task '{task.id}'.")
            dependents[dependency].append(task.id)

    ready = deque(task.id for task in tasks if dependency_count[task.id] == 0)
    ordered_ids: list[str] = []

    while ready:
        task_id = ready.popleft()
        ordered_ids.append(task_id)
        for dependent_id in dependents[task_id]:
            dependency_count[dependent_id] -= 1
            if dependency_count[dependent_id] == 0:
                ready.append(dependent_id)

    if len(ordered_ids) != len(tasks):
        raise ValueError("Task plan contains a dependency cycle.")

    return [task_by_id[task_id] for task_id in ordered_ids]


def _needs_research(structured: StructuredRequest) -> bool:
    text = structured.goal.lower()
    return any(
        keyword in text
        for keyword in ["find", "research", "search", "compare", "validate", "startup", "car"]
    )


def _needs_comparison(structured: StructuredRequest) -> bool:
    text = structured.goal.lower()
    return bool(structured.constraints) or any(
        keyword in text
        for keyword in ["compare", "best", "under", "less than", "tradeoff", "tradeoffs"]
    )


def _has_task(tasks: list[WorkflowTask], task_id: str) -> bool:
    return any(task.id == task_id for task in tasks)

