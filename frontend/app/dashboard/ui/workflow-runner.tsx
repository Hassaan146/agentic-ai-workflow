"use client";

import { Play, RefreshCw } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { listRuns, listRunTraces, listRunUsage, streamRun } from "../../lib/api";
import type { NodeTrace, RunResponse, UsageLog } from "../../lib/types";

type WorkflowRunnerProps = {
  getToken: () => Promise<string | null>;
};

const GENERIC_TEMPLATE_KEY = "generic";

export default function WorkflowRunner({ getToken }: WorkflowRunnerProps) {
  const [run, setRun] = useState<RunResponse | null>(null);
  const [traces, setTraces] = useState<NodeTrace[]>([]);
  const [usageLogs, setUsageLogs] = useState<UsageLog[]>([]);
  const [recentRuns, setRecentRuns] = useState<RunResponse[]>([]);
  const [error, setError] = useState("");
  const [isRunning, setIsRunning] = useState(false);

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
        setTraces([]);
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
        setTraces([]);
        setUsageLogs([]);
      }
    }

    loadRunInspection();
  }, [getToken, run]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const form = event.currentTarget as HTMLFormElement;
    const formData = new FormData(form);
    const submittedRequest = String(formData.get("request") ?? "").trim();
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
    <main className="dashboard-shell">
      <section className="workspace">
        <div className="panel">
          <h1>Run a workflow</h1>
          <form onSubmit={handleSubmit} className="workflow-form">
            <label>
              Request
              <textarea
                name="request"
                placeholder="Ask the agentic workflow to research, compare, plan, validate, or explain something..."
              />
            </label>
            <button className="primary-button" disabled={isRunning} type="submit">
              {isRunning ? <RefreshCw size={18} /> : <Play size={18} />}
              {isRunning ? "Running" : "Start workflow"}
            </button>
          </form>
          {error && <p className="error-text">{error}</p>}
        </div>

        <div className="panel">
          <h2>Final output</h2>
          {!run && <p className="muted">Your answer will appear here after the workflow finishes.</p>}
          {run && (
            <div className="run-output">
              <p className="status-pill">{run.status}</p>
              <h3>{run.final_output?.title ?? "Workflow result"}</h3>
              <p className="final-answer">{run.final_output?.answer ?? "The workflow is still preparing the final answer."}</p>
              {!!run.final_output?.sources.length && (
                <div className="inspection-block">
                  <h3>Source context</h3>
                  {run.final_output.sources.map((source, index) => (
                    <article className="source-card" key={`${source.url}-${index}`}>
                      <a href={source.url} target="_blank">{source.title}</a>
                      {source.context && <small>{source.context}</small>}
                      {source.summary && <p>{source.summary}</p>}
                      {source.facts && <p><strong>Facts:</strong> {source.facts}</p>}
                    </article>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        <div className="panel recent-panel">
          <h2>Agent execution trace</h2>
          {!traces.length && <p className="muted">Agent steps will stream here while the workflow runs.</p>}
          {!!traces.length && (
            <div className="live-trace">
              {traces.map((trace) => (
                <div className={`live-trace-row ${trace.status}`} key={traceKey(trace)}>
                  <strong>{trace.agent_name}</strong>
                  <span>{trace.node_key.replaceAll("_", " ")}</span>
                  <small>{trace.status}</small>
                </div>
              ))}
            </div>
          )}
          {run?.final_output?.trace_summary.length ? (
            <div className="timeline">
              {run.final_output.trace_summary.map((item) => (
                <div className="timeline-item" key={item}>
                  {item}
                </div>
              ))}
            </div>
          ) : null}
        </div>

        {run && (
          <div className="panel recent-panel">
            <h2>Run inspection</h2>
            <div className="inspection-grid">
              <div>
                <h3>Node traces</h3>
                <div className="compact-list">
                  {traces.map((trace) => (
                    <div className="compact-row" key={traceKey(trace)}>
                      <strong>{trace.agent_name}</strong>
                      <span>{trace.node_key}</span>
                      <small>{trace.status}</small>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3>Usage logs</h3>
                <div className="compact-list">
                  {usageLogs.map((usage) => (
                    <div className="compact-row" key={usage.id}>
                      <strong>{usage.purpose}</strong>
                      <span>{usage.provider} / {usage.model}</span>
                      <small>{usage.prompt_tokens + usage.completion_tokens} est. tokens</small>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="panel recent-panel">
          <h2>Recent runs</h2>
          {!recentRuns.length && <p className="muted">Completed runs will appear here during this local session.</p>}
          <div className="recent-list">
            {recentRuns.slice(0, 5).map((item) => (
              <button className="recent-run" key={item.id} onClick={() => setRun(item)} type="button">
                <span>Generic workflow</span>
                <strong>{item.user_request}</strong>
                <small>{item.status}</small>
              </button>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

function traceKey(trace: NodeTrace) {
  return `${trace.id}-${trace.status}-${trace.completed_at ?? trace.started_at}`;
}
