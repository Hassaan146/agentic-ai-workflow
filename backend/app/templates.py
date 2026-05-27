from app.schemas.workflow import TemplateResponse


TEMPLATES = [
    TemplateResponse(
        key="generic",
        name="Generic Agentic Workflow",
        description="Accepts any user request, structures it, plans tasks, routes agents, verifies the result, and returns a traceable answer.",
        starter_prompt="Ask the workflow to research, compare, plan, validate, or explain a task.",
    ),
]


def get_template(template_key: str) -> TemplateResponse | None:
    return next((template for template in TEMPLATES if template.key == template_key), None)
