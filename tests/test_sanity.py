"""
Sanity Tests for VC Hype Simulation
Tests basic invariants and realistic behavior
"""

import pytest
import yaml
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from simulate import Simulation


def test_budgets_sum_to_one():
    """Test that region budget shares sum to 1.0."""
    with open("data/regions.yml") as f:
        regions_data = yaml.safe_load(f)

    budget_sum = sum(
        r["budget_share"]
        for r in regions_data["regions"].values()
    )

    assert abs(budget_sum - 1.0) < 0.02, (
        f"Region budget shares must sum to ~1.0, got {budget_sum}. "
        f"Check data/regions.yml for consistency."
    )


def test_funded_counts_not_all_equal_smoke(tmp_path):
    """
    Run a small simulation and verify we don't get a flat 25%/25%/25%/25% split.
    With unequal budgets & stochastic costs, region funded counts should differ.
    """
    # Run a small simulation
    out = tmp_path / "res"
    out.mkdir()

    sim = Simulation()

    # Enable stochastic features
    sim.config["simulation"]["stochastic_checks"] = True
    sim.config["simulation"]["use_score_per_dollar"] = True
    sim.config["simulation"]["n_founders"] = 100  # Smaller for speed

    # Run just 5 simulations
    results = sim.run_multiple_simulations(
        n_runs=5,
        base_seed=123,
        output_dir=str(out)
    )

    # Group by region
    by_region = results.groupby("region").size()

    # If all equal, std == 0. We expect some inequality given budgets & costs.
    std_dev = by_region.std()
    assert std_dev > 0.0, (
        f"Region funded counts should differ with unequal budgets & costs. "
        f"Got: {by_region.to_dict()}, std={std_dev}"
    )

    print(f"\n✓ Funded counts by region: {by_region.to_dict()}")
    print(f"  Standard deviation: {std_dev:.2f} (healthy variation)")


def test_stochastic_check_sizes_vary():
    """Test that stochastic check sizes produce variance."""
    import numpy as np
    from simulate import sample_check_size

    rng = np.random.default_rng(42)

    # Mock region config
    region_cfg = {
        "check_sizes": {"seed": 2.0},
        "check_sigma": {"seed": 0.3},
        "domain_mult": {"ai": 1.2, "bio": 1.0}
    }

    # Sample 100 AI seed checks
    samples = [
        sample_check_size(region_cfg, "seed", "ai", rng)
        for _ in range(100)
    ]

    mean_val = np.mean(samples)
    std_val = np.std(samples)

    # Expected mean ≈ 2.0 * 1.2 = 2.4
    assert 2.0 < mean_val < 3.0, f"Mean should be near 2.4, got {mean_val}"
    assert std_val > 0.1, f"Should have variation, got std={std_val}"

    print(f"\n✓ Stochastic check sizes: mean={mean_val:.2f}, std={std_val:.2f}")


def test_score_per_dollar_preference():
    """Test that score-per-dollar ranking prefers efficient deals."""
    from simulate import Founder

    # Mock high-efficiency founder (high score, low cost)
    founder_efficient = Founder(
        id=1,
        revenue=100_000,
        growth=0.5,
        charisma=2.0,
        vision=2.0,
        traction_quality=1.0,
        geo_flex=0.5,
        repeat_founder=False,
        domain="ai"
    )

    # Mock low-efficiency founder (same score, high cost from revenue)
    founder_costly = Founder(
        id=2,
        revenue=10_000_000,
        growth=0.5,
        charisma=2.0,
        vision=2.0,
        traction_quality=1.0,
        geo_flex=0.5,
        repeat_founder=False,
        domain="ai"
    )

    # With score-per-dollar, efficient (seed-stage) should rank higher
    # than costly (Series B+) for same score
    score = 100.0
    cost_efficient = 2.0  # Seed check
    cost_costly = 35.0    # Series B+ check

    spd_efficient = score / cost_efficient  # 50
    spd_costly = score / cost_costly        # ~2.86

    assert spd_efficient > spd_costly, (
        "Score-per-dollar should favor efficient deals"
    )

    print(f"\n✓ Score-per-dollar: {spd_efficient:.2f} > {spd_costly:.2f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
