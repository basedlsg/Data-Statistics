import type { ParsedQuery, QueryResult } from '../types';
import type { SimulationMeta } from '../types';

/**
 * Generate answer from parsed query (to be called client-side with fetched data)
 */
export async function generateAnswer(parsed: ParsedQuery, meta: SimulationMeta | null): Promise<QueryResult> {
  if (!meta) {
    return {
      query: parsed.raw,
      intent: parsed.intent,
      answer: 'Could not load simulation metadata. Please ensure data is available.',
      error: 'NO_META',
    };
  }

  switch (parsed.intent) {
    case 'FEATURE_IMPORTANCE':
      return await answerFeatureImportance(parsed, meta);

    case 'FUNDING_LIKELIHOOD':
      return await answerFundingLikelihood(parsed, meta);

    case 'COMPARE':
      return await answerCompare(parsed, meta);

    case 'CALIBRATION':
      return await answerCalibration(parsed, meta);

    case 'DOMAIN_STAGE_MIX':
      return await answerDomainStageMix(parsed, meta);

    default:
      return {
        query: parsed.raw,
        intent: 'UNKNOWN',
        answer:
          "I don't understand that question. Try asking:\n" +
          '• "Where is charisma most important?"\n' +
          '• "Where am I most likely to get funded?"\n' +
          '• "Compare Champion vs RevenueFirst"\n' +
          '• "Show domain/stage mix for NYC"',
      };
  }
}

async function answerFeatureImportance(parsed: ParsedQuery, meta: SimulationMeta): Promise<QueryResult> {
  const feature = parsed.slots.feature || 'charisma';
  const region = parsed.slots.region || 'global';

  if (region === 'global') {
    // Compare feature weight across all regions
    const weights: Array<{ region: string; weight: number }> = [];

    for (const [regionKey, regionConfig] of Object.entries(meta.regions)) {
      const weight = regionConfig.weights[feature as keyof typeof regionConfig.weights] || 0;
      weights.push({ region: regionConfig.name, weight });
    }

    weights.sort((a, b) => b.weight - a.weight);

    const top = weights[0];
    const answer = `**${feature}** is most valued in **${top.region}** (weight: ${top.weight.toFixed(2)}).\n\nFull ranking:\n${weights
      .map((w, i) => `${i + 1}. ${w.region}: ${w.weight.toFixed(2)}`)
      .join('\n')}`;

    return {
      query: parsed.raw,
      intent: parsed.intent,
      answer,
      data: weights,
      chartType: 'bar',
      chartProps: {
        dataKey: 'weight',
        xKey: 'region',
        title: `${feature} importance by region`,
      },
    };
  } else {
    // Single region
    const regionConfig = meta.regions[region as keyof typeof meta.regions];
    if (!regionConfig) {
      return {
        query: parsed.raw,
        intent: parsed.intent,
        answer: `Region "${region}" not found.`,
        error: 'INVALID_REGION',
      };
    }

    const weight = regionConfig.weights[feature as keyof typeof regionConfig.weights] || 0;
    const answer = `In **${regionConfig.name}**, **${feature}** has a weight of **${weight.toFixed(2)}**.`;

    return {
      query: parsed.raw,
      intent: parsed.intent,
      answer,
    };
  }
}

async function answerFundingLikelihood(parsed: ParsedQuery, meta: SimulationMeta): Promise<QueryResult> {
  // Fetch actual funding likelihood from API
  const response = await fetch('/api/summaries?metric=funding_likelihood');
  const data = await response.json();

  if (!data.summaries || data.summaries.length === 0) {
    return {
      query: parsed.raw,
      intent: parsed.intent,
      answer: 'No funding likelihood data available.',
      error: 'NO_DATA',
    };
  }

  const summaries = data.summaries;
  summaries.sort((a: any, b: any) => b.mean - a.mean);

  const topRegion = summaries[0];
  const regionName = meta.regions[topRegion.group_by as keyof typeof meta.regions]?.name || topRegion.group_by;

  const answer = `You are most likely to get funded in **${regionName}** (${(topRegion.mean * 100).toFixed(1)}% likelihood).\n\nAll regions:\n${summaries
    .map(
      (s: any) =>
        `• ${meta.regions[s.group_by as keyof typeof meta.regions]?.name || s.group_by}: ${(s.mean * 100).toFixed(1)}% (95% CI: ${(s.ci_low * 100).toFixed(1)}%-${(s.ci_high * 100).toFixed(1)}%)`
    )
    .join('\n')}`;

  return {
    query: parsed.raw,
    intent: parsed.intent,
    answer,
    data: summaries,
    chartType: 'bar',
    chartProps: {
      dataKey: 'mean',
      xKey: 'group_by',
      title: 'Funding likelihood by region',
    },
  };
}

async function answerCompare(parsed: ParsedQuery, meta: SimulationMeta): Promise<QueryResult> {
  const personaA = parsed.slots.personaA || 'Champion';
  const personaB = parsed.slots.personaB || 'RevenueFirst';

  const answer = `Comparison between **${personaA}** and **${personaB}** personas.\n\nNavigate to the **Founder** page to see a detailed comparison with probabilities by region.`;

  return {
    query: parsed.raw,
    intent: parsed.intent,
    answer,
  };
}

async function answerCalibration(parsed: ParsedQuery, meta: SimulationMeta): Promise<QueryResult> {
  const response = await fetch('/api/summaries?metric=calibration');
  const data = await response.json();

  if (!data.calibration || data.calibration.length === 0) {
    return {
      query: parsed.raw,
      intent: parsed.intent,
      answer: 'No calibration data available.',
      error: 'NO_DATA',
    };
  }

  const calibration = data.calibration;

  const answer = `**Calibration Analysis** (Dollar Share vs Count Share):\n\n${calibration
    .map(
      (c: any) =>
        `• ${meta.regions[c.region as keyof typeof meta.regions]?.name || c.region}: ${(c.dollar_share * 100).toFixed(1)}% dollars, ${(c.count_share * 100).toFixed(1)}% deals`
    )
    .join('\n')}`;

  return {
    query: parsed.raw,
    intent: parsed.intent,
    answer,
    data: calibration,
    chartType: 'scatter',
    chartProps: {
      xKey: 'count_share',
      yKey: 'dollar_share',
      title: 'Calibration: Dollar Share vs Count Share',
    },
  };
}

async function answerDomainStageMix(parsed: ParsedQuery, meta: SimulationMeta): Promise<QueryResult> {
  const region = parsed.slots.region || 'all';

  const answer = `Domain/stage mix for **${region === 'all' ? 'all regions' : meta.regions[region as keyof typeof meta.regions]?.name || region}**.\n\nNavigate to the **Regions** page to see detailed breakdowns.`;

  return {
    query: parsed.raw,
    intent: parsed.intent,
    answer,
  };
}
