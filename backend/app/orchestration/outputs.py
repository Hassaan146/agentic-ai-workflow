from app.orchestration.toon import build_agent_handoff_payload
from app.schemas.workflow import AgentOutput, WorkflowTask


def build_agent_output(
    *,
    task: WorkflowTask,
    agent_name: str,
    summary: str,
    extra_data: dict | None = None,
) -> AgentOutput:
    data = {
        "task_title": task.title,
        "agent_type": task.agent_type,
        "depends_on": task.depends_on,
        "output_format": "structured_summary",
    }
    if extra_data:
        data.update(extra_data)
    data["handoff_format"] = "toon"
    data["toon_payload"] = build_agent_handoff_payload(
        task_id=task.id,
        agent_name=agent_name,
        summary=summary,
        data=data,
    )

    return AgentOutput(
        task_id=task.id,
        agent_name=agent_name,
        summary=summary,
        data=data,
    )

