"use client";

import { useState } from "react";
import { Sparkles, Play, CheckCircle2, RefreshCw } from "lucide-react";
import { triggerDemoScenario } from "@/lib/api";

interface DemoControlBarProps {
  onScenarioTriggered?: (result: any) => void;
}

const scenarios = [
  { id: "scenario_1", label: "1. Price Drop", title: "Sony WH-1000XM6 Deal Qualification" },
  { id: "scenario_2", label: "2. Competitor Shift", title: "Multi-signal AI Expansion" },
  { id: "scenario_3", label: "3. Policy Reduction", title: "Return Window 30d -> 15d" },
  { id: "scenario_4", label: "4. Reputation Spike", title: "Firmware v4.2.1 Complaints" },
  { id: "scenario_5", label: "5. Action Recovery", title: "Wire Fail -> Browser Replan" },
  { id: "scenario_6", label: "6. Price Conflict", title: "Cross-store authority check" },
];

export default function DemoControlBar({ onScenarioTriggered }: DemoControlBarProps) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async (scenarioId: string) => {
    try {
      setLoading(true);
      setActiveId(scenarioId);
      const res = await triggerDemoScenario(scenarioId);
      if (onScenarioTriggered) onScenarioTriggered(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 rounded-2xl bg-gradient-to-r from-[#121626] via-[#161b2e] to-[#121626] border border-[#232a42] shadow-xl mb-6">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          <h3 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Demo Control Center (Hackathon Judge Suite)</h3>
        </div>
        <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
          Deterministic Mode
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2">
        {scenarios.map((sc) => {
          const isSelected = activeId === sc.id;
          return (
            <button
              key={sc.id}
              onClick={() => handleRun(sc.id)}
              disabled={loading}
              className={`p-2.5 rounded-xl border text-left transition-all duration-200 flex flex-col justify-between ${
                isSelected
                  ? "bg-emerald-500/20 border-emerald-500/50 text-white"
                  : "bg-[#0b0d17] border-[#1d2235] text-slate-300 hover:border-slate-600 hover:bg-[#111422]"
              }`}
            >
              <div className="text-xs font-bold mb-1 flex items-center justify-between">
                <span>{sc.label}</span>
                {isSelected && !loading && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                {isSelected && loading && <RefreshCw className="w-3.5 h-3.5 text-emerald-400 animate-spin" />}
              </div>
              <p className="text-[10px] text-slate-400 line-clamp-1">{sc.title}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
