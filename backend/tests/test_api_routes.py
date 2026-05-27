from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_run_creation_requires_auth() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/runs",
        json={"user_request": "Research AI workflow tools.", "template_key": "research"},
    )

    assert response.status_code == 401


def test_templates_endpoint_lists_mvp_templates() -> None:
    client = TestClient(create_app())

    response = client.get("/api/templates")

    assert response.status_code == 200
    template_keys = {template["key"] for template in response.json()}
    assert {"research", "product_comparison", "startup_validator"}.issubset(template_keys)


def test_run_creation_and_listing_with_dev_token() -> None:
    client = TestClient(create_app())
    headers = {"Authorization": "Bearer dev-token"}

    create_response = client.post(
        "/api/runs",
        headers=headers,
        json={"user_request": "Find me a car under $500.", "template_key": "product_comparison"},
    )
    list_response = client.get("/api/runs", headers=headers)

    assert create_response.status_code == 200
    created_run = create_response.json()
    assert created_run["status"] == "completed"
    assert created_run["final_output"]["trace_summary"]
    assert list_response.status_code == 200
    assert any(run["id"] == created_run["id"] for run in list_response.json())


def test_run_event_stream_returns_node_traces() -> None:
    client = TestClient(create_app())
    headers = {"Authorization": "Bearer dev-token"}

    create_response = client.post(
        "/api/runs",
        headers=headers,
        json={"user_request": "Validate my startup idea.", "template_key": "startup_validator"},
    )
    run_id = create_response.json()["id"]
    events_response = client.get(f"/api/runs/{run_id}/events", headers=headers)

    assert events_response.status_code == 200
    assert "structure_request" in events_response.text
    assert "final_response" in events_response.text


def test_run_stream_creates_run_and_emits_trace_events() -> None:
    client = TestClient(create_app())
    headers = {"Authorization": "Bearer dev-token"}

    response = client.post(
        "/api/runs/stream",
        headers=headers,
        json={"user_request": "Compare two AI workflow tools.", "template_key": "product_comparison"},
    )

    assert response.status_code == 200
    assert "event: run" in response.text
    assert "event: trace" in response.text
    assert "event: done" in response.text
    assert "final_response" in response.text


def test_run_trace_and_usage_endpoints_return_inspection_data() -> None:
    client = TestClient(create_app())
    headers = {"Authorization": "Bearer dev-token"}

    create_response = client.post(
        "/api/runs",
        headers=headers,
        json={"user_request": "Find me a car under $500.", "template_key": "product_comparison"},
    )
    run_id = create_response.json()["id"]

    traces_response = client.get(f"/api/runs/{run_id}/traces", headers=headers)
    usage_response = client.get(f"/api/runs/{run_id}/usage", headers=headers)

    assert traces_response.status_code == 200
    assert usage_response.status_code == 200
    assert any(trace["node_key"] == "structure_request" for trace in traces_response.json())
    assert any(log["purpose"] == "structure" for log in usage_response.json())
