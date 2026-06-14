"use client";

import { ArrowUpRight, LockKeyhole, Mail, UserRound } from "lucide-react";
import Link from "next/link";
import { FormEvent, useState } from "react";
import { signup } from "../lib/api";

export default function SignupPage() {
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setIsSubmitting(true);
    setError("");
    try {
      const result = await signup({
        full_name: String(formData.get("name") ?? ""),
        email: String(formData.get("email") ?? ""),
        password: String(formData.get("password") ?? "")
      });
      localStorage.setItem("agentic_auth_token", result.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed.");
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
          <p>// Start building</p>
          <h1>Create your agent workspace.</h1>
          <span>Save chats, inspect execution steps, and run multi-agent workflows from one place.</span>
        </div>
        <form className="auth-form liquid-glass" onSubmit={handleSubmit}>
          <label><UserRound size={18} /> Name<input name="name" placeholder="Your name" /></label>
          <label><Mail size={18} /> Email<input name="email" placeholder="you@example.com" required type="email" /></label>
          <label><LockKeyhole size={18} /> Password<input minLength={8} name="password" placeholder="At least 8 characters" required type="password" /></label>
          <button className="glass-button strong" disabled={isSubmitting} type="submit">{isSubmitting ? "Creating" : "Create account"} <ArrowUpRight size={18} /></button>
          {error && <p className="error-text">{error}</p>}
          <p>Already have an account? <Link href="/login">Login</Link></p>
        </form>
      </section>
    </main>
  );
}

function AuthVideo() {
  return <video aria-hidden="true" autoPlay className="video-backdrop" loop muted playsInline preload="auto" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_094631_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4" />;
}
