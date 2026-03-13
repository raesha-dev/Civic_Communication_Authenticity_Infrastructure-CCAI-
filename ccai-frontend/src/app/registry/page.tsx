"use client";

import { useDeferredValue, useEffect, useState } from "react";
import { ExternalLink, Link2, Search, ShieldCheck } from "lucide-react";
import { searchRegistry, type RegistryEntry } from "@/services/api";

export default function RegistryPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<RegistryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const deferredQuery = useDeferredValue(query.trim());

  useEffect(() => {
    let cancelled = false;

    const runSearch = async () => {
      if (!deferredQuery) {
        setResults([]);
        setError(null);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const response = await searchRegistry(
          deferredQuery.includes(".")
            ? { domain: deferredQuery.toLowerCase() }
            : { entity_name: deferredQuery.toLowerCase() }
        );
        if (!cancelled) {
          setResults(response.results);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(requestError instanceof Error ? requestError.message : "Registry search failed.");
          setResults([]);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void runSearch();
    return () => {
      cancelled = true;
    };
  }, [deferredQuery]);

  return (
    <div className="pt-24 min-h-screen bg-background relative">
      <div className="container mx-auto px-6 lg:px-12 py-12">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">Registry Explorer</h1>
          <p className="text-xl text-foreground/70">
            Search the live institutional registry in DynamoDB by exact entity name or verified domain.
          </p>
        </div>

        <div className="max-w-3xl mx-auto mb-12 relative">
          <input
            type="text"
            placeholder="Search by entity name or domain"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            className="w-full p-6 pl-16 rounded-2xl glass-panel text-lg outline-none focus:ring-4 focus:ring-blue-500/20 transition-all"
          />
          <Search className="absolute left-6 top-6 text-foreground/40 w-7 h-7" />
        </div>

        {loading ? <p className="text-center text-foreground/60 mb-8">Searching live registry...</p> : null}
        {error ? <p className="text-center text-red-300 mb-8">{error}</p> : null}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {results.map((item, idx) => (
            <div
              key={`${item.entity_name ?? "entity"}-${idx}`}
              className="glass-panel p-6 rounded-2xl border border-foreground/10 hover:border-blue-500/50 transition-colors group"
            >
              <div className="flex justify-between items-start mb-4">
                <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                  {String(item.entity_type || "Verified")}
                </span>
                <ShieldCheck className="text-green-500 w-6 h-6" />
              </div>
              <h3 className="text-2xl font-bold mb-2 group-hover:text-blue-500 transition-colors">
                {String(item.entity_name || "Unnamed entity")}
              </h3>
              <div className="flex items-center gap-2 text-foreground/70 mb-2">
                <Link2 className="w-4 h-4" />
                <span className="font-mono">{String(item.domain || "No domain available")}</span>
              </div>
              <p className="text-sm text-foreground/60">Confidence {Math.round(Number(item.confidence || 0) * 100)}%</p>
              {item.domain ? (
                <a
                  href={`https://${String(item.domain)}`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 text-sm font-semibold text-blue-500 hover:text-blue-400 mt-4"
                >
                  Visit Official Website <ExternalLink className="w-4 h-4" />
                </a>
              ) : null}
            </div>
          ))}
          {!loading && deferredQuery && results.length === 0 && !error ? (
            <div className="col-span-1 md:col-span-2 text-center py-12 text-foreground/50 text-lg">
              No verified entities found for this live query.
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
