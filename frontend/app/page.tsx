"use client";

import Link from "next/link";
import { ShieldAlert, ArrowRight, Eye, Search, Zap, CheckCircle2, Sparkles, Target, Compass } from "lucide-react";

export default function LandingPage() {
  const modes = [
    { title: "Deals & Commerce", desc: "Qualify price drops with seller rating & warranty verification." },
    { title: "Competitor Intelligence", desc: "Correlate pricing, product launches, hiring & messaging shifts." },
    { title: "Reputation Watch", desc: "Detect sentiment velocity spikes across Reddit, YouTube & news." },
    { title: "Policy & Terms", desc: "Track return policy, refund & legal terms changes." },
    { title: "News & Events", desc: "Cluster duplicate coverage and extract underlying events." },
    { title: "SaaS & Software", desc: "Monitor plan limits, free tier shifts & find alternatives." },
    { title: "AI Visibility", desc: "Track brand presence in AI discovery engines." },
    { title: "Custom Objective", desc: "Convert any natural language goal into a machine mission." }
  ];

  return (
    <div className="min-h-screen bg-[#08090d] text-slate-100 flex flex-col justify-between selection:bg-emerald-500 selection:text-slate-950">
      {/* Top Header */}
      <header className="px-8 py-6 flex items-center justify-between border-b border-[#181b29]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-400 p-0.5 shadow-lg shadow-emerald-500/20">
            <div className="w-full h-full bg-[#08090d] rounded-[10px] flex items-center justify-center">
              <ShieldAlert className="w-5 h-5 text-emerald-400 animate-pulse" />
            </div>
          </div>
          <span className="font-bold text-lg tracking-wider text-white">WATCHDOG</span>
        </div>
        <div className="flex items-center gap-4">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold px-5 py-2.5 rounded-xl text-sm shadow-lg shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-400 transition"
          >
            Launch Dashboard <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto px-6 py-20 text-center flex-1 flex flex-col items-center justify-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 mb-8">
          <Sparkles className="w-3.5 h-3.5" />
          ANAKIN FORGE HACKATHON • AGENTIC WEB INTELLIGENCE
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white max-w-4xl leading-tight mb-6">
          Don't just watch the web. <br />
          <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            Understand what changed, why it matters, and what should happen next.
          </span>
        </h1>

        <p className="text-base md:text-lg text-slate-400 max-w-2xl leading-relaxed mb-10">
          An autonomous intelligence system that watches what matters, filters noise, correlates cross-source signals, decides optimal actions, and verifies execution.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-extrabold px-8 py-4 rounded-xl text-base shadow-xl shadow-emerald-500/25 hover:scale-105 transition"
          >
            Create Mission <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            href="/demo"
            className="flex items-center gap-2 bg-[#121626] border border-[#232a42] text-slate-200 hover:text-white font-semibold px-8 py-4 rounded-xl text-base hover:bg-[#181e33] transition"
          >
            Explore Judge Demo Suite
          </Link>
        </div>

        {/* 5-Stage Agent Loop Bar */}
        <div className="w-full max-w-4xl p-6 rounded-2xl bg-[#0e111d] border border-[#1e2438] shadow-2xl mb-20">
          <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-6">
            THE CORE AUTONOMOUS AGENT LOOP
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            {[
              { label: "WATCH", icon: Eye, text: "Read Live Web" },
              { label: "UNDERSTAND", icon: Search, text: "Semantic Diff" },
              { label: "DECIDE", icon: Compass, text: "Evaluate Rules" },
              { label: "ACT", icon: Zap, text: "Authorized Action" },
              { label: "VERIFY", icon: CheckCircle2, text: "Confirm Outcome" }
            ].map((st, i) => {
              const Icon = st.icon;
              return (
                <div key={i} className="p-3.5 rounded-xl bg-[#141827] border border-[#22283e] flex flex-col items-center text-center">
                  <Icon className="w-5 h-5 text-emerald-400 mb-2" />
                  <span className="text-xs font-bold text-white mb-0.5">{st.label}</span>
                  <span className="text-[10px] text-slate-400 font-mono">{st.text}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Application Modes Grid */}
        <div className="w-full text-left">
          <h3 className="text-xl font-bold text-white mb-6 text-center">8 Application Modes • 1 Reusable Agent Engine</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {modes.map((m, idx) => (
              <div key={idx} className="p-5 rounded-xl bg-[#0d101a] border border-[#1d2235] hover:border-emerald-500/30 transition">
                <h4 className="text-sm font-bold text-white mb-1">{m.title}</h4>
                <p className="text-xs text-slate-400 leading-relaxed">{m.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="px-8 py-6 border-t border-[#181b29] text-center text-xs text-slate-500 font-mono">
        WATCHDOG • Built for Anakin Forge Hackathon • Powered by Anakin Agentic Search & Wire Infrastructure
      </footer>
    </div>
  );
}
