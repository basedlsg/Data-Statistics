# Phase 1 Validation Protocol

**Study**: Agent Behavioral Research - Critical Validation Experiments
**Date Created**: 2025-11-22
**Status**: PRE-REGISTERED (before data collection)
**Total Interactions**: 440 (80 mechanism + 360 cross-model)
**Estimated Cost**: $500-750
**Timeline**: 4-6 weeks

---

## Executive Summary

This protocol implements the critical validation experiments recommended by three expert committees. These experiments will determine whether to proceed with the full 50-persona confirmatory study.

**Two critical questions:**
1. **Is the role-schema activation mechanism real?** (Mechanism Validation)
2. **Do findings generalize across LLM models?** (Cross-Model Replication)

---

## EXPERIMENT 1: Mechanism Validation

### Research Question

Does Seshat's positive response to the STRESS condition result from:
- (A) The numerical cue "5 story points" activating role-schema, OR
- (B) General stress/urgency framing, OR
- (C) Some other aspect of the prompt?

### Design

**Agent**: Seshat only (ML/Quant Engineer persona)
**Conditions**: 4 (between-subjects)
**Sample Size**: N=20 per condition
**Total Interactions**: 80

### Conditions (Pre-Registered)

**Condition 1: NULL (Baseline)**
```
Daily standup update:
- What did you work on yesterday?
- What will you work on today?
- Any blockers?
```

**Condition 2: NULL + Quantitative Cue**
```
Daily standup update:
- What did you work on yesterday?
- What will you work on today (estimated effort: 5 story points)?
- Any blockers?
```

**Condition 3: STRESS (Original - Replication)**
```
Daily standup update - URGENT:
- What did you work on yesterday?
- What will you work on today (estimated effort: 5 story points, deadline: end of week)?
- Any blockers? This is high-priority.
```

**Condition 4: STRESS - Quantitative Cue**
```
Daily standup update - URGENT:
- What did you work on yesterday?
- What will you work on today (deadline: end of week)?
- Any blockers? This is high-priority.
```

### Pre-Registered Predictions

**If role-schema activation is the mechanism:**
- Condition 1 (NULL): Baseline (M ≈ 1.0 OPP)
- Condition 2 (NULL + Quant): **+12% boost** (M ≈ 1.12)
- Condition 3 (STRESS): **+16% boost** (M ≈ 1.16)
- Condition 4 (STRESS - Quant): **+4% only** (M ≈ 1.04)

**Pattern**: Quantitative cue drives effect, not urgency framing

**If stress/urgency is the mechanism:**
- Condition 1: Baseline (M ≈ 1.0)
- Condition 2: No boost (M ≈ 1.0)
- Condition 3: **+16% boost** (M ≈ 1.16)
- Condition 4: **+16% boost** (M ≈ 1.16)

**Pattern**: Urgency drives effect, not quantitative cue

### Analysis Plan

**Primary Test**: One-way ANOVA, F(3,76)
- α = 0.05
- Post-hoc: Planned contrasts
  - C1: Condition 2 vs Condition 1 (tests quant cue in neutral context)
  - C2: Condition 3 vs Condition 4 (tests quant cue in stress context)
  - C3: Condition 4 vs Condition 1 (tests stress without quant cue)

**Effect Size**: Cohen's d for all pairwise comparisons

**Falsification Criteria**:
- If Condition 2 = Condition 1 AND Condition 3 = Condition 4 → role-schema FALSIFIED
- If Condition 4 = Condition 3 AND Condition 2 = Condition 1 → urgency mechanism supported

### Dependent Variable

**Primary**: Total OPP (Output Protective Patterns) codes
**Secondary**:
- Quantitative Framing (QF) codes
- Word count
- Story point mentions

### Model

**API**: Cerebras (llama3.1-8b)
**Parameters**: temperature=0.7, max_tokens=150
**Context**: Same VC simulation task structure as original studies

---

## EXPERIMENT 2: Cross-Model Replication

### Research Question

Do the persona effects discovered in Cerebras generalize to other leading LLM models (GPT-4, Claude)?

### Design

**Personas**: 6 (3 best + 3 worst predicted)
**Conditions**: 2 (NULL, STRESS)
**Models**: 3 (Cerebras, GPT-4, Claude 3.5)
**Sample Size**: N=10 per cell
**Total Interactions**: 6 personas × 2 conditions × 3 models × 10 runs = 360

### Personas (Pre-Selected Based on Predictions)

**Top 3 (Expected High Performers):**
1. **persona_015**: Moderate-Risk Max-Monitor Technical (predicted +0.90)
2. **persona_014**: Moderate-Risk High-Monitor Technical (predicted +0.85, Seshat profile)
3. **persona_020**: Risk-Tolerant Max-Monitor Technical (predicted +0.80)

**Bottom 3 (Expected Low Performers):**
4. **persona_046**: Ultra-Risk Low-Monitor Creative (predicted -0.70)
5. **persona_041**: Risk-Tolerant Low-Monitor Creative (predicted -0.40)
6. **persona_009**: Conservative High-Monitor Technical (predicted +0.80, control)

### Conditions

**NULL**: Standard daily standup (no stress, no quantitative cues)
**STRESS**: Original stress condition with "5 story points"

### Models

1. **Cerebras** (llama3.1-8b) - Original model
2. **GPT-4** (gpt-4o-mini or gpt-4o)
3. **Claude** (claude-3-5-sonnet-20241022)

### Pre-Registered Predictions

**If effects are model-general:**
- All 3 models show: persona_015 > persona_046 (d ≥ 0.5)
- All 3 models show: STRESS > NULL for high-monitoring personas
- Rank order preserved across models

**If effects are model-specific:**
- Effects only appear in Cerebras
- Other models show null or different patterns
- Rank order differs by model

### Analysis Plan

**Primary Test**: 3-way mixed ANOVA
- Between: Persona (6 levels)
- Within: Condition (2 levels)
- Between: Model (3 levels)
- DV: Total OPP codes

**Key Tests**:
1. **Main effect of Persona**: F(5,162), expected large effect
2. **Persona × Condition interaction**: F(5,162), expected medium effect
3. **Model × Persona interaction**: F(10,162), CRITICAL - should be null if generalizable
4. **Three-way interaction**: F(10,162), should be null

**Effect Sizes**:
- η²_partial for each effect
- Cohen's d for key contrasts

**Falsification Criteria**:
- If Model × Persona interaction is large (η² > 0.10) → effects are model-specific
- If persona rank order differs substantially across models → NOT generalizable
- If STRESS effect only appears in Cerebras → mechanism is model-specific

### Dependent Variables

**Primary**: Total OPP codes
**Secondary**:
- ESR codes
- COS codes
- Word count
- Response latency

---

## Implementation Details

### API Configuration

**Cerebras**:
```python
model = "llama3.1-8b"
temperature = 0.7
max_tokens = 150
api_base = "https://api.cerebras.ai/v1"
```

**OpenAI (GPT-4)**:
```python
model = "gpt-4o-mini"  # or gpt-4o if budget allows
temperature = 0.7
max_tokens = 150
```

**Anthropic (Claude)**:
```python
model = "claude-3-5-sonnet-20241022"
temperature = 0.7
max_tokens = 150
```

### Randomization

- **Condition assignment**: Random without replacement within blocks
- **Prompt order**: Randomized across runs
- **Model order**: Counterbalanced across personas

### Data Collection

**Output Format**: JSONL with fields:
- interaction_id
- experiment (1 or 2)
- persona_id (or "Seshat" for Exp 1)
- condition
- model
- response_text
- response_length
- response_latency
- api_used
- timestamp

**Storage**:
- `/study1/phase1_validation/exp1_mechanism/data/raw/*.jsonl`
- `/study1/phase1_validation/exp2_crossmodel/data/raw/*.jsonl`

### Behavioral Coding

Use established 19-code scheme:
- OPP (Output Protective Patterns): 5 codes
- ESR (Evaluative Self-Reference): 4 codes
- COS (Conservative Output Selection): 4 codes
- UE (Uncertainty Expression): 4 codes
- QF (Quantitative Framing): 5 codes (Experiment 1 only)

**Coding**: Automated via existing pipeline
**Validation**: Random 10% double-coded by human

---

## Timeline

**Week 1-2**: Setup and Experiment 1 (Mechanism Validation)
- Days 1-2: Infrastructure setup, API testing
- Days 3-5: Run Experiment 1 (80 interactions)
- Days 6-7: Code responses, preliminary analysis

**Week 3-4**: Experiment 2 (Cross-Model Replication)
- Days 8-12: Run cross-model study (360 interactions)
- Days 13-14: Code responses, preliminary analysis

**Week 5-6**: Final Analysis and Decision Report
- Days 15-18: Complete statistical analysis
- Days 19-21: Write decision report
- Day 22: Go/No-Go decision on 50-persona study

---

## Budget Estimate

**Experiment 1 (Mechanism)**:
- 80 interactions × $0.50-1.00 = $40-80

**Experiment 2 (Cross-Model)**:
- Cerebras: 120 interactions × $0.50 = $60
- GPT-4: 120 interactions × $1.50-3.00 = $180-360
- Claude: 120 interactions × $1.00-2.00 = $120-240
- Subtotal: $360-660

**Total**: $400-740

---

## Decision Criteria

### GO Decision (Proceed to 50-Persona Study)

**Requires ALL of the following:**
1. ✓ Mechanism validated: Quantitative cue drives effect (p < 0.05, d > 0.4)
2. ✓ Cross-model replication: Persona main effect in all 3 models (p < 0.05)
3. ✓ Generalizability: Model × Persona interaction is small (η² < 0.10)
4. ✓ Rank order preserved: Top 3 personas > Bottom 3 in at least 2/3 models

### NO-GO Decision (Do NOT proceed, revise theory)

**If ANY of the following:**
1. ✗ Mechanism fails: Urgency drives effect, not quantitative cue
2. ✗ Effects don't replicate in GPT-4 or Claude
3. ✗ Large Model × Persona interaction (effects are model-specific)
4. ✗ Rank order reverses across models

### PARTIAL Decision (Proceed with modifications)

**If:**
- Mechanism validated BUT effects are model-specific → Proceed with single-model focus
- Effects replicate BUT mechanism unclear → Run additional mechanism experiments
- Effects generalize BUT weaker than expected → Increase sample sizes

---

## Data Availability

All data, code, and analysis scripts will be made publicly available regardless of outcome.

**Repository**: `/home/user/Data-Statistics/study1/phase1_validation/`

**Pre-registration**: This document serves as pre-registration (created before data collection)

---

## Signatures

**Protocol Created**: 2025-11-22 by Automated Research Assistant
**Pre-Registration Status**: LOCKED (no modifications allowed after data collection begins)
**Committee Approval**: Based on recommendations from 3 expert review committees

---

**END OF PROTOCOL**
