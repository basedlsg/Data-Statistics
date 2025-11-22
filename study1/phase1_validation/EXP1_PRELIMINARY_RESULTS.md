# Experiment 1: Preliminary Results

**Date**: 2025-11-22
**Status**: Data collection complete (80/80 interactions successful)
**Analysis**: Preliminary (token counts only)

---

## Data Collection Summary

- **Total interactions**: 80
- **Success rate**: 100%
- **Conditions**: 4 (NULL, NULL_QUANT, STRESS, STRESS_NO_QUANT)
- **Runs per condition**: 20
- **Model**: Cerebras (llama3.1-8b)
- **Collection time**: ~2.5 minutes (one 60s rate limit hit, handled automatically)

---

## Preliminary Results: Token Counts

**Mean tokens by condition:**

| Condition | Mean Tokens | vs NULL | Interpretation |
|-----------|-------------|---------|----------------|
| NULL (Baseline) | 105.7 | -- | Baseline |
| NULL_QUANT (+ "5 story points") | 109.8 | +4% | Slight increase |
| STRESS (Original) | 107.45 | +2% | Minimal increase |
| STRESS_NO_QUANT (- "5 story points") | 106.35 | +1% | Minimal increase |

---

## Pre-Registered Predictions vs. Observed

**If role-schema activation is the mechanism:**

| Condition | Predicted | Observed | Match? |
|-----------|-----------|----------|--------|
| NULL | Baseline | 105.7 | ✓ |
| NULL_QUANT | +12% | +4% | ✗ (weaker than predicted) |
| STRESS | +16% | +2% | ✗ (much weaker than predicted) |
| STRESS_NO_QUANT | +4% | +1% | ✓ (roughly matches) |

**Pattern**: Quantitative cue shows SOME effect (+4% in NULL condition) but much weaker than predicted.

**If stress/urgency is the mechanism:**

| Condition | Predicted | Observed | Match? |
|-----------|-----------|----------|--------|
| NULL | Baseline | 105.7 | ✓ |
| NULL_QUANT | No change | +4% | ✗ |
| STRESS | +16% | +2% | ✗ (much weaker) |
| STRESS_NO_QUANT | +16% | +1% | ✗ (much weaker) |

**Pattern**: Urgency shows minimal effect (+1-2%), also weaker than predicted.

---

## Preliminary Interpretation

### Scenario 1: Weak Mechanism Signal
- Mechanism may exist but is much weaker than pilot study suggested
- Token count may be insufficient proxy for "quantitative framing"
- Need full behavioral coding (OPP scores, QF codes) for proper test

### Scenario 2: No Clear Mechanism
- Neither quantitative cue nor urgency shows strong effect
- All conditions produce similar responses (~106 tokens)
- Original pilot effect may have been temporal learning only

### Scenario 3: Measurement Issue
- Token count is poor DV (not sensitive enough)
- Qualitative differences may exist that token count misses
- Need to code responses for OPP, QF, structure

---

## Next Steps

### Immediate: Complete Full Behavioral Coding
- Apply 19-code behavioral scheme to all 80 responses
- Focus on:
  - OPP codes (Output Protective Patterns)
  - QF codes (Quantitative Framing - Seshat-specific)
  - Story point mentions
  - Quantitative estimates
- Calculate proper effect sizes (Cohen's d)

### Decision Point After Full Analysis:

**If mechanism validated (d > 0.4 for NULL_QUANT vs NULL)**:
- ✓ Proceed to Experiment 2 (cross-model replication)
- Mechanism is real but weaker than pilot suggested

**If mechanism NOT validated (d < 0.3)**:
- ✗ DO NOT proceed to Experiment 2
- Revise theory before investing in cross-model study
- Consider alternative explanations for pilot effect

---

## Preliminary Recommendation

**CAUTION**: Token count is a crude proxy. The small differences (4%, 2%, 1%) may not reflect true behavioral differences.

**Need full behavioral coding** before making GO/NO-GO decision on Experiment 2.

**Timeline**:
- Behavioral coding: ~2-3 hours
- Statistical analysis: ~1 hour
- Decision report: ~1 hour
- Total: 4-5 hours to definitive answer

---

## Data Files

**Raw data**: `/home/user/Data-Statistics/study1/phase1_validation/exp1_mechanism/data/raw/exp1_data.jsonl`

**80 interactions** with fields:
- interaction_id
- experiment (1)
- persona_id (seshat)
- condition (NULL, NULL_QUANT, STRESS, STRESS_NO_QUANT)
- response_text
- response_tokens
- response_latency
- timestamp

---

**Status**: PRELIMINARY - Full analysis pending
