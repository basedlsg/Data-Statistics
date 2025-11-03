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
 * Generate mock simulation runs with REALISTIC distributions
 */
export function getMockRuns(filter?: RunFilter): FounderRun[] {
  const runs: FounderRun[] = [];

  // Realistic regional distribution (matches budget shares)
  const regionalDistribution: Record<Region, number> = {
    bay_area: 0.524,  // 52.4%
    nyc: 0.238,       // 23.8%
    boston: 0.131,    // 13.1%
    la: 0.107,        // 10.7%
  };

  // Domain preferences by region
  const domainPreferences: Record<Region, Record<Domain, number>> = {
    bay_area: { ai: 0.45, bio: 0.15, consumer: 0.20, enterprise: 0.20 },
    nyc: { ai: 0.20, bio: 0.10, consumer: 0.20, enterprise: 0.50 },
    boston: { ai: 0.25, bio: 0.40, consumer: 0.10, enterprise: 0.25 },
    la: { ai: 0.15, bio: 0.10, consumer: 0.50, enterprise: 0.25 },
  };

  // Generate 1000 mock founders across 5 runs
  for (let runId = 0; runId < 5; runId++) {
    for (let founderId = 0; founderId < 200; founderId++) {
      // Select region based on realistic distribution
      const rand = Math.random();
      let region: Region;
      if (rand < 0.524) region = 'bay_area';
      else if (rand < 0.762) region = 'nyc';
      else if (rand < 0.893) region = 'boston';
      else region = 'la';

      // Select domain based on regional preferences
      const domainRand = Math.random();
      const domainPref = domainPreferences[region];
      let domain: Domain;
      if (domainRand < domainPref.ai) domain = 'ai';
      else if (domainRand < domainPref.ai + domainPref.bio) domain = 'bio';
      else if (domainRand < domainPref.ai + domainPref.bio + domainPref.consumer) domain = 'consumer';
      else domain = 'enterprise';

      // Stage distribution (realistic mix)
      const stageRand = Math.random();
      let stage: Stage;
      if (stageRand < 0.25) stage = 'seed';
      else if (stageRand < 0.60) stage = 'series_a';
      else stage = 'series_b_plus';

      const funded = Math.random() > 0.33; // ~67% funding rate
      const lead = funded && Math.random() > 0.25;
      const syndication = funded && !lead;

      // Generate traits that vary by region
      const charisma = region === 'bay_area' || region === 'la'
        ? Math.random() * 3 - 0.5  // Higher charisma in Bay/LA
        : Math.random() * 3 - 1.5;  // Lower in NYC/Boston

      const vision = region === 'bay_area'
        ? Math.random() * 3 - 0.3   // Highest vision in Bay
        : Math.random() * 3 - 1.2;

      const revenue = region === 'nyc'
        ? Math.exp(Math.random() * 3 + 15)  // Higher revenue in NYC
        : Math.exp(Math.random() * 3 + 13);

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
        dollars: funded ? (stage === 'seed' ? Math.random() * 3 + 1.5 : stage === 'series_a' ? Math.random() * 10 + 8 : Math.random() * 25 + 20) : 0,
        score: Math.random() * 100,
        prob: funded ? Math.random() * 0.5 + 0.5 : Math.random() * 0.3,
        revenue,
        growth: Math.random() * 2 - 0.5,
        charisma,
        vision,
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
