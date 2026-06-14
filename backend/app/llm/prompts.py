from app.schemas.workflow import StructuredRequest, WorkflowTask


def structure_request_prompt(user_request: str) -> str:
    return (
        "You are the Request Structuring Agent.\n"
        "Convert the user's messy request into structured intent.\n"
        "Return GCF with goal, constraints, and expected_output.\n\n"
        f"User request:\n{user_request}"
    )


def agent_task_prompt(task: WorkflowTask, structured_request: StructuredRequest, handoff_context: str = "") -> str:
    dependencies = ", ".join(task.depends_on) if task.depends_on else "none"
    handoff_block = ""
    if handoff_context:
        handoff_block = (
            "\nPrerequisite handoff format: GCF (Graph Compact Format). "
            "Use this compact handoff as factual context from previous agents:\n"
            f"```gcf\n{handoff_context}\n```\n"
        )
    return (
        f"You are the {task.agent_type.title()} Agent.\n"
        "Complete only your assigned task and return concise structured findings.\n\n"
        f"Overall goal: {structured_request.goal}\n"
        f"Known constraints: {structured_request.constraints or ['none']}\n"
        f"Task title: {task.title}\n"
        f"Prerequisites completed: {dependencies}\n"
        f"Instructions: {task.instructions}"
        f"{handoff_block}"
    )
