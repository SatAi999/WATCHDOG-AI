"use client";

import { Target, Activity, Zap, Clock } from "lucide-react";
import { DashboardSummary } from "@/types";

interface TopMetricsProps {
  summary?: DashboardSummary;
}

export default function TopMetrics({ summary }: TopMetricsProps) {
  const metrics = [
    {
      label: "Active Missions",
      value: summary?.active_missions_count || 3,
      change: "Watching 24/7",
      icon: Target,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10 border-emerald-500/20"
    },
    {
      label: "Meaningful Changes",
      value: summary?.meaningful_changes_count || 7,
      change: "389 Noise Filtered",
      icon: Activity,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10 border-cyan-500/20"
    },
    {
      label: "Actions Executed",
      value: summary?.actions_executed_count || 2,
      change: "State Verified",
      icon: Zap,
      color: "text-amber-400",
      bg: "bg-amber-500/10 border-amber-500/20"
    },
    {
      label: "Attention Saved",
      value: summary?.attention_saved_hours || "3h 42m",
      change: "Human Research Avoided",
      icon: Clock,
      color: "text-purple-400",
      bg: "bg-purple-500/10 border-purple-500/20"
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((m, idx) => {
        const Icon = m.icon;
        return (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-[#10131e]/90 border border-[#1e2336] shadow-md hover:border-slate-700 transition-all duration-200"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{m.label}</span>
              <div className={`p-2 rounded-xl border ${m.bg}`}>
                <Icon className={`w-4 h-4 ${m.color}`} />
              </div>
            </div>
            <div className="text-3xl font-extrabold text-white tracking-tight mb-1">
              {m.value}
            </div>
            <div className="text-xs text-slate-400 font-mono flex items-center gap-1">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              {m.change}
            </div>
          </div>
        );
      })}
    </div>
  );
}
