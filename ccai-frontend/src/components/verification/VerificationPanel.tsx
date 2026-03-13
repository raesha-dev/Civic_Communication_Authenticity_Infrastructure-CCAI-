"use client";

import { startTransition, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Globe, Mail, MessageSquare, Search, ShieldCheck } from "lucide-react";
import ScoreVisualizer from "@/components/score/ScoreVisualizer";
import { cn } from "@/lib/utils";
import {
  analyzeCommunication,
  getAnalysisResult,
  translateMessage,
  type AnalysisResult,
  type TranslationResult,
} from "@/services/api";

type Channel = "sms" | "email" | "url";

function deriveDomain(channel: Channel, value: string) {
  if (channel === "url") {
    try {
      return new URL(value).hostname.toLowerCase();
    } catch {
      return "";
    }
  }
  return "";
}

export default function VerificationPanel() {
  const [channel, setChannel] = useState<Channel>("sms");
  const [inputVal, setInputVal] = useState("");
  const [entityName, setEntityName] = useState("");
  const [originDomain, setOriginDomain] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [translationTarget, setTranslationTarget] = useState("hi");
  const [translationLoading, setTranslationLoading] = useState(false);
  const [translationError, setTranslationError] = useState<string | null>(null);
  const [translationResult, setTranslationResult] = useState<TranslationResult | null>(null);

  const channels = [
    { id: "sms", icon: MessageSquare, label: "SMS / WhatsApp" },
    { id: "email", icon: Mail, label: "Email Content" },
    { id: "url", icon: Globe, label: "Website URL" },
  ] as const;

  const resetResponses = () => {
    setError(null);
    setResult(null);
    setTranslationError(null);
    setTranslationResult(null);
  };

  const handleVerify = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!inputVal.trim()) {
      return;
    }

    setLoading(true);
    resetResponses();

    try {
      const submitted = await analyzeCommunication({
        communication_text: inputVal.trim(),
        channel_type: channel,
        metadata: {
          entity_name: entityName.trim() || undefined,
          domain: (originDomain.trim() || deriveDomain(channel, inputVal)).toLowerCase() || undefined,
        },
      });
      const persisted = await getAnalysisResult(submitted.analysis_id).catch(() => submitted);
      startTransition(() => {
        setResult(persisted);
      });
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async () => {
    if (!result) {
      return;
    }
    setTranslationLoading(true);
    setTranslationError(null);
    setTranslationResult(null);
    try {
      const translated = await translateMessage({
        analysis_id: result.analysis_id,
        original_text: inputVal,
        target_lang: translationTarget,
      });
      setTranslationResult(translated);
    } catch (requestError) {
      setTranslationError(requestError instanceof Error ? requestError.message : "Translation failed.");
    } finally {
      setTranslationLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto py-12">
      <div className="glass-panel rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute -top-32 -left-32 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-32 -right-32 w-64 h-64 bg-green-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 space-y-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-2">Verify Communication</h2>
            <p className="text-foreground/60">
              Submit live content for registry verification, fraud analysis, and explainable scoring.
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-4">
            {channels.map((entry) => {
              const Icon = entry.icon;
              const isActive = channel === entry.id;
              return (
                <button
                  key={entry.id}
                  type="button"
                  onClick={() => {
                    setChannel(entry.id);
                    resetResponses();
                  }}
                  className={cn(
                    "flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300",
                    isActive
                      ? "bg-foreground text-background shadow-lg scale-105"
                      : "bg-foreground/5 hover:bg-foreground/10 text-foreground"
                  )}
                >
                  <Icon className="w-5 h-5" />
                  {entry.label}
                </button>
              );
            })}
          </div>

          <form onSubmit={handleVerify} className="space-y-6">
            <div className="relative">
              {channel === "url" ? (
                <input
                  type="url"
                  placeholder="https://example.gov.in"
                  value={inputVal}
                  onChange={(event) => setInputVal(event.target.value)}
                  className="w-full p-6 pl-14 rounded-2xl bg-background/50 border border-foreground/10 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all font-mono outline-none text-lg"
                  required
                />
              ) : (
                <textarea
                  placeholder="Paste the message or email content here..."
                  value={inputVal}
                  onChange={(event) => setInputVal(event.target.value)}
                  className="w-full p-6 pl-14 rounded-2xl bg-background/50 border border-foreground/10 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all resize-none h-40 outline-none text-lg"
                  required
                />
              )}
              <Search className="absolute top-6 left-5 text-foreground/40 w-6 h-6" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Institution or sender name"
                value={entityName}
                onChange={(event) => setEntityName(event.target.value)}
                className="w-full p-4 rounded-2xl bg-background/50 border border-foreground/10 focus:border-blue-500 outline-none transition-all"
              />
              <input
                type="text"
                placeholder="Sender domain (optional if URL)"
                value={originDomain}
                onChange={(event) => setOriginDomain(event.target.value)}
                className="w-full p-4 rounded-2xl bg-background/50 border border-foreground/10 focus:border-blue-500 outline-none transition-all font-mono"
              />
            </div>

            {error ? (
              <div className="rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-red-200">{error}</div>
            ) : null}

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading || !inputVal.trim()}
                className="group flex items-center gap-2 px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                    <Search className="w-5 h-5" />
                  </motion.div>
                ) : (
                  <>
                    <ShieldCheck className="w-5 h-5 group-hover:scale-110 transition-transform" />
                    Analyze Context
                  </>
                )}
              </button>
            </div>
          </form>

          <AnimatePresence>
            {result ? (
              <motion.div
                initial={{ opacity: 0, height: 0, scale: 0.95 }}
                animate={{ opacity: 1, height: "auto", scale: 1 }}
                exit={{ opacity: 0, height: 0, scale: 0.95 }}
                transition={{ duration: 0.5, ease: "backOut" }}
                className="border-t border-foreground/10 pt-8 mt-8 space-y-8"
              >
                <ScoreVisualizer data={result} />

                <div className="rounded-3xl border border-foreground/10 bg-background/30 p-6 space-y-4">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div>
                      <h3 className="text-2xl font-bold">Live Translation</h3>
                      <p className="text-foreground/60">
                        Available only for highly verified communications. Analysis ID: {result.analysis_id}
                      </p>
                    </div>
                    <div className="flex gap-3">
                      <select
                        value={translationTarget}
                        onChange={(event) => setTranslationTarget(event.target.value)}
                        className="rounded-xl border border-foreground/10 bg-background/50 px-4 py-3 outline-none"
                      >
                        <option value="hi">Hindi</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                      </select>
                      <button
                        type="button"
                        onClick={handleTranslate}
                        disabled={!result.translation_allowed || translationLoading}
                        className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:bg-foreground/20 text-white font-semibold transition-colors"
                      >
                        {translationLoading ? "Translating..." : "Translate"}
                      </button>
                    </div>
                  </div>

                  {!result.translation_allowed ? (
                    <p className="text-amber-300">
                      Translation is disabled until the authenticity score is 4 or higher.
                    </p>
                  ) : null}
                  {translationError ? <p className="text-red-300">{translationError}</p> : null}
                  {translationResult ? (
                    <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-5 space-y-2">
                      <p className="text-sm text-foreground/60">
                        Integrity {Math.round(translationResult.translation_integrity_score * 100)}% ·{" "}
                        {translationResult.integrity_status}
                      </p>
                      <p className="text-lg leading-relaxed">{translationResult.translated_text}</p>
                    </div>
                  ) : null}
                </div>
              </motion.div>
            ) : null}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
