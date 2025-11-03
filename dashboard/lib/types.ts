// Core simulation data types

export type Region = 'bay_area' | 'nyc' | 'boston' | 'la';
export type Stage = 'seed' | 'series_a' | 'series_b_plus';
export type Domain = 'ai' | 'bio' | 'consumer' | 'enterprise';
export type HypeState = 'risk_off' | 'normal' | 'hype';

export interface FounderRun {
  seed: number;
  run_id: number;
  t: number;
  region: Region;
  stage: Stage;
  domain: Domain;
  founder_id: number;
  funded: boolean;
  lead: boolean;
  syndication: boolean;
  dollars: number;
  score: number;
  prob?: number;
  // Additional fields
  revenue?: number;
  growth?: number;
  charisma?: number;
  vision?: number;
  traction_quality?: number;
  repeat_founder?: boolean;
  geo_flex?: number;
}

export interface SummaryMetric {
  metric: string;
  group_by: string;
  mean: number;
  ci_low: number;
  ci_high: number;
  n?: number;
}

export interface RegionConfig {
  name: string;
  budget_share: number;
  annual_capital_bn: number;
  weights: {
    revenue: number;
    growth: number;
    charisma: number;
    vision: number;
    traction_quality: number;
    repeat_founder: number;
    geo_flex: number;
  };
  domain_preferences: Record<Domain, number>;
  hype_beta: number;
  check_sizes: Record<Stage, number>;
  stage_mix: Record<Stage, number>;
}

export interface HypeConfig {
  beta_multipliers: Record<HypeState, number>;
  transition_matrix: Record<HypeState, Record<HypeState, number>>;
}

export interface SimulationMeta {
  seed: number;
  n_founders: number;
  n_runs: number;
  budget_scale_factor: number;
  stochastic_checks: boolean;
  use_score_per_dollar: boolean;
  syndication_rate: number;
  regions: Record<Region, RegionConfig>;
  hype: HypeConfig;
  git_hash?: string;
  timestamp?: string;
  sources?: Array<{
    name: string;
    url: string;
    description: string;
  }>;
}

export interface Persona {
  name: string;
  revenue: number;
  growth: number;
  charisma: number;
  vision: number;
  traction_quality: number;
  repeat_founder: boolean;
  geo_flex: number;
  domain: Domain;
}

export interface QueryResult {
  query: string;
  intent: string;
  answer: string;
  data?: any;
  chartType?: 'bar' | 'line' | 'radar' | 'area' | 'scatter';
  chartProps?: any;
  error?: string;
}
