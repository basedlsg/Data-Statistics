/**
 * Pitch Library - Curated examples for educational Pitch Theater
 */

export type Domain = 'ai' | 'bio' | 'consumer' | 'enterprise';
export type Stage = 'Pre-seed' | 'Seed' | 'Series A' | 'Series B';
export type HypeState = 'risk_off' | 'normal' | 'hype';
export type Region = 'bay_area' | 'nyc' | 'boston' | 'la';
export type Outcome = 'yes' | 'maybe' | 'no';

export interface PitchTraits {
  charisma: number;
  vision: number;
  revenue: number;
  growth: number;
  traction: string;
}

export interface VCEvaluation {
  region: Region;
  score: number;
  outcome: Outcome;
  reasoning: string;
}

export interface Pitch {
  id: number;
  company: string;
  stage: Stage;
  ask: string;
  domain: Domain;
  founder: string;
  pitch: string;
  traits: PitchTraits;
  hypeState: HypeState;
  evaluations: VCEvaluation[];
  tags: string[];
}

// Sample pitches for MVP (full 50 can be loaded from JSON)
export const pitches: Pitch[] = [
  {
    id: 1,
    company: 'QuickLearn AI',
    stage: 'Seed',
    ask: '$2.5M',
    domain: 'ai',
    founder: 'Sarah Chen, Ex-Google PM',
    pitch: 'We\'re using GPT-4 to personalize learning paths. Adaptive curriculum that adjusts in real-time. $80k ARR across 12 schools. Teachers love it, students engage 3x more.',
    traits: {
      charisma: 1.8,
      vision: 2.1,
      revenue: 80000,
      growth: 280,
      traction: '12 schools, 4,200 students, 3x engagement lift'
    },
    hypeState: 'hype',
    evaluations: [
      {
        region: 'bay_area',
        score: 89.2,
        outcome: 'yes',
        reasoning: 'Love the AI-ed vision in this hype cycle. EdTech + personalization = huge TAM.'
      },
      {
        region: 'nyc',
        score: 64.3,
        outcome: 'no',
        reasoning: 'Too early. Need to see $500k ARR minimum before we commit at this valuation.'
      },
      {
        region: 'boston',
        score: 71.8,
        outcome: 'maybe',
        reasoning: 'Strong engagement metrics but EdTech is crowded. What\'s the moat?'
      },
      {
        region: 'la',
        score: 76.5,
        outcome: 'yes',
        reasoning: 'Teacher testimonials are powerful. Consumer angle (students) is compelling.'
      }
    ],
    tags: ['split_decision', 'ai_hype', 'early_revenue']
  },
  {
    id: 2,
    company: 'GeneCure',
    stage: 'Series A',
    ask: '$15M',
    domain: 'bio',
    founder: 'Dr. James Liu, MIT PhD, Published in Nature',
    pitch: 'CRISPR therapy for sickle cell disease. Completed Phase 1 trial: 8/8 patients symptom-free at 12 months. FDA fast-track designation. Partnering with Boston Children\'s Hospital.',
    traits: {
      charisma: 1.3,
      vision: 1.9,
      revenue: 0,
      growth: 0,
      traction: 'Phase 1 complete, 8/8 success, FDA fast-track, hospital partnership'
    },
    hypeState: 'normal',
    evaluations: [
      {
        region: 'bay_area',
        score: 82.7,
        outcome: 'yes',
        reasoning: 'CRISPR + rare disease = massive upside. MIT + Nature publication validates science.'
      },
      {
        region: 'nyc',
        score: 74.2,
        outcome: 'maybe',
        reasoning: 'Strong scientific foundation but we typically wait for Phase 2 data.'
      },
      {
        region: 'boston',
        score: 94.6,
        outcome: 'yes',
        reasoning: '8/8 patient success rate is exceptional. Hospital partnership de-risks clinical path. Perfect for us.'
      },
      {
        region: 'la',
        score: 68.1,
        outcome: 'no',
        reasoning: 'Outside our domain. Would defer to specialist bio funds.'
      }
    ],
    tags: ['mostly_yes', 'scientific_validation', 'boston_specialty']
  },
  {
    id: 3,
    company: 'FitFam',
    stage: 'Seed',
    ask: '$3M',
    domain: 'consumer',
    founder: 'Jessica Martinez, Fitness Influencer (2.1M followers)',
    pitch: 'Family fitness app. Gamified workouts parents do with kids. $450k ARR, 85k families subscribed. Featured on Good Morning America. 92% monthly retention.',
    traits: {
      charisma: 2.3,
      vision: 1.7,
      revenue: 450000,
      growth: 310,
      traction: '85k families, 92% retention, GMA feature, viral on Instagram'
    },
    hypeState: 'normal',
    evaluations: [
      {
        region: 'bay_area',
        score: 78.4,
        outcome: 'yes',
        reasoning: 'Retention is phenomenal. Influencer-founded consumer plays can scale fast.'
      },
      {
        region: 'nyc',
        score: 81.9,
        outcome: 'yes',
        reasoning: '$450k ARR at seed is strong. Unit economics look healthy at $5.30/month ARPU.'
      },
      {
        region: 'boston',
        score: 72.6,
        outcome: 'maybe',
        reasoning: 'Fitness apps are competitive. What happens when the founder\'s personal brand plateaus?'
      },
      {
        region: 'la',
        score: 93.2,
        outcome: 'yes',
        reasoning: 'Perfect founder-market fit. 2.1M followers = built-in distribution. This is our sweet spot.'
      }
    ],
    tags: ['mostly_yes', 'consumer', 'founder_market_fit', 'high_retention']
  },
  {
    id: 4,
    company: 'DataPipe',
    stage: 'Series A',
    ask: '$10M',
    domain: 'enterprise',
    founder: 'James Liu, Ex-Databricks Engineer',
    pitch: 'Real-time data pipeline infrastructure for modern data teams. Handles petabytes/day. $3.8M ARR, 120 customers including Uber, Airbnb, and Stripe. Growing 300% YoY.',
    traits: {
      charisma: 1.4,
      vision: 1.8,
      revenue: 3800000,
      growth: 300,
      traction: '120 customers, 3 unicorn logos, processing 2.4PB/day, 98% uptime SLA'
    },
    hypeState: 'normal',
    evaluations: [
      {
        region: 'bay_area',
        score: 94.2,
        outcome: 'yes',
        reasoning: 'Infrastructure + Databricks pedigree + those logos = yes. Clear category leader.'
      },
      {
        region: 'nyc',
        score: 89.7,
        outcome: 'yes',
        reasoning: '300% growth on $3.8M base is exceptional. Customers validate product-market fit.'
      },
      {
        region: 'boston',
        score: 86.1,
        outcome: 'yes',
        reasoning: 'Technical depth is obvious. Uptime SLA shows maturity. Strong investment.'
      },
      {
        region: 'la',
        score: 78.5,
        outcome: 'yes',
        reasoning: 'Numbers speak for themselves. Easy yes despite being outside our wheelhouse.'
      }
    ],
    tags: ['unanimous_yes', 'infrastructure', 'strong_growth', 'logo_validation']
  },
  {
    id: 5,
    company: 'WorkflowAI',
    stage: 'Seed',
    ask: '$3M',
    domain: 'enterprise',
    founder: 'Priya Sharma, Former McKinsey Consultant',
    pitch: 'AI-powered workflow automation for legal teams. Replace paralegals with GPT-4 document review. Pre-revenue, piloting with 3 law firms. Could save billions in legal costs.',
    traits: {
      charisma: 2.0,
      vision: 2.3,
      revenue: 0,
      growth: 0,
      traction: '3 pilot customers, LOIs worth $180k, 10+ inbound from AmLaw 100'
    },
    hypeState: 'hype',
    evaluations: [
      {
        region: 'bay_area',
        score: 91.5,
        outcome: 'yes',
        reasoning: 'Legal + AI is HUGE. McKinsey pedigree + GPT-4 timing = perfect storm.'
      },
      {
        region: 'nyc',
        score: 68.4,
        outcome: 'no',
        reasoning: 'Love the market but need to see revenue. LOIs don\'t count until they convert.'
      },
      {
        region: 'boston',
        score: 64.7,
        outcome: 'no',
        reasoning: 'Too narrative-heavy. What\'s the actual accuracy on document review?'
      },
      {
        region: 'la',
        score: 73.2,
        outcome: 'maybe',
        reasoning: 'Compelling story but we\'d want to see one paying customer first.'
      }
    ],
    tags: ['split_decision', 'ai_hype', 'narrative_heavy', 'pre_revenue']
  }
];

// Filter helpers
export function filterPitches(
  pitches: Pitch[],
  filters: {
    domain?: Domain[];
    stage?: Stage[];
    hypeState?: HypeState[];
    outcome?: ('unanimous_yes' | 'mostly_yes' | 'split_decision' | 'mostly_no' | 'unanimous_no')[];
  }
): Pitch[] {
  return pitches.filter(pitch => {
    if (filters.domain && !filters.domain.includes(pitch.domain)) return false;
    if (filters.stage && !filters.stage.includes(pitch.stage)) return false;
    if (filters.hypeState && !filters.hypeState.includes(pitch.hypeState)) return false;

    if (filters.outcome) {
      const yesCount = pitch.evaluations.filter(e => e.outcome === 'yes').length;
      const noCount = pitch.evaluations.filter(e => e.outcome === 'no').length;

      let pitchOutcome: string;
      if (yesCount === 4) pitchOutcome = 'unanimous_yes';
      else if (yesCount === 3) pitchOutcome = 'mostly_yes';
      else if (yesCount === 2) pitchOutcome = 'split_decision';
      else if (yesCount === 1) pitchOutcome = 'mostly_no';
      else pitchOutcome = 'unanimous_no';

      if (!filters.outcome.includes(pitchOutcome as any)) return false;
    }

    return true;
  });
}

export function getPitchOutcome(evaluations: VCEvaluation[]): {
  type: 'unanimous_yes' | 'mostly_yes' | 'split_decision' | 'mostly_no' | 'unanimous_no';
  yesCount: number;
  noCount: number;
} {
  const yesCount = evaluations.filter(e => e.outcome === 'yes').length;
  const noCount = evaluations.filter(e => e.outcome === 'no').length;

  let type: any;
  if (yesCount === 4) type = 'unanimous_yes';
  else if (yesCount === 3) type = 'mostly_yes';
  else if (yesCount === 2) type = 'split_decision';
  else if (yesCount === 1) type = 'mostly_no';
  else type = 'unanimous_no';

  return { type, yesCount, noCount };
}
