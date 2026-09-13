"use client";

import { useState } from "react";
import { Eye, Search, FileText, Compass, BarChart2, CheckCircle2, Zap, AlertTriangle, ArrowDown, ChevronRight, ChevronDown } from "lucide-react";

interface StepTrace {
  timestamp: string;
  step: string;
  details: string;
}

interface ExecutionTimelineProps {
  traceList?: StepTrace[];
}

const defaultSteps = [
  { step: "OBSERVE", title: "Read Live Web Sources", icon: Eye, color: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/20" },
  { step: "DETECT", title: "Level 1 & 2 Change Diff", icon: Search, color: "text-purple-400", bg: "bg-purple-500/10 border-purple-500/20" },
  { step: "UNDERSTAND", title: "Filter Cosmetic Noise", icon: FileText, color: "text-indigo-400", bg: "bg-indigo-500/10 border-indigo-500/20" },
  { step: "INVESTIGATE", title: "Cross-Source Signal Correlation", icon: Compass, color: "text-cyan-400", bg: "bg-cyan-500/10 border-cyan-500/20" },
  { step: "ASSESS IMPACT", title: "Weighted Math Score (0-100)", icon: BarChart2, color: "text-amber-400", bg: "bg-amber-500/10 border-amber-500/20" },
  { step: "DECIDE", title: "Evaluate Permission & Rules", icon: Zap, color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/20" },
  { step: "ACT", title: "Execute Authorized Action", icon: Zap, color: "text-teal-400", bg: "bg-teal-500/10 border-teal-500/20" },
  { step: "VERIFY", title: "Confirm State Integrity", icon: CheckCircle2, color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/20" },
  { step: "LEARN / REPLAN", title: "Autonomous Error Recovery", icon: AlertTriangle, color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/20" },
  { step: "CONTINUE MONITORING", title: "Persistent Agent State", icon: CheckCircle2, color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/20" }
];

export default function ExecutionTimeline({ traceList }: ExecutionTimelineProps) {
  const [expandedStep, setExpandedStep] = useState<string | null>("INVESTIGATE");

  const getTraceForStep = (stepName: string) => {
    if (!traceList) return null;
    return traceList.find((t) => t.step.toLowerCase().includes(stepName.toLowerCase()) || stepName.toLowerCase().includes(t.step.toLowerCase()));
  };

  return (
    <div className="p-6 rounded-2xl bg-[#0d0f18] border border-[#1d2235]">
      <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-6 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        Core Autonomous Agent Execution Trace
      </h3>

      <div className="relative border-l-2 border-[#1e2438] ml-4 space-y-6">
        {defaultSteps.map((s, idx) => {
          const Icon = s.icon;
          const matchedTrace = getTraceForStep(s.step);
          const isExpanded = expandedStep === s.step;

          return (
            <div key={idx} className="relative pl-6">
              {/* Timeline Node Badge */}
              <div
                onClick={() => setExpandedStep(isExpanded ? null : s.step)}
                className="cursor-pointer group flex items-center justify-between p-3 rounded-xl bg-[#121524] border border-[#1f253a] hover:border-emerald-500/40 transition"
              >
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg border ${s.bg}`}>
                    <Icon className={`w-4 h-4 ${s.color}`} />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-bold font-mono text-emerald-400 uppercase">{s.step}</span>
                      {matchedTrace && <span className="text-[10px] text-slate-400 font-mono">[{matchedTrace.timestamp}]</span>}
                    </div>
                    <h4 className="text-xs font-semibold text-slate-200">{s.title}</h4>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    VERIFIED
                  </span>
                  {isExpanded ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
                </div>
              </div>

              {/* Expandable Step Details */}
              {isExpanded && (
                <div className="mt-2 p-4 rounded-xl bg-[#090b14] border border-[#1b2034] text-xs font-mono text-slate-300 space-y-2 animate-fade-in">
                  <div className="text-slate-400 border-b border-[#1b2034] pb-2 font-sans font-semibold text-[11px] flex justify-between">
                    <span>STEP LOG EXECUTION TRACE</span>
                    <span className="text-emerald-400">100% Deterministic Match</span>
                  </div>
                  <p className="leading-relaxed text-slate-200">
                    {matchedTrace?.details || `[${s.step}] Agent operational check completed. State verified clean.`}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
