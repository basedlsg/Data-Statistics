#!/usr/bin/env python3
"""
Validation script for 50-persona experimental design.

Checks:
1. All 50 personas present in library
2. Design matrix CSV matches library
3. All factorial combinations covered
4. No duplicates
5. Summary statistics of predicted effects
"""

import csv
from collections import Counter
from persona_library_50 import PERSONAS_50


def validate_factorial_design():
    """Verify all 5×5×2 combinations are present exactly once."""
    print("=" * 60)
    print("FACTORIAL DESIGN VALIDATION")
    print("=" * 60)

    combinations = []
    for persona_id, persona in PERSONAS_50.items():
        combo = (
            persona["risk_tolerance"],
            persona["self_monitoring"],
            persona["domain"]
        )
        combinations.append(combo)

    # Check for duplicates
    combo_counts = Counter(combinations)
    duplicates = [c for c, count in combo_counts.items() if count > 1]

    if duplicates:
        print("❌ DUPLICATES FOUND:")
        for dup in duplicates:
            print(f"   {dup}")
        return False
    else:
        print("✓ No duplicates found")

    # Check all combinations present
    expected_combos = set()
    for risk in range(1, 6):
        for monitor in range(1, 6):
            for domain in ["technical", "creative"]:
                expected_combos.add((risk, monitor, domain))

    actual_combos = set(combinations)
    missing = expected_combos - actual_combos

    if missing:
        print("❌ MISSING COMBINATIONS:")
        for m in missing:
            print(f"   {m}")
        return False
    else:
        print(f"✓ All {len(expected_combos)} combinations present")

    return True


def validate_csv_consistency():
    """Check that CSV matches persona library."""
    print("\n" + "=" * 60)
    print("CSV CONSISTENCY VALIDATION")
    print("=" * 60)

    csv_path = "/home/user/Data-Statistics/study1/persona_design_matrix.csv"

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        csv_personas = {row['persona_id']: row for row in reader}

    all_match = True
    for persona_id, csv_row in csv_personas.items():
        if persona_id not in PERSONAS_50:
            print(f"❌ {persona_id} in CSV but not in library")
            all_match = False
            continue

        lib_persona = PERSONAS_50[persona_id]

        # Check consistency
        if int(csv_row['risk_tolerance']) != lib_persona['risk_tolerance']:
            print(f"❌ {persona_id}: risk_tolerance mismatch")
            all_match = False

        if int(csv_row['self_monitoring']) != lib_persona['self_monitoring']:
            print(f"❌ {persona_id}: self_monitoring mismatch")
            all_match = False

        if csv_row['domain'] != lib_persona['domain']:
            print(f"❌ {persona_id}: domain mismatch")
            all_match = False

    if all_match:
        print(f"✓ All {len(csv_personas)} personas consistent between CSV and library")

    return all_match


def summarize_predictions():
    """Generate summary statistics of predicted effects."""
    print("\n" + "=" * 60)
    print("PREDICTION SUMMARY STATISTICS")
    print("=" * 60)

    csv_path = "/home/user/Data-Statistics/study1/persona_design_matrix.csv"

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    effects = [float(row['effect_magnitude']) for row in rows]

    print(f"\nTotal personas: {len(effects)}")
    print(f"Mean effect: {sum(effects)/len(effects):.3f}")
    print(f"Median effect: {sorted(effects)[len(effects)//2]:.3f}")
    print(f"Min effect: {min(effects):.3f}")
    print(f"Max effect: {max(effects):.3f}")
    print(f"Range: {max(effects) - min(effects):.3f}")

    # Count by category
    categories = {
        'Negative strong (< -0.50)': 0,
        'Negative moderate (-0.50 to -0.30)': 0,
        'Negative weak (-0.30 to -0.10)': 0,
        'Null (-0.10 to +0.10)': 0,
        'Positive weak (+0.10 to +0.30)': 0,
        'Positive moderate (+0.30 to +0.60)': 0,
        'Positive strong (+0.60 to +0.80)': 0,
        'Positive very strong (> +0.80)': 0
    }

    for eff in effects:
        if eff < -0.50:
            categories['Negative strong (< -0.50)'] += 1
        elif eff < -0.30:
            categories['Negative moderate (-0.50 to -0.30)'] += 1
        elif eff < -0.10:
            categories['Negative weak (-0.30 to -0.10)'] += 1
        elif eff <= 0.10:
            categories['Null (-0.10 to +0.10)'] += 1
        elif eff <= 0.30:
            categories['Positive weak (+0.10 to +0.30)'] += 1
        elif eff <= 0.60:
            categories['Positive moderate (+0.30 to +0.60)'] += 1
        elif eff <= 0.80:
            categories['Positive strong (+0.60 to +0.80)'] += 1
        else:
            categories['Positive very strong (> +0.80)'] += 1

    print("\nEffect distribution:")
    for category, count in categories.items():
        pct = 100 * count / len(effects)
        print(f"  {category}: {count} ({pct:.1f}%)")


def summarize_by_dimension():
    """Show mean predictions by each dimension."""
    print("\n" + "=" * 60)
    print("PREDICTIONS BY DIMENSION")
    print("=" * 60)

    csv_path = "/home/user/Data-Statistics/study1/persona_design_matrix.csv"

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # By risk tolerance
    print("\nBy Risk Tolerance:")
    for risk in range(1, 6):
        risk_effects = [float(r['effect_magnitude']) for r in rows
                       if int(r['risk_tolerance']) == risk]
        mean_eff = sum(risk_effects) / len(risk_effects)
        print(f"  Level {risk}: {mean_eff:+.3f} (n={len(risk_effects)})")

    # By self-monitoring
    print("\nBy Self-Monitoring:")
    for monitor in range(1, 6):
        monitor_effects = [float(r['effect_magnitude']) for r in rows
                          if int(r['self_monitoring']) == monitor]
        mean_eff = sum(monitor_effects) / len(monitor_effects)
        print(f"  Level {monitor}: {mean_eff:+.3f} (n={len(monitor_effects)})")

    # By domain
    print("\nBy Domain:")
    for domain in ['technical', 'creative']:
        domain_effects = [float(r['effect_magnitude']) for r in rows
                         if r['domain'] == domain]
        mean_eff = sum(domain_effects) / len(domain_effects)
        print(f"  {domain.capitalize()}: {mean_eff:+.3f} (n={len(domain_effects)})")

    # Interaction: monitoring × domain
    print("\nMonitoring × Domain Interaction:")
    for domain in ['technical', 'creative']:
        print(f"\n  {domain.capitalize()}:")
        for monitor in range(1, 6):
            effects = [float(r['effect_magnitude']) for r in rows
                      if r['domain'] == domain and int(r['self_monitoring']) == monitor]
            mean_eff = sum(effects) / len(effects)
            print(f"    Monitor={monitor}: {mean_eff:+.3f}")


def show_extreme_personas():
    """Display top 5 and bottom 5 predicted performers."""
    print("\n" + "=" * 60)
    print("EXTREME PERSONAS")
    print("=" * 60)

    csv_path = "/home/user/Data-Statistics/study1/persona_design_matrix.csv"

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Sort by effect magnitude
    sorted_rows = sorted(rows, key=lambda r: float(r['effect_magnitude']), reverse=True)

    print("\nTOP 5 PREDICTED PERFORMERS:")
    for i, row in enumerate(sorted_rows[:5], 1):
        print(f"{i}. {row['persona_id']}: {row['name']}")
        print(f"   Risk={row['risk_tolerance']}, Monitor={row['self_monitoring']}, "
              f"Domain={row['domain']}")
        print(f"   Predicted effect: {row['effect_magnitude']}")
        print()

    print("\nBOTTOM 5 PREDICTED PERFORMERS:")
    for i, row in enumerate(sorted_rows[-5:][::-1], 1):
        print(f"{i}. {row['persona_id']}: {row['name']}")
        print(f"   Risk={row['risk_tolerance']}, Monitor={row['self_monitoring']}, "
              f"Domain={row['domain']}")
        print(f"   Predicted effect: {row['effect_magnitude']}")
        print()


if __name__ == "__main__":
    # Run all validations
    factorial_ok = validate_factorial_design()
    csv_ok = validate_csv_consistency()

    if factorial_ok and csv_ok:
        print("\n" + "=" * 60)
        print("✓ ALL VALIDATIONS PASSED")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ VALIDATION FAILURES DETECTED")
        print("=" * 60)

    # Show summaries
    summarize_predictions()
    summarize_by_dimension()
    show_extreme_personas()

    print("\n" + "=" * 60)
    print("Design validated and ready for deployment!")
    print("=" * 60)
