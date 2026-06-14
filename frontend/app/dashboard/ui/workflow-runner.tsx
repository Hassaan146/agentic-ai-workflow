"use client";

import {
  ArrowUpRight,
  Bot,
  CheckCircle2,
  CircleDashed,
  Clock3,
  FileText,
  GitBranch,
  Loader2,
  Menu,
  MessageSquareText,
  PanelLeftClose,
  Play,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  UserRound,
  Workflow,
  XCircle
} from "lucide-react";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { listRuns, listRunTraces, listRunUsage, streamRun } from "../../lib/api";
import type { NodeTrace, RunResponse, UsageLog } from "../../lib/types";

type WorkflowRunnerProps = {
  getToken: () => Promise<string | null>;
};

type DisplayStep = {
  key: string;
  label: string;
  description: string;
  icon: typeof CircleDashed;
};

const GENERIC_TEMPLATE_KEY = "generic";

const AGENT_STEPS: DisplayStep[] = [
  { key: "structure_request", label: "Structuring prompt", description: "Converting the user message into clean intent.", icon: MessageSquareText },
  { key: "decompose_tasks", label: "Planning tasks", description: "Breaking the request into executable agent work.", icon: GitBranch },
  { key: "analyze_prerequisites", label: "Checking prerequisites", description: "Ordering dependencies before agent execution.", icon: ShieldCheck },
  { key: "execute_agents", label: "Running specialists", description: "Routing search, reasoning, writing, and extraction agents.", icon: Bot },
  { key: "verify_output", label: "Verifying output", description: "Checking whether every required task completed.", icon: CheckCircle2 },
  { key: "final_response", label: "Formatting response", description: "Preparing the final answer for the user.", icon: FileText }
];

const SUGGESTED_PROMPTS = [
  "Research the future of AI agents in SaaS and give sources.",
  "Compare LangGraph and CrewAI for a student project.",
  "Plan a launch workflow for an AI news aggregator.",
  "Extract key facts from recent AI model announcements."
];

export default function WorkflowRunner({ getToken }: WorkflowRunnerProps) {
  const [run, setRun] = useState<RunResponse | null>(null);
  const [traces, setTraces] = useState<NodeTrace[]>([]);
  const [usageLogs, setUsageLogs] = useState<UsageLog[]>([]);
  const [recentRuns, setRecentRuns] = useState<RunResponse[]>([]);
  const [error, setError] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [requestText, setRequestText] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    async function loadInitialData() {
      try {
        const token = await getToken();
        const runData = await listRuns(token);
        setRecentRuns(runData);
      } catch {
        setRecentRuns([]);
      }
    }

    loadInitialData();
  }, [getToken]);

  useEffect(() => {
    async function loadRunInspection() {
      if (!run) {
        setUsageLogs([]);
        return;
      }

      try {
        const token = await getToken();
        const [traceData, usageData] = await Promise.all([
          listRunTraces(run.id, token),
          listRunUsage(run.id, token)
        ]);
        setTraces(traceData);
        setUsageLogs(usageData);
      } catch {
        setUsageLogs([]);
      }
    }

    loadRunInspection();
  }, [getToken, run]);

  const stepStatuses = useMemo(() => buildStepStatuses(traces), [traces]);
  const activeStep = useMemo(() => {
    const runningTrace = traces.find((trace) => trace.status === "running");
    if (runningTrace) return runningTrace.node_key;
    const completed = new Set(traces.filter((trace) => trace.status === "completed").map((trace) => trace.node_key));
    return AGENT_STEPS.find((step) => !completed.has(step.key))?.key ?? "final_response";
  }, [traces]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const submittedRequest = requestText.trim();
    if (submittedRequest.length < 3) {
      setError("Please enter a request before starting the workflow.");
      return;
    }

    setIsRunning(true);
    setError("");
    setRun(null);
    setTraces([]);
    setUsageLogs([]);
    try {
      const token = await getToken();
      let completedRunId: string | null = null;
      await streamRun(
        { user_request: submittedRequest, template_key: GENERIC_TEMPLATE_KEY },
        token,
        {
          onRun: (nextRun) => {
            completedRunId = nextRun.id;
            setRun(nextRun);
            setRecentRuns((currentRuns) => [
              nextRun,
              ...currentRuns.filter((item) => item.id !== nextRun.id)
            ]);
          },
          onTrace: (trace) => {
            // The backend streams every agent switch here; the UI turns those traces into user-readable progress.
            setTraces((currentTraces) => {
              const withoutDuplicate = currentTraces.filter((item) => item.id !== trace.id);
              return [...withoutDuplicate, trace];
            });
          },
          onError: (message) => setError(message)
        }
      );

      if (completedRunId) {
        const usageData = await listRunUsage(completedRunId, token);
        setUsageLogs(usageData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Workflow failed.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <main className="agent-app-shell">
      <video
        aria-hidden="true"
        autoPlay
        className="video-backdrop"
        loop
        muted
        playsInline
        preload="auto"
        src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_094631_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4"
      />

      <aside className={`chat-sidebar liquid-glass ${sidebarOpen ? "open" : "closed"}`}>
        <div className="sidebar-head">
          <a className="brand-orb small" href="/">a</a>
          <button aria-label="Toggle sidebar" className="icon-button" onClick={() => setSidebarOpen((value) => !value)} type="button">
            {sidebarOpen ? <PanelLeftClose size={18} /> : <Menu size={18} />}
          </button>
        </div>
        {sidebarOpen && (
          <>
            <button className="new-chat-button" onClick={() => { setRun(null); setTraces([]); setUsageLogs([]); setRequestText(""); }} type="button">
              <Sparkles size={16} /> New workflow
            </button>
            <div className="history-list">
              <p>Previous chats</p>
              {!recentRuns.length && <span className="muted-small">Your completed workflows will appear here.</span>}
              {recentRuns.slice(0, 12).map((item) => (
                <button className="history-item" key={item.id} onClick={() => setRun(item)} type="button">
                  <MessageSquareText size={15} />
                  <span>{item.user_request}</span>
                  <small>{item.status}</small>
                </button>
              ))}
            </div>
          </>
        )}
      </aside>

      <section className="chat-stage">
        <header className="workspace-topbar liquid-glass">
          <div>
            <p>// AI orchestration workspace</p>
            <h1>Agentic AI Workflow</h1>
          </div>
          <a className="glass-button" href="/signup">Save workspace <ArrowUpRight size={16} /></a>
        </header>

        <div className="conversation-panel liquid-glass">
          <div className="message-row user-row">
            <span className="avatar"><UserRound size={18} /></span>
            <div>
              <small>User prompt</small>
              <p>{run?.user_request || requestText || "Ask the orchestration platform to research, compare, plan, validate, extract, or write anything."}</p>
            </div>
          </div>

          <div className="message-row agent-row">
            <span className="avatar bot"><Bot size={18} /></span>
            <div className="assistant-output">
              <small>Final response</small>
              {!run && <p className="empty-output">The answer will appear here after the agents finish their workflow.</p>}
              {run && (
                <>
                  <span className={`run-status ${run.status}`}>{run.status}</span>
                  <h2>{run.final_output?.title ?? "Workflow result"}</h2>
                  <p className="final-answer">{run.final_output?.answer ?? "The workflow is still preparing the final answer."}</p>
                </>
              )}
            </div>
          </div>

          {run?.final_output?.sources.length ? (
            <div className="source-dock">
              <h3><Search size={18} /> Source context</h3>
              {run.final_output.sources.map((source, index) => (
                <article className="source-card" key={`${source.url}-${index}`}>
                  <a href={source.url} target="_blank">{source.title}</a>
                  {source.context && <small>{source.context}</small>}
                  {source.summary && <p>{source.summary}</p>}
                  {source.facts && <p><strong>Facts:</strong> {source.facts}</p>}
                </article>
              ))}
            </div>
          ) : null}
        </div>

        <form className="prompt-composer liquid-glass" onSubmit={handleSubmit}>
          <textarea
            aria-label="Workflow prompt"
            onChange={(event) => setRequestText(event.target.value)}
            placeholder="Ask your AI agents to research, compare, plan, validate, extract, or write..."
            value={requestText}
          />
          <div className="composer-footer">
            <div className="prompt-chips">
              {SUGGESTED_PROMPTS.slice(0, 3).map((prompt) => (
                <button key={prompt} onClick={() => setRequestText(prompt)} type="button">{prompt}</button>
              ))}
            </div>
            <button className="send-button" disabled={isRunning} type="submit">
              {isRunning ? <Loader2 className="spin" size={18} /> : <Send size={18} />}
              {isRunning ? "Running" : "Send"}
            </button>
          </div>
          {error && <p className="error-text">{error}</p>}
        </form>
      </section>

      <aside className="agent-rail liquid-glass">
        <div className="rail-head">
          <p>// Live execution</p>
          <h2>{isRunning ? "Agents are working" : "Agent timeline"}</h2>
        </div>
        <div className="agent-steps">
          {AGENT_STEPS.map((step) => {
            const Icon = step.icon;
            const status = stepStatuses.get(step.key) ?? (step.key === activeStep && isRunning ? "running" : "pending");
            return (
              <div className={`agent-step ${status}`} key={step.key}>
                <span><Icon size={18} /></span>
                <div>
                  <strong>{step.label}</strong>
                  <small>{step.description}</small>
                </div>
                {status === "running" && <Loader2 className="spin" size={16} />}
                {status === "completed" && <CheckCircle2 size={16} />}
                {status === "failed" && <XCircle size={16} />}
                {status === "pending" && <CircleDashed size={16} />}
              </div>
            );
          })}
        </div>

        <div className="usage-card">
          <h3><Clock3 size={16} /> Token estimate</h3>
          {!usageLogs.length && <p className="muted-small">Usage appears after a workflow run.</p>}
          {usageLogs.map((usage) => (
            <div className="usage-row" key={usage.id}>
              <span>{usage.purpose}</span>
              <strong>{usage.prompt_tokens + usage.completion_tokens}</strong>
            </div>
          ))}
        </div>
      </aside>
    </main>
  );
}

function buildStepStatuses(traces: NodeTrace[]) {
  const statuses = new Map<string, NodeTrace["status"]>();
  for (const trace of traces) {
    const previous = statuses.get(trace.node_key);
    if (previous === "failed") continue;
    statuses.set(trace.node_key, trace.status);
  }
  return statuses;
}