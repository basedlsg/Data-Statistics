import { promises as fs } from 'fs';
import path from 'path';
import type { FounderRun } from '../types';
import { getMockRuns } from './mock';

const SIM_DATA_DIR = process.env.SIM_DATA_DIR || './results';
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === '1';

export interface RunFilter {
  lead?: boolean;
  syndication?: boolean;
  region?: string;
  domain?: string;
  stage?: string;
  funded?: boolean;
  run_id?: number;
}

/**
 * Load simulation runs from JSON files
 */
export async function loadRuns(filter?: RunFilter): Promise<FounderRun[]> {
  if (USE_MOCK) {
    return getMockRuns(filter);
  }

  try {
    const resultsDir = path.join(process.cwd(), SIM_DATA_DIR);
    const files = await fs.readdir(resultsDir);

    // Find all run_*.json files
    const runFiles = files.filter((f) => f.match(/^run_\d+\.json$/));

    if (runFiles.length === 0) {
      console.warn('No run files found in', resultsDir);
      return [];
    }

    const allRuns: FounderRun[] = [];

    for (const file of runFiles) {
      try {
        const content = await fs.readFile(path.join(resultsDir, file), 'utf-8');
        const data = JSON.parse(content);

        // Handle different data formats
        if (data.founders && Array.isArray(data.founders)) {
          // Format: { founders: [...] }
          allRuns.push(...data.founders);
        } else if (Array.isArray(data)) {
          // Format: [...]
          allRuns.push(...data);
        }
      } catch (err) {
        console.warn(`Could not parse ${file}:`, err);
      }
    }

    // Apply filters
    return filterRuns(allRuns, filter);
  } catch (error) {
    console.error('Error loading runs:', error);
    return [];
  }
}

/**
 * Load aggregated results from CSV
 */
export async function loadAggregatedRuns(filter?: RunFilter): Promise<FounderRun[]> {
  if (USE_MOCK) {
    return getMockRuns(filter);
  }

  try {
    const csvPath = path.join(process.cwd(), SIM_DATA_DIR, 'aggregated_results.csv');
    const content = await fs.readFile(csvPath, 'utf-8');

    const lines = content.trim().split('\n');
    if (lines.length < 2) {
      return [];
    }

    const headers = lines[0].split(',');
    const runs: FounderRun[] = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',');
      const run: any = {};

      headers.forEach((header, idx) => {
        const value = values[idx];
        const key = header.trim();

        // Parse values based on key
        if (key === 'funded' || key === 'lead' || key === 'syndication' || key === 'repeat_founder') {
          run[key] = value === 'True' || value === 'true' || value === '1';
        } else if (
          key === 'dollars' ||
          key === 'score' ||
          key === 'prob' ||
          key === 'revenue' ||
          key === 'growth' ||
          key === 'charisma' ||
          key === 'vision' ||
          key === 'traction_quality' ||
          key === 'geo_flex'
        ) {
          run[key] = parseFloat(value);
        } else if (key === 'seed' || key === 'run_id' || key === 't' || key === 'founder_id') {
          run[key] = parseInt(value, 10);
        } else {
          run[key] = value;
        }
      });

      runs.push(run as FounderRun);
    }

    return filterRuns(runs, filter);
  } catch (error) {
    console.warn('Could not load aggregated CSV, trying JSON:', error);
    return loadRuns(filter);
  }
}

function filterRuns(runs: FounderRun[], filter?: RunFilter): FounderRun[] {
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
