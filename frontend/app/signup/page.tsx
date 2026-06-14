import { ArrowUpRight, LockKeyhole, Mail, UserRound } from "lucide-react";
import Link from "next/link";

export default function SignupPage() {
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
        <form className="auth-form liquid-glass" action="/dashboard">
          <label><UserRound size={18} /> Name<input name="name" placeholder="Your name" /></label>
          <label><Mail size={18} /> Email<input name="email" placeholder="you@example.com" type="email" /></label>
          <label><LockKeyhole size={18} /> Password<input name="password" placeholder="••••••••" type="password" /></label>
          <button className="glass-button strong" type="submit">Create account <ArrowUpRight size={18} /></button>
          <p>Already have an account? <Link href="/login">Login</Link></p>
        </form>
      </section>
    </main>
  );
}

function AuthVideo() {
  return <video aria-hidden="true" autoPlay className="video-backdrop" loop muted playsInline preload="auto" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_094631_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4" />;
}