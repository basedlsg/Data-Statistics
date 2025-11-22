# 50-Persona Systematic Experimental Design

**Research Study**: Next-Generation Agent Performance Protocol
**Design Type**: 5 × 5 × 2 Full Factorial
**Status**: ✓ Validated, Pre-Registered, Ready for Deployment
**Created**: 2025-11-22

---

## Quick Start

```python
# Load the persona library
from persona_library_50 import PERSONAS_50, get_persona

# Get a specific persona
persona = get_persona("persona_015")  # Best predicted performer
print(persona["system_prompt"])

# Filter personas by dimensions
from persona_library_50 import get_personas_by_dimension

# All high-monitoring technical personas
high_tech = get_personas_by_dimension(monitoring=4, domain="technical")
```

---

## What This Is

A systematically designed library of **50 unique AI agent personas** varying across three theoretically-motivated dimensions:

1. **Risk Tolerance** (5 levels): Ultra-conservative → Ultra risk-tolerant
2. **Self-Monitoring** (5 levels): None → Very High
3. **Domain** (2 levels): Technical vs Creative

Every combination of (risk × monitoring × domain) is represented exactly once, providing complete factorial coverage for rigorous experimental testing.

---

## Files in This Package

| File | Description |
|------|-------------|
| **persona_library_50.py** | Complete persona definitions with system prompts and validation functions |
| **persona_design_matrix.csv** | Design structure and pre-registered predictions in CSV format |
| **PERSONA_PREDICTIONS.md** | Detailed hypotheses and expected effects for all 50 personas |
| **EXAMPLE_PROMPTS.md** | Full system prompts for 5 extreme personas (best, worst, baseline, etc.) |
| **PERSONA_LIBRARY_SUMMARY.md** | Comprehensive overview, theory, and implementation guide |
| **validate_design.py** | Validation script with summary statistics |
| **README_PERSONA_LIBRARY.md** | This file - quick start guide |

---

## Design Highlights

### Factorial Structure
- **Total personas**: 50 (no duplicates, complete coverage)
- **Balance**: Each dimension level equally represented
- **Systematic**: No ad-hoc or cherry-picked personas

### Pre-Registered Predictions

**Top predicted performer:**
- **persona_015**: Moderate-Risk, Max-Monitor, Technical (+0.90 effect)

**Worst predicted performer:**
- **persona_046**: Ultra-Risk, Low-Monitor, Creative (-0.70 effect)

**Baseline control:**
- **persona_013**: Moderate across all dimensions (+0.65 effect)

### Expected Main Effects

| Dimension | Effect | Pattern |
|-----------|--------|---------|
| Self-Monitoring | **Strongest** (d ≈ 1.3) | Linear increase |
| Domain | **Strong** (d ≈ 0.9) | Technical > Creative |
| Risk Tolerance | **Moderate** | Inverted U (peak at level 3) |

### Key Interaction

**Self-Monitoring × Domain**: Monitoring is more beneficial in technical domain than creative domain (η² ≈ 0.15)

---

## Validation Results

```
✓ All 50 factorial combinations present
✓ No duplicates
✓ CSV consistent with library
✓ Mean predicted effect: +0.244
✓ Effect range: -0.70 to +0.90
✓ Distribution: Right-skewed (more positive than negative)
```

**By dimension:**
- Risk levels 1-5: +0.15, +0.28, **+0.44**, +0.31, +0.05 (peak at 3)
- Monitor levels 1-5: -0.15, 0.00, +0.32, +0.51, **+0.54** (monotonic increase)
- Domain: Technical +0.46, Creative +0.03

---

## Research Applications

### Primary Use Cases

1. **Test agent performance theories**: Systematic variation enables causal inference
2. **Identify optimal persona profiles**: Find best-performing combinations
3. **Understand interactions**: How dimensions combine to affect performance
4. **Replicate pilot findings**: persona_014 = Seshat profile from pilot study
5. **Generalize beyond pilot**: Not cherry-picked; covers full design space

### Experimental Protocol

**Recommended design:**
- Run all 50 personas on standardized task battery
- 10 tasks per persona = 500 total observations
- Mix of technical and creative tasks
- Blind scoring for quality assessment
- Compare actual to predicted performance

**Statistical power:**
- Can detect main effects: d ≥ 0.40
- Can detect interactions: f² ≥ 0.18
- Expected model R²: 0.65-0.75

---

## Theory Overview

Based on pilot study where:
- **Seshat** (technical, moderate risk, high monitoring) → Positive effect
- **Ma'at** (creative, risk-tolerant, low monitoring) → Negative effect

**Core hypotheses:**

**H1 (Self-Monitoring)**: Higher monitoring improves performance by enabling learning and error correction
- Prediction: Linear positive effect

**H2 (Domain)**: Technical domain advantages from structured problem-solving
- Prediction: Technical > Creative

**H3 (Risk Tolerance)**: Moderate risk balances speed and accuracy
- Prediction: Inverted U-curve

**H4 (Monitoring × Domain)**: Monitoring more beneficial in technical contexts
- Prediction: Stronger monitoring effect in technical domain

---

## Example Personas

### persona_015 (Best Expected)
**Profile**: Moderate-Risk, Max-Monitor, Technical
**Predicted effect**: +0.90

```
You are a principal data scientist and technical strategist...
Balance speed and accuracy appropriately.
Continuously assess output quality and self-reflect...
```

### persona_046 (Worst Expected)
**Profile**: Ultra-Risk, Low-Monitor, Creative
**Predicted effect**: -0.70

```
You are an avant-garde artist and provocative content creator...
Prioritize innovation; fail fast and learn.
Focus on task completion and boundary-pushing ideas...
```

### persona_013 (Baseline Control)
**Profile**: Moderate-Risk, Moderate-Monitor, Technical
**Predicted effect**: +0.65

```
You are a systems architect designing scalable applications...
Balance speed and accuracy appropriately.
Track your progress on tasks to ensure balanced outcomes...
```

See `EXAMPLE_PROMPTS.md` for complete system prompts.

---

## How to Use

### 1. Load and Explore

```python
from persona_library_50 import PERSONAS_50

# Browse all personas
for pid, persona in PERSONAS_50.items():
    print(f"{pid}: {persona['name']}")
    print(f"  Risk={persona['risk_tolerance']}, "
          f"Monitor={persona['self_monitoring']}, "
          f"Domain={persona['domain']}")
```

### 2. Deploy in Experiments

```python
# Get persona system prompt
persona = get_persona("persona_014")  # Seshat profile
system_prompt = persona["system_prompt"]

# Use with AI agent
agent = AIAgent(system_message=system_prompt)
result = agent.run_task(task)

# Score and record
performance = score_result(result)
record_data(persona_id="persona_014", performance=performance)
```

### 3. Analyze Results

```python
import pandas as pd

# Load predictions
predictions = pd.read_csv("persona_design_matrix.csv")

# Load actual results
results = pd.read_csv("experimental_results.csv")

# Compare
comparison = predictions.merge(results, on="persona_id")
correlation = comparison[['effect_magnitude', 'actual_performance']].corr()

# Test hypotheses
anova_results = run_factorial_anova(
    dv='actual_performance',
    factors=['risk_tolerance', 'self_monitoring', 'domain'],
    data=results
)
```

### 4. Validate Design

```bash
python validate_design.py
```

Output includes:
- Factorial completeness check
- CSV consistency validation
- Summary statistics of predictions
- Dimensional breakdowns
- Extreme persona identification

---

## Pre-Registration Commitment

We commit to:
1. ✓ Running all 50 personas (no selective reporting)
2. ✓ Reporting results regardless of prediction accuracy
3. ✓ Disclosing any protocol deviations
4. ✓ Publishing null results if predictions fail
5. ✓ Updating theory based on evidence

**Pre-registered predictions documented in**: `PERSONA_PREDICTIONS.md`
**Analysis plan**: Specified before data collection
**Falsification criteria**: Documented in predictions file

---

## Citation

If you use this persona library, please cite:

```bibtex
@misc{persona_library_50_2025,
  title={Systematic 50-Persona Design Library for AI Agent Performance Research},
  author={Prompt Engineering Research Team},
  year={2025},
  howpublished={Pre-registered experimental design},
  note={Full factorial design: 5 (risk) × 5 (monitoring) × 2 (domain)}
}
```

---

## Quality Assurance

**Design validation:**
- ✓ All 50 combinations present
- ✓ No duplicates
- ✓ Balanced coverage
- ✓ Unique system prompts

**Scientific rigor:**
- ✓ Pre-registered predictions
- ✓ Theory-driven design
- ✓ Falsification criteria
- ✓ Power analysis

**Reproducibility:**
- ✓ Complete code provided
- ✓ Detailed documentation
- ✓ Validation scripts
- ✓ Example usage

---

## Next Steps

1. **Deploy**: Run experimental protocol with all 50 personas
2. **Collect**: Gather performance data on standardized tasks
3. **Analyze**: Test pre-registered hypotheses
4. **Report**: Compare predictions to actual results
5. **Learn**: Update theory based on findings

---

## Contact

**Project**: Data-Statistics VC Hype Simulation
**Study**: Next-Generation Agent Performance Protocol
**Date**: 2025-11-22

**Questions?** See detailed documentation in:
- `PERSONA_LIBRARY_SUMMARY.md` - Comprehensive overview
- `PERSONA_PREDICTIONS.md` - Detailed hypotheses
- `EXAMPLE_PROMPTS.md` - Full prompt examples

---

**Status**: ✓ Ready for experimental deployment
**Validation**: ✓ All checks passed
**Pre-registration**: ✓ Complete
