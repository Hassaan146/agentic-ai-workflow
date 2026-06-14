"use client";

import WorkflowRunner from "./ui/workflow-runner";

export default function DashboardPage() {
  return <WorkflowRunner getToken={async () => localStorage.getItem("agentic_auth_token")} />;
}
