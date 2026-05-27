from app.schemas.workflow import TemplateResponse


TEMPLATES = [
    TemplateResponse(
        key="research",
        name="Research Assistant",
        description="Breaks a topic into research tasks, gathers sources, and synthesizes a clear answer.",
        starter_prompt="Research the latest practical use cases for AI workflow automation.",
    ),
    TemplateResponse(
        key="product_comparison",
        name="Product Comparison",
        description="Compares options against constraints, tradeoffs, and user priorities.",
        starter_prompt="Find me a car under $500 and explain the tradeoffs.",
    ),
    TemplateResponse(
        key="startup_validator",
        name="Startup Idea Validator",
        description="Analyzes a startup idea through market, customer, risk, and MVP lenses.",
        starter_prompt="Validate an AI tool idea for small clinics that need appointment automation.",
    ),
]


def get_template(template_key: str) -> TemplateResponse | None:
    return next((template for template in TEMPLATES if template.key == template_key), None)

