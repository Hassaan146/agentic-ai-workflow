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
