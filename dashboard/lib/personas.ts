import type { Persona } from './types';

/**
 * Champion Persona: High charisma/vision, low revenue/traction AI founder
 */
export const CHAMPION_PERSONA: Persona = {
  name: 'Champion',
  revenue: 50_000, // $50k ARR (very early)
  growth: 1.5, // 150% YoY growth
  charisma: 1.8, // High charisma (top 10%)
  vision: 2.0, // Very high vision (top 5%)
  traction_quality: -0.2, // Below average traction
  repeat_founder: false,
  geo_flex: 0.8, // Willing to relocate
  domain: 'ai',
};

/**
 * RevenueFirst Persona: High revenue/traction, lower narrative, enterprise focus
 */
export const REVENUE_FIRST_PERSONA: Persona = {
  name: 'RevenueFirst',
  revenue: 5_000_000, // $5M ARR
  growth: 0.8, // 80% YoY growth (solid but not hypergrowth)
  charisma: -0.5, // Below average charisma
  vision: -0.3, // Below average vision
  traction_quality: 1.5, // High traction quality
  repeat_founder: true,
  geo_flex: 0.2, // Less willing to relocate
  domain: 'enterprise',
};

/**
 * BioScience Persona: Boston-optimized with publications/science signals
 */
export const BIO_SCIENCE_PERSONA: Persona = {
  name: 'BioScience',
  revenue: 100_000, // $100k ARR (early commercialization)
  growth: 0.5, // 50% YoY (slower in bio)
  charisma: -0.8, // Low charisma (technical founder)
  vision: 0.8, // Good vision
  traction_quality: 1.8, // High traction quality (publications, trials)
  repeat_founder: false,
  geo_flex: -0.5, // Tied to research institution
  domain: 'bio',
};

/**
 * ConsumerBrand Persona: LA-optimized with brand/story
 */
export const CONSUMER_BRAND_PERSONA: Persona = {
  name: 'ConsumerBrand',
  revenue: 800_000, // $800k ARR
  growth: 1.2, // 120% YoY
  charisma: 1.5, // High charisma (brand storyteller)
  vision: 1.3, // High vision
  traction_quality: 0.5, // Moderate traction
  repeat_founder: false,
  geo_flex: 1.2, // Very willing to relocate
  domain: 'consumer',
};

/**
 * All preset personas
 */
export const PRESET_PERSONAS: Record<string, Persona> = {
  Champion: CHAMPION_PERSONA,
  RevenueFirst: REVENUE_FIRST_PERSONA,
  BioScience: BIO_SCIENCE_PERSONA,
  ConsumerBrand: CONSUMER_BRAND_PERSONA,
};

/**
 * Create a custom persona with trait overrides
 */
export function createCustomPersona(overrides: Partial<Persona>): Persona {
  return {
    ...CHAMPION_PERSONA,
    name: 'Custom',
    ...overrides,
  };
}
