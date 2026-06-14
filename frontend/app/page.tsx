import { ArrowUpRight, BrainCircuit, GitBranch, ShieldCheck, Sparkles, Workflow } from "lucide-react";
import Link from "next/link";

const capabilities = [
  {
    icon: BrainCircuit,
    title: "Prompt structuring",
    tags: ["Intent", "Constraints", "Goal"],
    body: "Messy user requests are converted into clean structured intent before any agent starts working."
  },
  {
    icon: GitBranch,
    title: "Agent routing",
    tags: ["LangGraph", "Prerequisites", "Trace"],
    body: "The workflow chooses the right specialist agents and runs prerequisite steps before dependent tasks."
  },
  {
    icon: ShieldCheck,
    title: "Verified output",
    tags: ["Evidence", "GCF", "Final format"],
    body: "Agent handoffs stay compact with GCF while the final answer remains readable, traceable, and user-focused."
  }
];

export default function HomePage() {
  return (
    <main className="cinematic-page">
      <section className="hero-section">
        <VideoBackdrop variant="hero" />
        <nav className="glass-nav" aria-label="Primary navigation">
          <Link className="brand-orb" href="/" aria-label="Agentic AI Workflow home">a</Link>
          <div className="nav-pill">
            <a href="#workflow">Workflow</a>
            <a href="#capabilities">Agents</a>
            <a href="#handoffs">GCF</a>
            <Link href="/login">Login</Link>
            <Link className="nav-cta" href="/signup">Get started <ArrowUpRight size={16} /></Link>
          </div>
          <span className="nav-spacer" />
        </nav>

        <div className="hero-content" id="workflow">
          <div className="glass-badge"><span>New</span> GCF-powered agent handoffs</div>
          <h1>One prompt. A full AI workflow behind it.</h1>
          <p>
            Build with an orchestration layer that structures messy requests, routes specialist agents,
            shows every switch in real time, and returns one complete response.
          </p>
          <div className="hero-actions">
            <Link className="glass-button strong" href="/login">Launch workspace <ArrowUpRight size={18} /></Link>
            <Link className="text-button" href="#capabilities">View system <Sparkles size={16} /></Link>
          </div>
          <div className="hero-stats" id="handoffs">
            <div className="glass-stat"><Workflow /><strong>Multi-agent</strong><span>planning, search, reasoning, writing</span></div>
            <div className="glass-stat"><GitBranch /><strong>GCF context</strong><span>compact handoffs between agents</span></div>
          </div>
        </div>

        <div className="partner-strip">
          <span>Designed for agentic builders</span>
          <strong>LangGraph</strong><strong>FastAPI</strong><strong>Groq</strong><strong>Next.js</strong><strong>GCF</strong>
        </div>
      </section>

      <section className="capabilities-section" id="capabilities">
        <VideoBackdrop variant="capabilities" />
        <div className="capability-heading">
          <p>// Capabilities</p>
          <h2>From prompt<br />to production workflow</h2>
        </div>
        <div className="capability-grid">
          {capabilities.map((item) => {
            const Icon = item.icon;
            return (
              <article className="glass-card" key={item.title}>
                <div className="card-topline">
                  <span className="icon-tile"><Icon size={24} /></span>
                  <div className="tag-cloud">{item.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
                </div>
                <div>
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>
                </div>
              </article>
            );
          })}
        </div>
      </section>
    </main>
  );
}

function VideoBackdrop({ variant }: { variant: "hero" | "capabilities" }) {
  const src = variant === "hero"
    ? "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_080021_d598092b-c4c2-4e53-8e46-94cf9064cd50.mp4"
    : "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_094631_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4";

  return (
    <video
      aria-hidden="true"
      autoPlay
      className={`video-backdrop ${variant === "hero" ? "hero-video" : ""}`}
      loop
      muted
      playsInline
      preload="auto"
      src={src}
    />
  );
}