from datetime import UTC, datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


RunStatus = Literal["queued", "running", "completed", "failed"]
NodeStatus = Literal["running", "completed", "failed"]
AgentType = Literal["reasoning", "search", "comparison", "extraction", "writing"]


class RunCreateRequest(BaseModel):
    user_request: str = Field(min_length=3, max_length=5000)
    template_key: str = Field(default="generic", max_length=80)


class TemplateResponse(BaseModel):
    key: str
    name: str
    description: str
    starter_prompt: str


class StructuredRequest(BaseModel):
    original_request: str
    goal: str
    constraints: list[str] = Field(default_factory=list)
    expected_output: str = "Clear final answer with reasoning"


class WorkflowTask(BaseModel):
    id: str
    title: str
    agent_type: AgentType
    depends_on: list[str] = Field(default_factory=list)
    instructions: str


class TaskPlan(BaseModel):
    tasks: list[WorkflowTask]
    execution_order: list[str]


class AgentOutput(BaseModel):
    task_id: str
    agent_name: str
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)


class FinalOutput(BaseModel):
    title: str
    answer: str
    sources: list[dict[str, str]] = Field(default_factory=list)
    trace_summary: list[str] = Field(default_factory=list)


class NodeTrace(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    node_key: str
    agent_name: str
    status: NodeStatus
    input_payload: dict[str, Any] = Field(default_factory=dict)
    output_payload: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None


class UsageLog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    provider: str
    model: str
    purpose: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost: float = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RunResponse(BaseModel):
    id: UUID
    clerk_user_id: str
    template_key: str
    user_request: str
    status: RunStatus
    final_output: FinalOutput | None = None
    error_message: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class WorkflowResult(BaseModel):
    final_output: FinalOutput


class AdminUser(BaseModel):
    id: UUID | str
    email: str
    full_name: str | None = None
    is_admin: bool = False
    auth_provider: str = "local"
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdminStats(BaseModel):
    users: int = 0
    runs: int = 0
    traces: int = 0
    usage_logs: int = 0
    estimated_tokens: int = 0
