import type { FounderRun, SummaryMetric } from '../types';

/**
 * Compute mean and 95% confidence interval for a numeric array
 */
export function computeCI(values: number[]): { mean: number; ci_low: number; ci_high: number; n: number } {
  if (values.length === 0) {
    return { mean: 0, ci_low: 0, ci_high: 0, n: 0 };
  }

  const n = values.length;
  const mean = values.reduce((sum, v) => sum + v, 0) / n;

  if (n === 1) {
    return { mean, ci_low: mean, ci_high: mean, n };
  }

  // Calculate standard deviation
  const variance = values.reduce((sum, v) => sum + (v - mean) ** 2, 0) / (n - 1);
  const std = Math.sqrt(variance);

  // 95% CI using t-distribution approximation (z=1.96 for large n)
  const se = std / Math.sqrt(n);
  const margin = 1.96 * se;

  return {
    mean,
    ci_low: mean - margin,
    ci_high: mean + margin,
    n,
  };
}

/**
 * Group runs by a key and compute CI for a metric
 */
export function groupByAndComputeCI(
  runs: FounderRun[],
  groupByKey: keyof FounderRun,
  metricKey: keyof FounderRun
): SummaryMetric[] {
  const groups = new Map<string, number[]>();

  for (const run of runs) {
    const groupValue = String(run[groupByKey]);
    const metricValue = run[metricKey];

    if (typeof metricValue !== 'number') continue;

    if (!groups.has(groupValue)) {
      groups.set(groupValue, []);
    }
    groups.get(groupValue)!.push(metricValue);
  }

  const summaries: SummaryMetric[] = [];

  for (const [groupValue, values] of groups.entries()) {
    const ci = computeCI(values);
    summaries.push({
      metric: String(metricKey),
      group_by: groupValue,
      mean: ci.mean,
      ci_low: ci.ci_low,
      ci_high: ci.ci_high,
      n: ci.n,
    });
  }

  return summaries;
}

/**
 * Compute funding likelihood (probability) by region
 */
export function computeFundingLikelihoodByRegion(runs: FounderRun[]): SummaryMetric[] {
  const regionGroups = new Map<string, { funded: number; total: number }>();

  for (const run of runs) {
    const region = run.region;

    if (!regionGroups.has(region)) {
      regionGroups.set(region, { funded: 0, total: 0 });
    }

    const group = regionGroups.get(region)!;
    group.total++;
    if (run.funded) {
      group.funded++;
    }
  }

  const summaries: SummaryMetric[] = [];

  for (const [region, { funded, total }] of regionGroups.entries()) {
    const p = funded / total;
    // Wilson score interval for binomial proportions
    const z = 1.96;
    const denominator = 1 + (z * z) / total;
    const center = (p + (z * z) / (2 * total)) / denominator;
    const margin = (z * Math.sqrt((p * (1 - p)) / total + (z * z) / (4 * total * total))) / denominator;

    summaries.push({
      metric: 'funding_likelihood',
      group_by: region,
      mean: p,
      ci_low: Math.max(0, center - margin),
      ci_high: Math.min(1, center + margin),
      n: total,
    });
  }

  return summaries;
}

/**
 * Compute aggregated dollar share vs count share (for calibration chart)
 */
export function computeCalibration(runs: FounderRun[]) {
  const fundedRuns = runs.filter((r) => r.funded);

  const regionStats = new Map<string, { dollars: number; count: number }>();

  for (const run of fundedRuns) {
    if (!regionStats.has(run.region)) {
      regionStats.set(run.region, { dollars: 0, count: 0 });
    }
    const stats = regionStats.get(run.region)!;
    stats.dollars += run.dollars;
    stats.count++;
  }

  const totalDollars = Array.from(regionStats.values()).reduce((sum, s) => sum + s.dollars, 0);
  const totalCount = Array.from(regionStats.values()).reduce((sum, s) => sum + s.count, 0);

  const calibration = Array.from(regionStats.entries()).map(([region, stats]) => ({
    region,
    dollar_share: stats.dollars / totalDollars,
    count_share: stats.count / totalCount,
  }));

  return calibration;
}
