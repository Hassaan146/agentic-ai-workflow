import ClerkDashboard from "./ui/clerk-dashboard";
import DevDashboard from "./ui/dev-dashboard";

export default function DashboardPage() {
  const authMode = process.env.NEXT_PUBLIC_AUTH_MODE ?? "dev";
  return authMode === "dev" ? <DevDashboard /> : <ClerkDashboard />;
}

