"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import { fetchActions, approveAction } from "@/lib/api";
import { ActionItem } from "@/types";
import { Zap, CheckCircle2, ShieldCheck, Clock, XCircle } from "lucide-react";

export default function ActionsPage() {
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadActions = async () => {
    try {
      setLoading(true);
      const data = await fetchActions();
      setActions(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadActions();
  }, []);

  const handleApprove = async (id: string) => {
    try {
      await approveAction(id);
      loadActions();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#08090d]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="p-8 space-y-6 max-w-7xl mx-auto w-full">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Action Control Center
            </h2>
            <p className="text-xs text-slate-400">Pending approvals, running actions, and verified state executions</p>
          </div>

          <div className="space-y-4">
            {actions.map((act) => (
              <div key={act.id} className="p-5 rounded-2xl bg-[#10131e] border border-[#1e2336] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wider">
                      {act.status}
                    </span>
                    <span className="text-xs font-mono text-slate-400">{act.action_name}</span>
                  </div>
                  <h3 className="text-sm font-bold text-white mb-1">{act.target}</h3>
                  <p className="text-xs text-slate-300 font-mono">Parameters: {JSON.stringify(act.parameters)}</p>
                </div>

                <div className="flex items-center gap-3">
                  {act.status === "PREPARED" || act.status === "PENDING_APPROVAL" ? (
                    <button
                      onClick={() => handleApprove(act.id)}
                      className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs shadow-lg shadow-emerald-500/20 hover:from-emerald-400 transition"
                    >
                      <CheckCircle2 className="w-4 h-4" /> Approve & Execute
                    </button>
                  ) : (
                    <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20">
                      <ShieldCheck className="w-4 h-4" /> State Verified
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
