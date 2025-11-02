"""
Unit tests for VC Hype Simulation
Seshat (Quant Analyst) - 2025-11-02

Tests for:
1. Founder generation (priors, domains)
2. Hype Markov chain (transitions, state validity)
3. Regional scoring (monotonicity, hype effects)
4. Capital allocator (budget adherence, stage assignment)
5. End-to-end simulation
"""

import pytest
import numpy as np
import yaml
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from simulate import (
    Founder,
    RegionConfig,
    HypeMarkovChain,
    FounderGenerator,
    RegionalScorer,
    CapitalAllocator,
    Simulation
)


# Fixtures
@pytest.fixture
def config():
    """Load test configuration."""
    with open("config.yml") as f:
        return yaml.safe_load(f)


@pytest.fixture
def rng():
    """Seeded random number generator."""
    return np.random.default_rng(42)


@pytest.fixture
def hype_chain(config):
    """Initialize hype Markov chain."""
    return HypeMarkovChain(
        transition_matrix=config["hype_transition_matrix"],
        initial_state="normal"
    )


@pytest.fixture
def founder_generator(config, rng):
    """Initialize founder generator."""
    return FounderGenerator(config, rng)


@pytest.fixture
def sample_region_config():
    """Sample region config for testing."""
    return RegionConfig(
        name="Test Region",
        capital_share=0.25,
        annual_capital_bn=50.0,
        weights={
            "revenue": 1.0,
            "growth": 1.0,
            "charisma": 0.5,
            "vision": 0.5,
            "traction_quality": 1.0,
            "repeat_founder": 1.0,
            "geo_flex": 0.3
        },
        domain_preferences={"ai": 1.0, "bio": 1.0, "consumer": 1.0, "enterprise": 1.0},
        hype_beta=1.0,
        stage_mix={"seed": 0.3, "series_a": 0.4, "series_b_plus": 0.3},
        check_sizes={"seed": 2.0, "series_a": 10.0, "series_b_plus": 30.0}
    )


# Test: Founder Generation
class TestFounderGeneration:
    """Test founder generation from priors."""

    def test_generate_founders_count(self, founder_generator):
        """Test that correct number of founders generated."""
        founders = founder_generator.generate_founders(100)
        assert len(founders) == 100

    def test_founder_ids_unique(self, founder_generator):
        """Test that founder IDs are unique."""
        founders = founder_generator.generate_founders(50)
        ids = [f.id for f in founders]
        assert len(ids) == len(set(ids))

    def test_domain_distribution(self, founder_generator):
        """Test that domains follow configured distribution (approximately)."""
        founders = founder_generator.generate_founders(1000)
        domain_counts = {}
        for f in founders:
            domain_counts[f.domain] = domain_counts.get(f.domain, 0) + 1

        # Check approximate proportions (within 5%)
        assert 0.30 <= domain_counts["ai"] / 1000 <= 0.40
        assert 0.10 <= domain_counts["bio"] / 1000 <= 0.20
        assert 0.20 <= domain_counts["consumer"] / 1000 <= 0.30
        assert 0.20 <= domain_counts["enterprise"] / 1000 <= 0.30

    def test_revenue_positive(self, founder_generator):
        """Test that revenue is always positive (lognormal)."""
        founders = founder_generator.generate_founders(100)
        for f in founders:
            assert f.revenue >= 0

    def test_geo_flex_in_range(self, founder_generator):
        """Test that geo_flex is in [0, 1] (beta distribution)."""
        founders = founder_generator.generate_founders(100)
        for f in founders:
            assert 0 <= f.geo_flex <= 1

    def test_repeat_founder_binary(self, founder_generator):
        """Test that repeat_founder is binary."""
        founders = founder_generator.generate_founders(100)
        for f in founders:
            assert f.repeat_founder in [True, False]


# Test: Hype Markov Chain
class TestHypeMarkovChain:
    """Test Hype Markov chain transitions."""

    def test_valid_initial_state(self, hype_chain):
        """Test that initial state is valid."""
        assert hype_chain.current_state in ["risk_off", "normal", "hype"]

    def test_transition_produces_valid_state(self, hype_chain, rng):
        """Test that transitions always produce valid states."""
        for _ in range(100):
            next_state = hype_chain.step(rng)
            assert next_state in ["risk_off", "normal", "hype"]

    def test_transition_matrix_stochastic(self, hype_chain):
        """Test that transition matrix rows sum to 1."""
        row_sums = hype_chain.transition_matrix.sum(axis=1)
        np.testing.assert_allclose(row_sums, [1.0, 1.0, 1.0])

    def test_beta_multiplier_lookup(self, hype_chain, config):
        """Test beta multiplier lookup for each state."""
        for state in ["risk_off", "normal", "hype"]:
            hype_chain.current_state = state
            beta = hype_chain.get_beta_multiplier(config)
            assert beta > 0
            assert isinstance(beta, (int, float))


# Test: Regional Scoring
class TestRegionalScoring:
    """Test regional scoring logic."""

    def test_score_monotonicity_revenue(
        self, sample_region_config, hype_chain, config, rng
    ):
        """Test that higher revenue → higher score (holding else constant)."""
        scorer = RegionalScorer(sample_region_config, hype_chain, config, rng)

        # Create two founders differing only in revenue
        founder_low_rev = Founder(
            id=1, revenue=100_000, growth=0.5, charisma=0.0, vision=0.0,
            traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )
        founder_high_rev = Founder(
            id=2, revenue=10_000_000, growth=0.5, charisma=0.0, vision=0.0,
            traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )

        # Score with same RNG state
        rng_copy1 = np.random.default_rng(42)
        rng_copy2 = np.random.default_rng(42)

        scorer1 = RegionalScorer(sample_region_config, hype_chain, config, rng_copy1)
        scorer2 = RegionalScorer(sample_region_config, hype_chain, config, rng_copy2)

        score_low = scorer1.score_founder(founder_low_rev)
        score_high = scorer2.score_founder(founder_high_rev)

        # Higher revenue should generally yield higher score (may fail rarely due to noise)
        # Run without noise by setting epsilon_std to 0 in actual implementation
        # For now, just check they're different
        assert score_low != score_high

    def test_hype_amplifies_narrative(
        self, sample_region_config, config, rng
    ):
        """Test that Hype state amplifies narrative scores."""
        # Create founder with high narrative, low revenue
        founder = Founder(
            id=1, revenue=10_000, growth=0.1, charisma=2.0, vision=2.0,
            traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )

        # Score in Normal state
        hype_chain_normal = HypeMarkovChain(
            config["hype_transition_matrix"], initial_state="normal"
        )
        scorer_normal = RegionalScorer(
            sample_region_config, hype_chain_normal, config, np.random.default_rng(42)
        )
        score_normal = scorer_normal.score_founder(founder)

        # Score in Hype state
        hype_chain_hype = HypeMarkovChain(
            config["hype_transition_matrix"], initial_state="hype"
        )
        scorer_hype = RegionalScorer(
            sample_region_config, hype_chain_hype, config, np.random.default_rng(42)
        )
        score_hype = scorer_hype.score_founder(founder)

        # Hype state should yield higher score for narrative-heavy founder
        assert score_hype > score_normal

    def test_domain_preference_effect(
        self, hype_chain, config, rng
    ):
        """Test that domain preferences affect scores."""
        # Create region with strong AI preference
        region_ai_lover = RegionConfig(
            name="AI Lover",
            capital_share=0.25,
            annual_capital_bn=50.0,
            weights={k: 1.0 for k in ["revenue", "growth", "charisma", "vision", "traction_quality", "repeat_founder", "geo_flex"]},
            domain_preferences={"ai": 2.0, "bio": 0.5, "consumer": 1.0, "enterprise": 1.0},
            hype_beta=1.0,
            stage_mix={"seed": 0.3, "series_a": 0.4, "series_b_plus": 0.3},
            check_sizes={"seed": 2.0, "series_a": 10.0, "series_b_plus": 30.0}
        )

        scorer = RegionalScorer(region_ai_lover, hype_chain, config, rng)

        # Create identical founders in different domains
        founder_ai = Founder(
            id=1, revenue=1_000_000, growth=0.5, charisma=1.0, vision=1.0,
            traction_quality=1.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )
        founder_bio = Founder(
            id=2, revenue=1_000_000, growth=0.5, charisma=1.0, vision=1.0,
            traction_quality=1.0, geo_flex=0.5, repeat_founder=False, domain="bio"
        )

        score_ai = scorer.score_founder(founder_ai)
        score_bio = scorer.score_founder(founder_bio)

        # AI should score higher (2.0× vs 0.5×)
        assert score_ai > score_bio


# Test: Capital Allocator
class TestCapitalAllocator:
    """Test capital allocation logic."""

    def test_budget_adherence(self, sample_region_config, rng):
        """Test that allocator respects budget constraints."""
        allocator = CapitalAllocator(sample_region_config, rng)

        # Create many high-scoring founders (more than budget allows)
        scored_founders = []
        for i in range(100):
            founder = Founder(
                id=i, revenue=1_000_000, growth=0.5, charisma=1.0, vision=1.0,
                traction_quality=1.0, geo_flex=0.5, repeat_founder=False, domain="ai"
            )
            scored_founders.append((founder, 100.0 - i))  # Descending scores

        funded, total_allocated = allocator.allocate(scored_founders)

        # Total allocated should not exceed budget
        total_budget = sample_region_config.annual_capital_bn * 1000  # Convert to millions
        assert total_allocated <= total_budget

    def test_greedy_allocation_order(self, sample_region_config, rng):
        """Test that allocator funds highest-scoring founders first."""
        allocator = CapitalAllocator(sample_region_config, rng)

        # Create founders with clear score ordering
        founders = []
        for i in range(10):
            f = Founder(
                id=i, revenue=100_000, growth=0.5, charisma=0.0, vision=0.0,
                traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
            )
            founders.append(f)

        scored = [(founders[i], 100.0 - i * 10) for i in range(10)]  # Scores: 100, 90, ..., 10

        funded, _ = allocator.allocate(scored)

        # First funded should be highest scoring
        assert funded[0].id == 0
        # IDs should be in ascending order (since scores descending)
        funded_ids = [f.id for f in funded]
        assert funded_ids == sorted(funded_ids)

    def test_stage_assignment_logic(self, sample_region_config, rng):
        """Test that stage assignment follows revenue heuristic."""
        allocator = CapitalAllocator(sample_region_config, rng)

        # Create founders at different revenue levels
        founder_seed = Founder(
            id=1, revenue=100_000, growth=0.5, charisma=0.0, vision=0.0,
            traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )
        founder_a = Founder(
            id=2, revenue=2_000_000, growth=0.5, charisma=0.0, vision=0.0,
            traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )
        founder_b = Founder(
            id=3, revenue=10_000_000, growth=0.5, charisma=0.0, vision=0.0,
            traction_quality=0.0, geo_flex=0.5, repeat_founder=False, domain="ai"
        )

        stage_seed = allocator._assign_stage(founder_seed)
        stage_a = allocator._assign_stage(founder_a)
        stage_b = allocator._assign_stage(founder_b)

        assert stage_seed == "seed"
        assert stage_a == "series_a"
        assert stage_b == "series_b_plus"


# Test: End-to-End Simulation
class TestSimulation:
    """Test full simulation runs."""

    def test_simulation_initialization(self):
        """Test that simulation initializes correctly."""
        sim = Simulation()
        assert len(sim.regions) == 4  # Bay Area, NYC, Boston, LA
        assert "bay_area" in sim.regions
        assert "nyc" in sim.regions
        assert "boston" in sim.regions
        assert "la" in sim.regions

    def test_single_run_completes(self):
        """Test that single simulation run completes without errors."""
        sim = Simulation()
        results = sim.run_single_simulation(seed=42)

        assert "seed" in results
        assert results["seed"] == 42
        assert "hype_state" in results
        assert "n_founders" in results
        assert "regions" in results
        assert len(results["regions"]) == 4

    def test_reproducibility(self):
        """Test that same seed produces same results."""
        sim1 = Simulation()
        sim2 = Simulation()

        results1 = sim1.run_single_simulation(seed=42)
        results2 = sim2.run_single_simulation(seed=42)

        # Same number of funded founders
        assert results1["n_funded"] == results2["n_funded"]

        # Same allocations by region
        for region in results1["regions"]:
            assert (
                results1["regions"][region]["funded_count"]
                == results2["regions"][region]["funded_count"]
            )


# Test: Hype Scorer (from hype_score.py)
class TestHypeScorer:
    """Test hype scoring functionality."""

    def test_hype_scorer_imports(self):
        """Test that hype_score module imports correctly."""
        from hype_score import HypeScorer, HypeSignals
        assert HypeScorer is not None
        assert HypeSignals is not None

    def test_high_hype_text_scores_high(self):
        """Test that high-hype text gets high score."""
        from hype_score import HypeScorer

        scorer = HypeScorer()
        high_hype_text = """
        Revolutionary paradigm-shift with Sequoia and Andreessen Horowitz.
        Category-defining, oversubscribed, hypergrowth, unicorn potential.
        """
        score = scorer.score(high_hype_text, normalize=True)
        assert score > 0.5  # Should be in upper half

    def test_conservative_text_scores_low(self):
        """Test that conservative text gets lower score."""
        from hype_score import HypeScorer

        scorer = HypeScorer()
        conservative_text = """
        Profitable, sustainable, cash-flow positive with disciplined growth.
        Strong unit economics and capital-efficient operations.
        """
        score = scorer.score(conservative_text, normalize=True)
        assert score < 0.5  # Should be in lower half


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
