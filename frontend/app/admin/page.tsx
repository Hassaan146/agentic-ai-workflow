"use client";

import { Activity, Database, ShieldCheck, UsersRound, Workflow } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { adminRuns, adminStats, adminTraces, adminUsage, adminUsers } from "../lib/api";
import type { AdminStats, AdminUser, NodeTrace, RunResponse, UsageLog } from "../lib/types";

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [runs, setRuns] = useState<RunResponse[]>([]);
  const [traces, setTraces] = useState<NodeTrace[]>([]);
  const [usage, setUsage] = useState<UsageLog[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadAdminData() {
      const token = localStorage.getItem("agentic_auth_token");
      try {
        const [statsData, usersData, runsData, tracesData, usageData] = await Promise.all([
          adminStats(token),
          adminUsers(token),
          adminRuns(token),
          adminTraces(token),
          adminUsage(token)
        ]);
        setStats(statsData);
        setUsers(usersData);
        setRuns(runsData);
        setTraces(tracesData);
        setUsage(usageData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Admin access failed.");
      }
    }

    loadAdminData();
  }, []);

  return (
    <main className="admin-shell">
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
      <section className="admin-panel liquid-glass">
        <header className="admin-header">
          <div>
            <p>// Admin control panel</p>
            <h1>System oversight</h1>
          </div>
          <Link className="glass-button" href="/dashboard">Back to workspace</Link>
        </header>

        {error && <p className="error-text">{error}</p>}

        <div className="admin-stats-grid">
          <Stat icon={UsersRound} label="Users" value={stats?.users ?? 0} />
          <Stat icon={Workflow} label="Runs" value={stats?.runs ?? 0} />
          <Stat icon={Activity} label="Traces" value={stats?.traces ?? 0} />
          <Stat icon={Database} label="Usage logs" value={stats?.usage_logs ?? 0} />
          <Stat icon={ShieldCheck} label="Est. tokens" value={stats?.estimated_tokens ?? 0} />
        </div>

        <div className="admin-grid">
          <AdminSection title="Users">
            {users.map((user) => (
              <div className="admin-row" key={String(user.id)}>
                <strong>{user.email}</strong>
                <span>{user.full_name || "No name"}</span>
                <small>{user.is_admin ? "admin" : "user"}</small>
              </div>
            ))}
          </AdminSection>

          <AdminSection title="All runs">
            {runs.slice(0, 12).map((run) => (
              <div className="admin-row" key={run.id}>
                <strong>{run.user_request}</strong>
                <span>{run.status}</span>
                <small>{new Date(run.created_at).toLocaleString()}</small>
              </div>
            ))}
          </AdminSection>

          <AdminSection title="Recent traces">
            {traces.slice(0, 12).map((trace) => (
              <div className="admin-row" key={trace.id}>
                <strong>{trace.agent_name}</strong>
                <span>{trace.node_key}</span>
                <small>{trace.status}</small>
              </div>
            ))}
          </AdminSection>

          <AdminSection title="Usage">
            {usage.slice(0, 12).map((item) => (
              <div className="admin-row" key={item.id}>
                <strong>{item.purpose}</strong>
                <span>{item.provider} / {item.model}</span>
                <small>{item.prompt_tokens + item.completion_tokens} tokens</small>
              </div>
            ))}
          </AdminSection>
        </div>
      </section>
    </main>
  );
}

function Stat({ icon: Icon, label, value }: { icon: typeof ShieldCheck; label: string; value: number }) {
  return (
    <article className="admin-stat">
      <Icon size={22} />
      <span>{label}</span>
      <strong>{value.toLocaleString()}</strong>
    </article>
  );
}

function AdminSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="admin-card">
      <h2>{title}</h2>
      <div className="admin-list">{children}</div>
    </section>
  );
}
