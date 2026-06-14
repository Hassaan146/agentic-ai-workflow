import type {
  NodeTrace,
  RunCreateRequest,
  RunResponse,
  UsageLog
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type AuthPayload = {
  email: string;
  password: string;
  full_name?: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  user: { user_id: string; email?: string; name?: string };
};

export async function login(payload: AuthPayload): Promise<AuthResponse> {
  return authRequest("/api/auth/login", payload);
}

export async function signup(payload: AuthPayload): Promise<AuthResponse> {
  return authRequest("/api/auth/signup", payload);
}

async function authRequest(path: string, payload: AuthPayload): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Authentication failed.");
  }

  return response.json();
}


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
