"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import MissionCreatorModal from "@/components/MissionCreatorModal";
import { fetchMissions, runMission } from "@/lib/api";
import { Mission } from "@/types";
import { Target, Play, Pause, Plus, ArrowRight, ShieldCheck } from "lucide-react";

export default function MissionsPage() {
  const [missions, setMissions] = useState<Mission[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const loadMissions = async () => {
    try {
      setLoading(true);
      const data = await fetchMissions();
      setMissions(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMissions();
  }, []);

  const handleTriggerRun = async (id: string) => {
    try {
      await runMission(id);
      loadMissions();
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
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Target className="w-5 h-5 text-emerald-400" />
                Active Machine Missions
              </h2>
              <p className="text-xs text-slate-400">Structured persistent goals evaluated by the 10-step agent loop</p>
            </div>

            <button
              onClick={() => setIsModalOpen(true)}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs shadow-lg shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-400 transition"
            >
              <Plus className="w-4 h-4" />
              New Mission
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {missions.map((m) => (
              <div key={m.id} className="p-5 rounded-2xl bg-[#10131e] border border-[#1e2336] flex flex-col justify-between hover:border-emerald-500/30 transition">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wider">
                      {m.mode} MODE
                    </span>
                    <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                      {m.status}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-white mb-2">{m.name}</h3>
                  <p className="text-xs text-slate-300 mb-4 line-clamp-2 leading-relaxed">{m.objective}</p>

                  <div className="space-y-1.5 mb-4 text-xs text-slate-400 font-mono">
                    <div>Target: <strong className="text-white">{m.targets?.[0] || m.name}</strong></div>
                    <div>Approval Level: <strong className="text-emerald-400">{m.approval_level}</strong></div>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-[#1a1f32]">
                  <button
                    onClick={() => handleTriggerRun(m.id)}
                    className="flex items-center gap-1 text-xs font-semibold text-slate-300 hover:text-white bg-[#161a29] px-3 py-1.5 rounded-lg border border-[#232a40] transition"
                  >
                    <Play className="w-3.5 h-3.5 text-emerald-400" /> Run Cycle Now
                  </button>
                  <Link
                    href={`/missions/${m.id}`}
                    className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1 transition"
                  >
                    Details & Trace <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </main>

        {isModalOpen && <MissionCreatorModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onMissionCreated={loadMissions} />}
      </div>
    </div>
  );
}
