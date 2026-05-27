from typing import Literal

from pydantic import BaseModel, Field


DecisionStep = Literal[
    "project",
    "feeling",
    "audience",
    "anti_audience",
    "hero_object",
    "job",
    "cut",
    "three_second_memory",
    "feeling_references",
    "structure_references",
    "detail_references",
    "color_logic",
    "type_logic",
    "spatial_logic",
    "complete",
]


class ReferenceItem(BaseModel):
    name: str
    note: str


class DecisionBriefState(BaseModel):
    current_step: DecisionStep = "project"
    project_name: str | None = None
    project_summary: str | None = None
    feeling: str | None = None
    audience: str | None = None
    anti_audience: str | None = None
    hero_object: str | None = None
    job: str | None = None
    cut: str | None = None
    three_second_memory: str | None = None
    feeling_references: list[ReferenceItem] = Field(default_factory=list)
    structure_references: list[ReferenceItem] = Field(default_factory=list)
    detail_references: list[ReferenceItem] = Field(default_factory=list)
    color_logic: str | None = None
    type_logic: str | None = None
    spatial_logic: str | None = None


class DecisionAnswerRequest(BaseModel):
    state: DecisionBriefState = Field(default_factory=DecisionBriefState)
    answer: str = Field(min_length=1, max_length=5000)


class DecisionSkillResponse(BaseModel):
    state: DecisionBriefState
    locked: bool
    message: str
    next_step: DecisionStep
    outputs: dict[str, str] | None = None


class PipelineStep(BaseModel):
    number: str
    phase: str
    title: str
    purpose: str
    tools: list[str]

