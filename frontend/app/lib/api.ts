import type {
  DecisionBriefState,
  DecisionSkillResponse,
  PipelineStep,
  NodeTrace,
  RunCreateRequest,
  RunResponse,
  TemplateResponse,
  UsageLog
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function createRun(payload: RunCreateRequest, token: string | null): Promise<RunResponse> {
  const response = await fetch(`${API_BASE_URL}/api/runs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to create workflow run.");
  }

  return response.json();
}

type StreamRunHandlers = {
  onRun: (run: RunResponse) => void;
  onTrace: (trace: NodeTrace) => void;
  onError: (message: string) => void;
};

export async function streamRun(
  payload: RunCreateRequest,
  token: string | null,
  handlers: StreamRunHandlers
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/runs/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok || !response.body) {
    const text = await response.text();
    throw new Error(text || "Unable to stream workflow run.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";

    for (const eventBlock of events) {
      const eventName = eventBlock.match(/^event:\s*(.+)$/m)?.[1];
      const data = eventBlock.match(/^data:\s*(.+)$/m)?.[1];
      if (!eventName || !data) continue;
      const parsed = JSON.parse(data);

      if (eventName === "run") handlers.onRun(parsed as RunResponse);
      if (eventName === "trace") handlers.onTrace(parsed as NodeTrace);
      if (eventName === "error") handlers.onError(parsed.message ?? "Workflow run failed.");
    }
  }
}

export async function listRuns(token: string | null): Promise<RunResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/runs`, {
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to load workflow runs.");
  }

  return response.json();
}

export async function listRunTraces(runId: string, token: string | null): Promise<NodeTrace[]> {
  const response = await fetch(`${API_BASE_URL}/api/runs/${runId}/traces`, {
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to load run traces.");
  }

  return response.json();
}

export async function listRunUsage(runId: string, token: string | null): Promise<UsageLog[]> {
  const response = await fetch(`${API_BASE_URL}/api/runs/${runId}/usage`, {
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to load usage logs.");
  }

  return response.json();
}

export async function listTemplates(): Promise<TemplateResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/templates`);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to load workflow templates.");
  }

  return response.json();
}

export async function startDecisionSkill(): Promise<DecisionSkillResponse> {
  const response = await fetch(`${API_BASE_URL}/api/design-skill/start`);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to start Decision Maker.");
  }

  return response.json();
}

export async function answerDecisionSkill(
  state: DecisionBriefState,
  answer: string
): Promise<DecisionSkillResponse> {
  const response = await fetch(`${API_BASE_URL}/api/design-skill/answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ state, answer })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to advance Decision Maker.");
  }

  return response.json();
}

export async function listDesignPipeline(): Promise<PipelineStep[]> {
  const response = await fetch(`${API_BASE_URL}/api/design-skill/pipeline`);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Unable to load design pipeline.");
  }

  return response.json();
}
