"use client";

import { ArrowUpRight, LockKeyhole, Mail } from "lucide-react";
import Link from "next/link";
import { FormEvent, useState } from "react";
import { login } from "../lib/api";

export default function LoginPage() {
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setIsSubmitting(true);
    setError("");
    try {
      const result = await login({
        email: String(formData.get("email") ?? ""),
        password: String(formData.get("password") ?? "")
      });
      localStorage.setItem("agentic_auth_token", result.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-screen">
      <AuthVideo />
      <section className="auth-shell">
        <Link className="brand-orb" href="/" aria-label="Agentic AI Workflow home">a</Link>
        <div className="auth-copy">
          <p>// Welcome back</p>
          <h1>Enter the orchestration cockpit.</h1>
          <span>Continue to your previous chats, live agent traces, and workflow runs.</span>
        </div>
        <form className="auth-form liquid-glass" onSubmit={handleSubmit}>
          <label><Mail size={18} /> Email<input name="email" placeholder="you@example.com" required type="email" /></label>
          <label><LockKeyhole size={18} /> Password<input name="password" placeholder="????????" required type="password" /></label>
          <button className="glass-button strong" disabled={isSubmitting} type="submit">{isSubmitting ? "Logging in" : "Login"} <ArrowUpRight size={18} /></button>
          {error && <p className="error-text">{error}</p>}
          <p>New here? <Link href="/signup">Create an account</Link></p>
        </form>
      </section>
    </main>
  );
}

function AuthVideo() {
  return <video aria-hidden="true" autoPlay className="video-backdrop" loop muted playsInline preload="auto" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_080021_d598092b-c4c2-4e53-8e46-94cf9064cd50.mp4" />;
}
