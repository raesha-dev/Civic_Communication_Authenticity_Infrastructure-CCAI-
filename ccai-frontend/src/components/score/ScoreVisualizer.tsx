"use client";

import { motion } from "framer-motion";
import { AlertTriangle, BadgeCheck, CheckCircle2, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";
import type { AnalysisResult } from "@/services/api";

export default function ScoreVisualizer({ data }: { data: AnalysisResult }) {
  const getScoreInfo = (score: number) => {
    if (score >= 4) {
      return { color: "text-green-500", label: "Authentic" };
    }
    if (score === 3) {
      return { color: "text-yellow-500", label: "Suspicious" };
    }
    return { color: "text-red-500", label: "Likely Fraud" };
  };

  const info = getScoreInfo(data.authenticity_score);
  const percentage = (data.authenticity_score / 5) * 100;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
      <div className="flex flex-col items-center justify-center p-8 bg-background/30 rounded-2xl border border-foreground/5">
        <div className="relative w-48 h-48 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90">
            <circle
              cx="96"
              cy="96"
              r="80"
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              className="text-foreground/10"
            />
            <motion.circle
              cx="96"
              cy="96"
              r="80"
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              strokeDasharray={2 * Math.PI * 80}
              initial={{ strokeDashoffset: 2 * Math.PI * 80 }}
              animate={{
                strokeDashoffset: 2 * Math.PI * 80 - (2 * Math.PI * 80 * percentage) / 100,
              }}
              transition={{ duration: 1.5, ease: "easeOut" }}
              strokeLinecap="round"
              className={info.color}
            />
          </svg>
          <div className="absolute flex flex-col items-center">
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 1, type: "spring" }}
              className={cn("text-6xl font-black tabular-nums tracking-tighter", info.color)}
            >
              {data.authenticity_score}
            </motion.span>
            <span className="text-sm font-medium text-foreground/50 uppercase tracking-widest mt-1">/ 5</span>
          </div>
        </div>

        <div className="mt-6 text-center space-y-2">
          <h3 className={cn("text-2xl font-bold", info.color)}>{info.label}</h3>
          <p className="text-foreground/70">Confidence {(data.confidence * 100).toFixed(0)}%</p>
          <p className="text-sm text-foreground/60">
            Semantic similarity {Math.round(data.semantic_similarity * 100)}% · {data.processing_time_ms} ms
          </p>
        </div>

        <div className="mt-6 w-full rounded-2xl border border-foreground/10 bg-background/40 p-4 text-sm text-foreground/70">
          <div className="flex justify-between">
            <span>Domain</span>
            <span>{data.breakdown.domain_contribution.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Similarity</span>
            <span>{data.breakdown.similarity_contribution.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Fraud resistance</span>
            <span>{data.breakdown.fraud_contribution.toFixed(2)}</span>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div>
          <h4 className="text-xl font-semibold flex items-center gap-2 mb-4 border-b border-foreground/10 pb-2">
            <BadgeCheck className="text-blue-500 w-6 h-6" /> Explainable Flags
          </h4>
          {data.explainable_flags.length > 0 ? (
            <ul className="space-y-3">
              {data.explainable_flags.map((flag, idx) => (
                <motion.li
                  key={`${flag}-${idx}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1.2 + idx * 0.1 }}
                  className="flex items-center gap-3 bg-green-500/10 text-green-700 dark:text-green-300 px-4 py-3 rounded-xl border border-green-500/20"
                >
                  <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                  <span className="font-medium">{flag}</span>
                </motion.li>
              ))}
            </ul>
          ) : (
            <p className="text-foreground/50 italic px-4">No explainable signals returned.</p>
          )}
        </div>

        <div>
          <h4 className="text-xl font-semibold flex items-center gap-2 mb-4 border-b border-foreground/10 pb-2">
            <AlertTriangle className="text-red-500 w-6 h-6" /> Fraud Signals
          </h4>
          {data.fraud_signals.length > 0 ? (
            <ul className="space-y-3">
              {data.fraud_signals.map((signal, idx) => (
                <motion.li
                  key={`${signal.type}-${idx}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1.2 + data.explainable_flags.length * 0.1 + idx * 0.1 }}
                  className="bg-red-500/10 text-red-700 dark:text-red-300 px-4 py-3 rounded-xl border border-red-500/20"
                >
                  <div className="flex items-center gap-3">
                    <ShieldAlert className="w-5 h-5 flex-shrink-0" />
                    <span className="font-medium">{signal.description}</span>
                  </div>
                  {signal.matches?.length ? (
                    <p className="mt-2 text-sm text-red-800/80 dark:text-red-200/80">
                      Matched: {signal.matches.join(", ")}
                    </p>
                  ) : null}
                </motion.li>
              ))}
            </ul>
          ) : (
            <p className="text-foreground/50 italic px-4">No fraud signals detected.</p>
          )}
        </div>
      </div>
    </div>
  );
}
