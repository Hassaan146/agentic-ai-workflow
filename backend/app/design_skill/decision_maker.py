from app.design_skill.models import (
    DecisionAnswerRequest,
    DecisionBriefState,
    DecisionSkillResponse,
    ReferenceItem,
)
from app.design_skill.memory import design_prompt_preamble


BANNED_WORDS = {
    "modern",
    "clean",
    "minimal",
    "professional",
    "sleek",
    "premium",
    "beautiful",
    "elegant",
}


OPENING_MESSAGE = """Hey - I'm the Decision Maker. I'll walk you through building a sharp visual brief for your website in about 20 minutes.

Here's what we'll do:

1. Six decisions - feeling, audience, hero object, job, cut, three-second test
2. References - three buckets: feeling, structure, detail
3. Style extraction - color, type, and spatial logic
4. Output - four ready-to-use prompts plus GitHub and Vercel launch guide

Let's start. What's the project? Give me the name and one paragraph: what it is, who it's for, what it does."""


def start_decision_maker() -> DecisionSkillResponse:
    state = DecisionBriefState()
    return DecisionSkillResponse(
        state=state,
        locked=False,
        message=OPENING_MESSAGE,
        next_step=state.current_step,
    )


def answer_decision_maker(request: DecisionAnswerRequest) -> DecisionSkillResponse:
    state = request.state.model_copy(deep=True)
    answer = request.answer.strip()

    if state.current_step == "project":
        state.project_name, state.project_summary = _split_project(answer)
        state.current_step = "feeling"
        return _locked(
            state,
            f"Locked. Project: {state.project_name}.\n\nNext: feeling. What does the visitor need to feel in the first three seconds? Avoid modern, clean, minimal, professional, sleek, premium, beautiful, elegant. Example: 'watched by something invisible' for a security SaaS.",
        )

    if state.current_step == "feeling":
        if _has_banned_word(answer):
            return _pushback(
                state,
                f"'{answer}' is too generic. Push harder: uncomfortable, sensory, narrow. What does {state.project_name or 'this project'} actually do to the person using it? Translate that into a feeling.",
            )
        state.feeling = answer
        state.current_step = "audience"
        return _locked(
            state,
            f"Locked. Decision 1: {answer}.\n\nNext: audience. Who is this for? Picture one real human, not a demographic.",
        )

    if state.current_step == "audience":
        state.audience = answer
        state.current_step = "anti_audience"
        return _locked(
            state,
            f"Locked. Audience: {answer}.\n\nNow the harder half: who is this site not for?",
        )

    if state.current_step == "anti_audience":
        state.anti_audience = answer
        state.current_step = "hero_object"
        return _locked(
            state,
            f"Locked. Decision 2: For {state.audience}. Not for {answer}.\n\nNext: hero object. If the first screen could show only one thing, what is it?",
        )

    if state.current_step == "hero_object":
        state.hero_object = answer
        state.current_step = "job"
        return _locked(
            state,
            f"Locked. Decision 3: {answer}.\n\nNext: the site's one verb. Not 'convert and inform'. One job only. Examples: seduce, convince, disarm, invite.",
        )

    if state.current_step == "job":
        if len(answer.split()) > 3:
            return _pushback(state, "That's too broad. Pick one verb. The whole site will be measured against it.")
        state.job = answer
        state.current_step = "cut"
        return _locked(
            state,
            f"Locked. Decision 4: {answer}.\n\nNext: the cut. List competitor sections you are removing. Example: no logo wall, no generic feature grid, no huge FAQ.",
        )

    if state.current_step == "cut":
        state.cut = answer
        state.current_step = "three_second_memory"
        return _locked(
            state,
            f"Locked. Decision 5: We're cutting {answer}.\n\nLast decision: if someone closes the tab after three seconds, what specific image, word, or feeling do they remember?",
        )

    if state.current_step == "three_second_memory":
        if _has_banned_word(answer) or "nice" in answer.lower():
            return _pushback(state, "That's a failure state. Be specific: object, phrase, feeling. What would they describe to a friend?")
        state.three_second_memory = answer
        state.current_step = "feeling_references"
        return _locked(
            state,
            _decision_summary(state)
            + "\n\nNext: feeling references. Give 3-5 non-website references and one sentence on what visual rule each one gives us.",
        )

    if state.current_step.endswith("_references"):
        references = _parse_references(answer)
        if len(references) < 3:
            return _pushback(state, "Give me at least 3 references. Each one needs a name and one sentence explaining what visual rule we steal.")
        if state.current_step == "feeling_references":
            state.feeling_references = references
            state.current_step = "structure_references"
            return _locked(state, "Locked. Feeling bucket loaded.\n\nNext: structural references. Give 3-5 websites for layout logic, not style.")
        if state.current_step == "structure_references":
            state.structure_references = references
            state.current_step = "detail_references"
            return _locked(state, "Locked. Structure bucket loaded.\n\nNext: detail references. Give 3-5 examples for hover, scroll, type pairings, transitions, or motion.")
        state.detail_references = references
        state.current_step = "color_logic"
        return _locked(state, "Locked. All three buckets loaded.\n\nNext: color logic. What is the color relationship, not the palette?")

    if state.current_step == "color_logic":
        state.color_logic = answer
        state.current_step = "type_logic"
        return _locked(state, f"Locked. Color logic: {answer}.\n\nNext: typography logic. What is the typographic contrast?")

    if state.current_step == "type_logic":
        state.type_logic = answer
        state.current_step = "spatial_logic"
        return _locked(state, f"Locked. Type logic: {answer}.\n\nNext: spatial logic. How is the screen organized?")

    if state.current_step == "spatial_logic":
        state.spatial_logic = answer
        state.current_step = "complete"
        outputs = compile_outputs(state)
        return DecisionSkillResponse(
            state=state,
            locked=True,
            message="Locked. Spatial logic complete. The brief is ready.",
            next_step="complete",
            outputs=outputs,
        )

    return DecisionSkillResponse(
        state=state,
        locked=False,
        message="The brief is already complete. Use the outputs or start a new session.",
        next_step="complete",
        outputs=compile_outputs(state),
    )


def compile_outputs(state: DecisionBriefState) -> dict[str, str]:
    missing = _missing_output_fields(state)
    if missing:
        return {"missing": ", ".join(missing)}

    survivor_sections = state.cut or "hero, proof, features, CTA"
    preamble = design_prompt_preamble()
    return {
        "copywriter_prompt": (
            preamble
            + 
            "You are a senior brand copywriter. Write website copy with this brief:\n"
            f"- Feeling: {state.feeling}\n"
            f"- Audience: {state.audience}\n"
            f"- Anti-audience: {state.anti_audience}\n"
            f"- Hero object: {state.hero_object}\n"
            f"- Job: {state.job}\n"
            f"- Three-second memory: {state.three_second_memory}\n"
            f"Sections: {survivor_sections}\n"
            "Return JSON with hero headline, subheadline, section headlines, CTA, footer line."
        ),
        "visual_prompt": (
            preamble
            +
            f"Generate a hero visual. Object: {state.hero_object}. Feeling: {state.feeling}. "
            f"Color logic: {state.color_logic}. Spatial logic: {state.spatial_logic}. "
            "4K, cinematic lighting, transparent background, no humans unless explicitly part of the object."
        ),
        "design_prompt": (
            preamble
            +
            f"Design a landing page. Feeling: {state.feeling}. Hero object: {state.hero_object}. "
            f"Color: {state.color_logic}. Type: {state.type_logic}. Spatial: {state.spatial_logic}. "
            f"Sections: {survivor_sections}."
        ),
        "developer_prompt": (
            preamble
            +
            "Build a responsive animated landing page with Next.js. Use CSS custom properties for the style logic, "
            "GSAP or Framer Motion for entrance/scroll animation, WebP assets, lazy loading, AA contrast, "
            "and prefers-reduced-motion support."
        ),
        "launch_guide": (
            "1. git init, git add ., git commit -m \"Initial commit\".\n"
            "2. Create a GitHub repo and push the code.\n"
            "3. Import the repo into Vercel.\n"
            "4. Add environment variables.\n"
            "5. Deploy and connect a custom domain if needed."
        ),
    }


def _locked(state: DecisionBriefState, message: str) -> DecisionSkillResponse:
    return DecisionSkillResponse(state=state, locked=True, message=message, next_step=state.current_step)


def _pushback(state: DecisionBriefState, message: str) -> DecisionSkillResponse:
    return DecisionSkillResponse(state=state, locked=False, message=message, next_step=state.current_step)


def _split_project(answer: str) -> tuple[str, str]:
    if "\n" in answer:
        first, rest = answer.split("\n", 1)
        return first.strip()[:80], rest.strip()
    words = answer.split()
    name = " ".join(words[:4]) if words else "Untitled Project"
    return name, answer


def _has_banned_word(answer: str) -> bool:
    words = {word.strip(".,!?;:").lower() for word in answer.split()}
    return bool(words.intersection(BANNED_WORDS))


def _parse_references(answer: str) -> list[ReferenceItem]:
    lines = [line.strip(" -\t") for line in answer.splitlines() if line.strip()]
    if len(lines) == 1 and ";" in lines[0]:
        lines = [item.strip() for item in lines[0].split(";") if item.strip()]
    references = []
    for line in lines:
        if ":" in line:
            name, note = line.split(":", 1)
        elif "-" in line:
            name, note = line.split("-", 1)
        else:
            name, note = line[:60], line
        references.append(ReferenceItem(name=name.strip(), note=note.strip()))
    return references


def _decision_summary(state: DecisionBriefState) -> str:
    return (
        "That's the decision layer:\n"
        f"1. Feeling: {state.feeling}\n"
        f"2. Audience: {state.audience}. Not for: {state.anti_audience}\n"
        f"3. Hero object: {state.hero_object}\n"
        f"4. Job: {state.job}\n"
        f"5. Cut: {state.cut}\n"
        f"6. Three-second memory: {state.three_second_memory}"
    )


def _missing_output_fields(state: DecisionBriefState) -> list[str]:
    required = {
        "feeling": state.feeling,
        "audience": state.audience,
        "anti_audience": state.anti_audience,
        "hero_object": state.hero_object,
        "job": state.job,
        "three_second_memory": state.three_second_memory,
        "color_logic": state.color_logic,
        "type_logic": state.type_logic,
        "spatial_logic": state.spatial_logic,
    }
    return [name for name, value in required.items() if not value]
