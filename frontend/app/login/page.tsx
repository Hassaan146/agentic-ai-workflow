import { ArrowUpRight, LockKeyhole, Mail } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
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
        <form className="auth-form liquid-glass" action="/dashboard">
          <label><Mail size={18} /> Email<input name="email" placeholder="you@example.com" type="email" /></label>
          <label><LockKeyhole size={18} /> Password<input name="password" placeholder="••••••••" type="password" /></label>
          <button className="glass-button strong" type="submit">Login <ArrowUpRight size={18} /></button>
          <p>New here? <Link href="/signup">Create an account</Link></p>
        </form>
      </section>
    </main>
  );
}

function AuthVideo() {
  return <video aria-hidden="true" autoPlay className="video-backdrop" loop muted playsInline preload="auto" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_080021_d598092b-c4c2-4e53-8e46-94cf9064cd50.mp4" />;
}