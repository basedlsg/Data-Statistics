#!/usr/bin/env python3
"""
Comprehensive Analysis of Full Study Results

This script:
1. Extracts all responses from JSONL logs
2. Applies 19-code behavioral scheme
3. Runs statistical analysis (mixed-effects models)
4. Calculates effect sizes
5. Generates publication-quality figures
6. Creates results summary for paper
"""

import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Add study1 to path
sys.path.insert(0, str(Path(__file__).parent))

from behavioral_coding import AutoCoder
from analysis import PowerAnalysis, MixedEffectsModels


def extract_responses_from_jsonl(data_dir: Path) -> list:
    """Extract all responses from JSONL log files."""
    responses = []

    for jsonl_file in data_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                if 'interaction_id' in data and 'response_text' in data:
                    responses.append({
                        'response_id': data['interaction_id'],
                        'agent_name': data['agent_id'],
                        'condition': data['condition'],
                        'response_text': data['response_text'],
                        'response_length': len(data['response_text']),
                        'session_number': data.get('session_number', 0),
                        'run_number': data.get('run_number', 0),
                        'order_position': data.get('order_position', 0)
                    })

    return responses


def apply_behavioral_coding(responses: list, output_path: Path) -> pd.DataFrame:
    """Apply 19-code behavioral scheme to all responses."""
    print("Applying behavioral coding to all responses...")

    auto_coder = AutoCoder()
    coded_data = auto_coder.process_batch(
        responses=responses,
        output_path=str(output_path)
    )

    auto_coder.print_summary_report(coded_data)

    # Convert to DataFrame if not already
    if not isinstance(coded_data, pd.DataFrame):
        # Convert list of ResponseCoding objects to DataFrame
        rows = []
        for coding in coded_data:
            row = {
                'response_id': coding.response_id,
                'agent_name': coding.agent_name,
                'condition': coding.condition,
                'response_text': coding.response_text,
                'response_length': coding.response_length,
                'opp_count': coding.get_opp_count(),
                'esr_count': coding.get_esr_count(),
                'cos_count': coding.get_cos_count(),
                'ue_count': coding.get_ue_count()
            }
            rows.append(row)
        coded_data = pd.DataFrame(rows)

    return coded_data


def calculate_descriptive_stats(df: pd.DataFrame) -> dict:
    """Calculate descriptive statistics by condition."""
    stats = {}

    conditions = ['N', 'I', 'B', 'P', 'S']
    measures = ['opp_count', 'esr_count', 'cos_count', 'ue_count']

    for measure in measures:
        stats[measure] = {}
        for cond in conditions:
            cond_data = df[df['condition'] == cond][measure]
            stats[measure][cond] = {
                'mean': cond_data.mean(),
                'std': cond_data.std(),
                'n': len(cond_data)
            }

    # Aggregate measure
    df['total_codes'] = df['opp_count'] + df['esr_count'] + df['cos_count'] + df['ue_count']
    stats['total_codes'] = {}
    for cond in conditions:
        cond_data = df[df['condition'] == cond]['total_codes']
        stats['total_codes'][cond] = {
            'mean': cond_data.mean(),
            'std': cond_data.std(),
            'n': len(cond_data)
        }

    return stats


def calculate_effect_sizes(df: pd.DataFrame) -> dict:
    """Calculate Cohen's d effect sizes (S vs N)."""
    effect_sizes = {}

    null_data = df[df['condition'] == 'N']
    stress_data = df[df['condition'] == 'S']

    measures = ['opp_count', 'esr_count', 'cos_count', 'ue_count', 'total_codes']

    for measure in measures:
        null_vals = null_data[measure]
        stress_vals = stress_data[measure]

        pooled_std = np.sqrt((null_vals.var() + stress_vals.var()) / 2)

        if pooled_std > 0.001:
            cohens_d = (stress_vals.mean() - null_vals.mean()) / pooled_std
        else:
            cohens_d = 0.0

        effect_sizes[measure] = {
            'd': cohens_d,
            'null_mean': null_vals.mean(),
            'stress_mean': stress_vals.mean(),
            'difference': stress_vals.mean() - null_vals.mean()
        }

    return effect_sizes


def run_mixed_effects_analysis(df: pd.DataFrame) -> dict:
    """Run mixed-effects models for confirmatory analysis."""
    print("\nRunning mixed-effects models...")

    # Note: This requires R backend or statsmodels GEE
    # For now, return placeholder
    return {
        'model': 'Mixed-effects model (requires R/statsmodels)',
        'note': 'Use analysis.py MixedEffectsModels class for full implementation'
    }


def generate_figures(df: pd.DataFrame, output_dir: Path):
    """Generate publication-quality figures."""
    print("\nGenerating figures...")

    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1.2)

    # Figure 1: OPP counts by condition
    fig, ax = plt.subplots(figsize=(8, 6))

    conditions = ['N', 'I', 'B', 'P', 'S']
    condition_labels = ['Null', 'Info', 'Baseline', 'Positive', 'Negative']

    data_for_plot = []
    for cond in conditions:
        data_for_plot.append(df[df['condition'] == cond]['opp_count'].values)

    # Box plot with individual points
    bp = ax.boxplot(data_for_plot, labels=condition_labels, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')

    # Add individual points
    for i, cond in enumerate(conditions):
        y = df[df['condition'] == cond]['opp_count'].values
        x = np.random.normal(i+1, 0.04, size=len(y))
        ax.plot(x, y, 'o', alpha=0.3, color='darkblue', markersize=4)

    ax.set_xlabel('Condition')
    ax.set_ylabel('Output Protective Patterns (OPP) Count')
    ax.set_title('OPP Codes by Experimental Condition')

    plt.tight_layout()
    plt.savefig(output_dir / 'fig1_opp_by_condition.pdf', dpi=300)
    plt.savefig(output_dir / 'fig1_opp_by_condition.png', dpi=300)
    plt.close()

    # Figure 2: Effect sizes
    fig, ax = plt.subplots(figsize=(8, 6))

    effect_sizes = calculate_effect_sizes(df)
    measures = ['opp_count', 'esr_count', 'cos_count', 'ue_count']
    measure_labels = ['OPP', 'ESR', 'COS', 'UE']

    d_values = [effect_sizes[m]['d'] for m in measures]

    ax.barh(measure_labels, d_values, color=['green' if d > 0.5 else 'orange' if d > 0.3 else 'gray' for d in d_values])
    ax.axvline(x=0.3, color='orange', linestyle='--', label='Small effect (d=0.3)')
    ax.axvline(x=0.5, color='green', linestyle='--', label='Medium effect (d=0.5)')
    ax.set_xlabel("Cohen's d (Negative vs Null)")
    ax.set_ylabel('Behavioral Code Category')
    ax.set_title('Effect Sizes by Code Category')
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_dir / 'fig2_effect_sizes.pdf', dpi=300)
    plt.savefig(output_dir / 'fig2_effect_sizes.png', dpi=300)
    plt.close()

    print(f"Figures saved to {output_dir}")


def generate_summary_report(
    responses: list,
    df: pd.DataFrame,
    stats: dict,
    effect_sizes: dict,
    output_path: Path
):
    """Generate comprehensive summary report."""

    report = []
    report.append("="*80)
    report.append("FULL STUDY RESULTS SUMMARY")
    report.append("="*80)
    report.append("")

    # Dataset info
    report.append(f"Total responses: {len(responses)}")
    report.append(f"Agents: {df['agent_name'].nunique()}")
    report.append(f"Conditions: {df['condition'].nunique()}")
    report.append("")

    # Descriptive statistics
    report.append("DESCRIPTIVE STATISTICS")
    report.append("-"*80)
    report.append("\nOutput Protective Patterns (OPP):")
    for cond in ['N', 'I', 'B', 'P', 'S']:
        s = stats['opp_count'][cond]
        report.append(f"  {cond}: M={s['mean']:.3f}, SD={s['std']:.3f}, n={s['n']}")

    report.append("\nTotal Behavioral Codes:")
    for cond in ['N', 'I', 'B', 'P', 'S']:
        s = stats['total_codes'][cond]
        report.append(f"  {cond}: M={s['mean']:.3f}, SD={s['std']:.3f}, n={s['n']}")

    report.append("")

    # Effect sizes
    report.append("EFFECT SIZES (Negative Stress vs Null)")
    report.append("-"*80)
    for measure, es in effect_sizes.items():
        report.append(f"\n{measure}:")
        report.append(f"  Null mean: {es['null_mean']:.3f}")
        report.append(f"  Stress mean: {es['stress_mean']:.3f}")
        report.append(f"  Difference: {es['difference']:.3f}")
        report.append(f"  Cohen's d: {es['d']:.3f}")

        if abs(es['d']) < 0.2:
            interp = "negligible"
        elif abs(es['d']) < 0.5:
            interp = "small"
        elif abs(es['d']) < 0.8:
            interp = "medium"
        else:
            interp = "large"
        report.append(f"  Interpretation: {interp}")

    report.append("")
    report.append("="*80)
    report.append("VERDICT")
    report.append("="*80)

    overall_d = effect_sizes['total_codes']['d']
    opp_d = effect_sizes['opp_count']['d']

    if overall_d > 0.5 or opp_d > 0.5:
        report.append("✓ MANIPULATION VALIDATED")
        report.append(f"  Overall effect size: d={overall_d:.3f}")
        report.append(f"  OPP effect size: d={opp_d:.3f}")
        report.append("  → Confirms pilot findings")
        report.append("  → Ready for publication")
    elif overall_d > 0.3 or opp_d > 0.3:
        report.append("⚠ WEAK EFFECT DETECTED")
        report.append(f"  Overall effect size: d={overall_d:.3f}")
        report.append(f"  OPP effect size: d={opp_d:.3f}")
        report.append("  → Weaker than pilot (d=0.534)")
        report.append("  → May need larger sample or stronger manipulation")
    else:
        report.append("✗ MANIPULATION FAILED")
        report.append(f"  Overall effect size: d={overall_d:.3f}")
        report.append(f"  OPP effect size: d={opp_d:.3f}")
        report.append("  → Effect not replicated from pilot")
        report.append("  → Reconsider research approach")

    report.append("")
    report.append("="*80)

    # Write to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))

    # Also print to console
    print('\n'.join(report))


def main():
    """Main analysis pipeline."""

    # Configuration
    data_dir = Path("larger_pilot_results/data/raw")
    output_dir = Path("larger_pilot_results/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*80)
    print("FULL STUDY ANALYSIS PIPELINE")
    print("="*80)
    print()

    # Step 1: Extract responses
    print("Step 1: Extracting responses from JSONL logs...")
    responses = extract_responses_from_jsonl(data_dir)
    print(f"  Extracted {len(responses)} responses")
    print()

    # Step 2: Apply behavioral coding
    print("Step 2: Applying behavioral coding...")
    coded_path = output_dir / "coded_responses.csv"
    df = apply_behavioral_coding(responses, coded_path)
    print()

    # Step 3: Calculate descriptive statistics
    print("Step 3: Calculating descriptive statistics...")
    stats = calculate_descriptive_stats(df)
    print()

    # Step 4: Calculate effect sizes
    print("Step 4: Calculating effect sizes...")
    effect_sizes = calculate_effect_sizes(df)
    print()

    # Step 5: Mixed-effects models (placeholder)
    print("Step 5: Mixed-effects models...")
    mixed_results = run_mixed_effects_analysis(df)
    print("  (Use analysis.py for full implementation)")
    print()

    # Step 6: Generate figures
    print("Step 6: Generating figures...")
    generate_figures(df, output_dir)
    print()

    # Step 7: Generate summary report
    print("Step 7: Generating summary report...")
    summary_path = output_dir / "RESULTS_SUMMARY.txt"
    generate_summary_report(responses, df, stats, effect_sizes, summary_path)
    print()

    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"Results saved to: {output_dir}")
    print(f"  - coded_responses.csv")
    print(f"  - fig1_opp_by_condition.pdf/png")
    print(f"  - fig2_effect_sizes.pdf/png")
    print(f"  - RESULTS_SUMMARY.txt")
    print()


if __name__ == '__main__':
    main()
