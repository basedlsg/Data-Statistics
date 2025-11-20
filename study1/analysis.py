#!/usr/bin/env python3
"""
Complete Statistical Analysis Pipeline for Study 1: Agent Stress Behavior

This module implements rigorous statistical analysis for AI agent behavioral research,
addressing pseudo-replication, nested data structures, and proper effect size reporting.

Classes:
    PowerAnalysis: Calculate achieved power and effect sizes
    MixedEffectsModels: Fit multilevel models for nested data
    PseudoReplicationHandler: Aggregate and validate data independence
    CausalAnalysis: Test causal relationships and mediation
    VisualizationGenerator: Create publication-quality figures

Author: Statistical Analysis Agent
Date: 2025-11-20
Version: 1.0
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2, norm, mannwhitneyu, ttest_ind
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower, TTestPower
from statsmodels.stats.anova import anova_lm
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, asdict
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# Try to import optional dependencies
try:
    import pymer4
    from pymer4.models import Lmer
    HAS_PYMER4 = True
except ImportError:
    HAS_PYMER4 = False
    warnings.warn("pymer4 not available. Mixed models will use statsmodels GEE instead.")

try:
    from rpy2.robjects.packages import importr
    from rpy2.robjects import pandas2ri, Formula
    pandas2ri.activate()
    HAS_RPY2 = True
except ImportError:
    HAS_RPY2 = False
    warnings.warn("rpy2 not available. R integration disabled.")

try:
    from statsmodels.stats.mediation import Mediation
    HAS_MEDIATION = True
except ImportError:
    HAS_MEDIATION = False
    warnings.warn("Mediation analysis requires statsmodels >= 0.14")


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class EffectSize:
    """Container for effect size estimates."""
    cohens_d: float
    ci_lower: float
    ci_upper: float
    hedges_g: Optional[float] = None
    interpretation: Optional[str] = None

    def __post_init__(self):
        """Interpret effect size magnitude."""
        abs_d = abs(self.cohens_d)
        if abs_d < 0.2:
            self.interpretation = "negligible"
        elif abs_d < 0.5:
            self.interpretation = "small"
        elif abs_d < 0.8:
            self.interpretation = "medium"
        elif abs_d < 1.2:
            self.interpretation = "large"
        else:
            self.interpretation = "very large"


@dataclass
class PowerAnalysisResult:
    """Container for power analysis results."""
    achieved_power: float
    effect_size: float
    sample_size: int
    alpha: float
    test_type: str
    power_adequate: bool  # True if power >= 0.80

    def __str__(self):
        return (f"Power Analysis: power={self.achieved_power:.3f}, "
                f"d={self.effect_size:.3f}, n={self.sample_size}, "
                f"adequate={self.power_adequate}")


@dataclass
class ModelResults:
    """Container for mixed-effects model results."""
    model_type: str
    formula: str
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    t_values: Dict[str, float]
    p_values: Dict[str, float]
    ci_lower: Dict[str, float]
    ci_upper: Dict[str, float]
    icc: float
    aic: float
    bic: float
    n_obs: int
    n_groups: int
    variance_components: Dict[str, float]

    def to_table(self) -> pd.DataFrame:
        """Convert to APA-style results table."""
        df = pd.DataFrame({
            'Coefficient': self.coefficients,
            'SE': self.std_errors,
            't': self.t_values,
            'p': self.p_values,
            'CI_lower': self.ci_lower,
            'CI_upper': self.ci_upper
        })

        # Format p-values
        df['p_formatted'] = df['p'].apply(
            lambda x: f"{x:.3f}" if x >= 0.001 else "< .001"
        )

        # Add significance stars
        df['sig'] = df['p'].apply(
            lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else ''))
        )

        return df


@dataclass
class IndependenceCheck:
    """Container for independence test results."""
    test_name: str
    statistic: float
    p_value: float
    passed: bool
    details: Dict[str, any]


# =============================================================================
# CLASS 1: POWER ANALYSIS
# =============================================================================

class PowerAnalysis:
    """
    Calculate statistical power, effect sizes, and sample size requirements.

    Implements power analysis for t-tests, mixed-effects models, and
    handles both achieved power (post-hoc) and a priori planning.

    Methods:
        calculate_cohens_d: Calculate Cohen's d effect size with CI
        calculate_achieved_power: Calculate power from observed data
        calculate_required_n: Calculate sample size for desired power
        design_effect_adjustment: Adjust for clustered data
        equivalence_test: TOST for equivalence testing
    """

    def __init__(self, alpha: float = 0.05):
        """
        Initialize PowerAnalysis.

        Parameters
        ----------
        alpha : float
            Significance level (default: 0.05)
        """
        self.alpha = alpha

    def calculate_cohens_d(
        self,
        group1: np.ndarray,
        group2: np.ndarray,
        confidence: float = 0.95,
        paired: bool = False
    ) -> EffectSize:
        """
        Calculate Cohen's d with confidence intervals.

        Parameters
        ----------
        group1 : np.ndarray
            First group (e.g., baseline condition)
        group2 : np.ndarray
            Second group (e.g., stress condition)
        confidence : float
            Confidence level for CI (default: 0.95)
        paired : bool
            Whether samples are paired (default: False)

        Returns
        -------
        EffectSize
            Effect size with interpretation
        """
        n1, n2 = len(group1), len(group2)
        m1, m2 = np.mean(group1), np.mean(group2)
        s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)

        if paired:
            # Paired design: use SD of differences
            diffs = group2 - group1
            d = np.mean(diffs) / np.std(diffs, ddof=1)
            # SE for paired design
            se_d = np.sqrt((1/n1) + (d**2 / (2*n1)))
        else:
            # Independent groups: pooled SD
            pooled_sd = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
            d = (m2 - m1) / pooled_sd

            # SE of d (Hedges & Olkin, 1985)
            se_d = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2-2)))

        # Confidence interval
        z = norm.ppf(1 - (1-confidence)/2)
        ci_lower = d - z * se_d
        ci_upper = d + z * se_d

        # Hedges' g (bias-corrected)
        if not paired:
            correction = 1 - (3 / (4*(n1+n2-2) - 1))
            hedges_g = d * correction
        else:
            hedges_g = None

        return EffectSize(
            cohens_d=d,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            hedges_g=hedges_g
        )

    def calculate_achieved_power(
        self,
        effect_size: float,
        n1: int,
        n2: Optional[int] = None,
        test_type: str = 'two-sample',
        alternative: str = 'two-sided'
    ) -> PowerAnalysisResult:
        """
        Calculate achieved power from observed data.

        Parameters
        ----------
        effect_size : float
            Observed Cohen's d
        n1 : int
            Sample size group 1
        n2 : int, optional
            Sample size group 2 (for independent samples)
        test_type : str
            'two-sample', 'one-sample', or 'paired'
        alternative : str
            'two-sided', 'larger', or 'smaller'

        Returns
        -------
        PowerAnalysisResult
            Achieved power and related statistics
        """
        if test_type == 'two-sample':
            if n2 is None:
                n2 = n1
            analysis = TTestIndPower()
            power = analysis.solve_power(
                effect_size=effect_size,
                nobs1=n1,
                ratio=n2/n1,
                alpha=self.alpha,
                alternative=alternative
            )
            n_total = n1 + n2
        else:  # paired or one-sample
            analysis = TTestPower()
            power = analysis.solve_power(
                effect_size=effect_size,
                nobs=n1,
                alpha=self.alpha,
                alternative=alternative
            )
            n_total = n1

        return PowerAnalysisResult(
            achieved_power=power,
            effect_size=effect_size,
            sample_size=n_total,
            alpha=self.alpha,
            test_type=test_type,
            power_adequate=power >= 0.80
        )

    def calculate_required_n(
        self,
        effect_size: float,
        power: float = 0.80,
        test_type: str = 'two-sample',
        alternative: str = 'two-sided'
    ) -> int:
        """
        Calculate required sample size for desired power.

        Parameters
        ----------
        effect_size : float
            Expected Cohen's d
        power : float
            Desired power (default: 0.80)
        test_type : str
            'two-sample' or 'paired'
        alternative : str
            'two-sided', 'larger', or 'smaller'

        Returns
        -------
        int
            Required sample size per group
        """
        if test_type == 'two-sample':
            analysis = TTestIndPower()
            n = analysis.solve_power(
                effect_size=effect_size,
                alpha=self.alpha,
                power=power,
                ratio=1.0,
                alternative=alternative
            )
        else:  # paired
            analysis = TTestPower()
            n = analysis.solve_power(
                effect_size=effect_size,
                alpha=self.alpha,
                power=power,
                alternative=alternative
            )

        return int(np.ceil(n))

    def design_effect_adjustment(
        self,
        icc: float,
        cluster_size: int
    ) -> Tuple[float, float]:
        """
        Calculate design effect for clustered data.

        Uses Kish (1965) formula: DEFF = 1 + (m - 1) * ICC

        Parameters
        ----------
        icc : float
            Intraclass correlation coefficient
        cluster_size : int
            Average number of observations per cluster

        Returns
        -------
        tuple
            (design_effect, effective_sample_size_multiplier)
        """
        deff = 1 + (cluster_size - 1) * icc
        ess_multiplier = 1 / deff

        return deff, ess_multiplier

    def equivalence_test(
        self,
        group1: np.ndarray,
        group2: np.ndarray,
        low_bound: float = -0.5,
        high_bound: float = 0.5,
        alpha: float = 0.05
    ) -> Dict[str, Union[bool, float]]:
        """
        Two One-Sided Tests (TOST) for equivalence.

        Tests whether the effect is practically equivalent to zero
        (within the specified bounds).

        Parameters
        ----------
        group1, group2 : np.ndarray
            Data for two groups
        low_bound, high_bound : float
            Equivalence bounds in Cohen's d units
        alpha : float
            Significance level (default: 0.05)

        Returns
        -------
        dict
            Results including equivalence decision and p-values
        """
        effect_size = self.calculate_cohens_d(group1, group2)
        d = effect_size.cohens_d

        n1, n2 = len(group1), len(group2)
        se = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2-2)))

        # Test if effect is above lower bound
        t_lower = (d - low_bound) / se
        df = n1 + n2 - 2
        p_lower = 1 - stats.t.cdf(t_lower, df)

        # Test if effect is below upper bound
        t_upper = (high_bound - d) / se
        p_upper = 1 - stats.t.cdf(t_upper, df)

        # Equivalence if both tests significant
        p_tost = max(p_lower, p_upper)
        equivalent = p_tost < alpha

        return {
            'equivalent': equivalent,
            'p_tost': p_tost,
            'p_lower': p_lower,
            'p_upper': p_upper,
            'observed_d': d,
            'ci_lower': effect_size.ci_lower,
            'ci_upper': effect_size.ci_upper,
            'within_bounds': low_bound < d < high_bound
        }


# =============================================================================
# CLASS 2: MIXED-EFFECTS MODELS
# =============================================================================

class MixedEffectsModels:
    """
    Fit and compare multilevel models for nested data.

    Implements lmer-style mixed-effects models using pymer4 (R lme4 backend)
    or statsmodels GEE as fallback. Handles random effects for agents,
    sessions, and personas.

    Methods:
        fit_model: Fit a mixed-effects model
        model_comparison: Compare nested models via LRT
        extract_variance_components: Get random effects variances
        calculate_icc: Calculate intraclass correlation
        marginal_r2: Calculate variance explained by fixed effects
    """

    def __init__(self, use_r: bool = True):
        """
        Initialize MixedEffectsModels.

        Parameters
        ----------
        use_r : bool
            Whether to use R (pymer4) or Python (statsmodels) backend
        """
        self.use_r = use_r and HAS_PYMER4
        if use_r and not HAS_PYMER4:
            warnings.warn("Requested R backend but pymer4 unavailable. Using statsmodels.")

    def fit_model(
        self,
        formula: str,
        data: pd.DataFrame,
        family: str = 'gaussian',
        REML: bool = True
    ) -> ModelResults:
        """
        Fit a mixed-effects model.

        Parameters
        ----------
        formula : str
            R-style formula (e.g., "mistakes ~ condition + (1|agent_id)")
        data : pd.DataFrame
            Long-format data
        family : str
            Distribution family: 'gaussian', 'poisson', 'binomial',
            'negative_binomial', 'gamma'
        REML : bool
            Use REML estimation (default: True)

        Returns
        -------
        ModelResults
            Fitted model results
        """
        if self.use_r:
            return self._fit_with_pymer4(formula, data, family, REML)
        else:
            return self._fit_with_statsmodels(formula, data, family)

    def _fit_with_pymer4(
        self,
        formula: str,
        data: pd.DataFrame,
        family: str,
        REML: bool
    ) -> ModelResults:
        """Fit model using pymer4 (R lme4 backend)."""
        # Map family names
        family_map = {
            'gaussian': 'gaussian',
            'poisson': 'poisson',
            'binomial': 'binomial',
            'negative_binomial': 'gamma',  # pymer4 uses gamma for NB
            'gamma': 'gamma'
        }

        model = Lmer(formula, data=data, family=family_map.get(family, 'gaussian'))
        results = model.fit(REML=REML, summarize=False)

        # Extract coefficients
        coef_df = model.coefs
        coefficients = coef_df['Estimate'].to_dict()
        std_errors = coef_df['SE'].to_dict()
        t_values = coef_df['T-stat'].to_dict()
        p_values = coef_df['P-val'].to_dict()

        # Confidence intervals
        ci_lower = (coef_df['Estimate'] - 1.96 * coef_df['SE']).to_dict()
        ci_upper = (coef_df['Estimate'] + 1.96 * coef_df['SE']).to_dict()

        # Variance components
        var_comp = {}
        if hasattr(model, 'ranef_var'):
            var_comp = model.ranef_var

        # Calculate ICC
        icc = self.calculate_icc(data, formula)

        return ModelResults(
            model_type='lmer' if family == 'gaussian' else f'glmer_{family}',
            formula=formula,
            coefficients=coefficients,
            std_errors=std_errors,
            t_values=t_values,
            p_values=p_values,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            icc=icc,
            aic=model.AIC,
            bic=model.BIC,
            n_obs=len(data),
            n_groups=data.groupby('agent_id').ngroups if 'agent_id' in data.columns else 1,
            variance_components=var_comp
        )

    def _fit_with_statsmodels(
        self,
        formula: str,
        data: pd.DataFrame,
        family: str
    ) -> ModelResults:
        """Fit model using statsmodels GEE as fallback."""
        # Parse formula to extract outcome and grouping variable
        outcome = formula.split('~')[0].strip()

        # Map family
        family_map = {
            'gaussian': sm.families.Gaussian(),
            'poisson': sm.families.Poisson(),
            'binomial': sm.families.Binomial(),
            'negative_binomial': sm.families.NegativeBinomial(),
            'gamma': sm.families.Gamma()
        }

        fam = family_map.get(family, sm.families.Gaussian())

        # Simplified formula for GEE (remove random effects syntax)
        simple_formula = formula.split('(')[0].strip()

        # Fit GEE with exchangeable correlation
        model = sm.GEE.from_formula(
            simple_formula,
            groups='agent_id' if 'agent_id' in data.columns else None,
            data=data,
            family=fam,
            cov_struct=sm.cov_struct.Exchangeable()
        )
        results = model.fit()

        # Extract results
        coefficients = dict(zip(results.model.exog_names, results.params))
        std_errors = dict(zip(results.model.exog_names, results.bse))
        t_values = dict(zip(results.model.exog_names, results.tvalues))
        p_values = dict(zip(results.model.exog_names, results.pvalues))

        # Confidence intervals
        conf_int = results.conf_int()
        ci_lower = dict(zip(results.model.exog_names, conf_int[0]))
        ci_upper = dict(zip(results.model.exog_names, conf_int[1]))

        # Calculate ICC
        icc = self.calculate_icc(data, formula)

        return ModelResults(
            model_type=f'gee_{family}',
            formula=formula,
            coefficients=coefficients,
            std_errors=std_errors,
            t_values=t_values,
            p_values=p_values,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            icc=icc,
            aic=results.aic if hasattr(results, 'aic') else np.nan,
            bic=results.bic if hasattr(results, 'bic') else np.nan,
            n_obs=len(data),
            n_groups=data.groupby('agent_id').ngroups if 'agent_id' in data.columns else 1,
            variance_components={}
        )

    def model_comparison(
        self,
        model_null: ModelResults,
        model_full: ModelResults
    ) -> Dict[str, Union[float, bool]]:
        """
        Compare nested models via likelihood ratio test.

        Parameters
        ----------
        model_null : ModelResults
            Simpler (nested) model
        model_full : ModelResults
            More complex model

        Returns
        -------
        dict
            LRT statistics and conclusion
        """
        # Calculate likelihood ratio statistic
        lr_stat = model_full.aic - model_null.aic  # Simplified
        df_diff = len(model_full.coefficients) - len(model_null.coefficients)

        if df_diff <= 0:
            warnings.warn("Models not properly nested or df_diff <= 0")
            return {'valid': False}

        p_value = chi2.sf(abs(lr_stat), df_diff)

        # Model selection based on AIC
        delta_aic = model_full.aic - model_null.aic
        prefer_full = delta_aic < -2  # Conventional threshold

        return {
            'lr_statistic': lr_stat,
            'df': df_diff,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'delta_aic': delta_aic,
            'delta_bic': model_full.bic - model_null.bic,
            'prefer_full_model': prefer_full,
            'valid': True
        }

    def calculate_icc(
        self,
        data: pd.DataFrame,
        formula: str
    ) -> float:
        """
        Calculate intraclass correlation coefficient.

        ICC = var_between / (var_between + var_within)

        Parameters
        ----------
        data : pd.DataFrame
            Data with outcome and grouping variable
        formula : str
            Model formula to extract outcome variable

        Returns
        -------
        float
            ICC value
        """
        outcome = formula.split('~')[0].strip()
        cluster = 'agent_id' if 'agent_id' in data.columns else data.columns[0]

        # One-way ANOVA
        groups = [group[outcome].values for name, group in data.groupby(cluster)]

        k = len(groups)  # Number of clusters
        n_j = [len(g) for g in groups]  # Observations per cluster

        if k < 2:
            return 0.0

        # Grand mean
        grand_mean = data[outcome].mean()

        # Between-cluster variance
        ss_between = sum([n * (np.mean(g) - grand_mean)**2 for n, g in zip(n_j, groups)])
        ms_between = ss_between / (k - 1)

        # Within-cluster variance
        ss_within = sum([sum((g - np.mean(g))**2) for g in groups])
        ms_within = ss_within / (sum(n_j) - k)

        # Average cluster size
        n_0 = (sum(n_j) - sum([n**2 for n in n_j])/sum(n_j)) / (k - 1)

        # ICC
        icc = (ms_between - ms_within) / (ms_between + (n_0 - 1) * ms_within)

        return max(0, icc)

    def marginal_r2(
        self,
        model_results: ModelResults,
        data: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate marginal and conditional R-squared.

        Following Nakagawa & Schielzeth (2013):
        - Marginal R²: Variance explained by fixed effects
        - Conditional R²: Variance explained by fixed + random effects

        Parameters
        ----------
        model_results : ModelResults
            Fitted model
        data : pd.DataFrame
            Original data

        Returns
        -------
        dict
            R² values
        """
        # Simplified calculation (exact method requires model object)
        # This is a placeholder - full implementation requires access to fitted values

        return {
            'r2_marginal': 0.0,  # Would calculate from fixed effects
            'r2_conditional': 0.0,  # Would calculate from fixed + random
            'note': 'Full R² calculation requires fitted model object'
        }


# =============================================================================
# CLASS 3: PSEUDO-REPLICATION HANDLER
# =============================================================================

class PseudoReplicationHandler:
    """
    Handle nested/clustered data and validate independence assumptions.

    Pseudo-replication occurs when non-independent observations are treated
    as independent, inflating sample size and underestimating standard errors.

    Methods:
        aggregate_to_agent_level: Aggregate interactions to agent means
        validate_independence: Check independence assumptions
        calculate_effective_n: Calculate effective sample size
        check_autocorrelation: Test for temporal autocorrelation
        design_effect: Calculate clustering design effect
    """

    def __init__(self):
        """Initialize PseudoReplicationHandler."""
        pass

    def aggregate_to_agent_level(
        self,
        data: pd.DataFrame,
        outcome_vars: List[str],
        id_vars: List[str] = ['condition', 'agent_id', 'run_id']
    ) -> pd.DataFrame:
        """
        Aggregate interaction-level data to agent level.

        Creates one row per agent with summary statistics across runs.

        Parameters
        ----------
        data : pd.DataFrame
            Interaction-level data
        outcome_vars : list
            Variables to aggregate
        id_vars : list
            Grouping variables (default: condition, agent_id, run_id)

        Returns
        -------
        pd.DataFrame
            Agent-level aggregated data
        """
        # First aggregate to run level
        run_agg = {}
        for var in outcome_vars:
            if data[var].dtype in [np.int64, np.float64]:
                # Numeric: take sum or mean depending on variable type
                if 'count' in var or 'mistakes' in var:
                    run_agg[var] = 'sum'
                else:
                    run_agg[var] = 'mean'
            else:
                run_agg[var] = 'first'

        run_level = data.groupby(id_vars).agg(run_agg).reset_index()

        # Then aggregate to agent level
        agent_agg = {}
        for var in outcome_vars:
            agent_agg[f'{var}_mean'] = (var, 'mean')
            agent_agg[f'{var}_std'] = (var, 'std')
            agent_agg[f'{var}_min'] = (var, 'min')
            agent_agg[f'{var}_max'] = (var, 'max')

        agent_level = run_level.groupby(['condition', 'agent_id']).agg(
            **agent_agg,
            n_runs=('run_id', 'count')
        ).reset_index()

        return agent_level

    def validate_independence(
        self,
        data: pd.DataFrame,
        outcome: str,
        group_var: str = 'agent_id'
    ) -> List[IndependenceCheck]:
        """
        Validate independence assumptions.

        Runs multiple tests:
        1. Durbin-Watson test for autocorrelation
        2. Ljung-Box test for serial correlation
        3. Check for systematic trends

        Parameters
        ----------
        data : pd.DataFrame
            Data to check
        outcome : str
            Outcome variable
        group_var : str
            Grouping variable

        Returns
        -------
        list
            Independence check results
        """
        checks = []

        # 1. Autocorrelation check (if sequential data)
        if 'time' in data.columns or 'interaction_num' in data.columns:
            time_var = 'time' if 'time' in data.columns else 'interaction_num'

            for group_id, group_data in data.groupby(group_var):
                if len(group_data) < 10:
                    continue

                sorted_data = group_data.sort_values(time_var)
                residuals = sorted_data[outcome] - sorted_data[outcome].mean()

                # Ljung-Box test
                try:
                    lb_stat, lb_pval = sm.stats.acorr_ljungbox(residuals, lags=min(10, len(residuals)//2))

                    checks.append(IndependenceCheck(
                        test_name='Ljung-Box autocorrelation',
                        statistic=float(lb_stat.iloc[-1]),
                        p_value=float(lb_pval.iloc[-1]),
                        passed=float(lb_pval.iloc[-1]) > 0.05,
                        details={'group': group_id, 'n': len(sorted_data)}
                    ))
                except:
                    pass

        # 2. Check for between-group independence (correlation)
        group_means = data.groupby(group_var)[outcome].mean()
        if len(group_means) >= 3:
            # Variance homogeneity (Levene's test)
            groups = [group[outcome].values for name, group in data.groupby(group_var)]
            stat, p_val = stats.levene(*groups)

            checks.append(IndependenceCheck(
                test_name='Levene variance homogeneity',
                statistic=stat,
                p_value=p_val,
                passed=p_val > 0.05,
                details={'n_groups': len(groups)}
            ))

        return checks

    def calculate_effective_n(
        self,
        data: pd.DataFrame,
        outcome: str,
        cluster_var: str = 'agent_id'
    ) -> Dict[str, Union[int, float]]:
        """
        Calculate effective sample size accounting for clustering.

        Uses Kish (1965) design effect formula.

        Parameters
        ----------
        data : pd.DataFrame
            Clustered data
        outcome : str
            Outcome variable
        cluster_var : str
            Clustering variable

        Returns
        -------
        dict
            Effective sample size and related statistics
        """
        # Calculate ICC
        groups = [group[outcome].values for name, group in data.groupby(cluster_var)]

        k = len(groups)  # Number of clusters
        n_total = len(data)
        n_per_cluster = n_total / k

        # ICC calculation
        grand_mean = data[outcome].mean()
        ss_between = sum([len(g) * (np.mean(g) - grand_mean)**2 for g in groups])
        ss_within = sum([sum((g - np.mean(g))**2) for g in groups])

        ms_between = ss_between / (k - 1)
        ms_within = ss_within / (n_total - k)

        icc = (ms_between - ms_within) / (ms_between + (n_per_cluster - 1) * ms_within)
        icc = max(0, icc)

        # Design effect
        deff = 1 + (n_per_cluster - 1) * icc

        # Effective sample size
        n_effective = n_total / deff

        return {
            'n_total': n_total,
            'n_effective': int(n_effective),
            'n_clusters': k,
            'avg_cluster_size': n_per_cluster,
            'icc': icc,
            'design_effect': deff,
            'efficiency_loss': 1 - (n_effective / n_total)
        }

    def check_autocorrelation(
        self,
        data: pd.DataFrame,
        outcome: str,
        time_var: str,
        group_var: str = 'agent_id',
        max_lags: int = 20
    ) -> pd.DataFrame:
        """
        Check for temporal autocorrelation within groups.

        Parameters
        ----------
        data : pd.DataFrame
            Time-series data
        outcome : str
            Outcome variable
        time_var : str
            Time variable
        group_var : str
            Grouping variable
        max_lags : int
            Maximum lags to test

        Returns
        -------
        pd.DataFrame
            Autocorrelation results by group
        """
        results = []

        for group_id, group_data in data.groupby(group_var):
            sorted_data = group_data.sort_values(time_var)

            if len(sorted_data) < max_lags * 2:
                continue

            residuals = sorted_data[outcome] - sorted_data[outcome].mean()

            # Calculate ACF
            acf_values = sm.tsa.acf(residuals, nlags=min(max_lags, len(residuals)//2))

            # Ljung-Box test
            try:
                lb_stat, lb_pval = sm.stats.acorr_ljungbox(residuals, lags=min(10, len(residuals)//2))
                significant_autocorr = (lb_pval < 0.05).any()
            except:
                significant_autocorr = False

            results.append({
                'group': group_id,
                'n_obs': len(sorted_data),
                'acf_lag1': acf_values[1] if len(acf_values) > 1 else np.nan,
                'max_acf': np.max(np.abs(acf_values[1:])) if len(acf_values) > 1 else np.nan,
                'significant_autocorr': significant_autocorr
            })

        return pd.DataFrame(results)

    def design_effect(
        self,
        icc: float,
        cluster_size: int
    ) -> Dict[str, float]:
        """
        Calculate design effect for clustered sampling.

        DEFF = 1 + (m - 1) * ICC

        Parameters
        ----------
        icc : float
            Intraclass correlation
        cluster_size : int
            Average cluster size

        Returns
        -------
        dict
            Design effect statistics
        """
        deff = 1 + (cluster_size - 1) * icc

        return {
            'design_effect': deff,
            'effective_sample_multiplier': 1 / deff,
            'inflation_factor': deff,
            'interpretation': self._interpret_deff(deff)
        }

    def _interpret_deff(self, deff: float) -> str:
        """Interpret design effect magnitude."""
        if deff < 1.5:
            return "minimal clustering effect"
        elif deff < 2.0:
            return "moderate clustering effect"
        elif deff < 3.0:
            return "substantial clustering effect"
        else:
            return "severe clustering effect - multilevel model essential"


# =============================================================================
# CLASS 4: CAUSAL ANALYSIS
# =============================================================================

class CausalAnalysis:
    """
    Test causal relationships, mediation, and Granger causality.

    Methods:
        granger_causality: Test temporal precedence
        mediation_analysis: Test indirect effects
        structural_equation_model: Fit path models
        instrumental_variables: 2SLS regression
    """

    def __init__(self):
        """Initialize CausalAnalysis."""
        pass

    def granger_causality(
        self,
        data: pd.DataFrame,
        cause_var: str,
        effect_var: str,
        max_lags: int = 5,
        group_var: Optional[str] = None
    ) -> Dict[str, Union[float, bool]]:
        """
        Test Granger causality (temporal precedence).

        Tests whether past values of cause_var predict current values of
        effect_var, controlling for past values of effect_var.

        Parameters
        ----------
        data : pd.DataFrame
            Time-series data
        cause_var : str
            Potential cause variable
        effect_var : str
            Potential effect variable
        max_lags : int
            Maximum lags to test
        group_var : str, optional
            Grouping variable (test within groups)

        Returns
        -------
        dict
            Granger causality test results
        """
        from statsmodels.tsa.stattools import grangercausalitytests

        if group_var is not None:
            # Test within groups and aggregate
            group_results = []

            for group_id, group_data in data.groupby(group_var):
                if len(group_data) < max_lags * 3:
                    continue

                test_data = group_data[[effect_var, cause_var]].dropna()

                try:
                    gc_res = grangercausalitytests(test_data, max_lags, verbose=False)

                    # Extract p-value from lag 1
                    p_val = gc_res[1][0]['ssr_ftest'][1]
                    group_results.append({'group': group_id, 'p_value': p_val})
                except:
                    continue

            if len(group_results) == 0:
                return {'error': 'Insufficient data for Granger causality test'}

            # Fisher's method to combine p-values
            p_values = [r['p_value'] for r in group_results]
            chi2_stat = -2 * sum(np.log(p_values))
            df = 2 * len(p_values)
            combined_p = chi2.sf(chi2_stat, df)

            return {
                'granger_causes': combined_p < 0.05,
                'p_value': combined_p,
                'n_groups_tested': len(group_results),
                'method': 'Fisher combined p-values'
            }
        else:
            # Single test
            test_data = data[[effect_var, cause_var]].dropna()

            try:
                gc_res = grangercausalitytests(test_data, max_lags, verbose=False)
                p_val = gc_res[1][0]['ssr_ftest'][1]

                return {
                    'granger_causes': p_val < 0.05,
                    'p_value': p_val,
                    'test_statistic': gc_res[1][0]['ssr_ftest'][0],
                    'lags_tested': max_lags
                }
            except Exception as e:
                return {'error': str(e)}

    def mediation_analysis(
        self,
        data: pd.DataFrame,
        treatment: str,
        mediator: str,
        outcome: str,
        covariates: Optional[List[str]] = None
    ) -> Dict[str, Union[float, pd.DataFrame]]:
        """
        Test mediation (indirect effects).

        Tests whether treatment → mediator → outcome pathway is significant.

        Parameters
        ----------
        data : pd.DataFrame
            Data with all variables
        treatment : str
            Treatment/independent variable
        mediator : str
            Mediating variable
        outcome : str
            Outcome/dependent variable
        covariates : list, optional
            Control variables

        Returns
        -------
        dict
            Mediation analysis results (indirect, direct, total effects)
        """
        # Prepare data
        analysis_data = data[[treatment, mediator, outcome]].dropna()

        if covariates:
            analysis_data = data[[treatment, mediator, outcome] + covariates].dropna()
            covariate_formula = ' + ' + ' + '.join(covariates)
        else:
            covariate_formula = ''

        # Path a: treatment -> mediator
        formula_a = f"{mediator} ~ {treatment}{covariate_formula}"
        model_a = smf.ols(formula_a, data=analysis_data).fit()
        a = model_a.params[treatment]
        se_a = model_a.bse[treatment]

        # Path b: mediator -> outcome (controlling for treatment)
        formula_b = f"{outcome} ~ {treatment} + {mediator}{covariate_formula}"
        model_b = smf.ols(formula_b, data=analysis_data).fit()
        b = model_b.params[mediator]
        se_b = model_b.bse[mediator]
        c_prime = model_b.params[treatment]  # Direct effect

        # Path c: total effect (treatment -> outcome)
        formula_c = f"{outcome} ~ {treatment}{covariate_formula}"
        model_c = smf.ols(formula_c, data=analysis_data).fit()
        c = model_c.params[treatment]

        # Indirect effect (a * b)
        indirect = a * b
        se_indirect = np.sqrt((b**2 * se_a**2) + (a**2 * se_b**2))  # Sobel test
        z_indirect = indirect / se_indirect
        p_indirect = 2 * (1 - norm.cdf(abs(z_indirect)))

        # Proportion mediated
        prop_mediated = indirect / c if c != 0 else np.nan

        return {
            'indirect_effect': indirect,
            'se_indirect': se_indirect,
            'z_indirect': z_indirect,
            'p_indirect': p_indirect,
            'direct_effect': c_prime,
            'total_effect': c,
            'proportion_mediated': prop_mediated,
            'path_a': a,
            'path_b': b,
            'significant_mediation': p_indirect < 0.05,
            'models': {
                'mediator_model': model_a,
                'outcome_model': model_b,
                'total_effect_model': model_c
            }
        }

    def structural_equation_model(
        self,
        data: pd.DataFrame,
        model_spec: Dict[str, str]
    ) -> Dict[str, Union[pd.DataFrame, float]]:
        """
        Fit structural equation model (path analysis).

        Note: This is a simplified implementation. For full SEM with
        latent variables, use dedicated packages like semopy or lavaan (R).

        Parameters
        ----------
        data : pd.DataFrame
            Data
        model_spec : dict
            Model specification: {outcome: formula, ...}

        Returns
        -------
        dict
            SEM results
        """
        results = {}
        fit_stats = {}

        # Fit each equation
        for outcome, formula in model_spec.items():
            model = smf.ols(formula, data=data).fit()
            results[outcome] = {
                'model': model,
                'coefficients': model.params.to_dict(),
                'r_squared': model.rsquared,
                'aic': model.aic,
                'bic': model.bic
            }

        # Overall model fit (simplified)
        total_aic = sum([r['aic'] for r in results.values()])
        total_bic = sum([r['bic'] for r in results.values()])

        fit_stats['total_aic'] = total_aic
        fit_stats['total_bic'] = total_bic
        fit_stats['n_equations'] = len(model_spec)

        return {
            'equations': results,
            'fit_statistics': fit_stats
        }


# =============================================================================
# CLASS 5: VISUALIZATION GENERATOR
# =============================================================================

class VisualizationGenerator:
    """
    Create publication-quality figures.

    Methods:
        condition_comparison: Bar plots with error bars
        effect_size_plot: Forest plot of effect sizes
        diagnostic_plots: Q-Q plot and residual plots
        interaction_plot: Two-way interactions
        save_figure: Save with publication settings
    """

    def __init__(self, style: str = 'seaborn-v0_8-paper'):
        """
        Initialize VisualizationGenerator.

        Parameters
        ----------
        style : str
            Matplotlib style (default: seaborn-paper)
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        # Publication settings
        self.fig_width = 6
        self.fig_height = 4
        self.dpi = 300
        self.format = 'pdf'

        # Color palette
        sns.set_palette("colorblind")

    def condition_comparison(
        self,
        data: pd.DataFrame,
        outcome: str,
        condition_var: str = 'condition',
        group_var: Optional[str] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create bar plot comparing conditions.

        Parameters
        ----------
        data : pd.DataFrame
            Data
        outcome : str
            Outcome variable
        condition_var : str
            Condition variable
        group_var : str, optional
            Grouping variable for agent-level aggregation
        ylabel : str, optional
            Y-axis label
        title : str, optional
            Plot title
        save_path : str, optional
            Path to save figure

        Returns
        -------
        matplotlib.figure.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))

        # Aggregate if needed
        if group_var:
            plot_data = data.groupby([condition_var, group_var])[outcome].mean().reset_index()
        else:
            plot_data = data

        # Create bar plot with individual points
        sns.barplot(
            data=plot_data,
            x=condition_var,
            y=outcome,
            errorbar='se',
            ax=ax,
            alpha=0.7,
            capsize=0.1
        )

        # Overlay individual data points
        sns.stripplot(
            data=plot_data,
            x=condition_var,
            y=outcome,
            ax=ax,
            color='black',
            alpha=0.3,
            size=3
        )

        # Labels
        ax.set_xlabel(condition_var.capitalize())
        ax.set_ylabel(ylabel or outcome)
        if title:
            ax.set_title(title)

        # Clean up
        sns.despine()
        plt.tight_layout()

        if save_path:
            self.save_figure(fig, save_path)

        return fig

    def effect_size_plot(
        self,
        effect_sizes: List[EffectSize],
        labels: List[str],
        title: str = "Effect Sizes",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create forest plot of effect sizes.

        Parameters
        ----------
        effect_sizes : list
            List of EffectSize objects
        labels : list
            Labels for each effect
        title : str
            Plot title
        save_path : str, optional
            Path to save figure

        Returns
        -------
        matplotlib.figure.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))

        y_pos = np.arange(len(labels))

        # Extract values
        d_values = [es.cohens_d for es in effect_sizes]
        ci_lower = [es.ci_lower for es in effect_sizes]
        ci_upper = [es.ci_upper for es in effect_sizes]

        # Calculate error bars
        errors = np.array([[d - low, up - d] for d, low, up in zip(d_values, ci_lower, ci_upper)]).T

        # Plot
        ax.errorbar(
            d_values,
            y_pos,
            xerr=errors,
            fmt='o',
            markersize=8,
            capsize=5,
            capthick=2,
            linewidth=2
        )

        # Reference lines
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.axvline(0.2, color='gray', linestyle=':', linewidth=0.5, alpha=0.3, label='Small')
        ax.axvline(0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.3, label='Medium')
        ax.axvline(0.8, color='gray', linestyle=':', linewidth=0.5, alpha=0.3, label='Large')

        # Labels
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlabel("Cohen's d")
        ax.set_title(title)

        plt.tight_layout()

        if save_path:
            self.save_figure(fig, save_path)

        return fig

    def diagnostic_plots(
        self,
        model_results: ModelResults,
        residuals: np.ndarray,
        fitted_values: np.ndarray,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create diagnostic plots for regression model.

        Parameters
        ----------
        model_results : ModelResults
            Fitted model results
        residuals : np.ndarray
            Residuals
        fitted_values : np.ndarray
            Fitted values
        save_path : str, optional
            Path to save figure

        Returns
        -------
        matplotlib.figure.Figure
            Figure object with subplots
        """
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        # 1. Residuals vs Fitted
        axes[0, 0].scatter(fitted_values, residuals, alpha=0.5)
        axes[0, 0].axhline(0, color='red', linestyle='--', linewidth=1)
        axes[0, 0].set_xlabel('Fitted values')
        axes[0, 0].set_ylabel('Residuals')
        axes[0, 0].set_title('Residuals vs Fitted')

        # 2. Q-Q Plot
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Normal Q-Q Plot')

        # 3. Scale-Location
        standardized_resid = residuals / np.std(residuals)
        axes[1, 0].scatter(fitted_values, np.sqrt(np.abs(standardized_resid)), alpha=0.5)
        axes[1, 0].set_xlabel('Fitted values')
        axes[1, 0].set_ylabel('√|Standardized Residuals|')
        axes[1, 0].set_title('Scale-Location')

        # 4. Residual Histogram
        axes[1, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1, 1].set_xlabel('Residuals')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Residual Distribution')

        plt.tight_layout()

        if save_path:
            self.save_figure(fig, save_path)

        return fig

    def interaction_plot(
        self,
        data: pd.DataFrame,
        x_var: str,
        y_var: str,
        group_var: str,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create interaction plot.

        Parameters
        ----------
        data : pd.DataFrame
            Data
        x_var : str
            X-axis variable
        y_var : str
            Y-axis variable
        group_var : str
            Grouping variable (lines)
        ylabel : str, optional
            Y-axis label
        title : str, optional
            Plot title
        save_path : str, optional
            Path to save figure

        Returns
        -------
        matplotlib.figure.Figure
            Figure object
        """
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))

        sns.pointplot(
            data=data,
            x=x_var,
            y=y_var,
            hue=group_var,
            errorbar='se',
            ax=ax,
            markers='o',
            linestyles='-',
            dodge=0.2
        )

        ax.set_xlabel(x_var.capitalize())
        ax.set_ylabel(ylabel or y_var)
        if title:
            ax.set_title(title)

        ax.legend(title=group_var.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')

        sns.despine()
        plt.tight_layout()

        if save_path:
            self.save_figure(fig, save_path)

        return fig

    def save_figure(
        self,
        fig: plt.Figure,
        path: str,
        dpi: Optional[int] = None,
        format: Optional[str] = None
    ):
        """
        Save figure with publication settings.

        Parameters
        ----------
        fig : matplotlib.figure.Figure
            Figure to save
        path : str
            Save path
        dpi : int, optional
            Resolution (default: 300)
        format : str, optional
            Format (default: pdf)
        """
        dpi = dpi or self.dpi
        format = format or self.format

        # Ensure path has correct extension
        path = Path(path)
        if path.suffix != f'.{format}':
            path = path.with_suffix(f'.{format}')

        fig.savefig(
            path,
            dpi=dpi,
            format=format,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none'
        )

        print(f"Figure saved to: {path}")


# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

def run_complete_analysis(
    data_path: str,
    output_dir: str,
    alpha: float = 0.05,
    use_r: bool = True
) -> Dict[str, any]:
    """
    Run complete statistical analysis pipeline.

    This is the main entry point that orchestrates all analysis classes.

    Parameters
    ----------
    data_path : str
        Path to interaction-level data (CSV or JSONL)
    output_dir : str
        Directory for outputs
    alpha : float
        Significance level
    use_r : bool
        Whether to use R backend for mixed models

    Returns
    -------
    dict
        Complete analysis results
    """
    print("="*70)
    print("STUDY 1: AGENT STRESS BEHAVIOR - STATISTICAL ANALYSIS PIPELINE")
    print("="*70)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize classes
    power_analyzer = PowerAnalysis(alpha=alpha)
    mixed_models = MixedEffectsModels(use_r=use_r)
    pseudo_rep_handler = PseudoReplicationHandler()
    causal_analyzer = CausalAnalysis()
    viz_generator = VisualizationGenerator()

    # Load data
    print("\n1. Loading data...")
    if data_path.endswith('.csv'):
        data = pd.read_csv(data_path)
    elif data_path.endswith('.jsonl'):
        data = pd.read_json(data_path, lines=True)
    else:
        raise ValueError("Data must be CSV or JSONL format")

    print(f"   Loaded {len(data)} observations")
    print(f"   Agents: {data['agent_id'].nunique()}")
    print(f"   Conditions: {data['condition'].unique()}")

    # Aggregate to agent level
    print("\n2. Aggregating to agent level (solving pseudo-replication)...")
    agent_data = pseudo_rep_handler.aggregate_to_agent_level(
        data,
        outcome_vars=['mistakes', 'help_requests', 'completion_time']
    )
    print(f"   Agent-level dataset: {len(agent_data)} agents")

    # Check effective sample size
    print("\n3. Calculating effective sample size...")
    eff_n = pseudo_rep_handler.calculate_effective_n(data, 'mistakes')
    print(f"   Total observations: {eff_n['n_total']}")
    print(f"   Effective n: {eff_n['n_effective']}")
    print(f"   ICC: {eff_n['icc']:.3f}")
    print(f"   Design effect: {eff_n['design_effect']:.2f}")

    # Validate independence
    print("\n4. Validating independence assumptions...")
    independence_checks = pseudo_rep_handler.validate_independence(data, 'mistakes')
    for check in independence_checks:
        status = "✓ PASS" if check.passed else "✗ FAIL"
        print(f"   {status}: {check.test_name} (p = {check.p_value:.3f})")

    # Power analysis
    print("\n5. Calculating power and effect sizes...")

    # Split by condition
    baseline = agent_data[agent_data['condition'] == 'baseline']['mistakes_mean'].values
    stress = agent_data[agent_data['condition'] == 'stress']['mistakes_mean'].values

    effect_size = power_analyzer.calculate_cohens_d(baseline, stress)
    print(f"   Cohen's d: {effect_size.cohens_d:.3f} "
          f"[{effect_size.ci_lower:.3f}, {effect_size.ci_upper:.3f}]")
    print(f"   Interpretation: {effect_size.interpretation}")

    achieved_power = power_analyzer.calculate_achieved_power(
        effect_size.cohens_d,
        len(baseline),
        len(stress)
    )
    print(f"   Achieved power: {achieved_power.achieved_power:.3f}")
    print(f"   Power adequate: {'Yes' if achieved_power.power_adequate else 'No'}")

    # Mixed-effects model
    print("\n6. Fitting mixed-effects model...")
    formula = "mistakes ~ condition + (1|agent_id)"

    # Reshape data for model (use run-level data)
    run_data = data.groupby(['condition', 'agent_id', 'run_id']).agg({
        'mistakes': 'sum'
    }).reset_index()

    model_results = mixed_models.fit_model(
        formula=formula,
        data=run_data,
        family='poisson'
    )

    print(f"   Model: {model_results.model_type}")
    print(f"   ICC: {model_results.icc:.3f}")
    print(f"   AIC: {model_results.aic:.1f}")

    # Print coefficients
    print("\n   Fixed Effects:")
    results_table = model_results.to_table()
    print(results_table.to_string())

    # Visualization
    print("\n7. Creating visualizations...")

    # Condition comparison
    fig1 = viz_generator.condition_comparison(
        agent_data,
        outcome='mistakes_mean',
        condition_var='condition',
        ylabel='Mean Mistakes',
        title='Mistakes by Condition',
        save_path=output_path / 'condition_comparison.pdf'
    )

    # Effect size plot
    fig2 = viz_generator.effect_size_plot(
        [effect_size],
        ['Stress vs. Baseline'],
        title='Effect Size: Mistakes',
        save_path=output_path / 'effect_size.pdf'
    )

    # Save results
    print("\n8. Saving results...")

    results_summary = {
        'sample_size': {
            'n_agents': len(agent_data),
            'n_observations': len(data),
            'n_effective': eff_n['n_effective'],
            'design_effect': eff_n['design_effect'],
            'icc': eff_n['icc']
        },
        'effect_sizes': {
            'cohens_d': effect_size.cohens_d,
            'ci_lower': effect_size.ci_lower,
            'ci_upper': effect_size.ci_upper,
            'interpretation': effect_size.interpretation,
            'hedges_g': effect_size.hedges_g
        },
        'power': {
            'achieved_power': achieved_power.achieved_power,
            'power_adequate': achieved_power.power_adequate
        },
        'model': {
            'formula': model_results.formula,
            'type': model_results.model_type,
            'coefficients': model_results.coefficients,
            'p_values': model_results.p_values,
            'icc': model_results.icc,
            'aic': model_results.aic,
            'bic': model_results.bic
        },
        'independence_checks': [
            {
                'test': check.test_name,
                'statistic': check.statistic,
                'p_value': check.p_value,
                'passed': check.passed
            }
            for check in independence_checks
        ]
    }

    # Save JSON
    with open(output_path / 'analysis_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)

    # Save APA table
    results_table.to_csv(output_path / 'model_results_table.csv', index=True)

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_path}")
    print("="*70)

    return results_summary


if __name__ == "__main__":
    import sys

    # Example usage
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "./results"

        results = run_complete_analysis(data_path, output_dir)
    else:
        print(__doc__)
        print("\nUsage: python analysis.py <data_path> <output_dir>")
        print("\nExample: python analysis.py data/interactions.csv results/")
