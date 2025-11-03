import type { QueryResult } from '../types';

export type Intent =
  | 'FEATURE_IMPORTANCE'
  | 'FUNDING_LIKELIHOOD'
  | 'COMPARE'
  | 'CALIBRATION'
  | 'DOMAIN_STAGE_MIX'
  | 'UNKNOWN';

export interface ParsedQuery {
  intent: Intent;
  slots: Record<string, string>;
  raw: string;
}

/**
 * Parse natural language query into intent and slots
 */
export function parseQuery(query: string): ParsedQuery {
  const lower = query.toLowerCase().trim();

  // FEATURE_IMPORTANCE: "Where is X most important?" / "Which region values X?"
  if (
    lower.includes('important') ||
    lower.includes('values') ||
    lower.includes('weights') ||
    lower.includes('prefers')
  ) {
    const feature = extractFeature(lower);
    const region = extractRegion(lower);

    return {
      intent: 'FEATURE_IMPORTANCE',
      slots: {
        feature: feature || 'charisma',
        region: region || 'global',
      },
      raw: query,
    };
  }

  // FUNDING_LIKELIHOOD: "Where am I most likely to get funded?" / "What are my chances?"
  if (
    lower.includes('likely') ||
    lower.includes('chances') ||
    lower.includes('probability') ||
    lower.includes('get funded')
  ) {
    const region = extractRegion(lower);
    const persona = extractPersona(lower);

    return {
      intent: 'FUNDING_LIKELIHOOD',
      slots: {
        region: region || 'all',
        persona: persona || 'current',
      },
      raw: query,
    };
  }

  // COMPARE: "Compare X vs Y" / "How does X differ from Y?"
  if (lower.includes('compare') || lower.includes('differ') || lower.includes(' vs ')) {
    const personas = extractComparePersonas(lower);

    return {
      intent: 'COMPARE',
      slots: {
        personaA: personas[0] || 'Champion',
        personaB: personas[1] || 'RevenueFirst',
      },
      raw: query,
    };
  }

  // CALIBRATION: "Show calibration" / "Dollar share vs count share"
  if (
    lower.includes('calibration') ||
    lower.includes('dollar share') ||
    lower.includes('allocation efficiency')
  ) {
    const region = extractRegion(lower);

    return {
      intent: 'CALIBRATION',
      slots: {
        region: region || 'all',
      },
      raw: query,
    };
  }

  // DOMAIN_STAGE_MIX: "Show domain mix for NYC" / "What stages does Boston fund?"
  if (
    lower.includes('domain') ||
    lower.includes('stage') ||
    lower.includes('mix') ||
    lower.includes('breakdown')
  ) {
    const region = extractRegion(lower);

    return {
      intent: 'DOMAIN_STAGE_MIX',
      slots: {
        region: region || 'all',
      },
      raw: query,
    };
  }

  return {
    intent: 'UNKNOWN',
    slots: {},
    raw: query,
  };
}

// Helper functions to extract entities from query

function extractFeature(query: string): string | null {
  const features = [
    'charisma',
    'vision',
    'revenue',
    'growth',
    'traction',
    'repeat',
    'geo',
    'founder',
  ];

  for (const feature of features) {
    if (query.includes(feature)) {
      if (feature === 'repeat' || query.includes('repeat founder')) return 'repeat_founder';
      if (feature === 'geo') return 'geo_flex';
      if (feature === 'traction') return 'traction_quality';
      return feature;
    }
  }

  return null;
}

function extractRegion(query: string): string | null {
  if (query.includes('bay area') || query.includes('sf') || query.includes('silicon valley'))
    return 'bay_area';
  if (query.includes('new york') || query.includes('nyc')) return 'nyc';
  if (query.includes('boston') || query.includes('cambridge')) return 'boston';
  if (query.includes('los angeles') || query.includes('la')) return 'la';

  return null;
}

function extractPersona(query: string): string | null {
  if (query.includes('champion')) return 'Champion';
  if (query.includes('revenue') && query.includes('first')) return 'RevenueFirst';
  if (query.includes('bio') && query.includes('science')) return 'BioScience';
  if (query.includes('consumer') && query.includes('brand')) return 'ConsumerBrand';

  return null;
}

function extractComparePersonas(query: string): [string, string] {
  const personas = ['Champion', 'RevenueFirst', 'BioScience', 'ConsumerBrand'];
  const found: string[] = [];

  for (const persona of personas) {
    if (query.toLowerCase().includes(persona.toLowerCase())) {
      found.push(persona);
    }
  }

  if (found.length >= 2) {
    return [found[0], found[1]];
  }

  // Default comparison
  return ['Champion', 'RevenueFirst'];
}
