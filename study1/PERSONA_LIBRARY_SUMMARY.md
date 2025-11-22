# 50-Persona Systematic Design Library - Summary

**Created**: 2025-11-22
**Design Type**: Full factorial (5 × 5 × 2 = 50 personas)
**Status**: Pre-registered, ready for experimental deployment

---

## Design Overview

### Factorial Structure

This library implements a complete 3-dimensional factorial design:

**Dimension 1: Risk Tolerance (5 levels)**
1. Ultra-conservative: "Prioritize accuracy over speed; triple-check everything"
2. Conservative: "Be thorough and careful; avoid mistakes"
3. Moderate: "Balance speed and accuracy appropriately"
4. Risk-tolerant: "Move fast and iterate quickly"
5. Ultra risk-tolerant: "Prioritize innovation; fail fast and learn"

**Dimension 2: Self-Monitoring (5 levels)**
1. None: "Focus on task completion"
2. Low: "Complete tasks efficiently"
3. Moderate: "Track your progress on tasks"
4. High: "Regularly evaluate your performance"
5. Very High: "Continuously assess output quality and self-reflect"

**Dimension 3: Domain (2 levels)**
- Technical: Software engineer / data scientist / systems architect
- Creative: Creative strategist / content creator / UX designer

**Total Coverage**: 5 × 5 × 2 = 50 unique personas

---

## Key Design Features

### 1. Systematic Variation
- Every combination of (risk × monitoring × domain) represented exactly once
- No ad-hoc or cherry-picked personas
- Balanced coverage across design space

### 2. Clear Differentiation
- Each persona has unique system prompt
- Explicit variation in risk tolerance instructions
- Explicit variation in self-monitoring instructions
- Domain-appropriate expertise and communication style

### 3. Pre-Registered Predictions
- Expected effect magnitude for all 50 personas
- Testable hypotheses about main effects and interactions
- Falsification criteria specified in advance

### 4. Theory-Driven
Based on pilot study findings:
- **Seshat** (technical, moderate risk, high monitoring): Positive effect
- **Ma'at** (creative, risk-tolerant, low monitoring): Negative effect

Extended to systematic 50-persona design to test theoretical framework.

---

## Expected Performance Distribution

### Top 10 Performers (Expected)

| Rank | ID | Profile | Expected Effect |
|------|----|---------|--------------|
| 1 | persona_015 | Moderate-Risk, Max-Monitor, Technical | +0.90 |
| 2 | persona_014 | Moderate-Risk, High-Monitor, Technical | +0.85 |
| 3 | persona_020 | Risk-Tolerant, Max-Monitor, Technical | +0.80 |
| 4 | persona_009 | Conservative, High-Monitor, Technical | +0.80 |
| 5 | persona_010 | Conservative, Max-Monitor, Technical | +0.75 |
| 6 | persona_019 | Risk-Tolerant, High-Monitor, Technical | +0.75 |
| 7 | persona_004 | Ultra-Conservative, High-Monitor, Technical | +0.70 |
| 8 | persona_013 | Moderate-Risk, Moderate-Monitor, Technical | +0.65 |
| 9 | persona_040 | Moderate-Risk, Max-Monitor, Creative | +0.60 |
| 10 | persona_018 | Risk-Tolerant, Moderate-Monitor, Technical | +0.60 |

**Pattern**: All top performers are technical domain; 9/10 have high/max monitoring; 7/10 have moderate/risk-tolerant risk levels.

### Bottom 10 Performers (Expected)

| Rank | ID | Profile | Expected Effect |
|------|----|---------|-----------------|
| 50 | persona_046 | Ultra-Risk, Low-Monitor, Creative | -0.70 |
| 49 | persona_047 | Ultra-Risk, Low-Self-Monitor, Creative | -0.50 |
| 48 | persona_026 | Ultra-Conservative, Low-Monitor, Creative | -0.50 |
| 47 | persona_041 | Risk-Tolerant, Low-Monitor, Creative | -0.40 |
| 46 | persona_042 | Risk-Tolerant, Low-Self-Monitor, Creative | -0.30 |
| 45 | persona_027 | Ultra-Conservative, Low-Self-Monitor, Creative | -0.30 |
| 44 | persona_031 | Conservative, Low-Monitor, Creative | -0.25 |
| 43 | persona_032 | Conservative, Low-Self-Monitor, Creative | -0.20 |
| 42 | persona_021 | Ultra-Risk, Low-Monitor, Technical | -0.20 |
| 41 | persona_036 | Moderate-Risk, Low-Monitor, Creative | -0.15 |

**Pattern**: 9/10 are creative domain; all have low/no monitoring; extreme risk tolerance (ultra-conservative or ultra-risk).

---

## Predicted Main Effects

### Self-Monitoring Effect (Strongest)

| Level | Mean Effect | Interpretation |
|-------|------------|----------------|
| 1 (None) | -0.10 | Negative: no learning or adaptation |
| 2 (Low) | +0.05 | Slightly positive: minimal improvement |
| 3 (Moderate) | +0.30 | Moderate: progress tracking helps |
| 4 (High) | +0.50 | Strong: systematic self-evaluation |
| 5 (Very High) | +0.55 | Strongest: continuous reflection |

**Expected**: Linear increase; d ≈ 1.3 from lowest to highest

### Domain Effect (Second Strongest)

| Domain | Mean Effect | Interpretation |
|--------|------------|----------------|
| Technical | +0.45 | Positive: structured problem-solving |
| Creative | +0.10 | Weak positive: more variable outcomes |

**Expected**: Technical advantage of d ≈ 0.88

### Risk Tolerance Effect (Curvilinear)

| Level | Mean Effect | Interpretation |
|-------|------------|----------------|
| 1 (Ultra-conservative) | +0.15 | Slow but accurate |
| 2 (Conservative) | +0.30 | Reliable and thorough |
| 3 (Moderate) | +0.50 | **Optimal**: balanced |
| 4 (Risk-tolerant) | +0.35 | Fast but some errors |
| 5 (Ultra risk-tolerant) | +0.10 | Reckless; errors outweigh speed |

**Expected**: Inverted U-curve; peak at moderate risk

---

## Predicted Interactions

### Self-Monitoring × Domain (Strongest Interaction)

**Technical domain**: Strong linear effect of monitoring
- Slope: +0.14 per monitoring level
- Monitoring highly beneficial in structured domain

**Creative domain**: Weaker, non-linear effect
- Slope: +0.19 per monitoring level (but starting negative)
- Monitoring helps but doesn't fully compensate for domain challenges

**Interaction size**: η² ≈ 0.15

### Risk Tolerance × Domain

**Technical domain**: Moderate risk optimal
- Too conservative: slow and rigid
- Too risky: errors and rework
- Sweet spot: risk levels 2-4

**Creative domain**: Higher risk more tolerated but still needs monitoring
- Conservative creativity is constrained
- Ultra-risk creativity is chaotic
- Needs monitoring to productively channel creative risk

**Interaction size**: η² ≈ 0.08

### Risk Tolerance × Self-Monitoring

**High monitoring**: Enables productive risk-taking
- Can take calculated risks because monitoring catches errors
- Risk levels 3-4 excel with high monitoring

**Low monitoring**: Risk is harmful
- Without monitoring, risk-taking leads to compounding errors
- Only conservative approaches viable

**Interaction size**: η² ≈ 0.05 (weaker)

---

## Statistical Power Analysis

### Sample Size
- 50 personas × 10 tasks each = 500 observations
- Between-persona design: n=50
- Within-persona repeated measures: n=10

### Detectable Effect Sizes

**Main effects** (α=0.05, power=0.80):
- Risk tolerance: d ≥ 0.40
- Self-monitoring: d ≥ 0.40
- Domain: d ≥ 0.57

**Two-way interactions** (α=0.05, power=0.80):
- Monitor×Domain: f² ≥ 0.18 (medium effect)
- Risk×Domain: f² ≥ 0.18
- Risk×Monitor: f² ≥ 0.10 (small-medium)

**Model R²**: Expecting 0.65-0.75, will detect if R² ≥ 0.45

---

## Implementation Guidelines

### How to Use This Library

**1. Load persona definitions:**
```python
from persona_library_50 import PERSONAS_50, get_persona

persona = get_persona("persona_015")
system_prompt = persona["system_prompt"]
```

**2. Apply to experimental tasks:**
- Use system_prompt as AI agent's system message
- Run standardized task battery
- Score performance on consistent criteria
- Compare to predictions

**3. Filter by dimension:**
```python
from persona_library_50 import get_personas_by_dimension

# All high-monitoring technical personas
tech_high_monitor = get_personas_by_dimension(
    monitoring=4,
    domain="technical"
)
```

**4. Validate design:**
```python
from persona_library_50 import validate_design
validate_design()  # Ensures all 50 combinations present
```

---

## Quality Assurance

### Design Validation

✓ **Factorial completeness**: All 50 combinations present
✓ **Unique prompts**: Each persona has distinct system prompt
✓ **Systematic variation**: Clear modulation of risk and monitoring language
✓ **Domain appropriateness**: Expertise and context match domain

### Pre-Registration

✓ **Predictions documented**: All 50 personas have expected effects
✓ **Hypotheses specified**: Main effects and interactions pre-registered
✓ **Falsification criteria**: Clear conditions that would disprove theory
✓ **Analysis plan**: Statistical tests specified before data collection

### Reproducibility

✓ **Code provided**: Python library with all definitions
✓ **CSV matrix**: Design structure in tabular format
✓ **Detailed predictions**: Effect magnitudes and rationales documented
✓ **Example prompts**: 5 extreme cases demonstrated

---

## Files in This Package

| File | Purpose |
|------|---------|
| `persona_library_50.py` | Complete persona definitions with validation |
| `persona_design_matrix.csv` | Design structure and predictions in tabular format |
| `PERSONA_PREDICTIONS.md` | Detailed pre-registered hypotheses for all 50 |
| `EXAMPLE_PROMPTS.md` | Full system prompts for 5 extreme personas |
| `PERSONA_LIBRARY_SUMMARY.md` | This file - overview and usage guide |

---

## Research Questions Addressed

This 50-persona design enables testing:

**RQ1**: Does self-monitoring improve agent performance?
- **Prediction**: Yes, linear positive effect

**RQ2**: Does domain (technical vs creative) moderate agent performance?
- **Prediction**: Yes, technical domain advantage

**RQ3**: Is there an optimal risk tolerance level?
- **Prediction**: Yes, moderate risk (level 3) optimal

**RQ4**: Do self-monitoring and domain interact?
- **Prediction**: Yes, monitoring more beneficial in technical domain

**RQ5**: Can monitoring compensate for suboptimal risk tolerance?
- **Prediction**: Partially, but cannot fully overcome extreme risk levels

**RQ6**: Are there emergent clusters beyond the 3-factor structure?
- **Exploratory**: May find performance clusters

---

## Comparison to Pilot Study

### Pilot Design (5 personas)
- **Seshat**: Technical, balanced risk, high monitoring → **Positive**
- **Ma'at**: Creative, risk-tolerant, low monitoring → **Negative**
- **Thoth**, **Ra**, **Ptah**: Mixed profiles, varied results

### This Design (50 personas)
- **Systematic replication**: persona_014 = Seshat profile
- **Theoretical extension**: Varies each dimension systematically
- **Enhanced coverage**: Tests extreme combinations (ultra-conservative, ultra-risk)
- **Interaction testing**: Sufficient N to detect two-way interactions
- **Generalizability**: Not cherry-picked; covers full design space

---

## Expected Outcomes

### If Predictions Hold

**Scientific contribution:**
1. Confirms self-monitoring is key driver of agent performance
2. Identifies optimal persona profile (moderate risk, high monitoring, technical)
3. Shows domain × monitoring interaction
4. Demonstrates risk tolerance has inverted-U relationship
5. Validates theory from pilot study at larger scale

**Practical implications:**
1. AI agents should be prompted with self-monitoring instructions
2. Technical tasks benefit more from monitoring than creative tasks
3. Moderate risk-taking is optimal (neither too cautious nor too reckless)
4. Persona design matters for performance

### If Predictions Fail

**Still valuable:**
- Falsification teaches us something important
- May discover unexpected patterns in 50-persona data
- Cluster analysis may reveal alternative structure
- Could show pilot results were spurious or context-dependent

**Commitment**: Will publish results either way

---

## Next Steps

1. **Deploy experimental protocol**
   - Run all 50 personas on standardized task battery
   - Ensure blind scoring and randomization

2. **Collect data**
   - 10 tasks × 50 personas = 500 observations
   - Record: completion time, error rate, quality score, task success

3. **Analyze results**
   - Test pre-registered hypotheses
   - Compare predictions to actual performance
   - Exploratory analyses for unexpected patterns

4. **Document findings**
   - Report all 50 personas (no cherry-picking)
   - Compare to pilot study
   - Update theory based on results

5. **Iterate**
   - If theory confirmed: refine optimal persona profile
   - If theory falsified: develop alternative theory
   - Either way: advance science of AI agent design

---

## Contact & Citation

**Authors**: Prompt Engineering Research Team
**Affiliation**: Data-Statistics VC Hype Simulation Project
**Date**: 2025-11-22

**Suggested citation:**
```
Prompt Engineering Team (2025). Systematic 50-Persona Design Library
for AI Agent Performance Research. Pre-registered experimental design.
https://github.com/[repo]/study1/
```

**License**: Open for research use with attribution

---

## Appendix: Design Space Visualization

### Persona Distribution Across Dimensions

**By Risk Tolerance:**
- Level 1: 10 personas (5 technical, 5 creative)
- Level 2: 10 personas (5 technical, 5 creative)
- Level 3: 10 personas (5 technical, 5 creative)
- Level 4: 10 personas (5 technical, 5 creative)
- Level 5: 10 personas (5 technical, 5 creative)

**By Self-Monitoring:**
- Level 1: 10 personas (5 technical, 5 creative)
- Level 2: 10 personas (5 technical, 5 creative)
- Level 3: 10 personas (5 technical, 5 creative)
- Level 4: 10 personas (5 technical, 5 creative)
- Level 5: 10 personas (5 technical, 5 creative)

**By Domain:**
- Technical: 25 personas (5 per risk level, 5 per monitoring level)
- Creative: 25 personas (5 per risk level, 5 per monitoring level)

**Perfect balance**: Each cell of the 5×5×2 design has exactly 1 persona.

### Performance Distribution (Predicted)

**Predicted effect magnitude ranges:**
- Negative strong (-0.70 to -0.50): 3 personas
- Negative moderate (-0.49 to -0.30): 4 personas
- Negative weak (-0.29 to -0.10): 5 personas
- Null (-0.09 to +0.09): 6 personas
- Positive weak (+0.10 to +0.29): 8 personas
- Positive moderate (+0.30 to +0.59): 12 personas
- Positive strong (+0.60 to +0.79): 8 personas
- Positive very strong (+0.80 to +1.00): 4 personas

**Distribution shape**: Right-skewed (more positive than negative personas expected)

---

**Status**: Ready for experimental deployment
**Validation**: ✓ Design complete and verified
**Pre-registration**: ✓ Predictions documented before data collection
