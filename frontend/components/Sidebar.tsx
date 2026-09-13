"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Target, 
  Activity, 
  Search, 
  Zap, 
  Globe, 
  Sliders,
  Sparkles
} from "lucide-react";

const navItems = [
  { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
  { name: "Missions", href: "/missions", icon: Target },
  { name: "Intelligence", href: "/activity", icon: Activity },
  { name: "Actions", href: "/actions", icon: Zap },
  { name: "Sources", href: "/sources", icon: Globe },
  { name: "Demo Suite", href: "/demo", icon: Sparkles },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#0a0c13] border-r border-[#1a1d2d] min-h-screen flex flex-col justify-between p-4 select-none">
      <div>
        {/* WATCHDOG Logo */}
        <Link href="/" className="flex items-center gap-3 px-3 py-4 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-primary via-emerald-400 to-cyan-400 p-0.5 shadow-lg shadow-emerald-500/20">
            <div className="w-full h-full bg-[#0a0c13] rounded-[10px] flex items-center justify-center">
              <ShieldAlert className="w-5 h-5 text-brand-primary animate-pulse" />
            </div>
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-wider text-white flex items-center gap-1.5">
              WATCHDOG
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">AI</span>
            </h1>
            <p className="text-[11px] text-dark-muted font-medium">Autonomous Intelligence</p>
          </div>
        </Link>

        {/* Navigation Menu */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-emerald-500/15 to-transparent text-emerald-400 border-l-2 border-brand-primary"
                    : "text-slate-400 hover:text-white hover:bg-[#131726]"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-brand-primary" : "text-slate-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer Status */}
      <div className="p-3.5 rounded-xl bg-[#111422] border border-[#1d2235]">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-300">Engine Status</span>
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
        </div>
        <div className="text-[11px] text-slate-400 font-mono">
          Loop Active • 15m Poll
        </div>
      </div>
    </aside>
  );
}
