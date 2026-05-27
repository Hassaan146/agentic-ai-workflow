from fastapi.testclient import TestClient

from app.design_skill.decision_maker import answer_decision_maker, start_decision_maker
from app.design_skill.memory import project_memory_payload
from app.design_skill.models import DecisionAnswerRequest, DecisionBriefState
from app.main import create_app


def test_decision_maker_starts_with_project_step() -> None:
    response = start_decision_maker()

    assert response.next_step == "project"
    assert "six decisions" in response.message.lower()


def test_decision_maker_pushes_back_on_generic_feeling() -> None:
    state = DecisionBriefState(
        current_step="feeling",
        project_name="Agentic AI Workflow",
        project_summary="A multi-agent workflow platform.",
    )

    response = answer_decision_maker(
        DecisionAnswerRequest(state=state, answer="modern and clean")
    )

    assert response.locked is False
    assert response.next_step == "feeling"
    assert "too generic" in response.message


def test_decision_maker_advances_and_compiles_outputs() -> None:
    state = DecisionBriefState(
        current_step="spatial_logic",
        project_name="Agentic AI Workflow",
        project_summary="A multi-agent workflow platform.",
        feeling="watching a mission control board come alive",
        audience="the builder who wants visible AI systems",
        anti_audience="people looking for a generic chatbot",
        hero_object="a live state graph",
        job="convince",
        cut="generic testimonials, logo wall, oversized FAQ",
        three_second_memory="a glowing graph routing tasks between agents",
        color_logic="dark neutral interface with one active execution color",
        type_logic="small functional sans paired with large command-style headlines",
    )

    response = answer_decision_maker(
        DecisionAnswerRequest(
            state=state,
            answer="center-weighted graph canvas with utility panels on the edges",
        )
    )

    assert response.next_step == "complete"
    assert response.outputs is not None
    assert "copywriter_prompt" in response.outputs
    assert "developer_prompt" in response.outputs
    assert "ALWAYS-ON PROJECT PIPELINE" in response.outputs["copywriter_prompt"]
    assert "Decision Maker" in response.outputs["developer_prompt"]


def test_design_skill_api_exposes_start_and_pipeline() -> None:
    client = TestClient(create_app())

    start_response = client.get("/api/design-skill/start")
    pipeline_response = client.get("/api/design-skill/pipeline")

    assert start_response.status_code == 200
    assert start_response.json()["next_step"] == "project"
    assert pipeline_response.status_code == 200
    assert len(pipeline_response.json()) == 11


def test_design_skill_memory_payload_is_available() -> None:
    payload = project_memory_payload()

    assert payload["skill"] == "Decision Maker"
    assert "always-on" in payload["rule"]
    assert "Mission Control Graph" in payload["frontend_visual_recommendation"]


def test_design_skill_memory_api() -> None:
    client = TestClient(create_app())

    response = client.get("/api/design-skill/memory")

    assert response.status_code == 200
    assert response.json()["skill"] == "Decision Maker"
