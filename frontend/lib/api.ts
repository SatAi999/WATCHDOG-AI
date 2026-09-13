import { DashboardSummary, Mission, EventItem, Investigation, ActionItem } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${API_BASE}/dashboard/summary`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch dashboard summary");
  return res.json();
}

export async function fetchMissions(): Promise<Mission[]> {
  const res = await fetch(`${API_BASE}/missions`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch missions");
  return res.json();
}

export async function fetchMission(id: string): Promise<Mission> {
  const res = await fetch(`${API_BASE}/missions/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch mission");
  return res.json();
}

export async function createMission(prompt: string, mode: string = "CUSTOM", approval_level: string = "RECOMMEND"): Promise<Mission> {
  const res = await fetch(`${API_BASE}/missions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, mode, approval_level })
  });
  if (!res.ok) throw new Error("Failed to create mission");
  return res.json();
}

export async function runMission(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/missions/${id}/run`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to run mission");
  return res.json();
}

export async function fetchEvents(): Promise<EventItem[]> {
  const res = await fetch(`${API_BASE}/events`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch events");
  return res.json();
}

export async function fetchEvent(id: string): Promise<EventItem> {
  const res = await fetch(`${API_BASE}/events/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch event detail");
  return res.json();
}

export async function fetchInvestigation(id: string): Promise<Investigation> {
  const res = await fetch(`${API_BASE}/investigations/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch investigation");
  return res.json();
}

export async function fetchActions(): Promise<ActionItem[]> {
  const res = await fetch(`${API_BASE}/actions`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch actions");
  return res.json();
}

export async function approveAction(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/actions/${id}/approve`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to approve action");
  return res.json();
}

export async function fetchSources(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/sources`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch sources");
  return res.json();
}

export async function triggerDemoScenario(scenarioId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/demo/scenario/${scenarioId}`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to trigger demo scenario");
  return res.json();
}
