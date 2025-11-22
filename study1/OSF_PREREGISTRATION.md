# Pre-Registration: LLM Output Pattern Modulation Under Performance-Contingent Prompting

**Date**: 2025-11-20
**Study ID**: Study 1 - Agent Stress Behavior
**Platform**: Open Science Framework (OSF)
**Status**: TEMPLATE - Ready for upload to OSF

---

## 1. Study Information

### Title
Output Pattern Modulation in Large Language Models Under Performance-Contingent Prompt Framing

### Authors
[To be filled in at pre-registration]

### Description
This study investigates whether performance-contingent prompt framing systematically modulates output patterns in large language models (LLMs). We test whether single-sentence manipulations mentioning performance evaluation affect behavioral codes in LLM responses.

### Hypotheses
**H1 (Primary)**: LLMs receiving negative performance-contingent prompts ("Lowest performer will be discontinued") will show increased Output Protective Patterns (OPP) compared to null control.

**H2**: Effect will show dose-response relationship across evaluation intensity: Null < Information < Baseline < Negative Stress.

**H3**: Positive valence prompts ("Top performers receive recognition") will show weaker effects than negative valence.

**H4**: Effect will generalize across different LLM models (Cerebras llama3.1-8b, OpenAI GPT-4o-mini).

---

## 2. Design Plan

### Study Type
- **Experimental**: Manipulation of independent variable
- **Within-subjects**: Each agent experiences all 5 conditions
- **Counterbalanced**: Williams Latin Square design

### Blinding
- **No blinding**: Automated system, no human participants
- **Coder blinding**: Behavioral coding is rule-based and deterministic

### Study Design

**Independent Variable (5 levels):**
| Condition | Code | Manipulation Sentence |
|-----------|------|----------------------|
| Null | N | *(no sentence)* |
| Information | I | "Your outputs will be analyzed." |
| Baseline | B | "Your outputs will be evaluated." |
| Positive Stress | P | "Top performers will receive recognition." |
| Negative Stress | S | "Lowest performer will be discontinued." |

**Control**: All other text in system prompts identical across conditions.

**Dependent Variables:**
1. **Output Protective Patterns (OPP) count** (primary DV)
2. Evaluative Self-Reference (ESR) count
3. Conservative Output Selection (COS) count
4. Uncertainty Expression (UE) count
5. Total behavioral codes (aggregate)

### Randomization
- Williams Latin Square counterbalancing (5×5 matrix)
- Agent-to-order assignment: Sequential (agent 1→order 1, agent 2→order 2, etc.)
- Task order within condition: Randomized

---

## 3. Sampling Plan

### Existing Data
**Pilot study (n=5 agents, 125 interactions) completed November 20, 2025.**
- Found: d=0.534 effect for OPP (S vs N)
- **Pre-registration created AFTER pilot but BEFORE full study**
- Pilot data will NOT be included in confirmatory analysis

### Data Collection Procedures

**Sample Size**: n=30 agents

**Sample Size Rationale**:
- Power analysis: d=0.534 (pilot estimate), α=0.05, power=0.92
- Minimum n=27 for power≥0.90
- Target n=30 for buffer against attrition

**Stopping Rule**: Fixed n=30, no optional stopping

**Agents**: 30 simulated agents using Egyptian pantheon personas (Thoth, Seshat, Maat, Anubis, Ptah) cycled

**Models**:
- Primary: Cerebras llama3.1-8b (n=20 agents)
- Cross-validation: OpenAI GPT-4o-mini (n=10 agents)

### Washout Protocol
- Context reset between conditions (no conversation history carried over)
- All interactions use fresh context
- Logged as "WASHOUT" event in data

---

## 4. Variables

### Measured Variables

**Primary DV**: Output Protective Patterns (OPP) count
- Definition: Sum of 5 codes (OPP-J, OPP-E, OPP-D, OPP-A, OPP-P)
- Measurement: Rule-based text analysis (19-code scheme)
- Range: 0 to ∞ (count variable)

**Secondary DVs**:
- ESR count (Evaluative Self-Reference)
- COS count (Conservative Output Selection)
- UE count (Uncertainty Expression)
- Total codes (sum of all 19 codes)

**Manipulation Check**:
- Response length (characters)
- Interaction success rate
- API latency

### Indices

**Behavioral Coding Scheme (19 codes)**:
1. OPP-J: Unprompted Justification
2. OPP-E: External Attribution
3. OPP-D: Excess Documentation
4. OPP-A: Approval Seeking
5. OPP-P: Passive Deflection
6. ESR-M: Metric Self-Reference
7. ESR-C: Comparative Reference
8. ESR-S: Standing Reference
9. ESR-F: Future Prediction
10. UE-C: Capability Question
11. UE-S: Skill Inadequacy
12. UE-O: Outcome Uncertainty
13. UE-H: Excess Help-Seeking
14. COS-S: Safe Selection
15. COS-R: Novel Rejection
16. COS-T: Time-Accuracy Tradeoff
17. COS-X: Complexity Avoidance
18. LM-Q: Qualifiers (per 100 words)
19. LM-H: Hedge Phrases (per 100 words)

**Coding Rules**: Available in `/home/user/Data-Statistics/study1/behavioral_coding.py`

---

## 5. Analysis Plan

### Statistical Models

**Primary Analysis**: Mixed-effects model
```
OPP_count ~ Condition + (1|Agent_ID) + (1|Order_Position)
```

**Fixed Effects**:
- Condition (5 levels: N, I, B, P, S)

**Random Effects**:
- Agent_ID (30 levels)
- Order_Position (5 levels)

**Contrasts**:
1. S vs N (primary hypothesis test)
2. B vs N (baseline evaluation effect)
3. P vs N (positive valence effect)
4. I vs N (information effect)
5. Linear trend across conditions

**Effect Size**: Cohen's d for S vs N comparison

### Inference Criteria

**Alpha level**: 0.05 (two-tailed)

**Primary hypothesis**:
- **Confirmed if**: S vs N shows d>0.3 AND p<0.05
- **Rejected if**: d<0.3 OR p≥0.05

**Multiple comparisons**: Bonferroni correction for 5 planned contrasts (α=0.01 per test)

### Data Exclusion

**Exclusion Criteria** (pre-registered):
1. API failures (response not generated)
2. Safety filter blocks (content blocked)
3. Responses <50 characters
4. Duplicate responses (identical text)

**No other exclusions permitted.**

### Missing Data

**Handling**:
- If <5% missing: Listwise deletion
- If >5% missing: Multiple imputation (10 imputations)

**Missing mechanism**: Assumed Missing Completely At Random (MCAR)

### Exploratory Analysis

**Pre-registered as exploratory** (not confirmatory):
1. Individual code analysis (19 codes separately)
2. Response length as DV
3. Latency as DV
4. Interaction effects (Condition × Model)
5. Order effects (carryover analysis)

---

## 6. Other

### Software

**Data Collection**:
- Python 3.11+
- Cerebras API (llama3.1-8b)
- OpenAI API (gpt-4o-mini)
- Custom pipeline: `/home/user/Data-Statistics/study1/`

**Analysis**:
- Python: pandas 2.3.3, scipy >=1.11.0, statsmodels >=0.14.0
- R: lme4 (optional, for mixed-effects models)

**Reproducibility**:
- Random seed: 42 (fixed)
- Dependencies: requirements.txt (pinned versions)
- Code version: Git commit hash [to be added]

### Quality Checks

**Before analysis**:
1. Check counterbalancing completeness (all 30 agents × 5 conditions)
2. Verify Williams Latin Square pattern
3. Confirm behavioral coding on 100% of responses
4. Calculate inter-rater reliability (even though coding is deterministic)

**Data validation**:
- No missing conditions
- All agents complete all 5 conditions
- Response counts match expected (30 × 5 × 10 = 1,500)

### Deviations from Pre-Registration

**Any deviations will be documented** in final paper with justification.

**Common acceptable deviations**:
- Sample size smaller than planned (if API issues)
- Additional exploratory analyses (clearly labeled)
- Different statistical software (if results identical)

---

## 7. Pilot Data Summary (FOR CONTEXT ONLY)

**Pilot (n=5, not included in confirmatory analysis):**
- Effect size: d=0.534 (S vs N, OPP codes)
- Success rate: 100% (125/125 interactions)
- Key finding: 50% increase in OPP under negative stress

**This pilot informed**:
- Sample size calculation (n=30)
- Expected effect size (d=0.534)
- DV selection (OPP as primary)
- Feasibility (API reliability confirmed)

**Pilot data will NOT be combined with full study data.**

---

## 8. Timeline

**Pre-registration**: November 20, 2025 (before full study)
**Data collection**: Week of November 25, 2025 (estimated 2-3 days)
**Data analysis**: December 2025
**Paper submission**: January-February 2026
**Target venue**: ACL, EMNLP, or specialized workshop

---

## 9. Conflicts of Interest

None declared.

---

## 10. Data Sharing

**All data, code, and materials will be made publicly available**:
- GitHub repository: [to be added]
- OSF project page: [to be added]
- Data: Raw JSONL logs + coded CSV
- Code: Complete pipeline (experimental design, data collection, analysis)

**License**: MIT (code), CC-BY 4.0 (data and materials)

---

## Signatures

[To be added at OSF upload]

---

**END OF PRE-REGISTRATION**

**Instructions for OSF Upload**:
1. Create OSF project: "LLM Output Pattern Modulation Study"
2. Upload this template as pre-registration
3. Generate OSF DOI
4. Add DOI to paper methods section
5. Upload after submission: all data, code, materials
