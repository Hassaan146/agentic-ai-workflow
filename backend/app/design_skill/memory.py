ALWAYS_ON_SKILL_NAME = "Decision Maker"

ALWAYS_ON_SKILL_RULE = (
    "Decision Maker is an always-on project pipeline skill for frontend, website, "
    "visual direction, copy, design, developer prompts, and launch guidance. "
    "Before a polished frontend is built, collect six decisions, three reference "
    "buckets, and three style logics, then compile copywriter, visual, design, "
    "developer, and launch outputs."
)

FRONTEND_VISUAL_RECOMMENDATION = (
    "Mission Control Graph is the recommended first visual direction because it "
    "communicates multi-agent orchestration, state graphs, traces, verification, "
    "and routing more clearly than a generic chatbot interface."
)


def design_prompt_preamble() -> str:
    return (
        "ALWAYS-ON PROJECT PIPELINE:\n"
        f"{ALWAYS_ON_SKILL_RULE}\n\n"
        f"Recommended visual direction: {FRONTEND_VISUAL_RECOMMENDATION}\n\n"
    )


def project_memory_payload() -> dict[str, str]:
    return {
        "skill": ALWAYS_ON_SKILL_NAME,
        "rule": ALWAYS_ON_SKILL_RULE,
        "frontend_visual_recommendation": FRONTEND_VISUAL_RECOMMENDATION,
    }

