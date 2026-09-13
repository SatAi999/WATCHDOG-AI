"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import EvidenceGraph from "@/components/EvidenceGraph";
import { fetchEvent, fetchInvestigation, approveAction } from "@/lib/api";
import { EventItem, Investigation } from "@/types";
import { ArrowLeft, ShieldCheck, Zap, ArrowDownRight, Compass, CheckCircle2 } from "lucide-react";
import Link from "next/link";

export default function EventDetailPage() {
  const params = useParams();
  const eventId = params?.id as string;
  const [event, setEvent] = useState<EventItem | null>(null);
  const [investigation, setInvestigation] = useState<Investigation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!eventId) return;
    const loadData = async () => {
      try {
        setLoading(true);
        const evt = await fetchEvent(eventId);
        setEvent(evt);
        if (evt.investigation_id) {
          const inv = await fetchInvestigation(evt.investigation_id);
          setInvestigation(inv);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [eventId]);

  const handleApprove = async () => {
    if (!event?.id) return;
    try {
      await approveAction(event.id);
      alert("Action approved & cart verified successfully!");
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#08090d]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="p-8 space-y-8 max-w-7xl mx-auto w-full">
          <Link href="/dashboard" className="inline-flex items-center gap-2 text-xs text-slate-400 hover:text-white transition">
            <ArrowLeft className="w-4 h-4" /> Back to Intelligence Feed
          </Link>

          {/* Investigation Header */}
          <div className="p-6 rounded-2xl bg-[#10131e] border border-[#1e2336] shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wider">
                WHY DID THIS CHANGE HAPPEN?
              </span>
              <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                <ShieldCheck className="w-4 h-4" /> 3 Independent Signals Corroborated
              </span>
            </div>
            <h1 className="text-2xl font-extrabold text-white mb-2">{event?.title || "Price Drop Detected: Sony WH-1000XM6"}</h1>
            <p className="text-xs text-slate-300 max-w-3xl leading-relaxed">{event?.summary}</p>
          </div>

          {/* Before & After State Diff */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-5 rounded-2xl bg-[#0d0f18] border border-[#1d2235]">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-3">BEFORE STATE</span>
              <div className="p-4 rounded-xl bg-[#131625] font-mono text-xs text-slate-300 space-y-1">
                <div>Price: ₹27,999</div>
                <div>Seller: Appario Retail Pvt Ltd</div>
                <div>Warranty: 1 Year Manufacturer</div>
                <div>Return Days: 10</div>
              </div>
            </div>

            <div className="p-5 rounded-2xl bg-[#0d0f18] border border-[#1d2235]">
              <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block mb-3 flex items-center gap-1">
                AFTER STATE <ArrowDownRight className="w-4 h-4 text-emerald-400" />
              </span>
              <div className="p-4 rounded-xl bg-[#131625] font-mono text-xs text-emerald-400 font-bold space-y-1 border border-emerald-500/20">
                <div>Price: ₹24,499 (-12.5%)</div>
                <div>Seller: Appario Retail Pvt Ltd (Verified)</div>
                <div>Warranty: 1 Year Manufacturer (Valid)</div>
                <div>Return Days: 10</div>
              </div>
            </div>
          </div>

          {/* Cross Source Evidence Graph */}
          <EvidenceGraph investigation={investigation || undefined} />

          {/* Action Decision & Authorization Center */}
          <div className="p-6 rounded-2xl bg-[#121524] border border-[#21273e] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block mb-1">
                RECOMMENDED ACTION PREPARED
              </span>
              <h4 className="text-sm font-bold text-white mb-1">Prepare Shopping Cart (Amazon India)</h4>
              <p className="text-xs text-slate-300 max-w-xl">
                WATCHDOG prepared item in cart at ₹24,499 with verified seller. Requires your approval before final checkout.
              </p>
            </div>

            <button
              onClick={handleApprove}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-extrabold px-6 py-3 rounded-xl text-xs shadow-lg shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-400 transition"
            >
              <CheckCircle2 className="w-4 h-4" /> Approve & Confirm Action
            </button>
          </div>
        </main>
      </div>
    </div>
  );
}
