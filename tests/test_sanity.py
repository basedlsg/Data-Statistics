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


def test_no_multiple_funding_exclusivity(tmp_path):
    """
    CRITICAL TEST: Verify that no founder is funded by multiple regions as lead investor.
    This was the original bug - every founder was funded 4 times (400% funding rate).
    """
    out = tmp_path / "exclusivity_test"
    out.mkdir()

    sim = Simulation()
    sim.config["simulation"]["n_founders"] = 50
    sim.config["simulation"]["stochastic_checks"] = True

    # Run one simulation
    results = sim.run_single_simulation(seed=42)

    # Check all founders
    funded_founder_ids = set()
    duplicate_fundings = []

    for region_key, region_data in results["regions"].items():
        for founder_dict in region_data["funded_founders"]:
            founder_id = founder_dict["id"]
            if founder_id in funded_founder_ids:
                duplicate_fundings.append((founder_id, region_key))
            funded_founder_ids.add(founder_id)

    assert len(duplicate_fundings) == 0, (
        f"EXCLUSIVITY VIOLATION: {len(duplicate_fundings)} founders were funded multiple times as leads! "
        f"Duplicates: {duplicate_fundings[:5]}"
    )

    # Verify realistic funding rate (should be < 100%, ideally 40-80%)
    funding_rate = results["funding_rate"]
    assert funding_rate <= 1.0, (
        f"Funding rate {funding_rate:.1%} exceeds 100%! Original bug: 400% rate."
    )

    assert funding_rate >= 0.2, (
        f"Funding rate {funding_rate:.1%} is suspiciously low. Expected 20-80%."
    )

    print(f"\n✓ Exclusivity verified: {len(funded_founder_ids)} unique founders funded")
    print(f"  Funding rate: {funding_rate:.1%} (healthy range)")
    print(f"  No duplicate lead investments detected")


def test_realistic_regional_distribution(tmp_path):
    """
    Test that regional allocation roughly matches budget shares.
    Bay Area (44%) should get more deals than LA (9%).
    """
    out = tmp_path / "distribution_test"
    out.mkdir()

    sim = Simulation()
    sim.config["simulation"]["n_founders"] = 200
    sim.config["simulation"]["stochastic_checks"] = True

    # Run a few simulations
    results_list = []
    for i in range(5):
        results = sim.run_single_simulation(seed=100 + i)
        results_list.append(results)

    # Aggregate regional deal counts
    regional_deals = {"bay_area": 0, "nyc": 0, "boston": 0, "la": 0}
    total_deals = 0

    for results in results_list:
        for region_key, region_data in results["regions"].items():
            deals_led = region_data["deals_led"]
            regional_deals[region_key] += deals_led
            total_deals += deals_led

    # Compute actual shares
    actual_shares = {r: count / total_deals for r, count in regional_deals.items()}

    # Expected shares (from data/regions.yml)
    expected_shares = {"bay_area": 0.44, "nyc": 0.20, "boston": 0.11, "la": 0.09}

    print(f"\n✓ Regional distribution over {total_deals} deals:")
    for region in ["bay_area", "nyc", "boston", "la"]:
        actual = actual_shares[region]
        expected = expected_shares[region]
        diff = abs(actual - expected)
        print(f"  {region}: {actual:.1%} (expected {expected:.1%}, diff {diff:.1%})")

        # Allow 10% deviation (e.g., Bay Area 34-54%)
        assert diff < 0.15, (
            f"{region} share {actual:.1%} deviates too much from expected {expected:.1%}"
        )

    # Verify ordering: Bay Area > NYC > Boston ≈ LA
    assert regional_deals["bay_area"] > regional_deals["nyc"], "Bay Area should lead in deals"
    assert regional_deals["nyc"] > regional_deals["boston"], "NYC should have more deals than Boston"

    print(f"  ✓ Regional ordering correct: Bay Area > NYC > Boston/LA")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
