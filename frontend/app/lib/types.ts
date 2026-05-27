export type RunCreateRequest = {
  user_request: string;
  template_key: string;
};

export type FinalOutput = {
  title: string;
  answer: string;
  sources: Array<{ title: string; url: string }>;
  trace_summary: string[];
};

export type RunResponse = {
  id: string;
  clerk_user_id: string;
  template_key: string;
  user_request: string;
  status: "queued" | "running" | "completed" | "failed";
  final_output: FinalOutput | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
};

export type TemplateResponse = {
  key: string;
  name: string;
  description: string;
  starter_prompt: string;
};

export type NodeTrace = {
  id: string;
  run_id: string;
  node_key: string;
  agent_name: string;
  status: "running" | "completed" | "failed";
  input_payload: Record<string, unknown>;
  output_payload: Record<string, unknown>;
  error_message: string | null;
  started_at: string;
  completed_at: string | null;
};

export type UsageLog = {
  id: string;
  run_id: string;
  provider: string;
  model: string;
  purpose: string;
  prompt_tokens: number;
  completion_tokens: number;
  estimated_cost: number;
  created_at: string;
};

export type DecisionStep =
  | "project"
  | "feeling"
  | "audience"
  | "anti_audience"
  | "hero_object"
  | "job"
  | "cut"
  | "three_second_memory"
  | "feeling_references"
  | "structure_references"
  | "detail_references"
  | "color_logic"
  | "type_logic"
  | "spatial_logic"
  | "complete";

export type ReferenceItem = {
  name: string;
  note: string;
};

export type DecisionBriefState = {
  current_step: DecisionStep;
  project_name: string | null;
  project_summary: string | null;
  feeling: string | null;
  audience: string | null;
  anti_audience: string | null;
  hero_object: string | null;
  job: string | null;
  cut: string | null;
  three_second_memory: string | null;
  feeling_references: ReferenceItem[];
  structure_references: ReferenceItem[];
  detail_references: ReferenceItem[];
  color_logic: string | null;
  type_logic: string | null;
  spatial_logic: string | null;
};

export type DecisionSkillResponse = {
  state: DecisionBriefState;
  locked: boolean;
  message: string;
  next_step: DecisionStep;
  outputs: Record<string, string> | null;
};

export type PipelineStep = {
  number: string;
  phase: string;
  title: string;
  purpose: string;
  tools: string[];
};
