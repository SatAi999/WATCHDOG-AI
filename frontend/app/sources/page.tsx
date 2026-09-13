"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import { fetchSources } from "@/lib/api";
import { Globe, ShieldCheck, RefreshCw } from "lucide-react";

export default function SourcesPage() {
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadSources = async () => {
    try {
      setLoading(true);
      const data = await fetchSources();
      setSources(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSources();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#08090d]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="p-8 space-y-6 max-w-7xl mx-auto w-full">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Globe className="w-5 h-5 text-cyan-400" />
              Source Explorer & Reliability Registry
            </h2>
            <p className="text-xs text-slate-400">Discovered web sources, authority ratings, and snapshot integrity</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {sources.map((s) => (
              <div key={s.id} className="p-5 rounded-2xl bg-[#10131e] border border-[#1e2336] hover:border-emerald-500/30 transition">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 uppercase">
                    {s.source_type}
                  </span>
                  <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5" /> {(s.reliability * 100).toFixed(0)}% Reliability
                  </span>
                </div>

                <h3 className="text-sm font-bold text-white mb-1">{s.name}</h3>
                <p className="text-xs text-slate-400 font-mono truncate mb-4">{s.url}</p>

                <div className="flex items-center justify-between pt-3 border-t border-[#1a1f32] text-xs font-mono text-slate-400">
                  <span>Snapshots: <strong className="text-white">{s.snapshot_count || 1}</strong></span>
                  <span className="text-emerald-400 font-semibold">{s.status}</span>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
