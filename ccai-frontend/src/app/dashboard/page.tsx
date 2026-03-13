import DashboardWidgets from "@/components/dashboard/DashboardWidgets";

export default function DashboardPage() {
  return (
    <div className="pt-24 min-h-screen bg-background relative overflow-hidden">
      <div className="absolute top-0 right-0 w-[50vw] h-[50vh] bg-purple-500/10 rounded-full blur-[128px] pointer-events-none" />

      <div className="container mx-auto px-6 lg:px-12 py-12 relative z-10">
        <header className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight">Transparency Dashboard</h1>
          <p className="text-xl text-foreground/70 max-w-3xl">
            Real-time insights into threat patterns, verification volumes, and active impersonation campaigns across government communication channels.
          </p>
        </header>

        <DashboardWidgets />
      </div>
    </div>
  );
}
