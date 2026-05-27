"use client";

import WorkflowRunner from "./workflow-runner";

export default function DevDashboard() {
  return <WorkflowRunner getToken={async () => "dev-token"} />;
}
