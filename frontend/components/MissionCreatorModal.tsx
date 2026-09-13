"use client";

import { useState } from "react";
import { X, Sparkles, Target, ShieldCheck, ArrowRight } from "lucide-react";
import { createMission } from "@/lib/api";

interface MissionCreatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onMissionCreated?: () => void;
}

export default function MissionCreatorModal({ isOpen, onClose, onMissionCreated }: MissionCreatorModalProps) {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    try {
      setLoading(true);
      await createMission(prompt);
      if (onMissionCreated) onMissionCreated();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    "Watch Sony WH-1000XM6 and tell me if it drops below ₹25,000 from a trustworthy seller with valid warranty.",
    "Watch Competitor X. Tell me when its pricing, product positioning, features or job hiring changes.",
    "Watch Acme return policy page. Alert me if the return policy window becomes worse than 30 days."
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-2xl bg-[#0e1019] border border-[#22273a] rounded-2xl shadow-2xl p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="w-5 h-5 text-emerald-400" />
          <h3 className="text-lg font-bold text-white">Create Machine Mission</h3>
        </div>
        <p className="text-xs text-slate-400 mb-5">Convert natural language into a persistent, autonomous monitoring agent.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              What should WATCHDOG watch?
            </label>
            <textarea
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g. Watch Sony WH-1000XM6. Tell me if price drops below ₹25,000 from a trusted seller with warranty..."
              className="w-full p-4 rounded-xl bg-[#141724] border border-[#23293e] text-slate-100 text-sm focus:outline-none focus:border-emerald-500 transition font-sans"
            />
          </div>

          <div>
            <span className="text-[11px] text-slate-400 block mb-2 font-medium">Or try an example prompt:</span>
            <div className="space-y-1.5">
              {samplePrompts.map((p, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setPrompt(p)}
                  className="w-full text-left text-xs p-2.5 rounded-lg bg-[#121522] border border-[#1e2338] text-slate-300 hover:border-emerald-500/40 hover:text-white transition"
                >
                  "{p}"
                </button>
              ))}
            </div>
          </div>

          <div className="pt-2 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !prompt.trim()}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-semibold px-5 py-2.5 rounded-xl text-xs shadow-lg shadow-emerald-500/20 disabled:opacity-50 transition"
            >
              {loading ? "Parsing Mission..." : "Activate Mission"}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
