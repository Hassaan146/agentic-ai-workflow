"use client";

import { SignInButton, SignedIn, SignedOut, useAuth } from "@clerk/nextjs";
import WorkflowRunner from "./workflow-runner";

function AuthenticatedDashboard() {
  const { getToken } = useAuth();
  return <WorkflowRunner getToken={getToken} />;
}

export default function ClerkDashboard() {
  return (
    <>
      <SignedOut>
        <main className="dashboard-shell">
          <section className="auth-panel">
            <h1>Sign in to run agentic workflows.</h1>
            <SignInButton mode="modal">
              <button className="primary-button">Sign in</button>
            </SignInButton>
          </section>
        </main>
      </SignedOut>
      <SignedIn>
        <AuthenticatedDashboard />
      </SignedIn>
    </>
  );
}

