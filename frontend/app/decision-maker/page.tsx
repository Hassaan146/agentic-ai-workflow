"use client";

import { RefreshCw, Send } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { answerDecisionSkill, listDesignPipeline, startDecisionSkill } from "../lib/api";
import type { DecisionSkillResponse, PipelineStep } from "../lib/types";

export default function DecisionMakerPage() {
  const [session, setSession] = useState<DecisionSkillResponse | null>(null);
  const [pipeline, setPipeline] = useState<PipelineStep[]>([]);
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [start, steps] = await Promise.all([
          startDecisionSkill(),
          listDesignPipeline()
        ]);
        setSession(start);
        setPipeline(steps);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load Decision Maker.");
      } finally {
        setIsLoading(false);
      }
    }

    load();
  }, []);

  async function submitAnswer(event: FormEvent) {
    event.preventDefault();
    if (!session || !answer.trim()) return;
    setIsLoading(true);
    setError("");

    try {
      const next = await answerDecisionSkill(session.state, answer);
      setSession(next);
      setAnswer("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to advance Decision Maker.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="dashboard-shell">
      <section className="decision-grid">
        <div className="panel decision-main">
          <p className="eyebrow dark">Saved project skill</p>
          <h1>Decision Maker</h1>
          {session && <p className="status-pill">Step: {session.next_step.replaceAll("_", " ")}</p>}
          <div className="decision-message">
            {isLoading && !session ? "Loading Decision Maker..." : session?.message}
          </div>
          {error && <p className="error-text">{error}</p>}

          {session?.next_step !== "complete" && (
            <form className="workflow-form" onSubmit={submitAnswer}>
              <label>
                Your answer
                <textarea
                  value={answer}
                  onChange={(event) => setAnswer(event.target.value)}
                  placeholder="Answer the current Decision Maker question..."
                />
              </label>
              <button className="primary-button" disabled={isLoading || !answer.trim()} type="submit">
                {isLoading ? <RefreshCw size={18} /> : <Send size={18} />}
                {isLoading ? "Working" : "Send answer"}
              </button>
            </form>
          )}
        </div>

        <aside className="panel">
          <h2>Locked brief</h2>
          {!session && <p className="muted">The brief summary will appear here.</p>}
          {session && (
            <dl className="brief-list">
              {Object.entries(session.state)
                .filter(([key, value]) => key !== "current_step" && value && !Array.isArray(value))
                .map(([key, value]) => (
                  <div key={key}>
                    <dt>{key.replaceAll("_", " ")}</dt>
                    <dd>{String(value)}</dd>
                  </div>
                ))}
            </dl>
          )}
        </aside>

        {session?.outputs && (
          <section className="panel decision-outputs">
            <h2>Generated outputs</h2>
            <div className="output-grid">
              {Object.entries(session.outputs).map(([key, value]) => (
                <article className="output-box" key={key}>
                  <h3>{key.replaceAll("_", " ")}</h3>
                  <pre>{value}</pre>
                </article>
              ))}
            </div>
          </section>
        )}

        <section className="panel decision-outputs">
          <h2>Claude Code website pipeline</h2>
          <div className="pipeline-list">
            {pipeline.map((step) => (
              <article className="pipeline-step" key={step.number}>
                <span>{step.number}</span>
                <div>
                  <h3>{step.title}</h3>
                  <p>{step.purpose}</p>
                  <small>{step.tools.join(" / ")}</small>
                </div>
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

