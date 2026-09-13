"use client";

import { ShieldCheck, Compass, GitMerge, FileText, CheckCircle2, ArrowRight } from "lucide-react";
import { Investigation } from "@/types";

interface EvidenceGraphProps {
  investigation?: Investigation;
}

export default function EvidenceGraph({ investigation }: EvidenceGraphProps) {
  const evidenceList = investigation?.evidence || [
    {
      id: "ev1",
      source_name: "Amazon Live Listing",
      snippet: "Verified price dropped to ₹24,499 with 12.5% promotional offer.",
      relevance_score: 0.98
    },
    {
      id: "ev2",
      source_name: "Sony Partner Registry",
      snippet: "Appario Retail Pvt Ltd confirmed as official authorized tier-1 distributor.",
      relevance_score: 0.95
    },
    {
      id: "ev3",
      source_name: "Price History Database",
      snippet: "Previous 30-day average price ₹27,999. Current price matches 6-month low.",
      relevance_score: 0.91
    }
  ];

  return (
    <div className="p-6 rounded-2xl bg-[#0e111d] border border-[#1f253a] space-y-6">
      <div className="flex items-center justify-between border-b border-[#1b2034] pb-4">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <GitMerge className="w-4 h-4 text-emerald-400" />
            Cross-Source Evidence Graph
          </h3>
          <p className="text-xs text-slate-400">Signal correlation chain across independent sources</p>
        </div>
        <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
          Confidence: {investigation ? Math.round(investigation.confidence * 100) : 94}%
        </span>
      </div>

      {/* Visual Graph Nodes */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative">
        {evidenceList.map((ev, idx) => (
          <div key={ev.id || idx} className="p-4 rounded-xl bg-[#131726] border border-[#21273e] hover:border-emerald-500/40 transition">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                <Compass className="w-3.5 h-3.5 text-emerald-400" />
                SIGNAL #{idx + 1}
              </span>
              <span className="text-[10px] font-mono text-slate-400">{(ev.relevance_score * 100).toFixed(0)}% Match</span>
            </div>
            <h4 className="text-xs font-semibold text-white mb-1.5">{ev.source_name}</h4>
            <p className="text-xs text-slate-300 leading-relaxed font-sans">{ev.snippet}</p>
          </div>
        ))}
      </div>

      {/* Synthesis Rationale Box */}
      <div className="p-4 rounded-xl bg-[#090c17] border border-[#1c2238]">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
          AGENT SYNTHESIZED RATIONALE
        </span>
        <p className="text-xs text-slate-200 leading-relaxed font-mono">
          {investigation?.reasoning_summary ||
            "Three independent signals confirm the price drop is genuine, seller is authorized, and full 1-year manufacturer warranty applies. Qualifying deal confirmed."}
        </p>
      </div>
    </div>
  );
}
