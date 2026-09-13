"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import ExecutionTimeline from "@/components/ExecutionTimeline";
import { fetchMission, runMission } from "@/lib/api";
import { Mission } from "@/types";
import { Target, Play, ShieldCheck, Clock, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function MissionDetailPage() {
  const params = useParams();
  const missionId = params?.id as string;
  const [mission, setMission] = useState<Mission | null>(null);
  const [loading, setLoading] = useState(true);

  const loadMissionData = async () => {
    if (!missionId) return;
    try {
      setLoading(true);
      const data = await fetchMission(missionId);
      setMission(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMissionData();
  }, [missionId]);

  const handleRunNow = async () => {
    if (!missionId) return;
    try {
      await runMission(missionId);
      loadMissionData();
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
          <Link href="/missions" className="inline-flex items-center gap-2 text-xs text-slate-400 hover:text-white transition">
            <ArrowLeft className="w-4 h-4" /> Back to Missions
          </Link>

          {/* Mission Header Card */}
          <div className="p-6 rounded-2xl bg-[#10131e] border border-[#1e2336] shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wider">
                  {mission?.mode || "DEALS"} MODE
                </span>
                <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  {mission?.status || "ACTIVE"}
                </span>
              </div>
              <h1 className="text-2xl font-extrabold text-white mb-2">{mission?.name || "Sony WH-1000XM6 Deal Watch"}</h1>
              <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">{mission?.objective}</p>
            </div>

            <button
              onClick={handleRunNow}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold px-5 py-2.5 rounded-xl text-xs shadow-lg shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-400 transition"
            >
              <Play className="w-4 h-4 stroke-[2.5]" /> Run Agentic Loop
            </button>
          </div>

          {/* 10-Step Execution Timeline Component */}
          <ExecutionTimeline />
        </main>
      </div>
    </div>
  );
}
