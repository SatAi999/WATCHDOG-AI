"use client";

import { useState } from "react";
import { Search, Command, Plus, Radio } from "lucide-react";
import MissionCreatorModal from "./MissionCreatorModal";

interface NavbarProps {
  executionMode?: string;
  agentStatus?: string;
}

export default function Navbar({ executionMode = "DEMO", agentStatus = "MONITORING" }: NavbarProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <header className="h-16 border-b border-[#1a1d2d] bg-[#0a0c13]/80 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-30">
        <div>
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            Good afternoon. <span className="text-emerald-400 font-bold">WATCHDOG is watching.</span>
          </h2>
          <p className="text-xs text-slate-400">Autonomous Web Intelligence & Action System</p>
        </div>

        <div className="flex items-center gap-4">
          {/* Execution Mode Badge */}
          <div className="flex items-center gap-2 px-3 py-1 rounded-lg bg-[#141824] border border-[#242b3f] text-xs font-mono">
            <Radio className={`w-3.5 h-3.5 ${executionMode === "LIVE" ? "text-emerald-400 animate-pulse" : "text-amber-400"}`} />
            <span className="text-slate-300 font-medium">{executionMode} MODE</span>
          </div>

          {/* Quick Create Mission Button */}
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-semibold px-4 py-2 rounded-xl text-sm shadow-lg shadow-emerald-500/20 transition-all duration-200"
          >
            <Plus className="w-4 h-4 stroke-[2.5]" />
            New Mission
          </button>
        </div>
      </header>

      {isModalOpen && <MissionCreatorModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />}
    </>
  );
}
