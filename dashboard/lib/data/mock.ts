import type { FounderRun, SimulationMeta, Region, Stage, Domain } from '../types';
import type { RunFilter } from './loadRuns';

/**
 * Generate mock simulation metadata
 */
export function getMockMeta(): SimulationMeta {
  return {
    seed: 42,
    n_founders: 200,
    n_runs: 10,
    budget_scale_factor: 0.004,
    stochastic_checks: true,
    use_score_per_dollar: true,
    syndication_rate: 0.25,
    regions: {
      bay_area: {
        name: 'San Francisco Bay Area',
        budget_share: 0.524,
        annual_capital_bn: 104.8,
        weights: {
          revenue: 0.6,
          growth: 1.1,
          charisma: 1.3,
          vision: 1.4,
          traction_quality: 0.9,
          repeat_founder: 0.7,
          geo_flex: 0.5,
        },
        domain_preferences: { ai: 1.5, bio: 1.0, consumer: 1.1, enterprise: 1.2 },
        hype_beta: 0.8,
        check_sizes: { seed: 2.8, series_a: 14.0, series_b_plus: 38.0 },
        stage_mix: { seed: 0.25, series_a: 0.35, series_b_plus: 0.40 },
      },
      nyc: {
        name: 'New York City',
        budget_share: 0.238,
        annual_capital_bn: 47.6,
        weights: {
          revenue: 1.4,
          growth: 1.2,
          charisma: 0.7,
          vision: 0.8,
          traction_quality: 1.2,
          repeat_founder: 0.9,
          geo_flex: 0.4,
        },
        domain_preferences: { ai: 1.0, bio: 0.8, consumer: 1.0, enterprise: 1.4 },
        hype_beta: 0.5,
        check_sizes: { seed: 2.2, series_a: 12.0, series_b_plus: 36.0 },
        stage_mix: { seed: 0.20, series_a: 0.35, series_b_plus: 0.45 },
      },
      boston: {
        name: 'Boston/Cambridge',
        budget_share: 0.131,
        annual_capital_bn: 26.2,
        weights: {
          revenue: 1.1,
          growth: 1.0,
          charisma: 0.6,
          vision: 0.7,
          traction_quality: 1.3,
          repeat_founder: 1.0,
          geo_flex: 0.3,
        },
        domain_preferences: { ai: 1.1, bio: 1.6, consumer: 0.8, enterprise: 1.0 },
        hype_beta: 0.3,
        check_sizes: { seed: 1.8, series_a: 10.5, series_b_plus: 28.0 },
        stage_mix: { seed: 0.20, series_a: 0.40, series_b_plus: 0.40 },
      },
      la: {
        name: 'Los Angeles',
        budget_share: 0.107,
        annual_capital_bn: 21.4,
        weights: {
          revenue: 0.8,
          growth: 1.0,
          charisma: 1.2,
          vision: 1.1,
          traction_quality: 0.8,
          repeat_founder: 0.6,
          geo_flex: 0.6,
        },
        domain_preferences: { ai: 0.9, bio: 0.7, consumer: 1.5, enterprise: 0.9 },
        hype_beta: 0.6,
        check_sizes: { seed: 2.0, series_a: 11.0, series_b_plus: 30.0 },
        stage_mix: { seed: 0.30, series_a: 0.40, series_b_plus: 0.30 },
      },
    },
    hype: {
      beta_multipliers: {
        risk_off: 0.5,
        normal: 1.0,
        hype: 2.0,
      },
      transition_matrix: {
        risk_off: { risk_off: 0.7, normal: 0.25, hype: 0.05 },
        normal: { risk_off: 0.1, normal: 0.75, hype: 0.15 },
        hype: { risk_off: 0.05, normal: 0.3, hype: 0.65 },
      },
    },
    git_hash: 'abc123',
    timestamp: new Date().toISOString(),
    sources: [
      {
        name: 'PitchBook Q4 2024',
        url: 'https://pitchbook.com',
        description: 'Quarterly VC data and regional breakdowns',
      },
      {
        name: 'NVCA 2024 Yearbook',
        url: 'https://nvca.org',
        description: 'National Venture Capital Association annual report',
      },
    ],
  };
}

/**
 * Generate mock simulation runs
 */
export function getMockRuns(filter?: RunFilter): FounderRun[] {
  const regions: Region[] = ['bay_area', 'nyc', 'boston', 'la'];
  const stages: Stage[] = ['seed', 'series_a', 'series_b_plus'];
  const domains: Domain[] = ['ai', 'bio', 'consumer', 'enterprise'];

  const runs: FounderRun[] = [];

  // Generate 1000 mock founders across 5 runs
  for (let runId = 0; runId < 5; runId++) {
    for (let founderId = 0; founderId < 200; founderId++) {
      const region = regions[Math.floor(Math.random() * regions.length)];
      const stage = stages[Math.floor(Math.random() * stages.length)];
      const domain = domains[Math.floor(Math.random() * domains.length)];
      const funded = Math.random() > 0.35; // ~65% funding rate
      const lead = funded && Math.random() > 0.25;
      const syndication = funded && !lead;

      const run: FounderRun = {
        seed: 42 + runId,
        run_id: runId,
        t: 0,
        region,
        stage,
        domain,
        founder_id: founderId,
        funded,
        lead,
        syndication,
        dollars: funded ? Math.random() * 20 + 5 : 0,
        score: Math.random() * 100,
        prob: funded ? Math.random() * 0.5 + 0.5 : Math.random() * 0.3,
        revenue: Math.exp(Math.random() * 15 + 5),
        growth: Math.random() * 2 - 0.5,
        charisma: Math.random() * 4 - 2,
        vision: Math.random() * 4 - 2,
        traction_quality: Math.random() * 2 - 0.5,
        repeat_founder: Math.random() > 0.7,
        geo_flex: Math.random() * 2 - 0.5,
      };

      runs.push(run);
    }
  }

  // Apply filters
  if (!filter) return runs;

  return runs.filter((run) => {
    if (filter.lead !== undefined && run.lead !== filter.lead) return false;
    if (filter.syndication !== undefined && run.syndication !== filter.syndication) return false;
    if (filter.region && run.region !== filter.region) return false;
    if (filter.domain && run.domain !== filter.domain) return false;
    if (filter.stage && run.stage !== filter.stage) return false;
    if (filter.funded !== undefined && run.funded !== filter.funded) return false;
    if (filter.run_id !== undefined && run.run_id !== filter.run_id) return false;
    return true;
  });
}
