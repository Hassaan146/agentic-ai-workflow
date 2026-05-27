from app.schemas.workflow import StructuredRequest, WorkflowTask


def structure_request_prompt(user_request: str) -> str:
    return (
        "You are the Request Structuring Agent.\n"
        "Convert the user's messy request into structured intent.\n"
        "Return JSON with goal, constraints, and expected_output.\n\n"
        f"User request:\n{user_request}"
    )


def agent_task_prompt(task: WorkflowTask, structured_request: StructuredRequest) -> str:
    dependencies = ", ".join(task.depends_on) if task.depends_on else "none"
    return (
        f"You are the {task.agent_type.title()} Agent.\n"
        "Complete only your assigned task and return concise structured findings.\n\n"
        f"Overall goal: {structured_request.goal}\n"
        f"Known constraints: {structured_request.constraints or ['none']}\n"
        f"Task title: {task.title}\n"
        f"Prerequisites completed: {dependencies}\n"
        f"Instructions: {task.instructions}"
    )

