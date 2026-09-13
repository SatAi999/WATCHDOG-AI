"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import { Activity, ShieldCheck } from "lucide-react";

export default function ActivityPage() {
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/dashboard/activity")
      .then((res) => res.json())
      .then((data) => setLogs(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="flex min-h-screen bg-[#08090d]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="p-8 space-y-6 max-w-7xl mx-auto w-full">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              Agent Audit & Activity Log
            </h2>
            <p className="text-xs text-slate-400">Complete immutable record of all agentic observations, decisions, and actions</p>
          </div>

          <div className="rounded-2xl bg-[#10131e] border border-[#1e2336] overflow-hidden">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#141827] text-slate-400 border-b border-[#1e2336] font-semibold">
                <tr>
                  <th className="p-4">Time</th>
                  <th className="p-4">Entity</th>
                  <th className="p-4">Action Performed</th>
                  <th className="p-4">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1b2034] text-slate-300">
                {logs.length > 0 ? (
                  logs.map((log) => (
                    <tr key={log.id} className="hover:bg-[#141827]">
                      <td className="p-4 font-mono text-slate-400">{new Date(log.timestamp).toLocaleTimeString()}</td>
                      <td className="p-4 font-bold text-emerald-400">{log.entity_type}</td>
                      <td className="p-4 font-semibold text-white">{log.action_performed}</td>
                      <td className="p-4 text-slate-400 truncate max-w-xs">{JSON.stringify(log.details)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className="p-6 text-center text-slate-500">
                      Audit trail initialized. Operational log active.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
}
