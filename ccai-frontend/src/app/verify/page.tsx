import VerificationPanel from "@/components/verification/VerificationPanel";

export default function Verify() {
  return (
    <div className="pt-24 min-h-screen bg-background relative overflow-hidden">
      {/* Decorative gradient patches */}
      <div className="absolute top-0 left-0 w-full h-[50vh] bg-gradient-to-b from-blue-500/5 to-transparent pointer-events-none" />
      <div className="absolute -left-1/4 top-1/2 w-[50vw] h-[50vw] bg-cyan-500/10 rounded-full blur-[128px] pointer-events-none" />

      <div className="container mx-auto px-6 lg:px-12 relative z-10 text-center py-16">
        <h1 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight">Authenticity Verification</h1>
        <p className="text-xl md:text-2xl text-foreground/70 max-w-2xl mx-auto mb-16">
          Paste a message, email, or website to check its legitimacy against government registries and our AI fraud engine.
        </p>

        <VerificationPanel />
      </div>
    </div>
  );
}
