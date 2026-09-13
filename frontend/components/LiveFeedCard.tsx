"use client";

import Link from "next/link";
import { EventItem } from "@/types";
import { AlertCircle, ShieldCheck, ArrowDownRight, ArrowUpRight, Zap, CheckCircle2, Search } from "lucide-react";

interface LiveFeedCardProps {
  event: EventItem;
}

export default function LiveFeedCard({ event }: LiveFeedCardProps) {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "CRITICAL":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      case "HIGH":
        return "bg-amber-500/20 text-amber-400 border-amber-500/30";
      default:
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
    }
  };

  const isPriceDrop = event.event_type === "PRICE";

  return (
    <div className="p-5 rounded-2xl bg-[#10131e] border border-[#1e2336] shadow-md hover:border-emerald-500/30 transition-all duration-200">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getSeverityBadge(event.severity)}`}>
            {event.severity} IMPACT
          </span>
          <span className="text-xs font-mono text-slate-400">
            {event.event_type} • {new Date(event.detected_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
          <ShieldCheck className="w-3.5 h-3.5" />
          Verified Signal
        </span>
      </div>

      <h3 className="text-sm font-bold text-white mb-1.5">{event.title}</h3>
      <p className="text-xs text-slate-300 mb-4 leading-relaxed">{event.summary}</p>

      {/* Before / After State comparison card */}
      {event.before_state && event.after_state && (
        <div className="grid grid-cols-2 gap-2 mb-4 p-3 rounded-xl bg-[#0b0d17] border border-[#1b2033]">
          <div>
            <span className="text-[10px] text-slate-400 uppercase font-semibold block mb-0.5">BEFORE</span>
            <span className="text-xs font-mono text-slate-300">
              {event.before_state.price ? `₹${event.before_state.price.toLocaleString()}` : JSON.stringify(event.before_state).slice(0, 35)}
            </span>
          </div>
          <div>
            <span className="text-[10px] text-emerald-400 uppercase font-semibold block mb-0.5 flex items-center gap-1">
              AFTER {isPriceDrop && <ArrowDownRight className="w-3 h-3 text-emerald-400" />}
            </span>
            <span className="text-xs font-mono font-bold text-emerald-400">
              {event.after_state.price ? `₹${event.after_state.price.toLocaleString()}` : JSON.stringify(event.after_state).slice(0, 35)}
            </span>
          </div>
        </div>
      )}

      {/* Footer Actions */}
      <div className="flex items-center justify-between pt-2 border-t border-[#1b2033]">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono text-slate-400">
            Action: <strong className="text-white font-semibold">{event.action_status || "PREPARED"}</strong>
          </span>
        </div>
        <Link
          href={`/events/${event.id}`}
          className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1 transition"
        >
          View Investigation <Search className="w-3 h-3" />
        </Link>
      </div>
    </div>
  );
}
