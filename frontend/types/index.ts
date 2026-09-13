export interface Mission {
  id: string;
  name: string;
  objective: string;
  mode: 'DEALS' | 'COMPETITORS' | 'REPUTATION' | 'POLICIES' | 'NEWS' | 'SOFTWARE' | 'AI_VISIBILITY' | 'CUSTOM';
  targets: string[];
  sources?: any[];
  conditions?: any[];
  constraints?: string[];
  thresholds?: Record<string, any>;
  allowed_actions?: string[];
  approval_level: 'NOTIFY' | 'RECOMMEND' | 'PREPARE' | 'EXECUTE';
  schedule: Record<string, any>;
  status: 'ACTIVE' | 'RUNNING' | 'CHANGE_DETECTED' | 'INVESTIGATING' | 'DECIDING' | 'EXECUTING' | 'VERIFYING' | 'WAITING' | 'PAUSED' | 'FAILED' | 'COMPLETED';
  created_at: string;
  last_run_at?: string;
}

export interface EventItem {
  id: string;
  mission_id: string;
  source_id?: string;
  mission_name?: string;
  target?: string;
  title: string;
  event_type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  summary: string;
  before_state?: Record<string, any>;
  after_state?: Record<string, any>;
  importance_score: number;
  investigation_id?: string;
  evidence_count?: number;
  decision_type?: string;
  action_status?: string;
  detected_at: string;
}

export interface Investigation {
  id: string;
  event_id: string;
  summary: string;
  possible_causes: string[];
  confidence: number;
  trend_description?: string;
  reasoning_summary: string;
  started_at: string;
  completed_at?: string;
  evidence: Array<{
    id: string;
    source_name: string;
    source_url?: string;
    snippet: string;
    relevance_score: number;
    created_at: string;
  }>;
}

export interface ActionItem {
  id: string;
  decision_id: string;
  action_name: string;
  target: string;
  parameters: Record<string, any>;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  status: 'DRAFT' | 'PREPARED' | 'PENDING_APPROVAL' | 'EXECUTING' | 'VERIFIED' | 'FAILED' | 'REPLANNED';
  created_at: string;
  executed_at?: string;
}

export interface DashboardSummary {
  active_missions_count: number;
  meaningful_changes_count: number;
  actions_executed_count: number;
  attention_saved_hours: string;
  attention_saved_details: {
    total_evaluated_changes: number;
    filtered_noise_changes: number;
    manual_research_avoided_mins: number;
  };
  mission_health: {
    active: number;
    investigating: number;
    waiting: number;
    needs_attention: number;
  };
  live_feed: EventItem[];
  agent_status: string;
  execution_mode: 'LIVE' | 'DEMO';
}
