"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import DemoControlBar from "@/components/DemoControlBar";
import ExecutionTimeline from "@/components/ExecutionTimeline";
import EvidenceGraph from "@/components/EvidenceGraph";
import { Sparkles, ShieldCheck, CheckCircle2 } from "lucide-react";

export default function DemoPage() {
  const [lastScenarioResult, setLastScenarioResult] = useState<any>(null);

  return (
    <div className="flex min-h-screen bg-[#08090d]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="p-8 space-y-8 max-w-7xl mx-auto w-full">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Sparkles className="w-5 h-5 text-emerald-400" />
              <h2 className="text-xl font-bold text-white">Anakin Forge Hackathon — Demo Control Suite</h2>
            </div>
            <p className="text-xs text-slate-400">
              Trigger any of the 6 deterministic hero scenarios below to witness WATCHDOG execute its 10-step autonomous agent loop in real time.
            </p>
          </div>

          <DemoControlBar onScenarioTriggered={(res) => setLastScenarioResult(res)} />

          {lastScenarioResult && (
            <div className="p-6 rounded-2xl bg-[#0e111d] border border-[#1f253a] space-y-4">
              <div className="flex items-center justify-between border-b border-[#1b2034] pb-3">
                <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" /> SCENARIO EXECUTED: {lastScenarioResult.scenario?.name}
                </span>
                <span className="text-xs font-mono text-slate-400">Mode: {lastScenarioResult.scenario?.mode}</span>
              </div>
              <p className="text-xs text-slate-300 font-mono leading-relaxed">{lastScenarioResult.scenario?.description}</p>
            </div>
          )}

          <EvidenceGraph />
          <ExecutionTimeline traceList={lastScenarioResult?.execution_result?.trace} />
        </main>
      </div>
    </div>
  );
}
