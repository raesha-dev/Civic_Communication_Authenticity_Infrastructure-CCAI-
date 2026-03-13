"use client";

import { useEffect, useState, type ComponentType } from "react";
import { Activity, Database, Languages, ShieldAlert } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { getHealth, getMethodology, type HealthResponse, type MethodologyResponse } from "@/services/api";

export default function DashboardWidgets() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [methodology, setMethodology] = useState<MethodologyResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getHealth(), getMethodology()])
      .then(([healthResponse, methodologyResponse]) => {
        setHealth(healthResponse);
        setMethodology(methodologyResponse);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, []);

  if (error) {
    return <p className="text-red-300">{error}</p>;
  }

  const services = Object.entries(health?.services || {});

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="System Status"
          value={health?.status || "loading"}
          change={health?.mock_mode ? "fallback enabled" : "aws first"}
          icon={Activity}
          color={health?.status === "degraded" ? "text-yellow-500" : "text-green-500"}
        />
        <KPICard
          title="Registry Table"
          value={methodology?.registry_data_source.table_status || "loading"}
          change={methodology?.registry_data_source.table_name || "registry"}
          icon={Database}
          color="text-blue-500"
        />
        <KPICard
          title="Translation Threshold"
          value={String(methodology?.translation_threshold.similarity_required_for_integrity ?? "...")}
          change="integrity floor"
          icon={Languages}
          color="text-emerald-500"
        />
        <KPICard
          title="Scoring Mode"
          value={methodology ? "live" : "loading"}
          change={`${services.filter(([, status]) => status === "ok").length}/${services.length || 0} services healthy`}
          icon={ShieldAlert}
          color="text-orange-500"
        />
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-foreground/10">
        <h3 className="text-xl font-semibold mb-6">AWS Service Health</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {services.map(([name, status]) => (
            <div key={name} className="rounded-2xl border border-foreground/10 bg-background/30 p-4">
              <div className="flex items-center justify-between">
                <span className="font-semibold uppercase tracking-wide text-sm">{name}</span>
                <span className={cn("text-sm font-bold", status === "ok" ? "text-green-400" : "text-red-400")}>
                  {status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-foreground/10">
        <h3 className="text-xl font-semibold mb-6">Live Weight Distribution</h3>
        <div className="space-y-4">
          <WeightRow label="Domain verification" value={methodology?.scoring_weights.domain_verification || 0} color="bg-blue-500" />
          <WeightRow label="Semantic similarity" value={methodology?.scoring_weights.semantic_similarity || 0} color="bg-orange-500" />
          <WeightRow label="Fraud detection" value={methodology?.scoring_weights.fraud_detection_penalty || 0} color="bg-red-500" />
        </div>
      </div>
    </div>
  );
}

function KPICard({
  title,
  value,
  change,
  icon: Icon,
  color,
}: {
  title: string;
  value: string;
  change: string;
  icon: ComponentType<{ className?: string }>;
  color: string;
}) {
  return (
    <motion.div whileHover={{ y: -5 }} className="glass-panel p-6 rounded-3xl border border-foreground/10">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-2xl bg-foreground/5 ${color}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      <div>
        <h4 className="text-foreground/60 font-medium text-sm mb-1">{title}</h4>
        <div className="text-3xl font-bold capitalize">{value}</div>
        <p className="text-sm text-foreground/50 mt-2">{change}</p>
      </div>
    </motion.div>
  );
}

function WeightRow({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex items-center justify-between text-sm mb-2">
        <span>{label}</span>
        <span>{Math.round(value * 100)}%</span>
      </div>
      <div className="h-3 rounded-full bg-foreground/10 overflow-hidden">
        <div className={`h-full ${color}`} style={{ width: `${value * 100}%` }} />
      </div>
    </div>
  );
}
