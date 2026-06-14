import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agentic AI Workflow",
  description: "Multi-agent orchestration for structured, dependency-aware AI workflows."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const authMode = process.env.NEXT_PUBLIC_AUTH_MODE ?? "dev";
  const publishableKey =
    process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? "pk_test_Y2xlcmsuZXhhbXBsZSQ";

  const body = (
    <html lang="en">
      <body>{children}</body>
    </html>
  );

  if (authMode === "dev") {
    return body;
  }

  const { ClerkProvider } = require("@clerk/nextjs");
  return <ClerkProvider publishableKey={publishableKey}>{body}</ClerkProvider>;
}