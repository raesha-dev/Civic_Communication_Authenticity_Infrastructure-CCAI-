"use client";

import { useEffect, useState } from "react";
import { AlertCircle, BookOpen, Cpu, Database, Link as LinkIcon } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { getMethodology, type MethodologyResponse } from "@/services/api";

export default function MethodologyPage() {
  const [activeTab, setActiveTab] = useState<"domain" | "semantic" | "fraud">("domain");
  const [data, setData] = useState<MethodologyResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void getMethodology()
      .then(setData)
      .catch((requestError: Error) => setError(requestError.message));
  }, []);

  const parameters = {
    domain: {
      title: "Domain Verification",
      icon: LinkIcon,
      weight: `${Math.round((data?.scoring_weights.domain_verification || 0) * 100)}%`,
      desc: "Queries the institutional registry in DynamoDB and scores whether the domain or institution is verified.",
      color: "text-blue-500",
      bg: "bg-blue-500/10",
    },
    semantic: {
      title: "Semantic Similarity",
      icon: BookOpen,
      weight: `${Math.round((data?.scoring_weights.semantic_similarity || 0) * 100)}%`,
      desc: "Uses Bedrock embeddings with S3-backed caching to compare live content against available official baselines.",
      color: "text-orange-500",
      bg: "bg-orange-500/10",
    },
    fraud: {
      title: "Fraud Detection",
      icon: AlertCircle,
      weight: `${Math.round((data?.scoring_weights.fraud_detection_penalty || 0) * 100)}%`,
      desc: "Combines Comprehend redaction with fraud heuristics to reduce risky communications in the final score.",
      color: "text-red-500",
      bg: "bg-red-500/10",
    },
  };

  return (
    <div className="pt-24 min-h-screen bg-background relative overflow-hidden">
      <div className="container mx-auto px-6 lg:px-12 py-12">
        <div className="text-center mb-16 max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">How It Works</h1>
          <p className="text-xl text-foreground/70">
            The scoring model is loaded from the backend in real time, along with live registry table metadata.
          </p>
          {error ? <p className="mt-4 text-red-300">{error}</p> : null}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 max-w-6xl mx-auto">
          <div className="md:col-span-4 space-y-4">
            {Object.entries(parameters).map(([key, param]) => {
              const Icon = param.icon;
              return (
                <button
                  key={key}
                  onClick={() => setActiveTab(key as "domain" | "semantic" | "fraud")}
                  className={cn(
                    "w-full text-left p-6 rounded-2xl flex items-center gap-4 transition-all duration-300",
                    activeTab === key ? "glass-panel border-l-4 border-l-blue-500 shadow-xl scale-105" : "hover:bg-foreground/5 border border-transparent"
                  )}
                >
                  <div className={cn("p-3 rounded-xl", param.bg, param.color)}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">{param.title}</h3>
                    <p className="text-sm font-semibold text-foreground/50">Weight: {param.weight}</p>
                  </div>
                </button>
              );
            })}
          </div>

          <div className="md:col-span-8 glass-panel p-8 md:p-12 rounded-3xl border border-foreground/10 min-h-[400px]">
            <motion.div key={activeTab} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.4 }}>
              {(() => {
                const param = parameters[activeTab];
                const Icon = param.icon;
                return (
                  <>
                    <div className="flex items-center gap-4 mb-8">
                      <div className={cn("p-4 rounded-2xl", param.bg, param.color)}>
                        <Icon className="w-8 h-8" />
                      </div>
                      <div>
                        <h2 className="text-3xl font-bold">{param.title}</h2>
                        <p className={cn("text-lg font-bold mt-1", param.color)}>Impact Weight: {param.weight}</p>
                      </div>
                    </div>
                    <p className="text-xl leading-relaxed text-foreground/80 mb-8 border-l-2 border-foreground/20 pl-6 py-2">
                      {param.desc}
                    </p>

                    <div className="bg-background/40 p-6 rounded-2xl border border-foreground/5 space-y-3">
                      <div className="flex items-center gap-3 text-sm font-mono text-foreground/60 uppercase tracking-widest">
                        <Cpu className="w-4 h-4" /> Live Execution Trace
                      </div>
                      <div className="font-mono text-sm text-green-400">
                        Registry table status: {data?.registry_data_source.table_status || "loading"}
                      </div>
                      <div className="font-mono text-sm text-blue-400">
                        Translation similarity threshold: {data?.translation_threshold.similarity_required_for_integrity ?? "..."}
                      </div>
                      <div className="font-mono text-sm text-foreground/70 flex items-center gap-2">
                        <Database className="w-4 h-4" />
                        {data?.registry_data_source.table_name || "registry"} · indexes:{" "}
                        {data?.registry_data_source.global_secondary_indexes.join(", ") || "loading"}
                      </div>
                    </div>
                  </>
                );
              })()}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
