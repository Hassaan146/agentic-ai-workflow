from datetime import UTC, datetime
from typing import Any, TypedDict
from uuid import UUID, uuid4

from langgraph.graph import END, StateGraph

from app.llm.providers import get_model_provider
from app.llm.prompts import agent_task_prompt, structure_request_prompt
from app.orchestration.outputs import build_agent_output
from app.orchestration.toon import to_toon
from app.orchestration.planner import build_task_plan, order_tasks_by_prerequisites
from app.schemas.workflow import (
    AgentOutput,
    FinalOutput,
    NodeTrace,
    StructuredRequest,
    UsageLog,
    WorkflowResult,
    WorkflowTask,
)
from app.storage.repository import RunRepository
from app.tools.search import ControlledSearchTool


class WorkflowState(TypedDict, total=False):
    run_id: UUID
    user_request: str
    template_key: str
    structured_request: StructuredRequest
    tasks: list[WorkflowTask]
    agent_outputs: list[AgentOutput]
    final_output: FinalOutput
    verification_passed: bool
    repository: RunRepository


async def run_agentic_workflow(
    *,
    run_id: UUID,
    user_request: str,
    template_key: str,
    repository: RunRepository,
) -> WorkflowResult:
    graph = _build_graph(repository)
    initial_state: WorkflowState = {
        "run_id": run_id,
        "user_request": user_request,
        "template_key": template_key,
        "repository": repository,
        "agent_outputs": [],
        "verification_passed": False,
    }
    final_state = await graph.ainvoke(initial_state)
    return WorkflowResult(final_output=final_state["final_output"])


def _build_graph(repository: RunRepository):
    workflow = StateGraph(WorkflowState)
    workflow.add_node("structure_request", _trace(repository, "structure_request", "Request Structuring Agent", structure_request))
    workflow.add_node("decompose_tasks", _trace(repository, "decompose_tasks", "Task Decomposition Agent", decompose_tasks))
    workflow.add_node("analyze_prerequisites", _trace(repository, "analyze_prerequisites", "Prerequisite Analyzer", analyze_prerequisites))
    workflow.add_node("execute_agents", _trace(repository, "execute_agents", "Specialized Agent Pool", execute_agents))
    workflow.add_node("verify_output", _trace(repository, "verify_output", "Verifier Agent", verify_output))
    workflow.add_node("final_response", _trace(repository, "final_response", "Final Response Agent", final_response))

    workflow.set_entry_point("structure_request")
    workflow.add_edge("structure_request", "decompose_tasks")
    workflow.add_edge("decompose_tasks", "analyze_prerequisites")
    workflow.add_edge("analyze_prerequisites", "execute_agents")
    workflow.add_edge("execute_agents", "verify_output")
    workflow.add_conditional_edges(
        "verify_output",
        lambda state: "final_response" if state.get("verification_passed") else "execute_agents",
        {"execute_agents": "execute_agents", "final_response": "final_response"},
    )
    workflow.add_edge("final_response", END)
    return workflow.compile()


def _trace(repository: RunRepository, node_key: str, agent_name: str, handler):
    async def wrapped(state: WorkflowState) -> WorkflowState:
        trace = NodeTrace(
            run_id=state["run_id"],
            node_key=node_key,
            agent_name=agent_name,
            status="running",
            input_payload=_compact_state(state),
        )
        repository.add_node_trace(trace)
        try:
            next_state = await handler(state)
            repository.add_node_trace(
                trace.model_copy(
                    update={
                        "id": uuid4(),
                        "status": "completed",
                        "output_payload": _compact_state(next_state),
                        "completed_at": datetime.now(UTC),
                    }
                )
            )
            return next_state
        except Exception as exc:
            repository.add_node_trace(
                trace.model_copy(
                    update={
                        "id": uuid4(),
                        "status": "failed",
                        "error_message": str(exc),
                        "completed_at": datetime.now(UTC),
                    }
                )
            )
            raise

    return wrapped


async def structure_request(state: WorkflowState) -> WorkflowState:
    provider = get_model_provider()
    request = state["user_request"]
    prompt = structure_request_prompt(request)
    response = await _complete_with_retry(provider, prompt, purpose="structure")
    _log_usage(state["run_id"], state["repository"], provider, "structure", prompt, response)
    structured = StructuredRequest(
        original_request=request,
        goal=request.strip(),
        constraints=_extract_constraints(request),
        expected_output="A clear answer with reasoning, sources when available, and trace summary.",
    )
    return {**state, "structured_request": structured}


async def decompose_tasks(state: WorkflowState) -> WorkflowState:
    structured = state["structured_request"]
    plan = build_task_plan(structured)
    return {**state, "tasks": plan.tasks}


async def analyze_prerequisites(state: WorkflowState) -> WorkflowState:
    tasks = order_tasks_by_prerequisites(state["tasks"])
    return {**state, "tasks": tasks}


async def execute_agents(state: WorkflowState) -> WorkflowState:
    provider = get_model_provider()
    search_tool = ControlledSearchTool()
    structured = state["structured_request"]
    outputs: list[AgentOutput] = list(state.get("agent_outputs", []))
    completed_ids = {output.task_id for output in outputs}

    for task in state["tasks"]:
        if task.id in completed_ids:
            continue
        if any(dependency not in completed_ids for dependency in task.depends_on):
            continue

        handoff_context = _dependency_handoff_context(task, outputs)

        if task.agent_type == "search":
            results = await search_tool.search(structured.goal, limit=5)
            fact_count = sum(len(result.facts) for result in results)
            outputs.append(
                build_agent_output(
                    task=task,
                    agent_name="Search Agent",
                    summary=f"Collected {len(results)} sources and extracted {fact_count} raw facts with website context.",
                    extra_data={
                        "sources": [result.model_dump() for result in results],
                        "input_handoff_format": "toon" if handoff_context else "none",
                        "input_handoff": handoff_context,
                    },
                )
            )
        else:
            prompt = agent_task_prompt(task, structured, handoff_context=handoff_context)
            content = await _complete_with_retry(provider, prompt, purpose=task.agent_type)
            _log_usage(
                state["run_id"],
                state["repository"],
                provider,
                task.agent_type,
                prompt,
                content,
            )
            outputs.append(
                build_agent_output(
                    task=task,
                    agent_name=f"{task.agent_type.title()} Agent",
                    summary=content,
                )
            )

    return {**state, "agent_outputs": outputs}


def _dependency_handoff_context(task: WorkflowTask, outputs: list[AgentOutput]) -> str:
    dependency_outputs = [output for output in outputs if output.task_id in task.depends_on]
    if not dependency_outputs:
        return ""
    blocks = []
    for output in dependency_outputs:
        payload = output.data.get("toon_payload")
        if payload:
            blocks.append(str(payload))
    if blocks:
        return "\n---\n".join(blocks)
    return to_toon(
        [
            {
                "task_id": output.task_id,
                "agent": output.agent_name,
                "summary": output.summary,
            }
            for output in dependency_outputs
        ]
    )


async def verify_output(state: WorkflowState) -> WorkflowState:
    task_ids = {task.id for task in state["tasks"]}
    completed_ids = {output.task_id for output in state.get("agent_outputs", [])}
    return {**state, "verification_passed": task_ids.issubset(completed_ids)}


async def final_response(state: WorkflowState) -> WorkflowState:
    structured = state["structured_request"]
    outputs = state.get("agent_outputs", [])
    sources = []
    for output in outputs:
        sources.extend(output.data.get("sources", []))

    answer = await _compose_final_answer(structured.goal, outputs, sources)
    final = FinalOutput(
        title=f"Research brief: {structured.goal[:80]}",
        answer=answer,
        sources=[
            {
                "title": source.get("title", "Untitled source"),
                "url": source.get("url", ""),
                "summary": source.get("summary", ""),
                "context": source.get("source_context", ""),
                "facts": " | ".join(source.get("facts", [])[:3]),
            }
            for source in sources[:5]
        ],
        trace_summary=[
            f"{output.agent_name}: {output.summary[:160]}"
            for output in outputs
        ],
    )
    _log_usage(state["run_id"], state["repository"], get_model_provider(), "final_response", structured.goal, answer)
    return {**state, "final_output": final}


def _extract_constraints(request: str) -> list[str]:
    constraints = []
    if "$" in request or "under" in request.lower() or "less than" in request.lower():
        constraints.append("Budget or price constraint detected")
    if "only if" in request.lower():
        constraints.append("Conditional prerequisite detected")
    return constraints


async def _compose_final_answer(goal: str, outputs: list[AgentOutput], sources: list[dict[str, Any]]) -> str:
    completed_agents = ", ".join(output.agent_name for output in outputs)
    source_context = _format_source_context(sources)
    if not source_context:
        return (
            f"Research request: {goal}\n\n"
            "No live source facts were available. Check that SEARCH_PROVIDER=duckduckgo and that the backend has network access. "
            f"Agents completed: {completed_agents}."
        )

    provider = get_model_provider()
    prompt = (
        "Write a concise research brief using only the source facts below. "
        "Do not invent facts. If the sources are weak, say so. "
        "Include these sections: Overview, Past, Present, Future, Sustainability, Bottom line, Sources used.\n\n"
        f"User request: {goal}\n\n"
        f"Source facts:\n{source_context}"
    )
    try:
        answer = await _complete_with_retry(provider, prompt, purpose="writing")
        if "Deterministic writing response" not in answer:
            return answer
    except Exception:
        pass

    return _compose_fallback_research_answer(goal, completed_agents, source_context)


def _format_source_context(sources: list[dict[str, Any]]) -> str:
    blocks = []
    for index, source in enumerate(sources[:5], start=1):
        facts = source.get("facts", [])
        fact_text = "\n".join(f"  - {fact}" for fact in facts[:4])
        if not fact_text:
            continue
        blocks.append(
            f"[{index}] {source.get('title', 'Untitled source')}\n"
            f"URL: {source.get('url', '')}\n"
            f"Context: {source.get('source_context', '')}\n"
            f"Facts:\n{fact_text}"
        )
    return "\n\n".join(blocks)


def _compose_fallback_research_answer(goal: str, completed_agents: str, source_context: str) -> str:
    return (
        f"Overview\nThe workflow researched: {goal}. The answer below is built from scraped source facts, not unsupported model opinion.\n\n"
        "Past\nUse the source context to identify historical milestones and early development.\n\n"
        "Present\nUse the source context to describe the current market/product state and adoption signals.\n\n"
        "Future\nUse the source context to describe likely future direction, while avoiding certainty where sources are limited.\n\n"
        "Sustainability\nUse the source context to separate sustainability claims from verified facts.\n\n"
        f"Bottom line\nAgents completed: {completed_agents}. The strongest available evidence is listed below.\n\n"
        f"Sources used\n{source_context}"
    )


def _compact_state(state: WorkflowState) -> dict[str, Any]:
    compact: dict[str, Any] = {
        "user_request": state.get("user_request"),
        "template_key": state.get("template_key"),
        "verification_passed": state.get("verification_passed"),
    }
    if state.get("structured_request"):
        compact["structured_request"] = state["structured_request"].model_dump()
    if state.get("tasks"):
        compact["task_count"] = len(state["tasks"])
    if state.get("agent_outputs"):
        compact["agent_output_count"] = len(state["agent_outputs"])
        compact["handoff_format"] = "toon"
    if state.get("final_output"):
        compact["final_output"] = state["final_output"].model_dump()
    return compact


async def _complete_with_retry(provider, prompt: str, *, purpose: str, attempts: int = 2) -> str:
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return await provider.complete(prompt, purpose=purpose)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Model call failed after {attempts} attempts.") from last_error


def _log_usage(
    run_id: UUID,
    repository: RunRepository,
    provider,
    purpose: str,
    prompt: str,
    response: str,
) -> None:
    repository.add_usage_log(
        UsageLog(
            run_id=run_id,
            provider=provider.provider_name,
            model=provider.model_name,
            purpose=purpose,
            prompt_tokens=_estimate_tokens(prompt),
            completion_tokens=_estimate_tokens(response),
            estimated_cost=0,
        )
    )


def _estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))
