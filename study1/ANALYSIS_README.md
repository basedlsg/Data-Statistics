# Study 1: Statistical Analysis Pipeline

Complete statistical analysis implementation for "Agent Stress Behavior" research.

## Overview

This analysis pipeline implements rigorous statistical methods for AI agent behavioral research, addressing:
- **Pseudo-replication**: Proper aggregation and multilevel modeling
- **Nested data structures**: Random effects for agents, sessions, and personas
- **Effect size reporting**: Cohen's d with confidence intervals
- **Power analysis**: Achieved and a priori calculations
- **Causal inference**: Mediation and Granger causality tests
- **Publication-quality visualizations**: APA-style figures

## Architecture

### Five Core Classes

1. **PowerAnalysis**
   - Calculate achieved power from observed data
   - A priori sample size calculation
   - Effect size estimation (Cohen's d, Hedges' g)
   - Design effect adjustment for clustered data
   - Equivalence testing (TOST)

2. **MixedEffectsModels**
   - lmer-style mixed-effects models
   - Random effects: agents, runs, personas
   - Multiple families: Gaussian, Poisson, Negative Binomial, Binomial
   - R backend (pymer4/lme4) or Python (statsmodels GEE)
   - Intraclass correlation calculation
   - Model comparison via likelihood ratio tests

3. **PseudoReplicationHandler**
   - Aggregate interaction → run → agent levels
   - Validate independence assumptions
   - Calculate effective sample size
   - Check temporal autocorrelation
   - Design effect calculation

4. **CausalAnalysis**
   - Granger causality tests (temporal precedence)
   - Mediation analysis (Sobel test)
   - Structural equation modeling (path analysis)
   - Instrumental variables (2SLS) - placeholder

5. **VisualizationGenerator**
   - Condition comparison plots
   - Effect size forest plots
   - Diagnostic plots (Q-Q, residuals)
   - Interaction plots
   - Publication-ready formatting (PDF, 300 DPI)

## Installation

```bash
# Install required packages
pip install -r requirements.txt

# Optional: Install R integration for mixed models
pip install rpy2 pymer4
# Requires R with lme4 package installed
```

## Quick Start

### Basic Usage

```python
from analysis import run_complete_analysis

# Run full analysis pipeline
results = run_complete_analysis(
    data_path='data/interactions.csv',
    output_dir='results/',
    alpha=0.05,
    use_r=False  # Set True to use R backend
)
```

### Individual Components

```python
from analysis import (
    PowerAnalysis,
    MixedEffectsModels,
    PseudoReplicationHandler,
    CausalAnalysis,
    VisualizationGenerator
)

# 1. Power Analysis
analyzer = PowerAnalysis(alpha=0.05)
effect = analyzer.calculate_cohens_d(group1, group2)
power = analyzer.calculate_achieved_power(effect.cohens_d, n1, n2)

# 2. Mixed-Effects Model
modeler = MixedEffectsModels(use_r=False)
model = modeler.fit_model(
    formula="mistakes ~ condition + (1|agent_id)",
    data=run_level_data,
    family='poisson'
)

# 3. Handle Pseudo-Replication
handler = PseudoReplicationHandler()
agent_data = handler.aggregate_to_agent_level(
    interaction_data,
    outcome_vars=['mistakes', 'help_requests']
)
eff_n = handler.calculate_effective_n(interaction_data, 'mistakes')

# 4. Mediation Analysis
causal = CausalAnalysis()
mediation = causal.mediation_analysis(
    data,
    treatment='condition',
    mediator='defensive_language',
    outcome='mistakes'
)

# 5. Visualization
viz = VisualizationGenerator()
fig = viz.condition_comparison(
    agent_data,
    outcome='mistakes_mean',
    condition_var='condition',
    save_path='figures/comparison.pdf'
)
```

## Examples

Run comprehensive demonstrations:

```bash
python example_usage.py
```

This will demonstrate:
1. Power analysis and effect size calculation
2. Mixed-effects model fitting
3. Pseudo-replication handling
4. Mediation analysis
5. Visualization generation

## Data Format

### Input Data Structure

**Interaction-level data** (long format):

```csv
agent_id,persona,condition,run_id,interaction_num,mistakes,help_request,defensive_language,completion_time
1,Thoth,baseline,0,1,0,0,0,3.2
1,Thoth,baseline,0,2,1,0,0,2.8
1,Thoth,baseline,0,3,0,1,0,4.1
...
```

Required columns:
- `agent_id`: Unique agent identifier
- `condition`: Experimental condition (e.g., 'baseline', 'stress')
- `run_id`: Replication identifier within agent
- Outcome variables (e.g., `mistakes`, `help_request`)

### Output Structure

```
results/
├── analysis_results.json          # Complete results summary
├── model_results_table.csv        # APA-style coefficient table
├── condition_comparison.pdf       # Bar plot with error bars
└── effect_size.pdf                # Forest plot
```

## Statistical Methodology

### Addressing Pseudo-Replication

**Problem**: 4,500 interactions from 30 agents are NOT 4,500 independent observations.

**Solution**:
1. Calculate ICC to quantify clustering
2. Aggregate to agent level for simple analyses
3. Use mixed-effects models for full data
4. Report effective sample size

```python
# Calculate effective n
handler = PseudoReplicationHandler()
eff_n = handler.calculate_effective_n(data, 'mistakes')

print(f"Total observations: {eff_n['n_total']}")
print(f"Effective n: {eff_n['n_effective']}")
print(f"ICC: {eff_n['icc']:.3f}")
```

### Mixed-Effects Model Specification

**Within-subjects design** (Study 1):

```R
# R formula notation
mistakes ~ condition + (1|agent_id) + (1|agent_id:run_id)
```

Components:
- `condition`: Fixed effect (treatment)
- `(1|agent_id)`: Random intercept for agent
- `(1|agent_id:run_id)`: Random intercept for run nested in agent

### Power Analysis

**A priori** (planning):
```python
analyzer = PowerAnalysis(alpha=0.05)
required_n = analyzer.calculate_required_n(
    effect_size=0.8,  # Large effect
    power=0.90        # High power
)
```

**Post-hoc** (achieved):
```python
effect = analyzer.calculate_cohens_d(group1, group2)
power = analyzer.calculate_achieved_power(
    effect.cohens_d, len(group1), len(group2)
)
```

### Effect Size Interpretation

Following Cohen (1988):

| Cohen's d | Interpretation |
|-----------|----------------|
| 0.2       | Small          |
| 0.5       | Medium         |
| 0.8       | Large          |
| 1.2+      | Very Large     |

## Advanced Features

### 1. Model Comparison

```python
modeler = MixedEffectsModels()

# Fit nested models
model_null = modeler.fit_model("mistakes ~ 1 + (1|agent_id)", data)
model_full = modeler.fit_model("mistakes ~ condition + (1|agent_id)", data)

# Compare
comparison = modeler.model_comparison(model_null, model_full)
print(f"Prefer full model: {comparison['prefer_full_model']}")
```

### 2. Equivalence Testing

Test whether effect is practically equivalent to zero:

```python
equiv = analyzer.equivalence_test(
    group1, group2,
    low_bound=-0.5,
    high_bound=0.5
)
print(f"Equivalent: {equiv['equivalent']}")
```

### 3. Mediation Analysis

Test indirect effects (X → M → Y):

```python
mediation = causal.mediation_analysis(
    data,
    treatment='condition',
    mediator='defensive_language',
    outcome='mistakes'
)
print(f"Indirect effect: {mediation['indirect_effect']:.3f}")
print(f"Proportion mediated: {mediation['proportion_mediated']:.2%}")
```

### 4. Granger Causality

Test temporal precedence:

```python
gc = causal.granger_causality(
    time_series_data,
    cause_var='stress_level',
    effect_var='mistakes',
    max_lags=5
)
print(f"Granger causes: {gc['granger_causes']}")
```

## Output Formats

### APA-Style Results Table

```
                      Coefficient    SE     t  p_formatted  sig
Intercept                   2.134  0.156  13.7       < .001  ***
condition[T.stress]         0.847  0.221   3.8        .002   **
```

### JSON Results Summary

```json
{
  "sample_size": {
    "n_agents": 30,
    "n_effective": 127,
    "icc": 0.153,
    "design_effect": 2.34
  },
  "effect_sizes": {
    "cohens_d": 0.843,
    "ci_lower": 0.412,
    "ci_upper": 1.274,
    "interpretation": "large"
  },
  "model": {
    "formula": "mistakes ~ condition + (1|agent_id)",
    "coefficients": {...},
    "p_values": {...}
  }
}
```

## Testing

Run unit tests:

```bash
pytest tests/ -v --cov=analysis
```

## Troubleshooting

### Issue: "pymer4 not available"

**Solution**: Install R integration or use statsmodels backend:
```python
modeler = MixedEffectsModels(use_r=False)
```

### Issue: Model convergence failure

**Solutions**:
1. Simplify random effects structure
2. Aggregate to higher level (agent instead of run)
3. Use GEE instead of mixed-effects model

### Issue: Low effective sample size

**Interpretation**: High ICC indicates strong clustering. This is expected with agent-level effects.

**Actions**:
1. Report ICC prominently
2. Use multilevel models (not simple t-tests)
3. Consider increasing number of independent agents

## References

### Statistical Methods

- **Power Analysis**: Faul et al. (2009). G*Power 3.1 manual.
- **Effect Sizes**: Cohen (1988). Statistical power analysis for the behavioral sciences.
- **Mixed Models**: Snijders & Bosker (2012). Multilevel analysis (2nd ed.).
- **Pseudo-replication**: Hurlbert (1984). Ecology, 65(1), 187-197.
- **ICC**: Kish (1965). Survey sampling.

### Implementation

- **statsmodels**: Seabold & Perktold (2010). Statsmodels.
- **pymer4**: Jolly (2018). pymer4: Bridging R and Python.
- **lme4** (R): Bates et al. (2015). lme4: Linear mixed-effects models.

## Citation

If you use this analysis pipeline, please cite:

```bibtex
@software{agent_stress_analysis,
  title={Statistical Analysis Pipeline for AI Agent Behavioral Research},
  author={Statistical Analysis Agent},
  year={2025},
  version={1.0},
  url={https://github.com/your-repo/Data-Statistics}
}
```

## License

MIT License - See LICENSE file for details.

## Contact

For questions or issues, please open a GitHub issue or contact the research team.

---

**Last Updated**: 2025-11-20
**Version**: 1.0
**Status**: Production-ready
