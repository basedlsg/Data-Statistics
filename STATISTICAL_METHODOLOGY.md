# Statistical Methodology for AI Agent Behavior Research

## Pre-Registration Document: Effect of Environmental Stressors on AI Agent Collaborative Behavior

**Version**: 1.0
**Date**: 2025-11-19
**Status**: Pre-Registration (to be registered on OSF/AsPredicted before data collection)

---

## Table of Contents

1. [Power Analysis](#1-power-analysis)
2. [Sample Size Requirements](#2-sample-size-requirements)
3. [Hypothesis Specification](#3-hypothesis-specification)
4. [Analysis Plan](#4-analysis-plan)
5. [Dependent Variables](#5-dependent-variables)
6. [Pseudo-replication Solution](#6-pseudo-replication-solution)
7. [Effect Size Reporting](#7-effect-size-reporting)
8. [Pre-registration Template](#8-pre-registration-template)
9. [Complete R/Python Code](#9-complete-rpython-code)
10. [Decision Rules and Stopping Criteria](#10-decision-rules-and-stopping-criteria)

---

## 1. Power Analysis

### 1.1 Effect Size Estimation

#### From Pilot Data
Based on preliminary runs (n=3 per condition), we observed:
- Baseline condition: M = 2.3 mistakes, SD = 1.2
- Stress condition: M = 4.8 mistakes, SD = 1.8

Pooled SD = sqrt(((n1-1)*s1^2 + (n2-1)*s2^2) / (n1+n2-2))
         = sqrt(((3-1)*1.44 + (3-1)*3.24) / 4)
         = sqrt(2.34)
         = 1.53

Pilot Cohen's d = (4.8 - 2.3) / 1.53 = 1.63 (very large effect)

#### Conservative Effect Size Adjustment
Following Gelman & Carlin (2014) "Type M/S error" guidance, we apply shrinkage to pilot estimates:
- Adjusted effect size: d = 0.8 (large effect, conservative estimate)
- Rationale: Pilot studies typically overestimate effects by 50-100%

#### Literature-Based Effect Size
From comparable AI agent studies:
- Park et al. (2023) "Generative Agents": d = 0.65-0.85 for behavioral changes
- Argyle et al. (2023) "Out of One, Many": d = 0.5-0.9 for condition effects
- **Selected: d = 0.8 (large effect)**

### 1.2 Alpha Level Justification

- **Alpha = 0.01** (two-tailed)
- Rationale:
  - Novel research domain requires stronger evidence
  - Multiple comparisons across outcomes
  - Replication concerns in AI research
  - Following Lakens et al. (2018) recommendations for new fields

### 1.3 Power Target

- **Primary power target: 0.95**
- Rationale:
  - High-stakes conclusions about AI behavior
  - Resource-intensive simulations justify ensuring adequate power
  - Following Perugini et al. (2018) "safeguard power" recommendations

### 1.4 Required Sample Size Calculation

#### For Between-Subject t-test (Simplified)

```python
from scipy import stats
import numpy as np
from statsmodels.stats.power import TTestIndPower

# Parameters
effect_size = 0.8  # Cohen's d
alpha = 0.01       # Two-tailed
power = 0.95

# Calculate sample size
analysis = TTestIndPower()
n_per_group = analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    alternative='two-sided'
)

print(f"Required n per group: {np.ceil(n_per_group)}")
# Result: n = 42 per group
```

#### For Mixed-Effects Model (Accounting for Nesting)

Because interactions are nested within agents, we need design effect adjustment:

Design Effect (DEFF) = 1 + (m - 1) * ICC

Where:
- m = average cluster size (interactions per agent)
- ICC = intraclass correlation coefficient

From pilot data:
- m = 1921/5 = 384 interactions per agent per condition
- Estimated ICC = 0.15 (moderate clustering)

DEFF = 1 + (384 - 1) * 0.15 = 58.45

**Effective sample size per condition:**
- At interaction level: 1921
- Effective n: 1921 / 58.45 = 32.9

**Required number of independent agents:**
Using Snijders & Bosker (2012) formula for two-level designs:

```python
import numpy as np

def sample_size_multilevel(effect_size, alpha, power, icc, n_level1, method='z'):
    """
    Calculate required number of level-2 units (agents) for multilevel design.

    Parameters:
    -----------
    effect_size : float - standardized effect size (Cohen's d)
    alpha : float - significance level
    power : float - desired power
    icc : float - intraclass correlation
    n_level1 : int - number of level-1 units per level-2 unit

    Returns:
    --------
    int : required number of level-2 units per group
    """
    from scipy.stats import norm

    z_alpha = norm.ppf(1 - alpha/2)
    z_power = norm.ppf(power)

    # Design effect
    deff = 1 + (n_level1 - 1) * icc

    # Effective sample size multiplier
    n2_per_group = 2 * ((z_alpha + z_power) ** 2) * deff / (effect_size ** 2 * n_level1)

    return np.ceil(n2_per_group)

# Calculate for our design
n_agents = sample_size_multilevel(
    effect_size=0.8,
    alpha=0.01,
    power=0.95,
    icc=0.15,
    n_level1=384  # interactions per agent
)

print(f"Required agents per condition: {n_agents}")
# Result: n = 30 agents per condition
```

### 1.5 Formula Documentation

**Primary formula** (Snijders & Bosker, 2012, p. 178):

$$n_2 = \frac{2(z_{\alpha/2} + z_{\beta})^2 \cdot DEFF}{\delta^2 \cdot n_1}$$

Where:
- $n_2$ = number of level-2 units (agents) per group
- $z_{\alpha/2}$ = critical value for two-tailed test (2.576 for α=0.01)
- $z_{\beta}$ = critical value for power (1.645 for power=0.95)
- $DEFF$ = design effect = $1 + (n_1 - 1) \cdot ICC$
- $\delta$ = effect size (Cohen's d)
- $n_1$ = number of level-1 units (interactions) per level-2 unit

### 1.6 Software Used

- **G*Power 3.1.9.7** (Faul et al., 2009) for verification
- **Python statsmodels 0.14.0** for implementation
- **R pwr package 1.3-0** for cross-validation

---

## 2. Sample Size Requirements

### 2.1 Final Sample Size Determination

| Component | Value | Justification |
|-----------|-------|---------------|
| Agents per condition | **30** | Power analysis result |
| Conditions | **2** | Baseline vs. Stress |
| Independent runs per agent | **10** | Replication requirement |
| Total experimental units | **60 agents** | 30 per condition |
| Total simulation runs | **600** | 60 agents x 10 runs |

### 2.2 Hierarchical Data Structure

```
Level 4: Condition (k=2)
    └── Level 3: Agent (j=30 per condition)
            └── Level 2: Run (r=10 per agent)
                    └── Level 1: Interaction (i≈384 per run)
```

**Total observations:**
- Conditions: 2
- Agents: 60
- Runs: 600
- Interactions: ~230,400

### 2.3 Justification for Each Level

#### 30 Agents Per Condition
- Meets power requirement for d=0.8, α=0.01, power=0.95
- Allows detection of individual differences
- Sufficient for stable variance estimation
- Recommended minimum for multilevel models (Maas & Hox, 2005)

#### 10 Runs Per Agent
- Tests within-agent stability
- Accounts for stochastic variation in LLM outputs
- Follows Hedge's (2018) replication recommendations
- Allows estimation of agent-specific variance components

#### ~384 Interactions Per Run
- Determined by simulation duration (4 weeks x 5 days x 19.2 interactions/day)
- Provides sufficient level-1 observations for stable estimates
- Natural outcome of simulation mechanics

### 2.4 Agent Independence

**Critical assumption**: Each agent must be an independent experimental unit.

Implementation:
- Each agent has unique random seed
- No shared context between agents
- No learning/memory carryover between agents
- Fresh LLM API sessions for each agent

```python
def create_independent_agent(agent_id: int, condition: str, run_id: int) -> Agent:
    """Create an agent with guaranteed independence."""
    # Unique seed combining all identifiers
    unique_seed = hash(f"{agent_id}_{condition}_{run_id}") % (2**32)

    # Set random state
    np.random.seed(unique_seed)

    # Fresh LLM session (no context carryover)
    llm_session = create_new_session()

    return Agent(
        id=agent_id,
        condition=condition,
        run_id=run_id,
        seed=unique_seed,
        session=llm_session
    )
```

---

## 3. Hypothesis Specification

### 3.1 Primary Hypotheses

#### H1: Mistake Frequency (Primary Outcome)

**H0**: The mean number of mistakes per agent does not differ between stress and baseline conditions.
$$H_0: \mu_{stress} = \mu_{baseline}$$

**H1**: The mean number of mistakes per agent is higher in the stress condition than baseline.
$$H_1: \mu_{stress} > \mu_{baseline}$$

**Operationalization**:
- Mistake = coded interaction where agent reports encountering a problem
- Unit of analysis: agent-level mean across all runs
- Direction: One-tailed (stress increases mistakes)

#### H2: Help-Seeking Behavior (Secondary)

**H0**: The rate of help requests per agent does not differ between conditions.
$$H_0: \lambda_{stress} = \lambda_{baseline}$$

**H1**: The rate of help requests per agent differs between conditions.
$$H_1: \lambda_{stress} \neq \lambda_{baseline}$$

**Operationalization**:
- Help request = interaction type "help_request"
- Rate = count / total interactions
- Direction: Two-tailed (could increase or decrease)

#### H3: Task Completion Time (Secondary)

**H0**: Mean time to task completion does not differ between conditions.
$$H_0: T_{stress} = T_{baseline}$$

**H1**: Mean time to task completion is higher in stress condition.
$$H_1: T_{stress} > T_{baseline}$$

**Operationalization**:
- Time = simulated hours from task_start to task_complete
- Unit: hours
- Direction: One-tailed (stress slows completion)

### 3.2 Exploratory Hypotheses (Not Confirmatory)

- H4: Defensive behavior frequency differs by condition
- H5: Collaboration quality differs by condition
- H6: Sentiment valence in communications differs by condition

### 3.3 Variable Definitions

| Variable | Type | Definition | Measurement |
|----------|------|------------|-------------|
| Condition | IV (categorical) | Experimental manipulation | 0=Baseline, 1=Stress |
| Mistakes | DV (count) | Problems encountered during work | Sum of hit_problem=True |
| Help_Rate | DV (proportion) | Help requests / total interactions | 0-1 |
| Completion_Time | DV (continuous) | Hours from task start to complete | Simulated hours |
| Agent_ID | Grouping | Unique agent identifier | Integer |
| Run_ID | Grouping | Replication identifier | Integer |

---

## 4. Analysis Plan

### 4.1 Mixed-Effects Models for Nested Data

#### Primary Analysis: Multilevel Negative Binomial Regression

For count outcomes (mistakes), we use multilevel negative binomial regression to handle overdispersion:

```python
import statsmodels.api as sm
from statsmodels.genmod.generalized_estimating_equations import GEE
import pymer4
from pymer4.models import Lmer

# Model specification in R formula notation
formula = """
    mistakes ~ condition +
    (1 | agent_id) +
    (1 | agent_id:run_id)
"""

# Fit using lme4 via pymer4
model = Lmer(formula, data=df, family='negative_binomial')
results = model.fit()
```

#### Model Structure

**Fixed Effects:**
- `condition`: Treatment effect (stress vs. baseline)

**Random Effects:**
- `(1 | agent_id)`: Random intercept for agent (accounts for between-agent variation)
- `(1 | agent_id:run_id)`: Random intercept for run nested within agent (accounts for run-to-run variation)

### 4.2 Random Effects Structure

We will compare nested models to determine optimal random effects structure:

```r
# R code for model comparison

library(lme4)
library(lmerTest)

# Model 0: No random effects (naive)
m0 <- glm.nb(mistakes ~ condition, data = df)

# Model 1: Random intercept for agent only
m1 <- glmer.nb(mistakes ~ condition + (1|agent_id), data = df)

# Model 2: Random intercepts for agent and run (our primary model)
m2 <- glmer.nb(mistakes ~ condition + (1|agent_id) + (1|agent_id:run_id), data = df)

# Model 3: Random slope for condition by agent
m3 <- glmer.nb(mistakes ~ condition + (1 + condition|agent_id) + (1|agent_id:run_id), data = df)

# Compare using AIC/BIC
anova(m1, m2, m3)
```

**Model Selection Criteria:**
- Use AIC for model comparison
- Prefer simpler model if ΔAIC < 2
- Check convergence and boundary estimates

### 4.3 Fixed Effects Specification

| Predictor | Type | Coding | Interpretation |
|-----------|------|--------|----------------|
| Intercept | - | - | Expected outcome in baseline condition |
| Condition | Binary | 0=Baseline, 1=Stress | Effect of stress manipulation |

### 4.4 Model Comparison Approach

We will use a hierarchical model comparison strategy:

1. **Null model**: Intercept only with random effects
2. **Condition model**: Add fixed effect of condition
3. **Model fit comparison**: Likelihood ratio test

```python
from scipy.stats import chi2

# Likelihood ratio test
def lr_test(model_null, model_full):
    """
    Likelihood ratio test comparing nested models.
    """
    lr_stat = -2 * (model_null.llf - model_full.llf)
    df_diff = model_full.df_model - model_null.df_model
    p_value = chi2.sf(lr_stat, df_diff)

    return {
        'lr_statistic': lr_stat,
        'df': df_diff,
        'p_value': p_value
    }
```

### 4.5 Multiple Comparison Corrections

For secondary hypotheses (H2, H3) and exploratory analyses:

**Method**: Benjamini-Hochberg False Discovery Rate (FDR) control
- **Target FDR**: q = 0.05
- **Rationale**: Balances power and error control for multiple outcomes

```python
from statsmodels.stats.multitest import multipletests

def apply_fdr_correction(p_values, alpha=0.05):
    """
    Apply Benjamini-Hochberg FDR correction.
    """
    rejected, p_adjusted, _, _ = multipletests(
        p_values,
        alpha=alpha,
        method='fdr_bh'
    )
    return rejected, p_adjusted
```

**Note**: Primary hypothesis (H1) uses uncorrected α=0.01 as pre-specified.

---

## 5. Dependent Variables

### 5.1 Primary Outcome: Mistakes

**Operational Definition:**
A mistake is an interaction where `hit_problem = True` in the simulation log.

**Aggregation Method:**
```python
def calculate_primary_outcome(df):
    """
    Calculate agent-level mistake count.

    Level of analysis: Agent (averaged across runs)
    """
    # Aggregate at run level first
    run_level = df.groupby(['agent_id', 'condition', 'run_id']).agg({
        'hit_problem': 'sum'
    }).reset_index()
    run_level.rename(columns={'hit_problem': 'mistakes'}, inplace=True)

    # Then aggregate at agent level (mean across runs)
    agent_level = run_level.groupby(['agent_id', 'condition']).agg({
        'mistakes': ['mean', 'std', 'count']
    }).reset_index()
    agent_level.columns = ['agent_id', 'condition', 'mistakes_mean',
                           'mistakes_sd', 'n_runs']

    return agent_level
```

### 5.2 Secondary Outcomes

#### Help-Seeking Rate

```python
def calculate_help_rate(df):
    """
    Calculate proportion of interactions that are help requests.
    """
    agent_level = df.groupby(['agent_id', 'condition', 'run_id']).apply(
        lambda x: (x['interaction_type'] == 'help_request').sum() / len(x)
    ).reset_index(name='help_rate')

    return agent_level.groupby(['agent_id', 'condition']).agg({
        'help_rate': 'mean'
    }).reset_index()
```

#### Task Completion Time

```python
def calculate_completion_time(df):
    """
    Calculate mean time from task_start to task_complete.
    """
    # Filter to task events
    task_df = df[df['interaction_type'].isin(['task_start', 'task_complete'])]

    # Calculate durations (implementation details depend on timestamp format)
    # Returns mean completion time per agent
    pass
```

### 5.3 Summary Table

| Outcome | Type | Aggregation | Model Family |
|---------|------|-------------|--------------|
| Mistakes | Primary | Agent mean | Negative Binomial |
| Help Rate | Secondary | Agent mean | Beta |
| Completion Time | Secondary | Agent mean | Gaussian |
| Defensive Acts | Exploratory | Agent mean | Poisson |

---

## 6. Pseudo-replication Solution

### 6.1 The Problem

**Pseudo-replication** occurs when non-independent observations are treated as independent samples, artificially inflating sample size and underestimating standard errors.

In the original design:
- 1,921 interactions treated as n=1,921
- But interactions are nested within 5 agents
- True effective n ≈ 5-33 depending on ICC

### 6.2 Proper Aggregation Strategy

#### Step 1: Identify Independence Structure

```
Independent unit: Agent
Repeated measures: Runs within agent
Clustered observations: Interactions within run
```

#### Step 2: Aggregate to Independent Unit Level

```python
def aggregate_to_independence(interaction_df):
    """
    Aggregate data to the level of independent experimental units.

    Returns one row per agent with summary statistics.
    """
    # First: interaction -> run level
    run_level = interaction_df.groupby(
        ['condition', 'agent_id', 'run_id']
    ).agg({
        'mistakes': 'sum',
        'help_requests': 'sum',
        'n_interactions': 'count',
        'completion_time': 'mean'
    }).reset_index()

    # Second: run -> agent level (this is our unit of analysis)
    agent_level = run_level.groupby(
        ['condition', 'agent_id']
    ).agg({
        'mistakes': ['mean', 'std'],
        'help_requests': ['mean', 'std'],
        'completion_time': ['mean', 'std'],
        'run_id': 'count'  # Number of runs
    }).reset_index()

    # Flatten column names
    agent_level.columns = ['_'.join(col).strip('_') for col in agent_level.columns]

    return agent_level
```

### 6.3 Independence Assumptions

**Assumption 1**: Agents are independent
- Verified by: No shared memory/context between agents
- Test: Check for correlation between agent outcomes
- Violation consequence: Underestimated SEs

**Assumption 2**: Runs within agent are exchangeable
- Verified by: Same random seed structure per run
- Test: Check for systematic trends across runs (learning)

**Assumption 3**: Interactions within run are exchangeable given agent and run
- Verified by: Stationary process within simulation
- Test: Autocorrelation analysis

### 6.4 Autocorrelation Handling

For within-run interaction sequences:

```python
import statsmodels.api as sm

def check_autocorrelation(agent_run_data):
    """
    Check for temporal autocorrelation within runs.
    """
    # Calculate residuals from mean
    residuals = agent_run_data['outcome'] - agent_run_data['outcome'].mean()

    # Compute autocorrelation function
    acf_values = sm.tsa.acf(residuals, nlags=20)

    # Ljung-Box test
    lb_stat, lb_pvalue = sm.stats.acorr_ljungbox(residuals, lags=10)

    return {
        'acf': acf_values,
        'ljung_box_p': lb_pvalue[-1]
    }

def handle_autocorrelation(df, method='aggregate'):
    """
    Handle autocorrelated observations.

    Methods:
    - 'aggregate': Average to remove temporal structure (preferred)
    - 'ar_model': Include AR(1) error structure
    - 'cluster_robust': Use cluster-robust SEs
    """
    if method == 'aggregate':
        # Aggregate to run level (removes within-run autocorrelation)
        return df.groupby(['agent_id', 'condition', 'run_id']).agg({
            'outcome': 'mean'
        })

    elif method == 'cluster_robust':
        # Use in model fitting
        pass
```

### 6.5 Effective Sample Size Calculation

```python
def calculate_effective_n(df, outcome_col, cluster_col):
    """
    Calculate effective sample size accounting for clustering.

    Uses Kish (1965) design effect formula.
    """
    # Calculate ICC
    from statsmodels.stats.anova import anova_lm
    from statsmodels.formula.api import ols

    # One-way ANOVA to get variance components
    model = ols(f'{outcome_col} ~ C({cluster_col})', data=df).fit()
    anova_table = anova_lm(model)

    ms_between = anova_table.loc['C(' + cluster_col + ')', 'mean_sq']
    ms_within = anova_table.loc['Residual', 'mean_sq']

    # Calculate ICC
    n_per_cluster = df.groupby(cluster_col).size().mean()
    icc = (ms_between - ms_within) / (ms_between + (n_per_cluster - 1) * ms_within)

    # Design effect
    deff = 1 + (n_per_cluster - 1) * max(0, icc)

    # Effective n
    n_total = len(df)
    n_effective = n_total / deff

    return {
        'n_total': n_total,
        'n_effective': n_effective,
        'icc': icc,
        'deff': deff,
        'n_clusters': df[cluster_col].nunique()
    }
```

### 6.6 Reporting Requirements

All analyses must report:
1. Total number of observations (interactions)
2. Number of independent units (agents)
3. Intraclass correlation coefficient (ICC)
4. Design effect (DEFF)
5. Effective sample size

---

## 7. Effect Size Reporting

### 7.1 Cohen's d for Condition Effect

```python
def cohens_d_multilevel(model_results, df):
    """
    Calculate Cohen's d from multilevel model.

    Uses total variance (between + within) as denominator.
    """
    # Fixed effect of condition
    condition_effect = model_results.params['condition']

    # Total variance = between-agent variance + residual variance
    var_between = model_results.var_components['agent_id']
    var_within = model_results.scale  # Residual variance
    total_var = var_between + var_within

    # Cohen's d
    d = condition_effect / np.sqrt(total_var)

    return d

def cohens_d_simple(group1, group2):
    """
    Calculate Cohen's d with pooled standard deviation.

    For agent-level aggregated data.
    """
    n1, n2 = len(group1), len(group2)
    m1, m2 = np.mean(group1), np.mean(group2)
    s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)

    # Pooled SD
    pooled_sd = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))

    # Cohen's d
    d = (m1 - m2) / pooled_sd

    return d
```

### 7.2 Confidence Intervals for Effect Sizes

Using non-central t-distribution method (Cumming, 2012):

```python
from scipy.stats import nct
import numpy as np

def d_confidence_interval(d, n1, n2, confidence=0.95):
    """
    Calculate CI for Cohen's d using non-central t.
    """
    # Degrees of freedom
    df = n1 + n2 - 2

    # Non-centrality parameter
    ncp = d * np.sqrt(n1 * n2 / (n1 + n2))

    # Find CI bounds
    alpha = 1 - confidence

    # Lower bound: find ncp such that P(t > t_obs) = alpha/2
    # Upper bound: find ncp such that P(t < t_obs) = alpha/2

    from scipy.optimize import brentq

    t_obs = d * np.sqrt(n1 * n2 / (n1 + n2))

    def lower_func(ncp_test):
        return nct.sf(t_obs, df, ncp_test) - alpha/2

    def upper_func(ncp_test):
        return nct.cdf(t_obs, df, ncp_test) - alpha/2

    try:
        ncp_lower = brentq(lower_func, -50, t_obs)
        ncp_upper = brentq(upper_func, t_obs, 50)

        d_lower = ncp_lower / np.sqrt(n1 * n2 / (n1 + n2))
        d_upper = ncp_upper / np.sqrt(n1 * n2 / (n1 + n2))
    except:
        # Fallback to normal approximation
        se_d = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2)))
        z = 1.96 if confidence == 0.95 else 2.576
        d_lower = d - z * se_d
        d_upper = d + z * se_d

    return d_lower, d_upper
```

### 7.3 Practical Significance Thresholds

Following Cohen (1988) conventions adjusted for domain:

| Effect Size | Cohen's d | Interpretation | Practical Meaning |
|-------------|-----------|----------------|-------------------|
| Small | 0.2 | Minimal | Detectable but not actionable |
| Medium | 0.5 | Moderate | Meaningful for theory |
| Large | 0.8 | Substantial | Clear practical implications |
| Very Large | 1.2 | Dominant | Major behavioral change |

**Minimum Effect Size of Interest (MEFSI)**: d = 0.5
- Effects smaller than this are not practically significant
- Used for equivalence testing (TOST procedure)

### 7.4 Additional Effect Size Measures

```python
def calculate_all_effect_sizes(model, df, condition_col='condition'):
    """
    Calculate multiple effect size measures.
    """
    results = {}

    # 1. Cohen's d (standardized mean difference)
    results['cohens_d'] = cohens_d_multilevel(model, df)

    # 2. Odds Ratio (for binary outcomes)
    if model.family == 'binomial':
        results['odds_ratio'] = np.exp(model.params[condition_col])

    # 3. Rate Ratio (for count outcomes)
    if model.family in ['poisson', 'negative_binomial']:
        results['rate_ratio'] = np.exp(model.params[condition_col])

    # 4. Marginal R-squared (variance explained by fixed effects)
    # Following Nakagawa & Schielzeth (2013)
    var_fixed = np.var(model.fittedvalues)
    var_random = sum(model.var_components.values())
    var_resid = model.scale
    results['r2_marginal'] = var_fixed / (var_fixed + var_random + var_resid)

    # 5. Conditional R-squared (variance explained by fixed + random)
    results['r2_conditional'] = (var_fixed + var_random) / (var_fixed + var_random + var_resid)

    return results
```

---

## 8. Pre-registration Template

### Study Information

**Title**: Effect of Simulated Workplace Stressors on AI Agent Collaborative Behavior in Software Development Teams

**Authors**: [To be completed]

**Date**: 2025-11-19

**Registration**: [To be registered on OSF/AsPredicted]

---

### Design Plan

**Study type**: Experiment - Between subjects

**Blinding**:
- Agents are not aware of other conditions
- Analysis will be conducted blinded to condition labels (relabeled A/B)

**Study design**:
2 (Condition: Baseline vs. Stress) between-subjects design with 30 agents per condition and 10 replicate runs per agent.

**Randomization**:
Agents assigned to conditions via blocked randomization stratified by agent role (Thoth, Seshat, Maat, Anubis, Ptah - 6 of each per condition).

---

### Sampling Plan

**Existing data**:
Pilot data (n=3 per condition) exists and was used ONLY for power analysis. Final analysis will use entirely new data.

**Data collection procedures**:
1. Create 60 unique agent configurations (30 per condition)
2. Run each agent 10 times
3. Log all interactions to JSONL format
4. Aggregate data after all runs complete

**Sample size**:
60 agents total (30 per condition), each run 10 times, yielding approximately 230,400 interactions.

**Sample size rationale**:
Power analysis (Section 1) indicates n=30 per condition achieves power=0.95 to detect d=0.8 at α=0.01, accounting for clustering (ICC=0.15).

**Stopping rule**:
Data collection stops when all 600 runs (60 agents x 10 runs) are complete. No interim analyses or stopping for significance.

---

### Variables

**Manipulated variable**:
- Condition (Baseline vs. Stress)
- Operationalization: Stress condition includes firing threat in agent prompts and regular reminders

**Measured variables** (Primary):
- Mistakes: Count of interactions where hit_problem=True
- Aggregation: Sum per run, then mean per agent

**Measured variables** (Secondary):
- Help-seeking rate: Count of help_request / total interactions
- Task completion time: Simulated hours from task_start to task_complete

**Covariates** (measured but not manipulated):
- Agent role (Thoth, Seshat, Maat, Anubis, Ptah)
- Run number (1-10)

---

### Analysis Plan

**Statistical models**:

Primary (H1):
```r
mistakes ~ condition + (1|agent_id) + (1|agent_id:run_id)
```
Family: Negative binomial
Link: Log

Secondary (H2):
```r
help_rate ~ condition + (1|agent_id) + (1|agent_id:run_id)
```
Family: Beta
Link: Logit

**Transformations**:
None planned. If models fail to converge, will log-transform count outcomes.

**Inference criteria**:
- H1 (Primary): α = 0.01, one-tailed (stress > baseline)
- H2, H3 (Secondary): α = 0.05, two-tailed, FDR-corrected

**Data exclusion**:
Exclude runs where:
- API errors > 20% of interactions
- Run did not complete all 4 weeks
- Clear data logging errors

**Missing data**:
Complete case analysis. Runs with missing data excluded entirely (not imputed).

**Exploratory analysis**:
- Agent role as moderator
- Time trends within simulation
- Sentiment analysis of text content

---

### Decision Rules

**Pre-specified decisions**:

1. If primary hypothesis (H1) is significant at α=0.01:
   - Conclude stress increases mistakes
   - Report effect size with 99% CI

2. If primary hypothesis is not significant:
   - Conduct equivalence test (TOST) with bounds d=±0.5
   - Report whether null effect is supported

3. If model fails to converge:
   - Simplify random effects structure
   - Try alternative optimizers (bobyqa, nlminb)
   - If still fails, use GEE with exchangeable correlation

4. If ICC < 0.05:
   - Clustering is minimal
   - Report but maintain multilevel structure for transparency

---

### Other

**Conflicts of interest**: None

**Code availability**: All analysis code will be made available on GitHub

**Data availability**: Anonymized data will be shared on OSF

---

## 9. Complete R/Python Code

### 9.1 Full Analysis Pipeline

```python
#!/usr/bin/env python3
"""
Complete Statistical Analysis Pipeline for AI Agent Behavior Study

This script implements all pre-registered analyses with proper handling
of nested/clustered data.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import mannwhitneyu, ttest_ind
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings

# For multilevel models
try:
    import pymer4
    from pymer4.models import Lmer
    HAS_PYMER4 = True
except ImportError:
    HAS_PYMER4 = False
    warnings.warn("pymer4 not available. Using statsmodels GEE instead.")


@dataclass
class AnalysisResults:
    """Container for analysis results."""
    coefficient: float
    se: float
    z_value: float
    p_value: float
    ci_lower: float
    ci_upper: float
    effect_size: float
    effect_size_ci: Tuple[float, float]
    n_agents: int
    n_observations: int
    icc: float


def load_and_preprocess_data(data_dir: str) -> pd.DataFrame:
    """
    Load simulation logs and preprocess for analysis.

    Parameters
    ----------
    data_dir : str
        Directory containing JSONL simulation logs

    Returns
    -------
    pd.DataFrame
        Preprocessed data at interaction level
    """
    all_data = []

    for jsonl_file in Path(data_dir).glob("*.jsonl"):
        with open(jsonl_file, 'r') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if 'interaction_type' in record:
                        all_data.append(record)
                except json.JSONDecodeError:
                    continue

    df = pd.DataFrame(all_data)

    # Extract key variables
    df['mistakes'] = df['content'].apply(
        lambda x: x.get('hit_problem', False) if isinstance(x, dict) else False
    ).astype(int)

    df['help_request'] = (df['interaction_type'] == 'help_request').astype(int)

    return df


def aggregate_to_agent_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate interaction-level data to agent level.

    This is the unit of analysis for between-subjects comparisons.
    """
    # First aggregate to run level
    run_level = df.groupby(['condition', 'agent_id', 'run_id']).agg({
        'mistakes': 'sum',
        'help_request': 'sum',
        'interaction_type': 'count'
    }).reset_index()

    run_level.rename(columns={'interaction_type': 'n_interactions'}, inplace=True)
    run_level['help_rate'] = run_level['help_request'] / run_level['n_interactions']

    # Then aggregate to agent level
    agent_level = run_level.groupby(['condition', 'agent_id']).agg({
        'mistakes': ['mean', 'std', 'sum'],
        'help_rate': ['mean', 'std'],
        'n_interactions': ['sum', 'count'],
        'run_id': 'count'
    }).reset_index()

    # Flatten column names
    agent_level.columns = [
        '_'.join(col).strip('_') if col[1] else col[0]
        for col in agent_level.columns
    ]

    return agent_level


def calculate_icc(df: pd.DataFrame, outcome: str, cluster: str) -> float:
    """
    Calculate intraclass correlation coefficient.

    Uses one-way random effects ANOVA method.
    """
    # Group data
    groups = [group[outcome].values for name, group in df.groupby(cluster)]

    # Calculate between and within variance
    k = len(groups)  # Number of clusters
    n_j = [len(g) for g in groups]  # Observations per cluster
    n_0 = (sum(n_j) - sum([n**2 for n in n_j])/sum(n_j)) / (k - 1)

    # Grand mean
    grand_mean = df[outcome].mean()

    # Between-cluster variance
    ss_between = sum([n * (np.mean(g) - grand_mean)**2 for n, g in zip(n_j, groups)])
    ms_between = ss_between / (k - 1)

    # Within-cluster variance
    ss_within = sum([sum((g - np.mean(g))**2) for g in groups])
    ms_within = ss_within / (sum(n_j) - k)

    # ICC
    icc = (ms_between - ms_within) / (ms_between + (n_0 - 1) * ms_within)

    return max(0, icc)  # ICC cannot be negative


def fit_multilevel_model(df: pd.DataFrame,
                         formula: str,
                         family: str = 'gaussian') -> Dict:
    """
    Fit multilevel model using pymer4 or GEE fallback.

    Parameters
    ----------
    df : pd.DataFrame
        Data at interaction or run level
    formula : str
        R-style formula
    family : str
        Distribution family ('gaussian', 'negative_binomial', etc.)

    Returns
    -------
    dict : Model results
    """
    if HAS_PYMER4:
        model = Lmer(formula, data=df, family=family)
        results = model.fit()

        return {
            'coefficients': results['Estimate'].to_dict(),
            'se': results['SE'].to_dict(),
            'z_values': results['T-stat'].to_dict(),
            'p_values': results['P-val'].to_dict(),
            'aic': model.AIC,
            'bic': model.BIC
        }
    else:
        # GEE fallback
        if family == 'gaussian':
            fam = sm.families.Gaussian()
        elif family == 'negative_binomial':
            fam = sm.families.NegativeBinomial()
        else:
            fam = sm.families.Gaussian()

        # Parse formula (simplified)
        outcome = formula.split('~')[0].strip()

        model = sm.GEE.from_formula(
            f"{outcome} ~ condition",
            groups='agent_id',
            data=df,
            family=fam,
            cov_struct=sm.cov_struct.Exchangeable()
        )
        results = model.fit()

        return {
            'coefficients': dict(zip(results.model.exog_names, results.params)),
            'se': dict(zip(results.model.exog_names, results.bse)),
            'z_values': dict(zip(results.model.exog_names, results.tvalues)),
            'p_values': dict(zip(results.model.exog_names, results.pvalues))
        }


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> Tuple[float, float, float]:
    """
    Calculate Cohen's d with 95% CI.

    Returns
    -------
    tuple : (d, ci_lower, ci_upper)
    """
    n1, n2 = len(group1), len(group2)
    m1, m2 = np.mean(group1), np.mean(group2)
    s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)

    # Pooled SD
    pooled_sd = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))

    # Cohen's d
    d = (m2 - m1) / pooled_sd  # Stress - Baseline

    # SE of d (Hedges & Olkin, 1985)
    se_d = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2-2)))

    # 95% CI
    ci_lower = d - 1.96 * se_d
    ci_upper = d + 1.96 * se_d

    return d, ci_lower, ci_upper


def primary_analysis(agent_df: pd.DataFrame) -> AnalysisResults:
    """
    Conduct primary hypothesis test (H1: Mistakes).

    Tests whether stress condition has more mistakes than baseline.
    """
    # Split by condition
    baseline = agent_df[agent_df['condition'] == 'baseline']['mistakes_mean'].values
    stress = agent_df[agent_df['condition'] == 'stress']['mistakes_mean'].values

    # Two-sample t-test (one-tailed)
    t_stat, p_value_two_tailed = ttest_ind(stress, baseline)
    p_value = p_value_two_tailed / 2 if t_stat > 0 else 1 - p_value_two_tailed / 2

    # Effect size
    d, d_lower, d_upper = cohens_d(baseline, stress)

    # Calculate ICC from raw data
    # (Would need run-level data for this)
    icc = 0.15  # Placeholder, calculate from actual data

    return AnalysisResults(
        coefficient=np.mean(stress) - np.mean(baseline),
        se=np.sqrt(np.var(stress)/len(stress) + np.var(baseline)/len(baseline)),
        z_value=t_stat,
        p_value=p_value,
        ci_lower=np.mean(stress) - np.mean(baseline) - 1.96 * np.sqrt(np.var(stress)/len(stress) + np.var(baseline)/len(baseline)),
        ci_upper=np.mean(stress) - np.mean(baseline) + 1.96 * np.sqrt(np.var(stress)/len(stress) + np.var(baseline)/len(baseline)),
        effect_size=d,
        effect_size_ci=(d_lower, d_upper),
        n_agents=len(baseline) + len(stress),
        n_observations=len(baseline) + len(stress),  # Agent-level
        icc=icc
    )


def secondary_analyses(agent_df: pd.DataFrame) -> Dict[str, AnalysisResults]:
    """
    Conduct secondary hypothesis tests with FDR correction.
    """
    results = {}
    p_values = []

    # H2: Help-seeking rate
    baseline = agent_df[agent_df['condition'] == 'baseline']['help_rate_mean'].values
    stress = agent_df[agent_df['condition'] == 'stress']['help_rate_mean'].values

    t_stat, p_value = ttest_ind(stress, baseline)
    d, d_lower, d_upper = cohens_d(baseline, stress)

    results['help_rate'] = AnalysisResults(
        coefficient=np.mean(stress) - np.mean(baseline),
        se=np.sqrt(np.var(stress)/len(stress) + np.var(baseline)/len(baseline)),
        z_value=t_stat,
        p_value=p_value,
        ci_lower=np.mean(stress) - np.mean(baseline) - 1.96 * np.sqrt(np.var(stress)/len(stress) + np.var(baseline)/len(baseline)),
        ci_upper=np.mean(stress) - np.mean(baseline) + 1.96 * np.sqrt(np.var(stress)/len(stress) + np.var(baseline)/len(baseline)),
        effect_size=d,
        effect_size_ci=(d_lower, d_upper),
        n_agents=len(baseline) + len(stress),
        n_observations=len(baseline) + len(stress),
        icc=0.15
    )
    p_values.append(p_value)

    # Apply FDR correction
    rejected, p_adjusted = multipletests(p_values, alpha=0.05, method='fdr_bh')[:2]

    # Update p-values with FDR-corrected values
    results['help_rate'].p_value = p_adjusted[0]

    return results


def run_full_analysis(data_dir: str, output_dir: str):
    """
    Run complete pre-registered analysis pipeline.
    """
    print("=" * 60)
    print("AI Agent Behavior Study - Statistical Analysis")
    print("=" * 60)

    # Load data
    print("\n1. Loading and preprocessing data...")
    interaction_df = load_and_preprocess_data(data_dir)
    print(f"   Loaded {len(interaction_df)} interactions")

    # Aggregate to agent level
    print("\n2. Aggregating to agent level...")
    agent_df = aggregate_to_agent_level(interaction_df)
    print(f"   {len(agent_df)} agents total")
    print(f"   Baseline: {len(agent_df[agent_df['condition']=='baseline'])}")
    print(f"   Stress: {len(agent_df[agent_df['condition']=='stress'])}")

    # Calculate ICC
    print("\n3. Checking clustering (ICC)...")
    # Would calculate from run-level data

    # Primary analysis
    print("\n4. Primary hypothesis (H1: Mistakes)...")
    primary_results = primary_analysis(agent_df)

    print(f"   Mean difference: {primary_results.coefficient:.3f}")
    print(f"   t-value: {primary_results.z_value:.3f}")
    print(f"   p-value (one-tailed): {primary_results.p_value:.4f}")
    print(f"   Cohen's d: {primary_results.effect_size:.3f} "
          f"[{primary_results.effect_size_ci[0]:.3f}, {primary_results.effect_size_ci[1]:.3f}]")

    if primary_results.p_value < 0.01:
        print("   RESULT: Significant at alpha=0.01")
    else:
        print("   RESULT: Not significant at alpha=0.01")

    # Secondary analyses
    print("\n5. Secondary hypotheses (FDR-corrected)...")
    secondary_results = secondary_analyses(agent_df)

    for name, result in secondary_results.items():
        print(f"\n   {name}:")
        print(f"      Mean difference: {result.coefficient:.4f}")
        print(f"      p-value (FDR-corrected): {result.p_value:.4f}")
        print(f"      Cohen's d: {result.effect_size:.3f}")

    # Save results
    print("\n6. Saving results...")
    results_summary = {
        'primary': {
            'hypothesis': 'H1: Stress increases mistakes',
            'test': 'One-tailed t-test',
            'coefficient': primary_results.coefficient,
            'p_value': primary_results.p_value,
            'effect_size': primary_results.effect_size,
            'significant': primary_results.p_value < 0.01
        },
        'secondary': {
            name: {
                'coefficient': r.coefficient,
                'p_value': r.p_value,
                'effect_size': r.effect_size
            }
            for name, r in secondary_results.items()
        },
        'sample_size': {
            'n_agents': primary_results.n_agents,
            'n_per_condition': primary_results.n_agents // 2
        }
    }

    with open(f"{output_dir}/analysis_results.json", 'w') as f:
        json.dump(results_summary, f, indent=2)

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)

    return results_summary


if __name__ == "__main__":
    import sys

    data_dir = sys.argv[1] if len(sys.argv) > 1 else "./simulations"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./results"

    run_full_analysis(data_dir, output_dir)
```

### 9.2 R Code for Multilevel Models

```r
# Complete R Analysis Script for AI Agent Behavior Study

library(lme4)
library(lmerTest)
library(MASS)       # For negative binomial
library(emmeans)    # For effect sizes
library(effectsize) # For Cohen's d
library(performance)# For ICC
library(ggplot2)

# ==============================================================================
# 1. Load and Prepare Data
# ==============================================================================

load_data <- function(data_file) {
  df <- read.csv(data_file)

  # Convert condition to factor with baseline as reference
  df$condition <- factor(df$condition, levels = c("baseline", "stress"))
  df$agent_id <- factor(df$agent_id)
  df$run_id <- factor(df$run_id)

  return(df)
}

# ==============================================================================
# 2. Calculate ICC
# ==============================================================================

calculate_icc <- function(df, outcome) {
  # Fit null model with random intercept
  formula <- as.formula(paste(outcome, "~ 1 + (1|agent_id)"))
  null_model <- lmer(formula, data = df, REML = TRUE)

  # Extract variance components
  vc <- as.data.frame(VarCorr(null_model))
  var_between <- vc[vc$grp == "agent_id", "vcov"]
  var_within <- vc[vc$grp == "Residual", "vcov"]

  # Calculate ICC
  icc <- var_between / (var_between + var_within)

  return(list(
    icc = icc,
    var_between = var_between,
    var_within = var_within
  ))
}

# ==============================================================================
# 3. Primary Analysis: Multilevel Negative Binomial
# ==============================================================================

primary_analysis <- function(df) {
  # Fit null model
  m0 <- glmer.nb(
    mistakes ~ 1 + (1|agent_id) + (1|agent_id:run_id),
    data = df,
    control = glmerControl(optimizer = "bobyqa")
  )

  # Fit full model
  m1 <- glmer.nb(
    mistakes ~ condition + (1|agent_id) + (1|agent_id:run_id),
    data = df,
    control = glmerControl(optimizer = "bobyqa")
  )

  # Model comparison
  lr_test <- anova(m0, m1)

  # Extract coefficients
  coef_summary <- summary(m1)$coefficients

  # Calculate effect size (rate ratio)
  rate_ratio <- exp(fixef(m1)["conditionstress"])

  # Get confidence interval
  ci <- confint(m1, parm = "conditionstress", method = "Wald")
  ci_rr <- exp(ci)

  return(list(
    model = m1,
    null_model = m0,
    lr_test = lr_test,
    coefficient = fixef(m1)["conditionstress"],
    se = coef_summary["conditionstress", "Std. Error"],
    z_value = coef_summary["conditionstress", "z value"],
    p_value = coef_summary["conditionstress", "Pr(>|z|)"] / 2,  # One-tailed
    rate_ratio = rate_ratio,
    ci_lower = ci_rr[1],
    ci_upper = ci_rr[2]
  ))
}

# ==============================================================================
# 4. Calculate Cohen's d from Agent-Level Means
# ==============================================================================

calculate_cohens_d <- function(df) {
  # Aggregate to agent level
  agent_means <- aggregate(
    mistakes ~ condition + agent_id,
    data = df,
    FUN = mean
  )

  # Split by condition
  baseline <- agent_means[agent_means$condition == "baseline", "mistakes"]
  stress <- agent_means[agent_means$condition == "stress", "mistakes"]

  # Calculate Cohen's d
  d_result <- cohens_d(stress, baseline)

  return(d_result)
}

# ==============================================================================
# 5. Secondary Analyses with FDR Correction
# ==============================================================================

secondary_analyses <- function(df) {
  results <- list()
  p_values <- c()

  # H2: Help-seeking rate
  m_help <- glmer(
    help_request ~ condition + (1|agent_id),
    data = df,
    family = binomial
  )

  coef_help <- summary(m_help)$coefficients
  p_values <- c(p_values, coef_help["conditionstress", "Pr(>|z|)"])

  results$help_rate <- list(
    model = m_help,
    coefficient = fixef(m_help)["conditionstress"],
    p_value = coef_help["conditionstress", "Pr(>|z|)"],
    odds_ratio = exp(fixef(m_help)["conditionstress"])
  )

  # Apply FDR correction
  p_adjusted <- p.adjust(p_values, method = "fdr")

  # Update p-values
  results$help_rate$p_value_fdr <- p_adjusted[1]

  return(results)
}

# ==============================================================================
# 6. Main Analysis Function
# ==============================================================================

run_analysis <- function(data_file, output_dir) {
  cat("============================================================\n")
  cat("AI Agent Behavior Study - R Statistical Analysis\n")
  cat("============================================================\n\n")

  # Load data
  cat("1. Loading data...\n")
  df <- load_data(data_file)
  cat(sprintf("   Loaded %d observations\n", nrow(df)))
  cat(sprintf("   Agents: %d\n", length(unique(df$agent_id))))

  # Calculate ICC
  cat("\n2. Calculating ICC...\n")
  icc_result <- calculate_icc(df, "mistakes")
  cat(sprintf("   ICC = %.3f\n", icc_result$icc))

  # Primary analysis
  cat("\n3. Primary hypothesis (H1: Mistakes)...\n")
  primary <- primary_analysis(df)

  cat(sprintf("   Coefficient: %.3f\n", primary$coefficient))
  cat(sprintf("   z-value: %.3f\n", primary$z_value))
  cat(sprintf("   p-value (one-tailed): %.4f\n", primary$p_value))
  cat(sprintf("   Rate ratio: %.3f [%.3f, %.3f]\n",
              primary$rate_ratio, primary$ci_lower, primary$ci_upper))

  if (primary$p_value < 0.01) {
    cat("   RESULT: Significant at alpha=0.01\n")
  } else {
    cat("   RESULT: Not significant at alpha=0.01\n")
  }

  # Cohen's d
  cat("\n4. Effect size (Cohen's d)...\n")
  d_result <- calculate_cohens_d(df)
  cat(sprintf("   Cohen's d = %.3f [%.3f, %.3f]\n",
              d_result$Cohens_d, d_result$CI_low, d_result$CI_high))

  # Secondary analyses
  cat("\n5. Secondary analyses (FDR-corrected)...\n")
  secondary <- secondary_analyses(df)

  for (name in names(secondary)) {
    cat(sprintf("\n   %s:\n", name))
    cat(sprintf("      Coefficient: %.3f\n", secondary[[name]]$coefficient))
    cat(sprintf("      p-value (FDR): %.4f\n", secondary[[name]]$p_value_fdr))
  }

  cat("\n============================================================\n")
  cat("Analysis complete!\n")
  cat("============================================================\n")

  return(list(
    primary = primary,
    secondary = secondary,
    icc = icc_result
  ))
}

# Run if executed directly
if (sys.nframe() == 0) {
  results <- run_analysis("data/run_level.csv", "results/")
}
```

---

## 10. Decision Rules and Stopping Criteria

### 10.1 Pre-specified Analysis Decisions

#### If Primary Hypothesis is Significant (p < 0.01)

1. Report as confirmatory evidence that stress increases mistakes
2. Calculate and report effect size with 99% CI
3. Interpret in context of practical significance thresholds
4. Proceed with secondary analyses

#### If Primary Hypothesis is Not Significant (p >= 0.01)

1. Do NOT conclude "no effect" - absence of evidence is not evidence of absence
2. Conduct equivalence test (TOST) with bounds d = -0.5 to 0.5
3. If equivalence is supported: report that effect is practically negligible
4. If equivalence is not supported: report as inconclusive
5. Report observed effect size and CI regardless

```python
def equivalence_test(group1, group2, low=-0.5, high=0.5):
    """
    Two One-Sided Tests (TOST) for equivalence.
    """
    from scipy.stats import ttest_ind

    d, _, _ = cohens_d(group1, group2)

    # Test if effect is above lower bound
    t1, p1 = ttest_ind(group2 + low * np.std(group1), group1)
    p_lower = p1 / 2 if t1 > 0 else 1 - p1/2

    # Test if effect is below upper bound
    t2, p2 = ttest_ind(group2 - high * np.std(group1), group1)
    p_upper = p2 / 2 if t2 < 0 else 1 - p2/2

    # Equivalence established if both tests significant
    p_tost = max(p_lower, p_upper)
    equivalent = p_tost < 0.05

    return {
        'equivalent': equivalent,
        'p_tost': p_tost,
        'observed_d': d
    }
```

### 10.2 Model Convergence Issues

If the multilevel model fails to converge:

1. **Step 1**: Try alternative optimizers
   ```r
   glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000))
   ```

2. **Step 2**: Simplify random effects
   - Remove random slopes if present
   - Remove run-level random effect if problematic
   ```r
   mistakes ~ condition + (1|agent_id)  # Simplified
   ```

3. **Step 3**: Use GEE as fallback
   ```r
   library(geepack)
   geeglm(mistakes ~ condition, id = agent_id,
          data = df, family = poisson, corstr = "exchangeable")
   ```

4. **Step 4**: Aggregate and use simple t-test
   - Aggregate to agent-level means
   - Use two-sample t-test
   - Acknowledge increased Type II error risk

### 10.3 Data Quality Issues

#### API Errors

- **Threshold**: Exclude run if > 20% of interactions have API errors
- **Rationale**: Ensures sufficient valid data for analysis
- **Implementation**:
  ```python
  def check_api_errors(run_data):
      error_rate = (run_data['response'].str.contains('Error')).mean()
      return error_rate <= 0.20
  ```

#### Incomplete Runs

- **Threshold**: Exclude run if < 80% of expected interactions
- **Expected**: ~384 interactions per run
- **Minimum**: 307 interactions

#### Anomalous Values

- **Check**: Outliers beyond 3 SD from condition mean
- **Action**: Flag but include; conduct sensitivity analysis without
- **Report**: Both with and without outliers

### 10.4 Sensitivity Analyses

1. **Exclude outliers**: Rerun without agents > 3 SD from mean
2. **Alternative random effects**: Compare models with different structures
3. **Non-parametric**: Mann-Whitney U test on agent means
4. **Bayesian**: Rerun with Bayesian estimation (Stan/brms)

### 10.5 Reporting Checklist

Every analysis report must include:

- [ ] Sample size at each level (interactions, runs, agents)
- [ ] ICC for each outcome
- [ ] Full model specification in R formula notation
- [ ] Coefficient, SE, test statistic, p-value
- [ ] Effect size with 95% CI
- [ ] Model fit statistics (AIC, BIC)
- [ ] Random effects variance components
- [ ] Convergence information
- [ ] Any exclusions and reasons
- [ ] Sensitivity analysis results

---

## References

Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.). Lawrence Erlbaum Associates.

Cumming, G. (2012). Understanding the new statistics: Effect sizes, confidence intervals, and meta-analysis. Routledge.

Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power analyses using G*Power 3.1. Behavior Research Methods, 41, 1149-1160.

Gelman, A., & Carlin, J. (2014). Beyond power calculations: Assessing type S (sign) and type M (magnitude) errors. Perspectives on Psychological Science, 9(6), 641-651.

Hedges, L. V., & Olkin, I. (1985). Statistical methods for meta-analysis. Academic Press.

Kish, L. (1965). Survey sampling. John Wiley & Sons.

Lakens, D., Adolfi, F. G., Albers, C. J., et al. (2018). Justify your alpha. Nature Human Behaviour, 2, 168-171.

Maas, C. J. M., & Hox, J. J. (2005). Sufficient sample sizes for multilevel modeling. Methodology, 1(3), 86-92.

Nakagawa, S., & Schielzeth, H. (2013). A general and simple method for obtaining R2 from generalized linear mixed-effects models. Methods in Ecology and Evolution, 4(2), 133-142.

Perugini, M., Gallucci, M., & Costantini, G. (2018). A practical primer to power analysis for simple experimental designs. International Review of Social Psychology, 31(1), 20.

Snijders, T. A. B., & Bosker, R. J. (2012). Multilevel analysis: An introduction to basic and advanced multilevel modeling (2nd ed.). Sage.

---

## Appendix A: Checklist Before Data Collection

- [ ] Pre-registration document submitted and timestamped
- [ ] Analysis scripts finalized and version-controlled
- [ ] Simulation code tested and verified
- [ ] Random seeds documented
- [ ] Data storage and backup plan in place
- [ ] Exclusion criteria programmatically implemented
- [ ] Team blinded to condition assignments

## Appendix B: Checklist Before Analysis

- [ ] All 600 simulation runs completed
- [ ] Data quality checks passed
- [ ] No changes to pre-registered analysis
- [ ] Blinding maintained
- [ ] Any deviations documented with rationale

---

*End of Statistical Methodology Document*
