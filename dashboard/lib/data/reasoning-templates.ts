/**
 * Reasoning Templates for VC Decision-Making
 *
 * These templates represent common patterns in how VCs evaluate startups
 * across different scenarios (hype states, founder profiles, metrics, etc.)
 */

export type ReasoningPattern =
  | 'narrative_hype_cycle'
  | 'revenue_focused_rejection'
  | 'scientific_validation'
  | 'domain_mismatch'
  | 'early_stage_risk'
  | 'risk_off_fundamentals'
  | 'solo_founder_concern'
  | 'founder_market_fit';

export interface ReasoningTemplate {
  pattern: ReasoningPattern;
  description: string;
  commonTriggers: string[];
  regionalVariance: {
    bay_area: string;
    nyc: string;
    boston: string;
    la: string;
  };
  examplePhrases: string[];
}

export const reasoningTemplates: Record<ReasoningPattern, ReasoningTemplate> = {
  narrative_hype_cycle: {
    pattern: 'narrative_hype_cycle',
    description: 'During hype cycles, VCs amplify importance of vision/narrative over fundamentals',
    commonTriggers: [
      'Hype state = 2.0x',
      'Pre-revenue or <$500k ARR',
      'High charisma (>1.8) + high vision (>2.0)',
      'AI/cutting-edge domain',
    ],
    regionalVariance: {
      bay_area: 'Most susceptible. Will fund bold vision at seed with minimal traction. β_hype = 0.80',
      nyc: 'Moderately cautious. Requires some revenue signal even in hype. β_hype = 0.50',
      boston: 'Least susceptible. Still demands scientific validation. β_hype = 0.30',
      la: 'Narrative-friendly but wants proof of brand/community traction. β_hype = 0.65',
    },
    examplePhrases: [
      'This is the future of [category]',
      'AI-powered [X] could be category-defining',
      'Perfect timing with the [tech] wave',
      'Vision is exactly what this market needs',
      'Love the AI-ed vision in this hype cycle',
    ],
  },

  revenue_focused_rejection: {
    pattern: 'revenue_focused_rejection',
    description: 'NYC VCs consistently reject pre-revenue or low-revenue plays regardless of narrative',
    commonTriggers: [
      'Revenue < $500k ARR',
      'No clear path to $1M+ ARR in 12 months',
      'High burn relative to revenue',
      'Monetization unproven',
    ],
    regionalVariance: {
      bay_area: 'Flexible on revenue at seed. Willing to fund vision.',
      nyc: 'STRICT revenue requirements. Primary rejection reason. w_revenue = 1.2',
      boston: 'Revenue important but will accept grants/scientific milestones as proxy.',
      la: 'Prefers revenue but will consider influencer traction/brand metrics.',
    },
    examplePhrases: [
      'Too early. Need to see $500k ARR minimum',
      'LOIs don't count until they convert',
      'Come back when you have paying customers',
      'Need 6 months of revenue data first',
      'Show us enterprise contracts, not pilots',
    ],
  },

  scientific_validation: {
    pattern: 'scientific_validation',
    description: 'Boston VCs require peer review, clinical data, or scientific proof for bio/deeptech',
    commonTriggers: [
      'Bio or deeptech domain',
      'Claims about efficacy, safety, or performance',
      'Regulatory pathway unclear',
      'Scientific founders without publications',
    ],
    regionalVariance: {
      bay_area: 'Values scientific founders but less rigorous on validation.',
      nyc: 'Defers to specialists. Needs external validation from experts.',
      boston: 'STRICT scientific standards. w_traction includes publications. w_science_signal high.',
      la: 'Generally passes on hard science plays.',
    },
    examplePhrases: [
      'Where's the peer-reviewed data?',
      'Need to see Phase 1 results before we commit',
      'Has this been validated in clinical trials?',
      'What's the FDA pathway timeline?',
      'Strong scientific foundation gives us confidence',
    ],
  },

  domain_mismatch: {
    pattern: 'domain_mismatch',
    description: 'VCs pass on strong companies outside their domain expertise',
    commonTriggers: [
      'Developer tools pitched to LA (consumer-focused)',
      'Consumer apps pitched to Boston (deeptech-focused)',
      'Bio/healthcare pitched to LA (media-focused)',
      'Enterprise SaaS pitched to LA',
    ],
    regionalVariance: {
      bay_area: 'Broadest aperture. Will consider most domains.',
      nyc: 'Enterprise/fintech focused. Passes on consumer unless exceptional.',
      boston: 'Bio/deeptech focused. Passes on consumer/media.',
      la: 'Consumer/media focused. Passes on enterprise/infrastructure.',
    },
    examplePhrases: [
      'Not our domain expertise',
      'Outside our wheelhouse',
      'Would pass to specialized funds',
      'Not our sweet spot',
      'Way outside our zone',
    ],
  },

  early_stage_risk: {
    pattern: 'early_stage_risk',
    description: 'Multiple risk factors compound: solo founder + pre-revenue + crowded market',
    commonTriggers: [
      'Solo founder (no co-founder)',
      'Pre-revenue or <$100k ARR',
      'Crowded/commoditizing market',
      'Unclear differentiation',
    ],
    regionalVariance: {
      bay_area: 'Most risk-tolerant. Will fund solo founders with strong technical backgrounds.',
      nyc: 'Risk-averse on solo founders without traction.',
      boston: 'Evaluates on scientific merit; team composition secondary.',
      la: 'Wants charismatic founding team. Solo founders face bias.',
    },
    examplePhrases: [
      'Solo founder risk concerns us',
      'Need to see team expansion before Series A',
      'Too many compounding risks',
      'Market is commoditizing fast',
      'What's stopping [incumbent] from building this?',
    ],
  },

  risk_off_fundamentals: {
    pattern: 'risk_off_fundamentals',
    description: 'In risk-off mode (0.5x), VCs focus on unit economics, retention, and proven ROI',
    commonTriggers: [
      'Hype state = 0.5x (risk-off)',
      'Economic uncertainty or market downturn',
      'Cost-cutting or efficiency narrative',
      'Strong unit economics',
    ],
    regionalVariance: {
      bay_area: 'Shifts to fundamentals but still values innovation.',
      nyc: 'THRIVES in risk-off. Revenue focus intensifies. w_revenue increases.',
      boston: 'Already fundamental-focused. Less variance across states.',
      la: 'Struggles in risk-off. Deal flow decreases.',
    },
    examplePhrases: [
      'Love this in risk-off mode',
      'ROI-focused products win when budgets tighten',
      'Counter-cyclical is exactly what we need',
      'Quantifiable value prop is critical now',
      'Perfect for this market environment',
    ],
  },

  solo_founder_concern: {
    pattern: 'solo_founder_concern',
    description: 'Solo technical founders face bias despite strong product traction',
    commonTriggers: [
      'Solo founder (charisma typically <1.0)',
      'Technical product (developer tools, infrastructure)',
      'Strong product metrics but no co-founder',
    ],
    regionalVariance: {
      bay_area: 'Most accepting. Values technical execution over team size.',
      nyc: 'Concerned about scaling without co-founder. Wants business partner.',
      boston: 'Neutral. Evaluates on technical merit.',
      la: 'Biased against solo founders. Values charismatic teams.',
    },
    examplePhrases: [
      'Solo founder risk concerns us',
      'Would invest if team expands',
      'Need a co-founder for go-to-market',
      'Who handles sales while you code?',
      'Execution risk is high with one person',
    ],
  },

  founder_market_fit: {
    pattern: 'founder_market_fit',
    description: 'Founder background perfectly aligns with problem space (doctor building healthcare, lawyer building legal tech)',
    commonTriggers: [
      'Founder has 5+ years in target industry',
      'Founder experienced the problem firsthand',
      'Domain expertise is rare/valuable',
      'Repeat founder in same vertical',
    ],
    regionalVariance: {
      bay_area: 'Values but not critical. Will fund smart outsiders.',
      nyc: 'Strong signal for enterprise sales. Domain expertise helps.',
      boston: 'CRITICAL for bio/healthcare. Scientific credentials required.',
      la: 'Important for consumer. Lived experience with target demographic.',
    },
    examplePhrases: [
      'Perfect founder-market fit',
      'Built by a [profession] for [profession]s',
      'Founder lived this problem for years',
      'Domain expertise is a huge advantage',
      'Insider knowledge creates unfair advantage',
    ],
  },
};

/**
 * Get the most relevant reasoning template for a given pitch
 */
export function getRelevantTemplate(
  domain: string,
  revenue: number,
  charisma: number,
  vision: number,
  hypeState: 'risk_off' | 'normal' | 'hype',
  soloFounder: boolean,
  founderBackground?: string
): ReasoningPattern[] {
  const patterns: ReasoningPattern[] = [];

  // Hype cycle narrative
  if (hypeState === 'hype' && revenue < 500000 && vision > 2.0) {
    patterns.push('narrative_hype_cycle');
  }

  // Revenue rejection
  if (revenue < 500000 && hypeState !== 'hype') {
    patterns.push('revenue_focused_rejection');
  }

  // Scientific validation
  if (domain === 'bio' || domain === 'deeptech') {
    patterns.push('scientific_validation');
  }

  // Risk-off fundamentals
  if (hypeState === 'risk_off' && revenue > 1000000) {
    patterns.push('risk_off_fundamentals');
  }

  // Solo founder
  if (soloFounder) {
    patterns.push('solo_founder_concern');
  }

  // Founder-market fit
  if (founderBackground && founderBackground.includes('Ex-')) {
    patterns.push('founder_market_fit');
  }

  // Early stage risk (compounding factors)
  if (soloFounder && revenue < 100000) {
    patterns.push('early_stage_risk');
  }

  return patterns;
}
