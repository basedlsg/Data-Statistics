import { promises as fs } from 'fs';
import path from 'path';
import type { SimulationMeta } from '../types';
import { getMockMeta } from './mock';

const SIM_DATA_DIR = process.env.SIM_DATA_DIR || './results';
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === '1';

/**
 * Load simulation metadata from config/meta.json or generate from simulation results
 */
export async function loadMeta(): Promise<SimulationMeta | null> {
  if (USE_MOCK) {
    return getMockMeta();
  }

  try {
    const metaPath = path.join(process.cwd(), SIM_DATA_DIR, 'summary_stats.json');

    try {
      const content = await fs.readFile(metaPath, 'utf-8');
      const data = JSON.parse(content);

      // Load region config from YAML equivalent
      const regionMeta = await loadRegionConfig();

      return {
        seed: data.seed || 42,
        n_founders: data.n_founders || 200,
        n_runs: data.n_runs || 10,
        budget_scale_factor: 0.004,
        stochastic_checks: true,
        use_score_per_dollar: true,
        syndication_rate: 0.25,
        regions: regionMeta,
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
        git_hash: data.git_hash,
        timestamp: data.timestamp || new Date().toISOString(),
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
          {
            name: 'Carta 2024',
            url: 'https://carta.com',
            description: 'Private market data and valuations',
          },
          {
            name: 'CBRE 2024',
            url: 'https://cbre.com',
            description: 'Regional tech market reports',
          },
        ],
      };
    } catch (err) {
      console.warn('Could not load summary_stats.json, using defaults', err);
      return getDefaultMeta();
    }
  } catch (error) {
    console.error('Error loading meta:', error);
    return null;
  }
}

async function loadRegionConfig() {
  // This would normally parse the YAML, but for now we'll use hardcoded values
  return {
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
      domain_preferences: {
        ai: 1.5,
        bio: 1.0,
        consumer: 1.1,
        enterprise: 1.2,
      },
      hype_beta: 0.8,
      check_sizes: {
        seed: 2.8,
        series_a: 14.0,
        series_b_plus: 38.0,
      },
      stage_mix: {
        seed: 0.25,
        series_a: 0.35,
        series_b_plus: 0.40,
      },
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
      domain_preferences: {
        ai: 1.0,
        bio: 0.8,
        consumer: 1.0,
        enterprise: 1.4,
      },
      hype_beta: 0.5,
      check_sizes: {
        seed: 2.2,
        series_a: 12.0,
        series_b_plus: 36.0,
      },
      stage_mix: {
        seed: 0.20,
        series_a: 0.35,
        series_b_plus: 0.45,
      },
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
      domain_preferences: {
        ai: 1.1,
        bio: 1.6,
        consumer: 0.8,
        enterprise: 1.0,
      },
      hype_beta: 0.3,
      check_sizes: {
        seed: 1.8,
        series_a: 10.5,
        series_b_plus: 28.0,
      },
      stage_mix: {
        seed: 0.20,
        series_a: 0.40,
        series_b_plus: 0.40,
      },
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
      domain_preferences: {
        ai: 0.9,
        bio: 0.7,
        consumer: 1.5,
        enterprise: 0.9,
      },
      hype_beta: 0.6,
      check_sizes: {
        seed: 2.0,
        series_a: 11.0,
        series_b_plus: 30.0,
      },
      stage_mix: {
        seed: 0.30,
        series_a: 0.40,
        series_b_plus: 0.30,
      },
    },
  };
}

function getDefaultMeta(): SimulationMeta {
  return {
    seed: 42,
    n_founders: 200,
    n_runs: 10,
    budget_scale_factor: 0.004,
    stochastic_checks: true,
    use_score_per_dollar: true,
    syndication_rate: 0.25,
    regions: {} as any, // Will be filled by loadRegionConfig
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
    sources: [],
  };
}
