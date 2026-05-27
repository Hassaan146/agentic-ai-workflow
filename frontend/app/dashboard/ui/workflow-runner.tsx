"use client";

import { Play, RefreshCw } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { listRuns, listRunTraces, listRunUsage, listTemplates, streamRun } from "../../lib/api";
import type { NodeTrace, RunResponse, TemplateResponse, UsageLog } from "../../lib/types";

const templates = [
  { key: "research", label: "Research Assistant" },
  { key: "product_comparison", label: "Product Comparison" },
  { key: "startup_validator", label: "Startup Idea Validator" }
];

type WorkflowRunnerProps = {
  getToken: () => Promise<string | null>;
};

export default function WorkflowRunner({ getToken }: WorkflowRunnerProps) {
  const [request, setRequest] = useState("Find me a car under $500 and explain the tradeoffs.");
  const [templateKey, setTemplateKey] = useState(templates[0].key);
  const [availableTemplates, setAvailableTemplates] = useState<TemplateResponse[]>([]);
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
        const [templateData, runData] = await Promise.all([
          listTemplates(),
          listRuns(token)
        ]);
        setAvailableTemplates(templateData);
        setRecentRuns(runData);
      } catch {
        setAvailableTemplates([]);
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
    setIsRunning(true);
    setError("");
    setRun(null);
    setTraces([]);
    setUsageLogs([]);
    try {
      const token = await getToken();
      let completedRunId: string | null = null;
      await streamRun(
        { user_request: request, template_key: templateKey },
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
              Template
              <select value={templateKey} onChange={(event) => setTemplateKey(event.target.value)}>
                {(availableTemplates.length ? availableTemplates : templates).map((template) => (
                  <option key={template.key} value={template.key}>
                    {"name" in template ? template.name : template.label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Request
              <textarea value={request} onChange={(event) => setRequest(event.target.value)} />
            </label>
            <button className="primary-button" disabled={isRunning} type="submit">
              {isRunning ? <RefreshCw size={18} /> : <Play size={18} />}
              {isRunning ? "Running" : "Start workflow"}
            </button>
          </form>
          {error && <p className="error-text">{error}</p>}
        </div>

        <div className="panel">
          <h2>Agent execution trace</h2>
          {!run && !traces.length && <p className="muted">Start a workflow to see the trace and final output.</p>}
          {!!traces.length && (
            <div className="live-trace">
              {traces.map((trace) => (
                <div className={`live-trace-row ${trace.status}`} key={trace.id}>
                  <strong>{trace.agent_name}</strong>
                  <span>{trace.node_key.replaceAll("_", " ")}</span>
                  <small>{trace.status}</small>
                </div>
              ))}
            </div>
          )}
          {run && (
            <div className="run-output">
              <p className="status-pill">{run.status}</p>
              <h3>{run.final_output?.title ?? "Workflow result"}</h3>
              <p>{run.final_output?.answer}</p>
              <div className="timeline">
                {run.final_output?.trace_summary.map((item) => (
                  <div className="timeline-item" key={item}>
                    {item}
                  </div>
                ))}
              </div>
              {!!run.final_output?.sources.length && (
                <div className="inspection-block">
                  <h3>Sources</h3>
                  {run.final_output.sources.map((source, index) => (
                    <a href={source.url} key={`${source.url}-${index}`} target="_blank">
                      {source.title}
                    </a>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {run && (
          <div className="panel recent-panel">
            <h2>Run inspection</h2>
            <div className="inspection-grid">
              <div>
                <h3>Node traces</h3>
                <div className="compact-list">
                  {traces.map((trace) => (
                    <div className="compact-row" key={trace.id}>
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
                <span>{item.template_key}</span>
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
