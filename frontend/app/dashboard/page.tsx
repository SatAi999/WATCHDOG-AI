"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import TopMetrics from "@/components/TopMetrics";
import DemoControlBar from "@/components/DemoControlBar";
import LiveFeedCard from "@/components/LiveFeedCard";
import { fetchDashboardSummary } from "@/lib/api";
import { DashboardSummary } from "@/types";
import { ShieldCheck, RefreshCw } from "lucide-react";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await fetchDashboardSummary();
      setSummary(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#08090d]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Navbar executionMode={summary?.execution_mode || "DEMO"} agentStatus={summary?.agent_status} />

        <main className="p-8 space-y-8 max-w-7xl mx-auto w-full">
          {/* Demo Control Suite for Judges */}
          <DemoControlBar onScenarioTriggered={() => loadData()} />

          {/* Top Metrics Cards */}
          <TopMetrics summary={summary || undefined} />

          {/* Mission Health Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-[#10131f] border border-[#1e2338]">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">Active Missions</span>
              <span className="text-xl font-bold text-white">{summary?.mission_health.active ?? 3}</span>
            </div>
            <div className="p-4 rounded-xl bg-[#10131f] border border-[#1e2338]">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">Investigating</span>
              <span className="text-xl font-bold text-cyan-400">{summary?.mission_health.investigating ?? 1}</span>
            </div>
            <div className="p-4 rounded-xl bg-[#10131f] border border-[#1e2338]">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">Waiting / Paused</span>
              <span className="text-xl font-bold text-amber-400">{summary?.mission_health.waiting ?? 0}</span>
            </div>
            <div className="p-4 rounded-xl bg-[#10131f] border border-[#1e2338]">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">Needs Approval</span>
              <span className="text-xl font-bold text-emerald-400">{summary?.mission_health.needs_attention ?? 1}</span>
            </div>
          </div>

          {/* Live Intelligence Feed Header */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  Live Intelligence Feed
                </h3>
                <p className="text-xs text-slate-400">Meaningful web events detected and verified by WATCHDOG agent</p>
              </div>

              <button
                onClick={loadData}
                className="p-2 rounded-lg bg-[#141824] border border-[#232a3f] text-slate-400 hover:text-white transition"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
              </button>
            </div>

            {/* Event Feed Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {summary?.live_feed && summary.live_feed.length > 0 ? (
                summary.live_feed.map((evt) => <LiveFeedCard key={evt.id} event={evt} />)
              ) : (
                <div className="col-span-2 p-8 text-center rounded-2xl bg-[#0d0f17] border border-[#1d2235] text-slate-400 text-sm">
                  Loading active intelligence feed...
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
