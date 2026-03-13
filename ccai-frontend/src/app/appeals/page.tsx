"use client";

import { useState } from "react";
import { CheckCircle, Send } from "lucide-react";
import { motion } from "framer-motion";
import { submitAppeal, type AppealResponse } from "@/services/api";

export default function AppealsPage() {
  const [analysisId, setAnalysisId] = useState("");
  const [entityName, setEntityName] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState<AppealResponse | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await submitAppeal({
        analysis_id: analysisId,
        contact_email: contactEmail,
        reason: entityName ? `${reason}\n\nEntity: ${entityName}` : reason,
      });
      setSubmitted(response);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Appeal submission failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pt-24 min-h-screen bg-background relative">
      <div className="container mx-auto px-6 lg:px-12 py-12">
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">Submit an Appeal</h1>
          <p className="text-xl text-foreground/70">
            If an official communication was misclassified, submit a live appeal. The request is stored and pushed to
            the review queue automatically.
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          {submitted ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-panel p-12 rounded-3xl border border-green-500/20 text-center"
            >
              <div className="w-20 h-20 bg-green-500/10 text-green-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="w-10 h-10" />
              </div>
              <h2 className="text-3xl font-bold mb-4">Appeal Received</h2>
              <p className="text-lg text-foreground/70 mb-3">
                Tracking ID: <span className="font-mono font-bold text-foreground">{submitted.appeal_id}</span>
              </p>
              <p className="text-foreground/60 mb-8">Queue status: {submitted.queue_status}</p>
              <button onClick={() => setSubmitted(null)} className="text-blue-500 font-semibold hover:underline">
                Submit another appeal
              </button>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="glass-panel p-8 md:p-12 rounded-3xl border border-foreground/10 space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-semibold tracking-wide uppercase text-foreground/70">Analysis ID</label>
                <input
                  required
                  type="text"
                  value={analysisId}
                  onChange={(event) => setAnalysisId(event.target.value)}
                  placeholder="Paste the analysis ID"
                  className="w-full p-4 rounded-xl bg-background/50 border border-foreground/10 focus:border-blue-500 outline-none transition-all font-mono"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-semibold tracking-wide uppercase text-foreground/70">Entity Name</label>
                  <input
                    required
                    type="text"
                    value={entityName}
                    onChange={(event) => setEntityName(event.target.value)}
                    placeholder="Department / Ministry / Bank"
                    className="w-full p-4 rounded-xl bg-background/50 border border-foreground/10 focus:border-blue-500 outline-none transition-all"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-semibold tracking-wide uppercase text-foreground/70">Contact Email</label>
                  <input
                    required
                    type="email"
                    value={contactEmail}
                    onChange={(event) => setContactEmail(event.target.value)}
                    placeholder="official@domain.gov"
                    className="w-full p-4 rounded-xl bg-background/50 border border-foreground/10 focus:border-blue-500 outline-none transition-all"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold tracking-wide uppercase text-foreground/70">Reason for Appeal</label>
                <textarea
                  required
                  rows={4}
                  value={reason}
                  onChange={(event) => setReason(event.target.value)}
                  placeholder="Describe why this communication is authentic..."
                  className="w-full p-4 rounded-xl bg-background/50 border border-foreground/10 focus:border-blue-500 outline-none transition-all resize-none"
                />
              </div>

              {error ? <p className="text-red-300">{error}</p> : null}

              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-foreground/20 text-white font-bold text-lg flex justify-center items-center gap-2 transition-all shadow-lg shadow-blue-500/20 mt-8"
              >
                {loading ? "Submitting..." : "Submit Appeal"} <Send className="w-5 h-5" />
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
