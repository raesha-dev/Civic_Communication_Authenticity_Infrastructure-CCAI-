"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background text-foreground flex items-center justify-center px-6">
        <div className="max-w-xl text-center space-y-4">
          <h1 className="text-3xl font-bold">Application Error</h1>
          <p className="text-foreground/70">{error.message || "An unexpected error occurred."}</p>
          <button
            onClick={reset}
            className="px-6 py-3 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </body>
    </html>
  );
}
