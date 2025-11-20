#!/usr/bin/env python3
"""
Example Usage of Statistical Analysis Pipeline

This script demonstrates how to use all analysis classes with synthetic data.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from analysis import (
    PowerAnalysis,
    MixedEffectsModels,
    PseudoReplicationHandler,
    CausalAnalysis,
    VisualizationGenerator
)


def generate_synthetic_data(
    n_agents: int = 30,
    n_runs: int = 3,
    n_interactions: int = 50,
    effect_size: float = 0.8,
    icc: float = 0.15
) -> pd.DataFrame:
    """
    Generate synthetic data for demonstration.

    Parameters
    ----------
    n_agents : int
        Number of agents (15 per condition)
    n_runs : int
        Runs per agent (within-subjects)
    n_interactions : int
        Interactions per run
    effect_size : float
        Cohen's d for condition effect
    icc : float
        Intraclass correlation (clustering)

    Returns
    -------
    pd.DataFrame
        Synthetic interaction-level data
    """
    np.random.seed(42)

    data = []

    conditions = ['baseline', 'positive', 'negative']
    personas = ['Thoth', 'Seshat', 'Maat', 'Anubis', 'Ptah']

    agent_id = 0

    for persona in personas:
        for agent_num in range(n_agents // 5):  # 6 agents per persona
            agent_id += 1

            # Agent-specific random effect
            agent_effect = np.random.normal(0, icc * 5)

            for run_num in range(n_runs):
                for condition in conditions:
                    # Condition effect
                    if condition == 'baseline':
                        condition_effect = 0
                    elif condition == 'positive':
                        condition_effect = effect_size * 0.5  # Medium stress
                    else:  # negative
                        condition_effect = effect_size  # High stress

                    # Generate interactions
                    for interaction_num in range(n_interactions):
                        # Baseline mistake rate
                        base_rate = 2.0

                        # Add effects
                        mistake_rate = base_rate + condition_effect + agent_effect

                        # Generate count (Poisson)
                        mistakes = np.random.poisson(max(0, mistake_rate))

                        # Help requests (negatively correlated with mistakes in stress)
                        help_prob = 0.15
                        if condition == 'negative':
                            help_prob = 0.08  # Reduced help-seeking under negative stress

                        help_request = np.random.binomial(1, help_prob)

                        # Defensive language (increases with stress)
                        defensive_prob = 0.10
                        if condition in ['positive', 'negative']:
                            defensive_prob = 0.25

                        defensive = np.random.binomial(1, defensive_prob)

                        # Task completion time
                        completion_time = np.random.exponential(4.0)
                        if condition != 'baseline':
                            completion_time *= 1.2  # Slower under stress

                        data.append({
                            'agent_id': agent_id,
                            'persona': persona,
                            'condition': condition,
                            'run_id': run_num,
                            'interaction_num': interaction_num,
                            'mistakes': 1 if mistakes > 0 else 0,
                            'mistake_count': mistakes,
                            'help_request': help_request,
                            'defensive_language': defensive,
                            'completion_time': completion_time,
                            'timestamp': interaction_num * 3600  # Hourly
                        })

    return pd.DataFrame(data)


def example_power_analysis():
    """Example 1: Power Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 1: POWER ANALYSIS")
    print("="*70)

    analyzer = PowerAnalysis(alpha=0.05)

    # Simulate two groups
    np.random.seed(42)
    baseline = np.random.normal(2.0, 1.5, 30)
    stress = np.random.normal(3.5, 1.8, 30)

    # Calculate effect size
    effect = analyzer.calculate_cohens_d(baseline, stress)
    print(f"\nCohen's d: {effect.cohens_d:.3f} [{effect.ci_lower:.3f}, {effect.ci_upper:.3f}]")
    print(f"Interpretation: {effect.interpretation}")

    # Achieved power
    power = analyzer.calculate_achieved_power(
        effect.cohens_d,
        len(baseline),
        len(stress)
    )
    print(f"\nAchieved power: {power.achieved_power:.3f}")
    print(f"Power adequate (≥0.80): {power.power_adequate}")

    # Required sample size
    required_n = analyzer.calculate_required_n(
        effect_size=0.5,  # Medium effect
        power=0.80
    )
    print(f"\nRequired n per group for d=0.5, power=0.80: {required_n}")

    # Equivalence test
    equiv = analyzer.equivalence_test(baseline, stress)
    print(f"\nEquivalence test (bounds ±0.5):")
    print(f"  Equivalent: {equiv['equivalent']}")
    print(f"  p-value: {equiv['p_tost']:.4f}")


def example_mixed_effects():
    """Example 2: Mixed-Effects Models"""
    print("\n" + "="*70)
    print("EXAMPLE 2: MIXED-EFFECTS MODELS")
    print("="*70)

    # Generate data
    data = generate_synthetic_data(n_agents=30, n_runs=3, n_interactions=50)

    print(f"\nData: {len(data)} interactions")
    print(f"Agents: {data['agent_id'].nunique()}")
    print(f"Conditions: {data['condition'].unique()}")

    # Aggregate to run level for count outcome
    run_data = data.groupby(['condition', 'agent_id', 'persona', 'run_id']).agg({
        'mistakes': 'sum',
        'help_request': 'sum',
        'defensive_language': 'sum'
    }).reset_index()

    print(f"\nRun-level data: {len(run_data)} runs")

    # Fit mixed-effects model
    modeler = MixedEffectsModels(use_r=False)  # Use statsmodels

    model = modeler.fit_model(
        formula="mistakes ~ condition + (1|agent_id)",
        data=run_data,
        family='poisson'
    )

    print(f"\nModel: {model.model_type}")
    print(f"ICC: {model.icc:.3f}")
    print(f"AIC: {model.aic:.1f}")

    print("\nFixed Effects:")
    table = model.to_table()
    print(table[['Coefficient', 'SE', 't', 'p_formatted', 'sig']].to_string())


def example_pseudo_replication():
    """Example 3: Pseudo-Replication Handling"""
    print("\n" + "="*70)
    print("EXAMPLE 3: PSEUDO-REPLICATION HANDLING")
    print("="*70)

    # Generate data
    data = generate_synthetic_data(n_agents=30, n_runs=3, n_interactions=50)

    handler = PseudoReplicationHandler()

    # Calculate effective sample size
    eff_n = handler.calculate_effective_n(data, 'mistakes')

    print(f"\nSample Size Analysis:")
    print(f"  Total observations: {eff_n['n_total']}")
    print(f"  Number of clusters (agents): {eff_n['n_clusters']}")
    print(f"  Average cluster size: {eff_n['avg_cluster_size']:.1f}")
    print(f"  ICC: {eff_n['icc']:.3f}")
    print(f"  Design effect: {eff_n['design_effect']:.2f}")
    print(f"  Effective sample size: {eff_n['n_effective']}")
    print(f"  Efficiency loss: {eff_n['efficiency_loss']*100:.1f}%")

    # Aggregate to agent level
    agent_data = handler.aggregate_to_agent_level(
        data,
        outcome_vars=['mistakes', 'help_request', 'defensive_language']
    )

    print(f"\nAgent-level aggregation:")
    print(f"  Original: {len(data)} observations")
    print(f"  Aggregated: {len(agent_data)} agents")
    print(f"  Pseudo-replication solved: ✓")

    # Check autocorrelation
    if 'interaction_num' in data.columns:
        autocorr = handler.check_autocorrelation(
            data,
            outcome='mistakes',
            time_var='interaction_num'
        )

        print(f"\nAutocorrelation check:")
        print(f"  Agents with significant autocorrelation: "
              f"{autocorr['significant_autocorr'].sum()}/{len(autocorr)}")
        print(f"  Mean lag-1 ACF: {autocorr['acf_lag1'].mean():.3f}")


def example_causal_analysis():
    """Example 4: Causal Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 4: CAUSAL ANALYSIS - MEDIATION")
    print("="*70)

    # Generate data with mediation structure
    np.random.seed(42)
    n = 200

    # Treatment -> Mediator -> Outcome
    treatment = np.random.binomial(1, 0.5, n)
    mediator = 2.0 + 1.5 * treatment + np.random.normal(0, 1, n)
    outcome = 1.0 + 0.5 * treatment + 0.8 * mediator + np.random.normal(0, 1.5, n)

    data = pd.DataFrame({
        'treatment': treatment,
        'mediator': mediator,
        'outcome': outcome
    })

    # Run mediation analysis
    analyzer = CausalAnalysis()

    mediation = analyzer.mediation_analysis(
        data,
        treatment='treatment',
        mediator='mediator',
        outcome='outcome'
    )

    print("\nMediation Analysis Results:")
    print(f"  Total effect (c): {mediation['total_effect']:.3f}")
    print(f"  Direct effect (c'): {mediation['direct_effect']:.3f}")
    print(f"  Indirect effect (a*b): {mediation['indirect_effect']:.3f}")
    print(f"  Proportion mediated: {mediation['proportion_mediated']*100:.1f}%")
    print(f"  p-value (Sobel test): {mediation['p_indirect']:.4f}")
    print(f"  Significant mediation: {mediation['significant_mediation']}")


def example_visualization():
    """Example 5: Visualization"""
    print("\n" + "="*70)
    print("EXAMPLE 5: VISUALIZATION")
    print("="*70)

    # Generate data
    data = generate_synthetic_data(n_agents=30, n_runs=3, n_interactions=50)

    # Aggregate to agent level
    handler = PseudoReplicationHandler()
    agent_data = handler.aggregate_to_agent_level(
        data,
        outcome_vars=['mistakes', 'help_request']
    )

    # Create visualizations
    viz = VisualizationGenerator()

    print("\nCreating figures...")

    # 1. Condition comparison
    fig1 = viz.condition_comparison(
        agent_data,
        outcome='mistakes_mean',
        condition_var='condition',
        ylabel='Mean Mistakes per Run',
        title='Mistakes by Condition'
    )
    print("  ✓ Condition comparison plot created")

    # 2. Effect sizes
    analyzer = PowerAnalysis()

    baseline = agent_data[agent_data['condition'] == 'baseline']['mistakes_mean'].values
    positive = agent_data[agent_data['condition'] == 'positive']['mistakes_mean'].values
    negative = agent_data[agent_data['condition'] == 'negative']['mistakes_mean'].values

    effect1 = analyzer.calculate_cohens_d(baseline, positive)
    effect2 = analyzer.calculate_cohens_d(baseline, negative)

    fig2 = viz.effect_size_plot(
        [effect1, effect2],
        ['Positive vs. Baseline', 'Negative vs. Baseline'],
        title='Effect Sizes: Stress Conditions'
    )
    print("  ✓ Effect size forest plot created")

    # Note: Figures are created but not saved unless save_path is provided
    print("\n(Figures not saved - provide save_path to save)")


def main():
    """Run all examples."""
    print("="*70)
    print("STATISTICAL ANALYSIS PIPELINE - DEMONSTRATION")
    print("Study 1: Agent Stress Behavior")
    print("="*70)

    try:
        example_power_analysis()
        example_mixed_effects()
        example_pseudo_replication()
        example_causal_analysis()
        example_visualization()

        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*70)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
