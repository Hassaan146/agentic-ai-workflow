import { ArrowRight, GitBranch, ShieldCheck, Workflow } from "lucide-react";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero-band">
        <div className="hero-copy">
          <p className="eyebrow">Multi-agent orchestration platform</p>
          <h1>Turn messy requests into structured AI workflows.</h1>
          <p>
            Agentic AI Workflow routes complex tasks through specialized agents,
            checks prerequisites, verifies outputs, and shows the full execution trace.
          </p>
          <Link className="cta-link" href="/dashboard">
            Open dashboard <ArrowRight size={18} />
          </Link>
        </div>
      </section>

      <section className="feature-grid">
        <article>
          <Workflow />
          <h2>Structured request handling</h2>
          <p>Convert broad user intent into clean tasks, constraints, and expected outputs.</p>
        </article>
        <article>
          <GitBranch />
          <h2>State graph execution</h2>
          <p>Use LangGraph routing so prerequisite tasks run before dependent agents.</p>
        </article>
        <article>
          <ShieldCheck />
          <h2>Traceable answers</h2>
          <p>Show every agent step, verification result, source, and final response.</p>
        </article>
      </section>
    </main>
  );
}

