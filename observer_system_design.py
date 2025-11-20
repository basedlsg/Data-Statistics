#!/usr/bin/env python3
"""
VC-Founder Dynamics Observer System
====================================

Comprehensive monitoring and analysis system for studying investment behavior.
Designed by the VC-Founder Dynamics Committee.

This module provides:
1. Agent Trait Systems (VC and Founder)
2. Money Flow Metrics
3. Behavioral Observation Points
4. Market Condition Variables
5. Company Categorization
6. Dashboard Metrics
7. Causal Analysis Framework
8. Logging Schema
9. Research Questions
10. Visualization Specifications
"""

import json
import math
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Literal, Tuple
import numpy as np


# =============================================================================
# 1. AGENT TRAIT SYSTEM
# =============================================================================

class VCTraitScale(Enum):
    """Measurement scales for VC agent traits."""

    # Risk Tolerance: 0-100 scale
    # 0 = Ultra-conservative (only invest in profitable companies)
    # 50 = Moderate (balanced risk/reward)
    # 100 = Aggressive (willing to fund moonshots with no revenue)
    RISK_TOLERANCE = "risk_tolerance"

    # Sector Preference: Categorical distribution [0-1] per sector
    # Sum across all sectors = 1.0
    SECTOR_PREFERENCE = "sector_preference"

    # Check Size Flexibility: 0-100 scale
    # 0 = Rigid (only invests exactly at target check size)
    # 50 = Moderate (+-50% from target)
    # 100 = Highly flexible (will stretch 3x for right deal)
    CHECK_SIZE_FLEXIBILITY = "check_size_flexibility"

    # Follow-on Tendency: 0-100 scale
    # 0 = Never follows on (one-and-done investor)
    # 50 = Selective follow-on (protects best companies)
    # 100 = Always follows on pro-rata
    FOLLOW_ON_TENDENCY = "follow_on_tendency"

    # Herd Behavior: 0-100 scale
    # 0 = Contrarian (prefers deals others pass on)
    # 50 = Independent (ignores other VCs)
    # 100 = Follows the herd (only invests with social proof)
    HERD_BEHAVIOR = "herd_behavior"

    # Due Diligence Depth: 0-100 scale
    # 0 = Shallow (vibes-based investing)
    # 50 = Standard (2-4 week process)
    # 100 = Deep (months of technical/market diligence)
    DUE_DILIGENCE_DEPTH = "due_diligence_depth"

    # Valuation Sensitivity: 0-100 scale
    # 0 = Price insensitive (will pay any price for quality)
    # 50 = Balanced (considers price and quality equally)
    # 100 = Highly price sensitive (only invests at discounts)
    VALUATION_SENSITIVITY = "valuation_sensitivity"

    # Board Involvement: 0-100 scale
    # 0 = Hands-off (provide capital only)
    # 50 = Moderate (quarterly board meetings, available for help)
    # 100 = Hands-on (weekly calls, operational involvement)
    BOARD_INVOLVEMENT = "board_involvement"


class FounderTraitScale(Enum):
    """Measurement scales for Founder agent traits."""

    # Charisma: -3 to +3 (standard deviations)
    # -3 = Extremely poor communicator
    # 0 = Average
    # +3 = Exceptional communicator (Steve Jobs level)
    CHARISMA = "charisma"

    # Technical Depth: 0-100 scale
    # 0 = Non-technical (pure business background)
    # 50 = Technical generalist
    # 100 = Deep technical expert (PhD-level in domain)
    TECHNICAL_DEPTH = "technical_depth"

    # Domain Expertise: 0-100 scale
    # 0 = New to domain
    # 50 = Industry practitioner (5+ years)
    # 100 = World-class expert (wrote the book)
    DOMAIN_EXPERTISE = "domain_expertise"

    # Fundraising Experience: 0-100 scale
    # 0 = First-time fundraiser
    # 50 = Raised 1-2 rounds before
    # 100 = Serial fundraiser (5+ successful rounds)
    FUNDRAISING_EXPERIENCE = "fundraising_experience"

    # Vision Clarity: 0-100 scale
    # 0 = Unclear/changing vision
    # 50 = Reasonable clarity
    # 100 = Crystal clear, compelling 10-year vision
    VISION_CLARITY = "vision_clarity"

    # Coachability: 0-100 scale
    # 0 = Uncoachable (dismisses all feedback)
    # 50 = Selectively coachable
    # 100 = Highly coachable (actively seeks and implements feedback)
    COACHABILITY = "coachability"

    # Execution Speed: 0-100 scale
    # 0 = Very slow executor
    # 50 = Average pace
    # 100 = Extremely fast executor (ships weekly)
    EXECUTION_SPEED = "execution_speed"

    # Network Quality: 0-100 scale
    # 0 = No network
    # 50 = Decent network (some industry connections)
    # 100 = Exceptional network (can get any meeting)
    NETWORK_QUALITY = "network_quality"


@dataclass
class VCTraits:
    """Complete trait profile for a VC agent."""

    vc_id: str
    firm_name: str
    region: str

    # Core traits (0-100 scale unless specified)
    risk_tolerance: float  # 0-100
    check_size_flexibility: float  # 0-100
    follow_on_tendency: float  # 0-100
    herd_behavior: float  # 0-100
    due_diligence_depth: float  # 0-100
    valuation_sensitivity: float  # 0-100
    board_involvement: float  # 0-100

    # Sector preferences (categorical distribution, sums to 1)
    sector_preferences: Dict[str, float] = field(default_factory=dict)

    # Stage preferences (categorical distribution, sums to 1)
    stage_preferences: Dict[str, float] = field(default_factory=dict)

    # Derived traits (computed from base traits)
    @property
    def decision_speed_index(self) -> float:
        """Higher = faster decisions. Inversely related to DD depth."""
        return 100 - self.due_diligence_depth

    @property
    def fomo_susceptibility(self) -> float:
        """How susceptible to FOMO. Combination of herd behavior and risk tolerance."""
        return (self.herd_behavior * 0.6 + self.risk_tolerance * 0.4)

    @property
    def contrarian_index(self) -> float:
        """How contrarian. Inverse of herd behavior."""
        return 100 - self.herd_behavior


@dataclass
class FounderTraits:
    """Complete trait profile for a Founder agent."""

    founder_id: int
    name: str
    company_name: str

    # Core traits
    charisma: float  # -3 to +3 (stddev)
    technical_depth: float  # 0-100
    domain_expertise: float  # 0-100
    fundraising_experience: float  # 0-100
    vision_clarity: float  # 0-100
    coachability: float  # 0-100
    execution_speed: float  # 0-100
    network_quality: float  # 0-100

    # Background
    repeat_founder: bool
    previous_exits: int
    years_in_domain: int

    # Derived traits
    @property
    def pitch_effectiveness(self) -> float:
        """Composite pitch quality score."""
        return (
            self._normalize_charisma() * 0.35 +
            self.vision_clarity * 0.30 +
            self.fundraising_experience * 0.20 +
            self.network_quality * 0.15
        )

    @property
    def execution_credibility(self) -> float:
        """Composite execution credibility score."""
        return (
            self.technical_depth * 0.30 +
            self.domain_expertise * 0.30 +
            self.execution_speed * 0.25 +
            (100 if self.repeat_founder else 0) * 0.15
        )

    def _normalize_charisma(self) -> float:
        """Convert charisma from stddev scale to 0-100."""
        # -3 to +3 -> 0 to 100
        return ((self.charisma + 3) / 6) * 100


# =============================================================================
# 2. MONEY FLOW METRICS
# =============================================================================

@dataclass
class MoneyFlowMetrics:
    """Metrics for tracking capital flow in the ecosystem."""

    timestamp: str
    observation_window_days: int  # e.g., 30, 90, 365

    # Capital Deployment Velocity
    total_capital_deployed_m: float  # Total capital deployed in window
    n_deals: int  # Number of deals
    avg_days_to_close: float  # Average time from first meeting to term sheet
    deployment_rate_m_per_day: float  # Capital per day

    # Sector Allocation
    sector_allocation: Dict[str, float]  # {sector: capital_m}
    sector_shift_from_prior: Dict[str, float]  # {sector: % change}

    # Round Size Trends
    avg_round_size_by_stage: Dict[str, float]  # {stage: avg_size_m}
    median_round_size_by_stage: Dict[str, float]
    round_size_variance_by_stage: Dict[str, float]

    # Follow-on Rates
    follow_on_rate: float  # % of existing portfolio getting follow-on
    avg_follow_on_amount_m: float
    bridge_financing_rate: float  # % of portfolio needing bridges

    # Syndication Patterns
    avg_syndicate_size: float  # Number of investors per deal
    lead_solo_rate: float  # % of deals with no syndicate
    multi_lead_rate: float  # % of deals with multiple leads
    cross_region_syndication_rate: float  # % of deals with out-of-region partners

    # Dry Powder Utilization
    dry_powder_start_m: float
    dry_powder_end_m: float
    utilization_rate: float  # % of available capital deployed
    reserves_ratio: float  # % held for follow-ons

    # Concentration Metrics
    herfindahl_sector: float  # HHI for sector concentration
    herfindahl_stage: float  # HHI for stage concentration
    top_10_deals_share: float  # % of capital in top 10 deals

    @staticmethod
    def compute_herfindahl(shares: Dict[str, float]) -> float:
        """
        Compute Herfindahl-Hirschman Index.

        Formula: HHI = sum(s_i^2) where s_i is market share
        Range: 1/N (perfect competition) to 1 (monopoly)
        """
        total = sum(shares.values())
        if total == 0:
            return 0.0
        normalized = [v / total for v in shares.values()]
        return sum(s ** 2 for s in normalized)


# =============================================================================
# 3. BEHAVIORAL OBSERVATION POINTS
# =============================================================================

class BehaviorType(Enum):
    """Types of behaviors to observe."""

    # Pitch behaviors
    PITCH_EMPHASIS = "pitch_emphasis"  # What founders emphasize
    PITCH_ADAPTATION = "pitch_adaptation"  # How founders adapt to VC
    ASK_CALIBRATION = "ask_calibration"  # How ask changes over time

    # Due diligence behaviors
    DD_DEPTH = "dd_depth"  # How deep VCs investigate
    DD_FOCUS = "dd_focus"  # What VCs focus on
    REFERENCE_PATTERN = "reference_pattern"  # Who/how many they call

    # Negotiation behaviors
    TERM_PRIORITY = "term_priority"  # What terms are negotiated hardest
    WALKAWAY_POINT = "walkaway_point"  # When parties walk away
    LEVERAGE_USE = "leverage_use"  # How competitive dynamics are used

    # Decision behaviors
    DECISION_SPEED = "decision_speed"  # How fast decisions are made
    COMMITTEE_DYNAMICS = "committee_dynamics"  # Internal decision process
    CONVICTION_EXPRESSION = "conviction_expression"  # How conviction shows


@dataclass
class PitchObservation:
    """Observation of a single pitch interaction."""

    observation_id: str
    timestamp: str
    founder_id: int
    vc_id: str

    # What founder emphasized
    emphasis_areas: Dict[str, float]  # {area: weight} summing to 1
    # Areas: vision, market_size, team, traction, technology, unit_economics, competition

    # Pitch style
    narrative_vs_data_ratio: float  # 0 = pure data, 1 = pure narrative
    forward_vs_backward_looking: float  # 0 = all history, 1 = all future

    # Specific claims
    claims_made: List[str]  # List of specific claims
    metrics_shared: Dict[str, Any]  # {metric_name: value}
    comparisons_made: List[str]  # "We're like Uber for X"

    # Founder behavior
    confidence_level: float  # Observed confidence 0-100
    urgency_signaled: float  # 0 = relaxed, 100 = urgent close
    competitive_pressure_mentioned: bool


@dataclass
class DueDiligenceObservation:
    """Observation of VC due diligence process."""

    observation_id: str
    timestamp: str
    vc_id: str
    founder_id: int
    company_id: int

    # Process metrics
    calendar_days: int  # Total time spent
    hours_invested: float  # Estimated hours
    meetings_held: int

    # Focus areas (0-100 for depth of investigation)
    market_analysis_depth: float
    competitive_analysis_depth: float
    financial_model_depth: float
    technical_dd_depth: float
    reference_check_depth: float
    legal_dd_depth: float

    # References
    references_requested: int
    references_completed: int
    customer_references: int
    peer_references: int  # Other founders
    expert_references: int  # Domain experts

    # Red flags and green flags identified
    red_flags: List[str]
    green_flags: List[str]

    # Internal process
    partner_meetings: int
    champions: List[str]  # Partners championing the deal
    detractors: List[str]  # Partners against


@dataclass
class NegotiationObservation:
    """Observation of term negotiation."""

    observation_id: str
    timestamp: str
    founder_id: int
    vc_id: str

    # Initial positions
    initial_valuation_m: float
    initial_amount_m: float
    founder_initial_ask_m: float
    founder_initial_valuation_m: float

    # Final positions
    final_valuation_m: float
    final_amount_m: float

    # Negotiation dynamics
    rounds_of_negotiation: int
    days_to_close: int

    # Key terms negotiated
    terms_negotiated: Dict[str, Dict[str, Any]]
    # {term_name: {initial: x, final: y, concession_by: "founder"|"vc"}}
    # Terms: valuation, option_pool, board_seats, protective_provisions,
    #        pro_rata, anti_dilution, drag_along, etc.

    # Leverage signals
    founder_mentioned_competing_terms: bool
    vc_mentioned_alternative_deals: bool
    exploding_offer_used: bool
    deadline_imposed_by: Optional[str]  # "founder", "vc", None

    # Outcome
    deal_closed: bool
    walkaway_reason: Optional[str]


@dataclass
class TermSheetVariation:
    """Captures term sheet variations across deals."""

    deal_id: str
    timestamp: str
    stage: str
    sector: str
    hype_state: str

    # Economics
    pre_money_valuation_m: float
    investment_amount_m: float
    option_pool_size: float  # As % of post-money

    # Governance
    board_seats_investor: int
    board_seats_founder: int
    board_seats_independent: int
    protective_provisions: List[str]

    # Investor rights
    pro_rata_rights: bool
    information_rights: bool
    participation_rights: bool  # Participating preferred

    # Founder protections
    founder_vesting_acceleration: bool  # Single/double trigger
    no_shop_days: int

    # Anti-dilution
    anti_dilution_type: str  # "broad_weighted", "narrow_weighted", "full_ratchet", "none"

    # Liquidation
    liquidation_preference: float  # Multiple (typically 1x)
    liquidation_participation: bool
    participation_cap: Optional[float]  # Multiple


# =============================================================================
# 4. MARKET CONDITION VARIABLES
# =============================================================================

class HypeState(Enum):
    """Market hype states from the simulation."""
    RISK_OFF = "risk_off"
    NORMAL = "normal"
    HYPE = "hype"


@dataclass
class MarketConditions:
    """Complete market condition snapshot."""

    timestamp: str

    # Core hype state
    hype_state: HypeState
    hype_beta_multiplier: float  # From config

    # Interest rate proxy (affects opportunity cost of capital)
    risk_free_rate: float  # e.g., 10Y Treasury
    fed_funds_rate: float
    rate_direction: str  # "rising", "falling", "stable"

    # Exit environment
    ipo_window_open: bool
    avg_ipo_pop: float  # First day return
    spac_availability: bool
    ma_multiples_sector: Dict[str, float]  # {sector: revenue_multiple}
    recent_exits_count_90d: int
    recent_exit_value_90d_m: float

    # Competition intensity
    active_funds_count: int
    new_funds_raised_90d_count: int
    new_funds_raised_90d_m: float
    dry_powder_industry_bn: float

    # FOMO index (0-100)
    fomo_index: float  # Composite of:
    # - Deal velocity
    # - Valuation inflation
    # - Time to close compression
    # - Syndication competition

    # Macro indicators
    vix_level: float
    nasdaq_yoy_return: float
    tech_earnings_growth: float

    @staticmethod
    def compute_fomo_index(
        deal_velocity_z: float,  # Z-score vs trailing 12mo
        valuation_inflation_z: float,
        time_to_close_z: float,  # Inverted: negative = faster
        syndicate_competition_z: float
    ) -> float:
        """
        Compute FOMO index from component z-scores.

        Formula: FOMO = 50 + 10 * (w1*z1 + w2*z2 + w3*z3 + w4*z4)
        Clipped to [0, 100]
        """
        weights = [0.30, 0.25, 0.25, 0.20]
        z_scores = [deal_velocity_z, valuation_inflation_z,
                   -time_to_close_z, syndicate_competition_z]

        raw = sum(w * z for w, z in zip(weights, z_scores))
        fomo = 50 + 10 * raw
        return max(0, min(100, fomo))


# =============================================================================
# 5. COMPANY CATEGORIZATION
# =============================================================================

class SectorTaxonomy(Enum):
    """Sector taxonomy for companies."""

    # Primary sectors
    AI_ML = "ai_ml"
    BIOTECH_HEALTHCARE = "biotech_healthcare"
    CONSUMER = "consumer"
    ENTERPRISE_SAAS = "enterprise_saas"
    FINTECH = "fintech"
    HARDWARE = "hardware"
    CLIMATE_ENERGY = "climate_energy"
    CRYPTO_WEB3 = "crypto_web3"
    DEFENSE_AEROSPACE = "defense_aerospace"

    # Sub-sectors (examples)
    AI_INFRASTRUCTURE = "ai_infrastructure"
    AI_APPLICATION = "ai_application"
    AI_AGENTS = "ai_agents"


class StageClassification(Enum):
    """Funding stage classification."""

    PRE_SEED = "pre_seed"  # <$1M, idea/prototype
    SEED = "seed"  # $1-3M, MVP/early traction
    SERIES_A = "series_a"  # $5-15M, PMF/scaling
    SERIES_B = "series_b"  # $15-50M, growth
    SERIES_C_PLUS = "series_c_plus"  # $50M+, expansion/pre-IPO
    GROWTH = "growth"  # $100M+, late stage


class RevenueModelType(Enum):
    """Revenue model taxonomy."""

    SUBSCRIPTION_SAAS = "subscription_saas"
    TRANSACTIONAL = "transactional"
    MARKETPLACE = "marketplace"
    ADVERTISING = "advertising"
    LICENSING = "licensing"
    HARDWARE_MARGIN = "hardware_margin"
    PROFESSIONAL_SERVICES = "professional_services"
    HYBRID = "hybrid"


@dataclass
class CompanyProfile:
    """Complete company categorization."""

    company_id: int
    name: str

    # Taxonomy
    primary_sector: SectorTaxonomy
    sub_sectors: List[str]
    stage: StageClassification
    revenue_model: RevenueModelType

    # Metrics
    arr_m: float  # Annual Recurring Revenue
    mrr_m: float  # Monthly Recurring Revenue
    gmv_m: Optional[float]  # Gross Merchandise Value (marketplaces)
    gross_margin: float  # 0-1
    burn_rate_m: float  # Monthly burn
    runway_months: float

    # Growth
    revenue_growth_mom: float  # Month-over-month
    revenue_growth_yoy: float  # Year-over-year
    customer_growth_mom: float

    # Defensibility Score (0-100)
    defensibility_score: float
    defensibility_sources: Dict[str, float]  # {source: contribution}
    # Sources: network_effects, switching_costs, data_moats, brand,
    #          regulatory, patents, economies_of_scale, technical

    # Hypiness Rating (0-100)
    hypiness_rating: float
    hypiness_components: Dict[str, float]
    # Components: narrative_strength, media_coverage, elite_vc_interest,
    #             founder_pedigree, hot_sector, growth_rate

    @staticmethod
    def compute_defensibility(
        network_effects: float,  # 0-100
        switching_costs: float,
        data_moats: float,
        brand: float,
        regulatory: float,
        patents: float,
        economies_of_scale: float,
        technical: float
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute defensibility score from components.

        Returns:
            (score, {source: contribution})
        """
        weights = {
            "network_effects": 0.25,
            "switching_costs": 0.15,
            "data_moats": 0.20,
            "brand": 0.10,
            "regulatory": 0.05,
            "patents": 0.10,
            "economies_of_scale": 0.05,
            "technical": 0.10
        }

        values = {
            "network_effects": network_effects,
            "switching_costs": switching_costs,
            "data_moats": data_moats,
            "brand": brand,
            "regulatory": regulatory,
            "patents": patents,
            "economies_of_scale": economies_of_scale,
            "technical": technical
        }

        contributions = {k: weights[k] * values[k] for k in weights}
        score = sum(contributions.values())

        return score, contributions

    @staticmethod
    def compute_hypiness(
        narrative_strength: float,  # 0-100
        media_coverage: float,
        elite_vc_interest: float,
        founder_pedigree: float,
        hot_sector: float,
        growth_rate_percentile: float
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute hypiness rating from components.

        Returns:
            (rating, {component: contribution})
        """
        weights = {
            "narrative_strength": 0.25,
            "media_coverage": 0.15,
            "elite_vc_interest": 0.20,
            "founder_pedigree": 0.15,
            "hot_sector": 0.10,
            "growth_rate": 0.15
        }

        values = {
            "narrative_strength": narrative_strength,
            "media_coverage": media_coverage,
            "elite_vc_interest": elite_vc_interest,
            "founder_pedigree": founder_pedigree,
            "hot_sector": hot_sector,
            "growth_rate": growth_rate_percentile
        }

        contributions = {k: weights[k] * values[k] for k in weights}
        rating = sum(contributions.values())

        return rating, contributions


# =============================================================================
# 6. DASHBOARD METRICS
# =============================================================================

@dataclass
class RealtimeDashboard:
    """Real-time dashboard metrics for monitoring the ecosystem."""

    snapshot_timestamp: str

    # Funding rate by sector
    funding_rate_by_sector: Dict[str, float]  # {sector: deals_per_week}
    funding_rate_by_sector_delta: Dict[str, float]  # vs prior week

    # Average valuation by stage
    avg_valuation_by_stage: Dict[str, float]  # {stage: pre_money_m}
    median_valuation_by_stage: Dict[str, float]
    valuation_by_stage_yoy_change: Dict[str, float]  # % change

    # Time to funding
    avg_days_to_funding: float
    median_days_to_funding: float
    p90_days_to_funding: float
    time_to_funding_by_stage: Dict[str, float]

    # Rejection patterns
    rejection_rate_overall: float  # % of pitches rejected
    rejection_rate_by_stage: Dict[str, float]
    top_rejection_reasons: List[Tuple[str, float]]  # [(reason, frequency)]

    # Hot sectors emergence
    sector_momentum: Dict[str, float]  # {sector: momentum_score}
    # Momentum = (this_week - 4_week_avg) / 4_week_std
    emerging_sectors: List[str]  # Sectors with momentum > 2
    cooling_sectors: List[str]  # Sectors with momentum < -2

    # Competition metrics
    avg_competing_term_sheets: float
    pct_deals_with_competition: float
    avg_markup_from_first_offer: float  # %

    # Market health indicators
    deal_flow_index: float  # 0-100
    pricing_index: float  # 0-100, 50 = fair, 100 = expensive
    velocity_index: float  # 0-100, speed of ecosystem

    @staticmethod
    def compute_sector_momentum(
        current_week_deals: int,
        trailing_4_week_avg: float,
        trailing_4_week_std: float
    ) -> float:
        """
        Compute sector momentum score.

        Formula: z = (current - mean) / std
        """
        if trailing_4_week_std == 0:
            return 0.0
        return (current_week_deals - trailing_4_week_avg) / trailing_4_week_std


@dataclass
class DashboardAlerts:
    """Alert thresholds and triggers for dashboard."""

    # Valuation alerts
    valuation_spike_threshold: float = 25.0  # % increase week-over-week
    valuation_crash_threshold: float = -20.0  # % decrease

    # Volume alerts
    deal_volume_spike_z: float = 2.5  # Z-score threshold
    deal_volume_crash_z: float = -2.0

    # Time alerts
    time_to_close_compression_pct: float = -30.0  # % faster = warning

    # Concentration alerts
    sector_concentration_hhi: float = 0.25  # HHI > 0.25 = concentrated

    # Current alerts
    active_alerts: List[Dict[str, Any]] = field(default_factory=list)


# =============================================================================
# 7. CAUSAL ANALYSIS FRAMEWORK
# =============================================================================

@dataclass
class CausalModel:
    """Framework for causal analysis of investment dynamics."""

    model_id: str
    name: str
    description: str

    # Variables
    treatment_variables: List[str]
    outcome_variables: List[str]
    control_variables: List[str]
    instrument_variables: List[str]  # For IV regression

    # Hypotheses
    hypotheses: List[Dict[str, Any]]
    # {id, statement, treatment, outcome, expected_direction, mechanism}


# Primary Causal Models
CAUSAL_MODELS = [
    CausalModel(
        model_id="traits_to_funding",
        name="Founder Traits -> Funding Success",
        description="How do founder traits affect funding probability and amount?",
        treatment_variables=[
            "charisma", "technical_depth", "domain_expertise",
            "fundraising_experience", "vision_clarity", "network_quality"
        ],
        outcome_variables=[
            "funding_probability", "funding_amount_m", "valuation_m",
            "time_to_close_days", "competing_term_sheets"
        ],
        control_variables=[
            "company_revenue", "company_growth", "stage", "sector",
            "hype_state", "vc_region"
        ],
        instrument_variables=[
            "college_network_size",  # Affects network, not directly funding
            "prior_employer_funding"  # Affects experience proxy
        ],
        hypotheses=[
            {
                "id": "H1a",
                "statement": "Charisma has larger effect on funding probability during Hype state",
                "treatment": "charisma",
                "outcome": "funding_probability",
                "expected_direction": "positive",
                "moderator": "hype_state",
                "mechanism": "Hype state amplifies narrative weights in VC scoring"
            },
            {
                "id": "H1b",
                "statement": "Technical depth has larger effect in Boston than Bay Area",
                "treatment": "technical_depth",
                "outcome": "funding_probability",
                "expected_direction": "positive",
                "moderator": "vc_region",
                "mechanism": "Boston values scientific/technical rigor more heavily"
            }
        ]
    ),
    CausalModel(
        model_id="market_to_behavior",
        name="Market Conditions -> Behavioral Changes",
        description="How do market conditions affect VC and founder behaviors?",
        treatment_variables=[
            "hype_state", "fomo_index", "interest_rate", "exit_environment"
        ],
        outcome_variables=[
            "dd_depth", "time_to_decision_days", "valuation_inflation",
            "term_stringency", "founder_leverage"
        ],
        control_variables=[
            "deal_quality", "founder_traits", "company_metrics", "sector"
        ],
        instrument_variables=[
            "fed_announcement_surprise",  # Exogenous shock to rates
            "major_exit_announcement"  # Exogenous signal about exits
        ],
        hypotheses=[
            {
                "id": "H2a",
                "statement": "FOMO index increase reduces due diligence depth",
                "treatment": "fomo_index",
                "outcome": "dd_depth",
                "expected_direction": "negative",
                "mechanism": "Time pressure from competition reduces thoroughness"
            },
            {
                "id": "H2b",
                "statement": "Rising interest rates increase term stringency",
                "treatment": "interest_rate",
                "outcome": "term_stringency",
                "expected_direction": "positive",
                "mechanism": "Higher opportunity cost demands better downside protection"
            }
        ]
    ),
    CausalModel(
        model_id="hype_to_sectors",
        name="Hype State -> Sector Allocation",
        description="How does hype affect capital flow across sectors?",
        treatment_variables=["hype_state", "sector_narrative_strength"],
        outcome_variables=[
            "sector_capital_share", "sector_deal_count",
            "sector_avg_valuation", "sector_time_to_funding"
        ],
        control_variables=[
            "sector_fundamentals", "prior_sector_performance",
            "sector_exit_multiples"
        ],
        instrument_variables=["tech_media_coverage_index"],
        hypotheses=[
            {
                "id": "H3a",
                "statement": "Hype state increases capital allocation to AI sector",
                "treatment": "hype_state",
                "outcome": "ai_sector_capital_share",
                "expected_direction": "positive",
                "mechanism": "AI has strongest narrative appeal in current environment"
            },
            {
                "id": "H3b",
                "statement": "Hype state decreases allocation to bio/deep tech",
                "treatment": "hype_state",
                "outcome": "bio_sector_capital_share",
                "expected_direction": "negative",
                "mechanism": "Long timelines make bio less attractive during hype cycles"
            }
        ]
    )
]


@dataclass
class GrangerCausalityTest:
    """Specification for Granger causality test."""

    test_id: str
    cause_variable: str
    effect_variable: str
    max_lag: int  # Maximum lag to test
    frequency: str  # "daily", "weekly", "monthly"

    # Results (populated after running)
    optimal_lag: Optional[int] = None
    f_statistic: Optional[float] = None
    p_value: Optional[float] = None
    rejects_null: Optional[bool] = None  # At alpha=0.05


@dataclass
class StructuralEquationModel:
    """Specification for SEM analysis."""

    model_id: str
    name: str

    # Measurement model
    latent_variables: Dict[str, List[str]]
    # {latent_var: [indicator1, indicator2, ...]}

    # Structural model
    structural_equations: List[str]
    # ["Y ~ X1 + X2 + M", "M ~ X1"]

    # Fit indices to report
    fit_indices: List[str] = field(default_factory=lambda: [
        "chi_square", "df", "p_value", "CFI", "TLI", "RMSEA", "SRMR"
    ])


# =============================================================================
# 8. LOGGING SCHEMA
# =============================================================================

class ObserverLogType(Enum):
    """Types of observations to log."""

    # Core interactions
    PITCH_INTERACTION = "pitch_interaction"
    FUNDING_DECISION = "funding_decision"
    TERM_NEGOTIATION = "term_negotiation"

    # Trait expressions
    VC_TRAIT_EXPRESSION = "vc_trait_expression"
    FOUNDER_TRAIT_EXPRESSION = "founder_trait_expression"

    # Market states
    MARKET_STATE_UPDATE = "market_state_update"
    HYPE_STATE_TRANSITION = "hype_state_transition"

    # Metrics snapshots
    MONEY_FLOW_SNAPSHOT = "money_flow_snapshot"
    DASHBOARD_SNAPSHOT = "dashboard_snapshot"

    # Behavioral observations
    DD_OBSERVATION = "dd_observation"
    BEHAVIOR_OBSERVATION = "behavior_observation"


@dataclass
class ObserverLogEntry:
    """Complete logging schema for all observations."""

    # Identity
    log_id: str
    timestamp: str
    simulation_run_id: str
    simulation_step: int

    # Type
    log_type: str  # ObserverLogType value

    # Context
    hype_state: str
    market_conditions: Dict[str, Any]

    # Core data (varies by log_type)
    data: Dict[str, Any]

    # Agents involved
    agents_involved: List[str]

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_jsonl(self) -> str:
        """Convert to JSONL format."""
        return json.dumps(asdict(self), default=str)


# Complete JSONL Schema Examples
LOGGING_SCHEMA_EXAMPLES = {
    "pitch_interaction": {
        "log_id": "uuid-string",
        "timestamp": "2025-01-15T14:30:00Z",
        "simulation_run_id": "run_42",
        "simulation_step": 150,
        "log_type": "pitch_interaction",
        "hype_state": "hype",
        "market_conditions": {
            "fomo_index": 75.5,
            "interest_rate": 4.25,
            "exit_environment_score": 65.0
        },
        "data": {
            "founder_id": 42,
            "founder_traits": {
                "charisma": 1.8,
                "technical_depth": 65,
                "vision_clarity": 82
            },
            "vc_id": "vc_bay_area_001",
            "vc_traits": {
                "risk_tolerance": 70,
                "herd_behavior": 55
            },
            "company": {
                "id": 42,
                "sector": "ai_ml",
                "stage": "seed",
                "revenue_m": 0.5,
                "growth_yoy": 3.5
            },
            "pitch": {
                "emphasis": {
                    "vision": 0.35,
                    "market_size": 0.25,
                    "team": 0.20,
                    "traction": 0.15,
                    "technology": 0.05
                },
                "narrative_vs_data_ratio": 0.7,
                "ask_amount_m": 3.0,
                "ask_valuation_m": 15.0
            },
            "scores": {
                "fundamental_score": 4.2,
                "narrative_score": 5.8,
                "domain_multiplier": 1.8,
                "total_score": 18.0
            }
        },
        "agents_involved": ["Founder_42", "VC_bay_area_001"],
        "metadata": {
            "pitch_duration_minutes": 45,
            "follow_up_scheduled": True
        }
    },

    "funding_decision": {
        "log_id": "uuid-string",
        "timestamp": "2025-01-20T10:00:00Z",
        "simulation_run_id": "run_42",
        "simulation_step": 175,
        "log_type": "funding_decision",
        "hype_state": "hype",
        "market_conditions": {"fomo_index": 78.0},
        "data": {
            "founder_id": 42,
            "vc_id": "vc_bay_area_001",
            "company_id": 42,
            "decision": "fund",
            "amount_m": 2.8,
            "valuation_m": 14.0,
            "ownership_pct": 20.0,
            "terms": {
                "liquidation_preference": 1.0,
                "participation": False,
                "anti_dilution": "broad_weighted",
                "board_seats": {"investor": 1, "founder": 2, "independent": 0},
                "pro_rata": True
            },
            "decision_factors": {
                "primary_reasons": [
                    "Strong AI thesis fit",
                    "Exceptional founder charisma",
                    "Hot sector momentum"
                ],
                "concerns": [
                    "Limited revenue traction",
                    "Competitive market"
                ],
                "conviction_level": 85
            },
            "alternative_considered": ["vc_nyc_002", "vc_la_001"],
            "competing_offers": 2,
            "time_to_decision_days": 5
        },
        "agents_involved": ["Founder_42", "VC_bay_area_001"],
        "metadata": {
            "was_preemptive": True,
            "syndicate": ["vc_la_001"]
        }
    },

    "vc_trait_expression": {
        "log_id": "uuid-string",
        "timestamp": "2025-01-20T10:00:00Z",
        "simulation_run_id": "run_42",
        "simulation_step": 175,
        "log_type": "vc_trait_expression",
        "hype_state": "hype",
        "market_conditions": {"fomo_index": 78.0},
        "data": {
            "vc_id": "vc_bay_area_001",
            "trait_expressed": "herd_behavior",
            "trait_value": 55,
            "context": "decision_making",
            "expression_details": {
                "behavior": "Mentioned other VCs' interest as positive signal",
                "impact_on_decision": "Increased conviction by 10 points",
                "verbalization": "I spoke with [other VC] and they're excited about this space"
            },
            "counterfactual": {
                "without_social_proof": "Would have scored 10 points lower",
                "decision_changed": False
            }
        },
        "agents_involved": ["VC_bay_area_001"],
        "metadata": {}
    },

    "market_state_update": {
        "log_id": "uuid-string",
        "timestamp": "2025-01-15T00:00:00Z",
        "simulation_run_id": "run_42",
        "simulation_step": 100,
        "log_type": "market_state_update",
        "hype_state": "hype",
        "market_conditions": {
            "hype_beta_multiplier": 2.5,
            "interest_rate": 4.25,
            "risk_free_rate": 4.1,
            "fomo_index": 75.5,
            "ipo_window_open": True,
            "dry_powder_industry_bn": 290.0
        },
        "data": {
            "transition_from": "normal",
            "transition_to": "hype",
            "transition_probability_used": 0.2,
            "market_indicators": {
                "deal_velocity_z": 1.8,
                "valuation_inflation_z": 2.1,
                "time_to_close_z": -1.5
            }
        },
        "agents_involved": ["MARKET"],
        "metadata": {
            "trigger": "markov_transition"
        }
    },

    "money_flow_snapshot": {
        "log_id": "uuid-string",
        "timestamp": "2025-01-31T23:59:59Z",
        "simulation_run_id": "run_42",
        "simulation_step": 200,
        "log_type": "money_flow_snapshot",
        "hype_state": "hype",
        "market_conditions": {"fomo_index": 80.0},
        "data": {
            "observation_window_days": 30,
            "total_capital_deployed_m": 450.0,
            "n_deals": 35,
            "deployment_rate_m_per_day": 15.0,
            "sector_allocation": {
                "ai_ml": 225.0,
                "enterprise_saas": 90.0,
                "consumer": 67.5,
                "biotech_healthcare": 45.0,
                "fintech": 22.5
            },
            "avg_round_size_by_stage": {
                "seed": 2.8,
                "series_a": 12.5,
                "series_b_plus": 35.0
            },
            "syndication_patterns": {
                "avg_syndicate_size": 2.3,
                "lead_solo_rate": 0.15,
                "cross_region_rate": 0.28
            },
            "concentration": {
                "herfindahl_sector": 0.35,
                "top_10_deals_share": 0.55
            }
        },
        "agents_involved": ["SYSTEM"],
        "metadata": {
            "is_end_of_month": True
        }
    }
}


class ObserverLogger:
    """Logger for the observer system."""

    def __init__(
        self,
        output_file: str = "observer_logs.jsonl",
        simulation_run_id: str = None
    ):
        self.output_file = output_file
        self.simulation_run_id = simulation_run_id or str(uuid.uuid4())[:8]
        self.step_counter = 0

        # Initialize file
        with open(output_file, 'w') as f:
            f.write(json.dumps({
                "session_start": datetime.now().isoformat(),
                "simulation_run_id": self.simulation_run_id,
                "schema_version": "1.0",
                "event": "SESSION_START"
            }) + "\n")

    def log(
        self,
        log_type: ObserverLogType,
        data: Dict[str, Any],
        agents_involved: List[str],
        hype_state: str,
        market_conditions: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log an observation and return log_id."""

        log_id = f"{self.simulation_run_id}-{self.step_counter:06d}"
        self.step_counter += 1

        entry = ObserverLogEntry(
            log_id=log_id,
            timestamp=datetime.now().isoformat(),
            simulation_run_id=self.simulation_run_id,
            simulation_step=self.step_counter,
            log_type=log_type.value,
            hype_state=hype_state,
            market_conditions=market_conditions,
            data=data,
            agents_involved=agents_involved,
            metadata=metadata or {}
        )

        with open(self.output_file, 'a') as f:
            f.write(entry.to_jsonl() + "\n")

        return log_id


# =============================================================================
# 9. RESEARCH QUESTIONS & HYPOTHESES
# =============================================================================

@dataclass
class ResearchHypothesis:
    """Formal research hypothesis specification."""

    hypothesis_id: str
    statement: str

    # Variables
    independent_var: str
    dependent_var: str
    moderator_vars: List[str]
    control_vars: List[str]

    # Operationalization
    iv_measurement: str  # How IV is measured
    dv_measurement: str  # How DV is measured

    # Expected effects
    expected_direction: str  # "positive", "negative", "nonlinear"
    expected_effect_size: str  # "small", "medium", "large"

    # Alternative explanations
    alternative_explanations: List[str]
    robustness_checks: List[str]


# Primary Research Hypotheses
RESEARCH_HYPOTHESES = [
    ResearchHypothesis(
        hypothesis_id="H1",
        statement="Founder charisma has a larger effect on funding probability during Hype market states than during Normal or Risk-off states",
        independent_var="founder_charisma",
        dependent_var="funding_probability",
        moderator_vars=["hype_state"],
        control_vars=[
            "company_revenue", "company_growth", "founder_experience",
            "sector", "stage", "vc_region"
        ],
        iv_measurement="Charisma score from founder traits (-3 to +3 standardized)",
        dv_measurement="Binary indicator: 1 if funded by any VC, 0 otherwise",
        expected_direction="positive",
        expected_effect_size="medium",
        alternative_explanations=[
            "Charismatic founders also have better companies",
            "Hype state founders self-select into pitching",
            "VC risk tolerance confounds the relationship"
        ],
        robustness_checks=[
            "Control for company quality metrics",
            "Propensity score matching on founder traits",
            "Instrumental variable: founder's public speaking background",
            "Placebo test: does charisma affect funding in simulation without hype modulation?"
        ]
    ),

    ResearchHypothesis(
        hypothesis_id="H2",
        statement="VC due diligence depth decreases as the FOMO index increases",
        independent_var="fomo_index",
        dependent_var="dd_depth",
        moderator_vars=[],
        control_vars=[
            "deal_quality", "stage", "sector", "vc_prior_relationship",
            "vc_traits.due_diligence_depth"
        ],
        iv_measurement="FOMO index (0-100) computed from market indicators",
        dv_measurement="DD depth score (0-100): hours spent, references checked, documents reviewed",
        expected_direction="negative",
        expected_effect_size="medium",
        alternative_explanations=[
            "Deal quality is higher during FOMO periods (less DD needed)",
            "VCs have prior relationships reducing DD need",
            "Selection: only high-conviction deals proceed during FOMO"
        ],
        robustness_checks=[
            "Control for objective deal quality metrics",
            "Subsample: first-time relationships only",
            "Instrumental variable: exogenous market shocks",
            "Fixed effects: VC firm and partner level"
        ]
    ),

    ResearchHypothesis(
        hypothesis_id="H3",
        statement="Regional VCs exhibit different sensitivity to founder technical depth vs. charisma",
        independent_var="founder_traits (technical_depth, charisma)",
        dependent_var="funding_probability",
        moderator_vars=["vc_region"],
        control_vars=[
            "company_metrics", "sector", "stage", "other_founder_traits"
        ],
        iv_measurement="Technical depth (0-100), Charisma (-3 to +3)",
        dv_measurement="Region-specific funding probability",
        expected_direction="positive for both, different magnitudes",
        expected_effect_size="medium",
        alternative_explanations=[
            "Regional sector specialization drives the pattern",
            "Founders self-select into regions",
            "Sample composition differences across regions"
        ],
        robustness_checks=[
            "Control for sector fixed effects",
            "Subsample: founders who pitched multiple regions",
            "Matched sample on company fundamentals",
            "Difference-in-differences: same founder, different regions"
        ]
    ),

    ResearchHypothesis(
        hypothesis_id="H4",
        statement="Hype market states shift capital allocation toward sectors with stronger narrative appeal (AI) and away from fundamental-heavy sectors (biotech)",
        independent_var="hype_state",
        dependent_var="sector_capital_allocation",
        moderator_vars=["sector_narrative_score"],
        control_vars=[
            "sector_fundamentals", "sector_prior_returns",
            "sector_exit_multiples", "total_market_capital"
        ],
        iv_measurement="Hype state: categorical (risk_off, normal, hype)",
        dv_measurement="Share of capital allocated to each sector (0-1)",
        expected_direction="positive for AI, negative for biotech",
        expected_effect_size="large",
        alternative_explanations=[
            "AI genuinely performs better during hype periods",
            "Founder supply shifts toward AI during hype",
            "Biotech has independent negative shock"
        ],
        robustness_checks=[
            "Control for sector deal flow",
            "Control for sector exit environment",
            "Placebo: non-narrative sectors (e.g., infrastructure)",
            "Cross-sectional regression: narrative score x hype interaction"
        ]
    ),

    ResearchHypothesis(
        hypothesis_id="H5",
        statement="Syndication rates increase during Hype states as VCs seek to share risk and gain information from co-investors",
        independent_var="hype_state",
        dependent_var="syndicate_size",
        moderator_vars=["vc_herd_behavior_trait"],
        control_vars=[
            "deal_size", "stage", "sector", "vc_fund_size", "founder_network"
        ],
        iv_measurement="Hype state: categorical",
        dv_measurement="Number of co-investors in round",
        expected_direction="positive",
        expected_effect_size="small to medium",
        alternative_explanations=[
            "Round sizes increase during hype (mechanical effect)",
            "VCs have more capital to deploy, can afford to syndicate",
            "Founder preference for multiple investors"
        ],
        robustness_checks=[
            "Control for round size",
            "Subsample: deals where founder didn't request syndicate",
            "Interaction: hype x vc_herd_behavior",
            "Synthetic control: non-hype-sensitive VC benchmark"
        ]
    )
]


# =============================================================================
# 10. VISUALIZATION SPECIFICATIONS
# =============================================================================

@dataclass
class VisualizationSpec:
    """Specification for a visualization."""

    viz_id: str
    title: str
    viz_type: str
    description: str

    # Data requirements
    data_sources: List[str]
    variables: Dict[str, str]  # {role: variable_name}

    # Visual encoding
    encoding: Dict[str, Any]

    # Annotations
    annotations: List[str]

    # Interactivity
    interactive_features: List[str]

    # Export
    recommended_size: Tuple[int, int]  # (width, height) in pixels
    export_formats: List[str]


# Core Visualization Specifications
VISUALIZATION_SPECS = [
    VisualizationSpec(
        viz_id="VIZ001",
        title="Capital Flow Sankey Diagram",
        viz_type="sankey",
        description="Shows money flow from VC regions to sectors to stages to outcomes",
        data_sources=["funding_decisions", "money_flow_snapshots"],
        variables={
            "source_levels": ["vc_region", "sector", "stage"],
            "target_levels": ["sector", "stage", "outcome"],
            "flow_value": "funding_amount_m"
        },
        encoding={
            "nodes": {
                "color_by": "level",
                "color_palette": {
                    "vc_region": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D"],
                    "sector": ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"],
                    "stage": ["#606C38", "#283618", "#DDA15E"]
                }
            },
            "links": {
                "opacity": 0.4,
                "hover_opacity": 0.8,
                "color": "source"
            }
        },
        annotations=[
            "Total capital deployed: ${total_m}M",
            "Largest flow: {source} -> {target} (${amount}M)",
            "Observation period: {start_date} to {end_date}"
        ],
        interactive_features=[
            "Hover for flow details",
            "Click node to isolate flows",
            "Slider for time period",
            "Toggle to show/hide stages"
        ],
        recommended_size=(1200, 800),
        export_formats=["png", "svg", "html"]
    ),

    VisualizationSpec(
        viz_id="VIZ002",
        title="Trait-Outcome Heatmap",
        viz_type="heatmap",
        description="Shows relationship between founder/VC traits and funding outcomes",
        data_sources=["pitch_interactions", "funding_decisions", "trait_expressions"],
        variables={
            "x_axis": "founder_trait",  # charisma, technical_depth, etc.
            "y_axis": "outcome_metric",  # funding_prob, valuation, time_to_close
            "cell_value": "effect_size",  # Standardized coefficient
            "facet": "hype_state"
        },
        encoding={
            "color_scale": {
                "type": "diverging",
                "scheme": "RdBu",
                "domain": [-1, 0, 1],
                "null_color": "#f0f0f0"
            },
            "cell_annotations": True,
            "dendrogram": {
                "rows": True,
                "cols": True
            }
        },
        annotations=[
            "* p < 0.05, ** p < 0.01, *** p < 0.001",
            "Effect sizes standardized (Cohen's d)",
            "N = {n_observations} pitch interactions"
        ],
        interactive_features=[
            "Hover for confidence intervals",
            "Click cell for scatter plot",
            "Toggle significance stars",
            "Filter by region/sector"
        ],
        recommended_size=(1000, 800),
        export_formats=["png", "svg", "pdf"]
    ),

    VisualizationSpec(
        viz_id="VIZ003",
        title="Sector Allocation Time Series",
        viz_type="stacked_area",
        description="Shows how sector allocation shifts over time with hype state overlay",
        data_sources=["money_flow_snapshots", "market_state_updates"],
        variables={
            "x_axis": "timestamp",
            "y_axis": "capital_share",  # 0-1
            "fill": "sector",
            "overlay": "hype_state"
        },
        encoding={
            "area": {
                "colors": {
                    "ai_ml": "#264653",
                    "enterprise_saas": "#2A9D8F",
                    "consumer": "#E9C46A",
                    "biotech_healthcare": "#F4A261",
                    "fintech": "#E76F51",
                    "other": "#8D99AE"
                },
                "opacity": 0.8
            },
            "hype_overlay": {
                "type": "background_band",
                "colors": {
                    "risk_off": "#E3F2FD",
                    "normal": "#FFFFFF",
                    "hype": "#FFEBEE"
                }
            }
        },
        annotations=[
            "Hype periods shaded in red",
            "Risk-off periods shaded in blue",
            "Vertical lines mark major exits"
        ],
        interactive_features=[
            "Hover for exact values",
            "Click sector to isolate",
            "Zoom/pan timeline",
            "Toggle absolute vs. percentage"
        ],
        recommended_size=(1200, 600),
        export_formats=["png", "svg", "html"]
    ),

    VisualizationSpec(
        viz_id="VIZ004",
        title="Syndication Network Graph",
        viz_type="network",
        description="Shows co-investment relationships between VCs",
        data_sources=["funding_decisions"],
        variables={
            "nodes": "vc_id",
            "edges": "co_investment",
            "node_size": "total_deals",
            "edge_weight": "n_coinvestments"
        },
        encoding={
            "nodes": {
                "color_by": "region",
                "size_scale": [10, 50],
                "label": "firm_name"
            },
            "edges": {
                "width_scale": [1, 10],
                "opacity": 0.5,
                "color": "#999999"
            },
            "layout": "force_directed",
            "layout_params": {
                "gravity": 0.3,
                "charge": -100,
                "link_distance": 100
            }
        },
        annotations=[
            "Node size = total deals led",
            "Edge width = co-investment frequency",
            "Colors = VC region"
        ],
        interactive_features=[
            "Drag nodes to rearrange",
            "Hover for VC details",
            "Click node to highlight connections",
            "Filter by time period/sector"
        ],
        recommended_size=(1000, 1000),
        export_formats=["png", "svg", "html"]
    ),

    VisualizationSpec(
        viz_id="VIZ005",
        title="Valuation Distribution by Stage and Hype State",
        viz_type="violin_box",
        description="Shows valuation distributions across stages, faceted by hype state",
        data_sources=["funding_decisions"],
        variables={
            "x_axis": "stage",
            "y_axis": "pre_money_valuation_m",
            "color": "hype_state",
            "facet": None  # Single panel
        },
        encoding={
            "violin": {
                "opacity": 0.3,
                "bandwidth": "scott"
            },
            "box": {
                "opacity": 0.8,
                "width": 0.1
            },
            "points": {
                "show_outliers": True,
                "jitter": 0.05
            },
            "colors": {
                "risk_off": "#2196F3",
                "normal": "#4CAF50",
                "hype": "#F44336"
            }
        },
        annotations=[
            "Median values shown in box",
            "Outliers beyond 1.5*IQR",
            "N = {n} per group"
        ],
        interactive_features=[
            "Hover for statistics",
            "Click point for deal details",
            "Toggle violin/box/points",
            "Log scale toggle"
        ],
        recommended_size=(1000, 600),
        export_formats=["png", "svg", "pdf"]
    ),

    VisualizationSpec(
        viz_id="VIZ006",
        title="Causal Effect Forest Plot",
        viz_type="forest_plot",
        description="Shows estimated causal effects with confidence intervals for key hypotheses",
        data_sources=["regression_results", "causal_analysis"],
        variables={
            "y_axis": "variable_name",
            "x_axis": "effect_size",
            "error_bars": "confidence_interval",
            "color": "significance"
        },
        encoding={
            "point": {
                "size": 8,
                "shape": "diamond"
            },
            "error_bars": {
                "width": 2,
                "cap_width": 6
            },
            "colors": {
                "significant": "#1976D2",
                "not_significant": "#BDBDBD"
            },
            "reference_line": {
                "x": 0,
                "style": "dashed",
                "color": "#000000"
            }
        },
        annotations=[
            "95% confidence intervals shown",
            "Dashed line = no effect",
            "Coefficients standardized"
        ],
        interactive_features=[
            "Hover for exact values",
            "Click to see regression table",
            "Sort by effect size",
            "Filter by hypothesis"
        ],
        recommended_size=(800, 600),
        export_formats=["png", "svg", "pdf"]
    ),

    VisualizationSpec(
        viz_id="VIZ007",
        title="Decision Timeline",
        viz_type="timeline",
        description="Shows sequence of events from first pitch to funding decision",
        data_sources=["pitch_interactions", "dd_observations", "funding_decisions"],
        variables={
            "x_axis": "days_from_first_contact",
            "y_axis": "deal_id",
            "events": ["pitch", "follow_up", "dd_start", "partner_meeting", "term_sheet", "close"],
            "color": "outcome"
        },
        encoding={
            "events": {
                "pitch": {"shape": "circle", "color": "#1976D2"},
                "follow_up": {"shape": "circle", "color": "#42A5F5"},
                "dd_start": {"shape": "square", "color": "#FFA726"},
                "partner_meeting": {"shape": "diamond", "color": "#AB47BC"},
                "term_sheet": {"shape": "triangle", "color": "#66BB6A"},
                "close": {"shape": "star", "color": "#4CAF50"}
            },
            "connecting_line": {
                "style": "solid",
                "color": "#E0E0E0"
            }
        },
        annotations=[
            "Average time to close: {avg_days} days",
            "Fastest: {min_days} days",
            "Legend shows event types"
        ],
        interactive_features=[
            "Hover for event details",
            "Filter by outcome/stage/sector",
            "Sort by time to close",
            "Zoom timeline"
        ],
        recommended_size=(1200, 800),
        export_formats=["png", "svg", "html"]
    ),

    VisualizationSpec(
        viz_id="VIZ008",
        title="FOMO Index vs. Due Diligence Depth Scatter",
        viz_type="scatter",
        description="Tests H2: FOMO index effect on DD depth",
        data_sources=["market_state_updates", "dd_observations"],
        variables={
            "x_axis": "fomo_index",
            "y_axis": "dd_depth_score",
            "color": "vc_region",
            "size": "deal_size_m"
        },
        encoding={
            "points": {
                "opacity": 0.6,
                "size_scale": [5, 30]
            },
            "regression_line": {
                "show": True,
                "confidence_band": True,
                "alpha": 0.95
            },
            "marginal_distributions": {
                "x": "histogram",
                "y": "histogram"
            }
        },
        annotations=[
            "R-squared: {r2:.3f}",
            "Slope: {beta:.3f} (p={p:.4f})",
            "Each point = one DD process"
        ],
        interactive_features=[
            "Hover for deal details",
            "Toggle regression by region",
            "Filter by stage/sector",
            "Brush to select subset"
        ],
        recommended_size=(800, 800),
        export_formats=["png", "svg", "pdf"]
    )
]


# =============================================================================
# MAIN: Export Complete Observer System Design
# =============================================================================

def export_observer_system_design(output_path: str = "observer_system_spec.json"):
    """
    Export complete observer system design as JSON.

    This creates a machine-readable specification that can be used to
    implement the observer system.
    """

    design = {
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "description": "VC-Founder Dynamics Observer System Specification",

        "1_agent_trait_system": {
            "vc_traits": {
                "scales": [e.value for e in VCTraitScale],
                "derived_traits": [
                    "decision_speed_index",
                    "fomo_susceptibility",
                    "contrarian_index"
                ]
            },
            "founder_traits": {
                "scales": [e.value for e in FounderTraitScale],
                "derived_traits": [
                    "pitch_effectiveness",
                    "execution_credibility"
                ]
            }
        },

        "2_money_flow_metrics": {
            "categories": [
                "capital_deployment_velocity",
                "sector_allocation",
                "round_size_trends",
                "follow_on_rates",
                "syndication_patterns",
                "dry_powder_utilization",
                "concentration_metrics"
            ],
            "key_formulas": {
                "herfindahl": "sum(s_i^2) where s_i is share",
                "deployment_rate": "total_capital / days",
                "utilization_rate": "(start - end) / start"
            }
        },

        "3_behavioral_observations": {
            "pitch_behaviors": ["emphasis", "adaptation", "ask_calibration"],
            "dd_behaviors": ["depth", "focus", "reference_pattern"],
            "negotiation_behaviors": ["term_priority", "walkaway", "leverage"],
            "decision_behaviors": ["speed", "committee", "conviction"]
        },

        "4_market_conditions": {
            "core_variable": "hype_state",
            "supporting_variables": [
                "interest_rate_proxy",
                "exit_environment",
                "competition_intensity",
                "fomo_index"
            ],
            "fomo_formula": "50 + 10 * weighted_sum(z_scores)"
        },

        "5_company_categorization": {
            "sector_taxonomy": [e.value for e in SectorTaxonomy],
            "stage_classification": [e.value for e in StageClassification],
            "revenue_models": [e.value for e in RevenueModelType],
            "composite_scores": ["defensibility", "hypiness"]
        },

        "6_dashboard_metrics": {
            "real_time": [
                "funding_rate_by_sector",
                "valuation_by_stage",
                "time_to_funding",
                "rejection_patterns",
                "hot_sectors"
            ],
            "health_indices": [
                "deal_flow_index",
                "pricing_index",
                "velocity_index"
            ]
        },

        "7_causal_analysis": {
            "models": [m.model_id for m in CAUSAL_MODELS],
            "methods": [
                "granger_causality",
                "structural_equations",
                "iv_regression",
                "propensity_matching"
            ]
        },

        "8_logging_schema": {
            "log_types": [e.value for e in ObserverLogType],
            "format": "JSONL",
            "examples": list(LOGGING_SCHEMA_EXAMPLES.keys())
        },

        "9_research_hypotheses": {
            "count": len(RESEARCH_HYPOTHESES),
            "hypotheses": [h.hypothesis_id for h in RESEARCH_HYPOTHESES]
        },

        "10_visualizations": {
            "count": len(VISUALIZATION_SPECS),
            "specs": [v.viz_id for v in VISUALIZATION_SPECS]
        }
    }

    with open(output_path, 'w') as f:
        json.dump(design, f, indent=2)

    print(f"Observer system design exported to: {output_path}")
    return design


if __name__ == "__main__":
    # Export the complete design specification
    design = export_observer_system_design()

    # Print summary
    print("\n" + "=" * 60)
    print("VC-FOUNDER DYNAMICS OBSERVER SYSTEM")
    print("=" * 60)
    print("\nSystem Components:")
    print(f"  1. Agent Trait System: {len(VCTraitScale)} VC + {len(FounderTraitScale)} Founder traits")
    print(f"  2. Money Flow Metrics: 7 categories, 3 key formulas")
    print(f"  3. Behavioral Observations: 12 behavior types")
    print(f"  4. Market Conditions: 5 core variables")
    print(f"  5. Company Categorization: {len(SectorTaxonomy)} sectors, {len(StageClassification)} stages")
    print(f"  6. Dashboard Metrics: 5 real-time, 3 health indices")
    print(f"  7. Causal Analysis: {len(CAUSAL_MODELS)} models")
    print(f"  8. Logging Schema: {len(ObserverLogType)} log types")
    print(f"  9. Research Hypotheses: {len(RESEARCH_HYPOTHESES)} formal hypotheses")
    print(f"  10. Visualizations: {len(VISUALIZATION_SPECS)} specifications")
    print("\n" + "=" * 60)
