#!/usr/bin/env python3
"""
VC Hype Simulation - Core Engine
Seshat (Quant Analyst) - 2025-11-02

Simulates capital allocation across 4 regional VC ecosystems under tunable Hype(t).
Models how market sentiment affects funding decisions across Bay Area, NYC, Boston, LA.
"""

import argparse
import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Literal, Tuple, Any
import numpy as np
import pandas as pd
import yaml


def sample_check_size(
    region_cfg: Dict[str, Any],
    stage: str,
    domain: str,
    rng: np.random.Generator
) -> float:
    """
    Returns a single deal cost (in USD millions) drawn from a lognormal
    with mean approximately = check_sizes[stage] * domain_mult[domain].

    Args:
        region_cfg: Region configuration dict with check_sizes, check_sigma, domain_mult
        stage: Funding stage (seed, series_a, series_b_plus)
        domain: Company domain (ai, bio, consumer, enterprise)
        rng: NumPy random number generator

    Returns:
        Deal cost in millions USD
    """
    base_mean = float(region_cfg["check_sizes"][stage])
    sigma = float(region_cfg.get("check_sigma", {}).get(stage, 0.3))
    dmult = float(region_cfg.get("domain_mult", {}).get(domain, 1.0))

    target_mean = base_mean * dmult
    # Convert target mean + sigma to mu for lognormal:
    # mean = exp(mu + 0.5*sigma^2) -> mu = ln(mean) - 0.5*sigma^2
    mu = math.log(max(1e-6, target_mean)) - 0.5 * (sigma ** 2)
    # NumPy's lognormal uses mu, sigma on natural log scale
    val = rng.lognormal(mu, sigma)
    return max(0.1, val)  # floor to avoid zeros


# Type aliases
HypeState = Literal["risk_off", "normal", "hype"]
Domain = Literal["ai", "bio", "consumer", "enterprise"]
Stage = Literal["seed", "series_a", "series_b_plus"]


@dataclass
class Founder:
    """Represents a founder/company with feature vector and domain."""

    id: int
    revenue: float  # Annual revenue (log-scale, dollars)
    growth: float  # YoY growth rate
    charisma: float  # Standardized charisma score
    vision: float  # Vision/narrative score
    traction_quality: float  # Quality of traction signals
    geo_flex: float  # Geographic flexibility [0, 1]
    repeat_founder: bool  # Whether founder has previous exits
    domain: Domain  # Company domain

    # Scores by region (computed during simulation)
    scores: Dict[str, float] = field(default_factory=dict)

    # Funding information (NEW: supports lead + syndicate)
    lead_investor: str | None = None  # Region that led the round
    syndicate: Dict[str, float] = field(default_factory=dict)  # {region: amount} for co-investors
    funding_stage: Stage | None = None
    total_funding_amount: float = 0.0

    @property
    def is_funded(self) -> bool:
        """Check if founder has been funded."""
        return self.lead_investor is not None

    @property
    def all_investors(self) -> List[str]:
        """Get list of all investors (lead + syndicate)."""
        if not self.is_funded:
            return []
        return [self.lead_investor] + list(self.syndicate.keys())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export."""
        d = asdict(self)
        # Add computed fields
        d['is_funded'] = self.is_funded
        d['all_investors'] = self.all_investors
        # Add lead investment amount for CSV compatibility
        if self.is_funded:
            d['funding_amount'] = self.total_funding_amount * 0.65  # Lead pays 65%
        else:
            d['funding_amount'] = 0.0
        # Deprecated field for backward compatibility
        d['funded_by'] = self.lead_investor
        return d


@dataclass
class RegionConfig:
    """Configuration for a VC region/ecosystem."""

    name: str
    budget_share: float  # Renamed from capital_share
    annual_capital_bn: float
    weights: Dict[str, float]  # Feature weights for scoring
    domain_preferences: Dict[str, float]  # Domain multipliers
    hype_beta: float  # Hype sensitivity
    stage_mix: Dict[str, float]  # Proportion of capital by stage
    check_sizes: Dict[str, float]  # Average check size by stage (millions)
    check_sigma: Dict[str, float] = field(default_factory=dict)  # Lognormal sigma by stage
    domain_mult: Dict[str, float] = field(default_factory=dict)  # Domain cost multipliers

    def get_stage_budget(self, stage: Stage) -> float:
        """Get budget for a specific stage (in millions)."""
        return self.annual_capital_bn * 1000 * self.stage_mix[stage]


@dataclass
class SimulationState:
    """State of the simulation at a given time step."""

    hype_state: HypeState
    founders: List[Founder]
    regions: Dict[str, RegionConfig]
    funded_founders: List[Founder]
    total_allocated: Dict[str, float]  # Total allocated by region


class HypeMarkovChain:
    """Hype state Markov chain with 3 states: risk_off, normal, hype."""

    def __init__(self, transition_matrix: np.ndarray, initial_state: HypeState):
        """
        Initialize Hype Markov chain.

        Args:
            transition_matrix: 3x3 transition probability matrix
            initial_state: Initial hype state
        """
        self.states: List[HypeState] = ["risk_off", "normal", "hype"]
        self.state_to_idx = {s: i for i, s in enumerate(self.states)}
        self.transition_matrix = np.array(transition_matrix)
        self.current_state = initial_state

        # Validate transition matrix
        assert self.transition_matrix.shape == (3, 3), "Transition matrix must be 3x3"
        assert np.allclose(self.transition_matrix.sum(axis=1), 1.0), "Rows must sum to 1"

    def step(self, rng: np.random.Generator) -> HypeState:
        """Transition to next state and return it."""
        current_idx = self.state_to_idx[self.current_state]
        next_idx = rng.choice(3, p=self.transition_matrix[current_idx])
        self.current_state = self.states[next_idx]
        return self.current_state

    def get_beta_multiplier(self, config: Dict[str, Any]) -> float:
        """Get beta multiplier for current hype state."""
        return config["hype_states"][self.current_state]["beta_multiplier"]

    def get_valuation_spread(self, config: Dict[str, Any]) -> float:
        """Get valuation spread multiplier for current hype state."""
        return config["hype_states"][self.current_state]["valuation_spread"]


class FounderGenerator:
    """Generates founder agents according to configured priors."""

    def __init__(self, config: Dict[str, Any], rng: np.random.Generator):
        """
        Initialize founder generator.

        Args:
            config: Simulation configuration dict
            rng: Random number generator
        """
        self.config = config
        self.rng = rng
        self.priors = config["founder_priors"]
        self.domains = config["domains"]

    def generate_founders(self, n: int) -> List[Founder]:
        """Generate n founders with random feature vectors."""
        founders = []

        for i in range(n):
            # Sample from priors
            revenue = self._sample_from_prior("revenue")
            growth = self._sample_from_prior("growth")
            charisma = self._sample_from_prior("charisma")
            vision = self._sample_from_prior("vision")
            traction_quality = self._sample_from_prior("traction_quality")
            geo_flex = self._sample_from_prior("geo_flex")
            repeat_founder = self._sample_from_prior("repeat_founder")

            # Sample domain
            domain = self.rng.choice(
                list(self.domains.keys()),
                p=list(self.domains.values())
            )

            founder = Founder(
                id=i,
                revenue=revenue,
                growth=growth,
                charisma=charisma,
                vision=vision,
                traction_quality=traction_quality,
                geo_flex=geo_flex,
                repeat_founder=bool(repeat_founder),
                domain=domain
            )
            founders.append(founder)

        return founders

    def _sample_from_prior(self, feature: str) -> float:
        """Sample a single feature from its prior distribution."""
        prior = self.priors[feature]
        dist = prior["distribution"]

        if dist == "normal":
            return self.rng.normal(prior["mean"], prior["std"])
        elif dist == "lognormal":
            return self.rng.lognormal(prior["mean"], prior["std"])
        elif dist == "beta":
            return self.rng.beta(prior["alpha"], prior["beta"])
        elif dist == "bernoulli":
            return float(self.rng.random() < prior["p"])
        else:
            raise ValueError(f"Unknown distribution: {dist}")


class RegionalScorer:
    """Scores founders for a specific regional ecosystem."""

    def __init__(
        self,
        region_config: RegionConfig,
        hype_chain: HypeMarkovChain,
        global_config: Dict[str, Any],
        rng: np.random.Generator
    ):
        """
        Initialize regional scorer.

        Args:
            region_config: Configuration for this region
            hype_chain: Hype state Markov chain
            global_config: Global simulation config
            rng: Random number generator
        """
        self.region = region_config
        self.hype_chain = hype_chain
        self.config = global_config
        self.rng = rng

    def score_founder(self, founder: Founder) -> float:
        """
        Score a founder for this region.

        Score = w_region • features + β_region * Hype(t) * narrative_score + ε

        Args:
            founder: Founder to score

        Returns:
            Score (higher is better)
        """
        weights = self.region.weights

        # Base score: weighted sum of features
        base_score = (
            weights["revenue"] * np.log1p(founder.revenue) +  # Log revenue
            weights["growth"] * founder.growth +
            weights["charisma"] * founder.charisma +
            weights["vision"] * founder.vision +
            weights["traction_quality"] * founder.traction_quality +
            weights["repeat_founder"] * (1.0 if founder.repeat_founder else 0.0) +
            weights["geo_flex"] * founder.geo_flex
        )

        # Domain preference multiplier
        domain_mult = self.region.domain_preferences[founder.domain]
        base_score *= domain_mult

        # Hype component: amplifies narrative features (charisma + vision)
        hype_multiplier = self.hype_chain.get_beta_multiplier(self.config)
        narrative_score = founder.charisma + founder.vision
        hype_component = self.region.hype_beta * hype_multiplier * narrative_score

        # Noise term
        epsilon = self.rng.normal(0, self.config["noise"]["scoring_epsilon_std"])

        total_score = base_score + hype_component + epsilon

        return total_score

    def score_all_founders(self, founders: List[Founder]) -> List[Tuple[Founder, float]]:
        """
        Score all founders and return sorted list.

        Args:
            founders: List of founders to score

        Returns:
            List of (founder, score) tuples sorted by score descending
        """
        scored = [(f, self.score_founder(f)) for f in founders]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


class CapitalAllocator:
    """Allocates capital via greedy algorithm subject to budget constraints."""

    def __init__(
        self,
        region_config: RegionConfig,
        region_data: Dict[str, Any],
        config: Dict[str, Any],
        rng: np.random.Generator
    ):
        """
        Initialize capital allocator.

        Args:
            region_config: Configuration for this region
            region_data: Raw region data dict (for stochastic checks)
            config: Global simulation config
            rng: Random number generator
        """
        self.region = region_config
        self.region_data = region_data
        self.config = config
        self.rng = rng

    def allocate(
        self,
        scored_founders: List[Tuple[Founder, float]]
    ) -> Tuple[List[Founder], float]:
        """
        Greedy allocation: fund top-scoring founders until budget exhausted.

        Args:
            scored_founders: List of (founder, score) sorted by score descending

        Returns:
            Tuple of (funded_founders, total_allocated)
        """
        funded = []
        budgets = {
            stage: self.region.get_stage_budget(stage)
            for stage in ["seed", "series_a", "series_b_plus"]
        }
        total_allocated = 0.0

        # Prepare candidates with check sizes and score-per-dollar
        candidates = []
        for founder, score in scored_founders:
            stage = self._assign_stage(founder)

            # Sample stochastic check size if enabled
            if self.config["simulation"].get("stochastic_checks", False):
                check_size = sample_check_size(
                    self.region_data,
                    stage,
                    founder.domain,
                    self.rng
                )
            else:
                check_size = self.region.check_sizes[stage]

            candidates.append((founder, score, check_size, stage))

        # Sort by score-per-dollar if enabled, otherwise by raw score
        if self.config["simulation"].get("use_score_per_dollar", False):
            def spd_key(item):
                founder, score, check_size, stage = item
                cost = max(1e-6, check_size)
                return (score / cost, score)  # Primary: efficiency, tie-break: raw score
            candidates.sort(key=spd_key, reverse=True)
        else:
            # Already sorted by score, but re-sort with check_size info
            candidates.sort(key=lambda x: x[1], reverse=True)

        # Allocate
        for founder, score, check_size, stage in candidates:
            # Check if budget available
            if budgets[stage] >= check_size:
                founder.funded_by = self.region.name
                founder.funding_stage = stage
                founder.funding_amount = check_size
                funded.append(founder)
                budgets[stage] -= check_size
                total_allocated += check_size

        return funded, total_allocated

    def _assign_stage(self, founder: Founder) -> Stage:
        """
        Assign funding stage based on founder characteristics.

        Simple heuristic:
        - Seed: revenue < $500K
        - Series A: $500K <= revenue < $5M
        - Series B+: revenue >= $5M or repeat founder with traction
        """
        if founder.revenue < 500_000:
            return "seed"
        elif founder.revenue < 5_000_000:
            return "series_a"
        else:
            return "series_b_plus"


class Simulation:
    """Main simulation orchestrator."""

    def __init__(self, config_path: str = "config.yml", regions_path: str = "data/regions.yml"):
        """
        Initialize simulation from config files.

        Args:
            config_path: Path to global config YAML
            regions_path: Path to regions data YAML
        """
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        with open(regions_path) as f:
            regions_data = yaml.safe_load(f)

        # Parse region configs (only main 4 regions for MVP)
        self.regions = {}
        self.regions_data = regions_data  # Store for later use
        for region_key in ["bay_area", "nyc", "boston", "la"]:
            r = regions_data["regions"][region_key]
            self.regions[region_key] = RegionConfig(
                name=r["name"],
                budget_share=r["budget_share"],
                annual_capital_bn=r["annual_capital_bn"],
                weights=r["weights"],
                domain_preferences=r["domain_preferences"],
                hype_beta=r["hype_beta"],
                stage_mix=r["stage_mix"],
                check_sizes=r["check_sizes"],
                check_sigma=r.get("check_sigma", {}),
                domain_mult=r.get("domain_mult", {})
            )

        # Store for robustness analysis
        self.robustness_regions = regions_data.get("robustness_regions", {})

    def _assign_stage(self, founder: Founder) -> Stage:
        """
        Assign funding stage based on founder characteristics.

        Simple heuristic:
        - Seed: revenue < $500K
        - Series A: $500K <= revenue < $5M
        - Series B+: revenue >= $5M
        """
        if founder.revenue < 500_000:
            return "seed"
        elif founder.revenue < 5_000_000:
            return "series_a"
        else:
            return "series_b_plus"

    def _competitive_allocation(
        self,
        founders: List[Founder],
        hype_chain: HypeMarkovChain,
        rng: np.random.Generator
    ) -> Dict[str, Any]:
        """
        Competitive allocation: founders go to highest-scoring region (lead investor).
        Optional syndication: other regions can co-invest.

        Args:
            founders: List of founder agents
            hype_chain: Hype Markov chain for scoring
            rng: Random number generator

        Returns:
            Dict with region allocations and statistics
        """
        # Step 1: Score all founders by all regions
        all_scores = {}  # {region_key: {founder_id: score}}
        for region_key, region_config in self.regions.items():
            scorer = RegionalScorer(region_config, hype_chain, self.config, rng)
            scored = scorer.score_all_founders(founders)

            # Store scores in founder objects and dict
            all_scores[region_key] = {}
            for founder, score in scored:
                founder.scores[region_key] = score
                all_scores[region_key][founder.id] = score

        # Step 2: Initialize regional budgets
        budgets = {}
        for region_key, region_config in self.regions.items():
            budgets[region_key] = {
                "seed": region_config.get_stage_budget("seed"),
                "series_a": region_config.get_stage_budget("series_a"),
                "series_b_plus": region_config.get_stage_budget("series_b_plus")
            }

        # Step 3: Sort founders by "market heat" (max score across all regions)
        founders_by_heat = sorted(
            founders,
            key=lambda f: max(all_scores[r][f.id] for r in all_scores.keys()),
            reverse=True
        )

        # Step 4: Competitive allocation (hottest deals first)
        syndication_rate = self.config["simulation"].get("syndication_rate", 0.25)

        for founder in founders_by_heat:
            if founder.is_funded:
                continue  # Skip if already funded

            stage = self._assign_stage(founder)

            # Find lead investor: highest-scoring region with sufficient budget
            lead_candidates = []
            for region_key in all_scores.keys():
                score = all_scores[region_key][founder.id]
                region_data = self.regions_data["regions"][region_key]

                # Sample check size
                if self.config["simulation"].get("stochastic_checks", False):
                    check_size = sample_check_size(region_data, stage, founder.domain, rng)
                else:
                    check_size = self.regions[region_key].check_sizes[stage]

                # Check if region has budget
                if budgets[region_key][stage] >= check_size * 0.65:  # Lead pays 65%
                    lead_candidates.append((region_key, score, check_size))

            if not lead_candidates:
                continue  # No region can afford this founder

            # Winner: highest score
            lead_candidates.sort(key=lambda x: x[1], reverse=True)
            lead_region, lead_score, total_check_size = lead_candidates[0]

            # Lead invests 65% of round
            lead_amount = total_check_size * 0.65
            budgets[lead_region][stage] -= lead_amount

            # Fund the founder
            founder.lead_investor = lead_region
            founder.funding_stage = stage
            founder.total_funding_amount = total_check_size

            # Step 5: Optional syndication (25% of deals by default)
            if rng.random() < syndication_rate and len(lead_candidates) > 1:
                # Remaining amount to syndicate (35% of round)
                syndicate_amount = total_check_size * 0.35

                # Find co-investors (2nd and 3rd highest scorers, excluding lead)
                co_investor_candidates = [
                    (r, s, cs) for r, s, cs in lead_candidates
                    if r != lead_region
                ][:2]  # Max 2 co-investors

                if co_investor_candidates:
                    # Split syndicate amount among co-investors
                    per_co_investor = syndicate_amount / len(co_investor_candidates)

                    for co_region, co_score, co_check in co_investor_candidates:
                        if budgets[co_region][stage] >= per_co_investor:
                            founder.syndicate[co_region] = per_co_investor
                            budgets[co_region][stage] -= per_co_investor

        # Step 6: Aggregate results by region
        region_allocations = {}
        for region_key in self.regions.keys():
            # Count deals led
            led_deals = [f for f in founders if f.lead_investor == region_key]

            # Count co-investments
            co_investments = [f for f in founders if region_key in f.syndicate]

            # Total capital deployed
            total_allocated = sum(f.total_funding_amount * 0.65 for f in led_deals)
            total_allocated += sum(f.syndicate[region_key] for f in co_investments)

            region_allocations[region_key] = {
                "deals_led": len(led_deals),
                "co_investments": len(co_investments),
                "total_deals": len(led_deals) + len(co_investments),
                "total_allocated_m": total_allocated,
                "funded_founders": [f.to_dict() for f in led_deals]  # Only report deals led
            }

        return region_allocations

    def run_single_simulation(self, seed: int) -> Dict[str, Any]:
        """
        Run a single simulation with given random seed.

        Args:
            seed: Random seed for reproducibility

        Returns:
            Results dictionary with allocation data
        """
        rng = np.random.default_rng(seed)

        # Initialize Hype Markov chain
        hype_chain = HypeMarkovChain(
            transition_matrix=self.config["hype_transition_matrix"],
            initial_state=self.config["initial_hype_state"]
        )

        # Generate founders
        n_founders = self.config["simulation"]["n_founders"]
        founder_gen = FounderGenerator(self.config, rng)
        founders = founder_gen.generate_founders(n_founders)

        # NEW: Competitive allocation (founders go to highest-scoring region)
        region_allocations = self._competitive_allocation(founders, hype_chain, rng)

        # Count unique funded founders
        funded_founders = [f for f in founders if f.is_funded]

        # Compute summary statistics
        results = {
            "seed": seed,
            "hype_state": hype_chain.current_state,
            "n_founders": n_founders,
            "n_funded": len(funded_founders),
            "funding_rate": len(funded_founders) / n_founders,
            "regions": region_allocations,
            "all_founders": [f.to_dict() for f in founders]
        }

        return results

    def run_multiple_simulations(
        self,
        n_runs: int,
        base_seed: int = 42,
        output_dir: str = "results/"
    ) -> pd.DataFrame:
        """
        Run multiple simulations and aggregate results.

        Args:
            n_runs: Number of simulation runs
            base_seed: Base random seed (each run uses base_seed + i)
            output_dir: Directory to save results

        Returns:
            DataFrame with aggregated results
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        all_results = []

        for i in range(n_runs):
            seed = base_seed + i
            print(f"Running simulation {i+1}/{n_runs} (seed={seed})...")

            results = self.run_single_simulation(seed)
            all_results.append(results)

            # Save individual run
            output_file = Path(output_dir) / f"run_{seed}.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)

        # Aggregate results into DataFrame
        df_rows = []
        for result in all_results:
            for region_key, region_data in result["regions"].items():
                for founder_dict in region_data["funded_founders"]:
                    row = {
                        "seed": result["seed"],
                        "hype_state": result["hype_state"],
                        "region": region_key,
                        **founder_dict
                    }
                    df_rows.append(row)

        df = pd.DataFrame(df_rows)

        # Save aggregated results
        df.to_csv(Path(output_dir) / "aggregated_results.csv", index=False)

        # Save summary statistics
        summary = self._compute_summary_stats(df)
        with open(Path(output_dir) / "summary_stats.json", "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\nSimulation complete! Results saved to {output_dir}")
        print(f"Total founders funded: {len(df)}")
        print(f"Funding rate: {len(df) / (n_runs * self.config['simulation']['n_founders']):.2%}")

        return df

    def _compute_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute summary statistics from aggregated results."""
        summary = {
            "total_funded": len(df),
            "by_region": df.groupby("region").size().to_dict(),
            "by_domain": df.groupby("domain").size().to_dict(),
            "by_stage": df.groupby("funding_stage").size().to_dict(),
            "avg_funding_by_region": df.groupby("region")["funding_amount"].mean().to_dict(),
            "repeat_founder_rate": df["repeat_founder"].mean(),
            "avg_charisma": df["charisma"].mean(),
            "avg_revenue": df["revenue"].mean()
        }
        return summary


def main():
    """CLI entry point for simulation."""
    parser = argparse.ArgumentParser(
        description="VC Hype Simulation - Model capital allocation under market sentiment"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=50,
        help="Number of simulation runs (default: 50)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base random seed (default: 42)"
    )
    parser.add_argument(
        "--out",
        type=str,
        default="results/",
        help="Output directory (default: results/)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yml",
        help="Path to config file (default: config.yml)"
    )
    parser.add_argument(
        "--regions",
        type=str,
        default="data/regions.yml",
        help="Path to regions data (default: data/regions.yml)"
    )
    parser.add_argument(
        "--stochastic-checks",
        action="store_true",
        help="Sample lognormal check sizes with domain multipliers"
    )
    parser.add_argument(
        "--score-per-dollar",
        action="store_true",
        help="Rank deals by score-per-dollar efficiency"
    )

    args = parser.parse_args()

    # Run simulation
    sim = Simulation(config_path=args.config, regions_path=args.regions)

    # Override config with CLI flags if provided
    if args.stochastic_checks:
        sim.config["simulation"]["stochastic_checks"] = True
    if args.score_per_dollar:
        sim.config["simulation"]["use_score_per_dollar"] = True

    df = sim.run_multiple_simulations(
        n_runs=args.runs,
        base_seed=args.seed,
        output_dir=args.out
    )

    print("\n✓ Simulation complete!")
    print(f"Results saved to: {args.out}")


if __name__ == "__main__":
    main()
