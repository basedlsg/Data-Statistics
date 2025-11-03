#!/usr/bin/env python3
"""
Quick test to verify budget scaling and distribution
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from simulate import Simulation

def test_budget_scaling():
    """Test that budgets are reasonable with scaling."""
    sim = Simulation()
    scale_factor = sim.config["simulation"].get("budget_scale_factor", 1.0)

    print(f"Budget scale factor: {scale_factor} ({scale_factor*100}% of annual budget)\n")

    for region_key, region in sim.regions.items():
        print(f"{region.name}:")
        for stage in ["seed", "series_a", "series_b_plus"]:
            budget = region.get_stage_budget(stage, scale_factor)
            check_size = region.check_sizes[stage]
            max_deals = int(budget / check_size)
            print(f"  {stage}:")
            print(f"    Budget: ${budget:.1f}M")
            print(f"    Avg check: ${check_size:.1f}M")
            print(f"    Max deals: {max_deals}")
        print()

    print(f"Total founders in simulation: 200")
    print(f"\nExpected: Regional competition, not all founders funded")


def test_quick_run():
    """Run a quick simulation to check distribution."""
    sim = Simulation()
    sim.config["simulation"]["n_founders"] = 200  # Full simulation

    print("\n" + "="*60)
    print("Running quick simulation with 200 founders...")
    print("="*60 + "\n")

    results = sim.run_single_simulation(seed=42)

    print(f"Funded: {results['n_funded']}/{results['n_founders']} ({results['funding_rate']:.1%})")
    print(f"\nDeals by region:")
    for region_key, data in results["regions"].items():
        deals_led = data["deals_led"]
        co_invest = data["co_investments"]
        allocated = data["total_allocated_m"]
        print(f"  {region_key}:")
        print(f"    Led: {deals_led} deals")
        print(f"    Co-invested: {co_invest} deals")
        print(f"    Capital: ${allocated:.1f}M")

    # Check for monopoly
    deals_led_by_region = {k: v["deals_led"] for k, v in results["regions"].items()}
    max_deals = max(deals_led_by_region.values())
    total_deals = sum(deals_led_by_region.values())

    if max_deals == total_deals and total_deals > 0:
        print(f"\n⚠️  WARNING: Monopoly detected! {max(deals_led_by_region, key=deals_led_by_region.get)} has all deals!")
    else:
        print(f"\n✓ Distribution looks reasonable")


if __name__ == "__main__":
    test_budget_scaling()
    test_quick_run()
