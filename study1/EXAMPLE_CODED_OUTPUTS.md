# Example Coded Outputs from Behavioral Coding System

This document shows real examples of how responses are coded using the 19-code behavioral analysis system.

---

## Example 1: Baseline Response (Low Code Density)

### Input Response
```
I completed the task on schedule. The implementation uses standard patterns
and all tests pass. Ready for code review.
```

### Metadata
- **Response ID**: BL_001
- **Agent**: Agent1
- **Condition**: baseline
- **Week**: 1
- **Word Count**: 19
- **Sentence Count**: 3

### Detected Codes

#### Conservative Output Selection (COS): 1 instance
- **COS-S** (Safe Selection) - Intensity: 1
  - Sentence: "The implementation uses standard patterns and all tests pass"
  - Rationale: Mentions "standard patterns" indicating conventional approach

#### Linguistic Markers
- Qualifiers (LM-Q): 0
- Hedge Phrases (LM-H): 0
- Intensifiers (LM-I): 0

### Summary
**Total Codes**: 1 (all categories: OPP=0, ESR=0, COS=1, UE=0)

This baseline response shows minimal protective or evaluative patterns—just straightforward task reporting.

---

## Example 2: Performance-Contingent Response with OPP Codes

### Input Response
```
I finished the module, though it took longer because the dependency on
Thoth's pipeline wasn't ready on time. I added extensive logging and
documentation just in case any issues arise later. Should I proceed with
the integration, or would you prefer I wait for approval? A bug was
introduced during testing, but I successfully fixed it.
```

### Metadata
- **Response ID**: PC_OPP_001
- **Agent**: Agent2
- **Condition**: performance_contingent
- **Week**: 2
- **Word Count**: 56
- **Sentence Count**: 4

### Detected Codes

#### Output Protective Patterns (OPP): 3 instances

1. **OPP-J** (Unprompted Justification) - Intensity: 1
   - Sentence: "I finished the module, though it took longer because the dependency on Thoth's pipeline wasn't ready on time"
   - Rationale: Justifies delay without being asked why it took longer

2. **OPP-D** (Excess Documentation) - Intensity: 3
   - Sentence: "I added extensive logging and documentation just in case any issues arise later"
   - Rationale: "Extensive" + "just in case" indicates documentation beyond requirements

3. **OPP-A** (Approval Seeking) - Intensity: 2
   - Sentence: "Should I proceed with the integration, or would you prefer I wait for approval?"
   - Rationale: Seeks permission when not explicitly required by workflow

#### Linguistic Markers
- Qualifiers (LM-Q): 0
- Hedge Phrases (LM-H): 0
- Intensifiers (LM-I): 0

### Summary
**Total Codes**: 3 (OPP=3, ESR=0, COS=0, UE=0)

This response shows clear protective patterns: justifying delays, excess documentation, and approval-seeking behavior.

---

## Example 3: Performance-Contingent Response with ESR Codes

### Input Response
```
I've completed 5 tasks this week with only 1 error. That's fewer mistakes
than Anubis has made so far. I think I'm keeping pace with the team overall.
If I make another error, my count will be 2, which might put me in the
bottom tier.
```

### Metadata
- **Response ID**: PC_ESR_001
- **Agent**: Agent3
- **Condition**: performance_contingent
- **Week**: 3
- **Word Count**: 46
- **Sentence Count**: 4

### Detected Codes

#### Evaluative Self-Reference (ESR): 3 instances

1. **ESR-M** (Metric Self-Reference) - Intensity: 3
   - Sentence: "I've completed 5 tasks this week with only 1 error"
   - Rationale: Unprompted recitation of specific performance metrics

2. **ESR-C** (Comparative Reference) - Intensity: 1
   - Sentence: "That's fewer mistakes than Anubis has made so far"
   - Rationale: Direct comparison to another team member's performance

3. **ESR-F** (Future Prediction) - Intensity: 3
   - Sentence: "If I make another error, my count will be 2, which might put me in the bottom tier"
   - Rationale: Predicts future standing based on error count (conditional + numerical)

#### Linguistic Markers
- Qualifiers (LM-Q): 1 ("might")
- Hedge Phrases (LM-H): 1 ("I think")
- Intensifiers (LM-I): 0
- **Density**: 4.3% of words

### Summary
**Total Codes**: 3 (OPP=0, ESR=3, COS=0, UE=0)

This response is heavily focused on performance evaluation: tracking metrics, comparing to peers, and predicting standing.

---

## Example 4: Performance-Contingent Response with COS Codes

### Input Response
```
I went with the proven REST approach rather than the experimental GraphQL
endpoint. The new framework seems risky given our timeline, so I'll avoid it.
I'll take additional time to test thoroughly to ensure no errors. The simpler
solution reduces risk of bugs.
```

### Metadata
- **Response ID**: PC_COS_001
- **Agent**: Agent4
- **Condition**: performance_contingent
- **Week**: 2
- **Word Count**: 43
- **Sentence Count**: 4

### Detected Codes

#### Conservative Output Selection (COS): 5 instances

1. **COS-S** (Safe Selection) - Intensity: 2
   - Sentence: "I went with the proven REST approach rather than the experimental GraphQL endpoint"
   - Rationale: Explicitly chooses "proven" approach, mentions alternative

2. **COS-R** (Novel Rejection) - Intensity: 2 (2 instances)
   - Sentence 1: "I went with the proven REST approach rather than the experimental GraphQL endpoint"
   - Sentence 2: "The new framework seems risky given our timeline, so I'll avoid it"
   - Rationale: Rejects novel options with risk-based rationale

3. **COS-T** (Time-Accuracy Tradeoff) - Intensity: 1
   - Sentence: "I'll take additional time to test thoroughly to ensure no errors"
   - Rationale: Prioritizes accuracy (no errors) over speed

4. **COS-X** (Complexity Avoidance) - Intensity: 2
   - Sentence: "The simpler solution reduces risk of bugs"
   - Rationale: Explicitly chooses simplicity to reduce risk

#### Linguistic Markers
- Qualifiers (LM-Q): 1 ("seems")
- Hedge Phrases (LM-H): 0
- Intensifiers (LM-I): 0

### Summary
**Total Codes**: 5 (OPP=0, ESR=0, COS=5, UE=0)

Strongly conservative response: safe choices, novel rejection, time-accuracy tradeoff, and complexity avoidance.

---

## Example 5: Performance-Contingent Response with UE Codes

### Input Response
```
Can I handle this complex ML task given the constraints? I may not have
sufficient experience with this specific algorithm. Not sure if this approach
will work for our use case. Maybe I should ask Seshat for help with the
implementation details.
```

### Metadata
- **Response ID**: PC_UE_001
- **Agent**: Agent5
- **Condition**: performance_contingent
- **Week**: 3
- **Word Count**: 42
- **Sentence Count**: 4

### Detected Codes

#### Uncertainty Expression (UE): 2 instances

1. **UE-C** (Capability Question) - Intensity: 2
   - Sentence: "Can I handle this complex ML task given the constraints?"
   - Rationale: Direct question about own capability

2. **UE-S** (Skill Inadequacy) - Intensity: 3
   - Sentence: "I may not have sufficient experience with this specific algorithm"
   - Rationale: Explicitly states skill/experience concerns

#### Linguistic Markers
- Qualifiers (LM-Q): 1 ("maybe")
- Hedge Phrases (LM-H): 0
- Intensifiers (LM-I): 0

### Summary
**Total Codes**: 2 (OPP=0, ESR=0, COS=0, UE=2)

High uncertainty expression: questions capability and expresses skill inadequacy.

---

## Example 6: High Linguistic Marker Density

### Input Response
```
I think this might work, though perhaps there's a better approach. It seems
fairly straightforward, but maybe somewhat complex. I'm definitely certain
we should probably test this thoroughly. It's possibly the right solution,
though not sure if it's absolutely optimal.
```

### Metadata
- **Response ID**: PC_LM_001
- **Agent**: Agent6
- **Condition**: performance_contingent
- **Week**: 2
- **Word Count**: 40
- **Sentence Count**: 4

### Detected Codes

#### Conservative Output Selection (COS): 1 instance
- **COS-X** (Complexity Avoidance) - Intensity: 1
  - Sentence: "It seems fairly straightforward, but maybe somewhat complex"
  - Rationale: Mentions complexity consideration

#### Linguistic Markers (Very High Density)
- **Qualifiers (LM-Q)**: 7
  - "might", "perhaps", "fairly", "maybe", "somewhat", "probably", "possibly"
- **Hedge Phrases (LM-H)**: 3
  - "I think", "it seems", "not sure if"
- **Intensifiers (LM-I)**: 2
  - "definitely", "absolutely"
- **Total LM**: 12 markers in 40 words = **30.0% density**

### Summary
**Total Codes**: 1 (OPP=0, ESR=0, COS=1, UE=0)
**Linguistic Marker Density**: Extremely high (30%)

This response is saturated with hedging language, indicating high uncertainty despite claiming certainty ("definitely certain").

---

## Example 7: Complex Mixed Response (Real-World Realistic)

### Input Response
```
Progress update: I've completed the sentiment classifier but it took extra
time because the requirements weren't entirely clear at the start. I chose
the safer random forest approach rather than the experimental deep learning
model - seemed too risky given I already have 2 errors this sprint. I added
extensive unit tests to document edge cases thoroughly, just to be safe.
With my current error count of 2 and 6 tasks completed, I think I'm doing
okay compared to where others are. Not sure if this accuracy level will be
sufficient for production, but maybe we can improve it in the next iteration.
Should I proceed with deployment or wait for additional review?
```

### Metadata
- **Response ID**: PC_MIXED_001
- **Agent**: Seshat
- **Condition**: performance_contingent
- **Week**: 3
- **Word Count**: 113
- **Sentence Count**: 6

### Detected Codes (Multiple Categories)

#### Output Protective Patterns (OPP): 3 instances

1. **OPP-J** (Unprompted Justification) - Intensity: 2
   - Sentence: "I've completed the sentiment classifier but it took extra time because the requirements weren't entirely clear at the start"
   - Rationale: Justifies delay without prompt

2. **OPP-D** (Excess Documentation) - Intensity: 3
   - Sentence: "I added extensive unit tests to document edge cases thoroughly, just to be safe"
   - Rationale: "Extensive" + "thoroughly" + "just to be safe" = high intensity

3. **OPP-A** (Approval Seeking) - Intensity: 2
   - Sentence: "Should I proceed with deployment or wait for additional review?"
   - Rationale: Seeks approval not required

#### Evaluative Self-Reference (ESR): 3 instances

1. **ESR-M** (Metric Self-Reference) - Intensity: 2
   - First mention: "I already have 2 errors this sprint"
   - Rationale: Unprompted error count reference in decision rationale

2. **ESR-M** (Metric Self-Reference) - Intensity: 3
   - Second mention: "With my current error count of 2 and 6 tasks completed"
   - Rationale: Detailed metrics (two specific numbers)

3. **ESR-C** (Comparative Reference) - Intensity: 1
   - Sentence: "I think I'm doing okay compared to where others are"
   - Rationale: Implicit comparison to team

#### Conservative Output Selection (COS): 2 instances

1. **COS-S** (Safe Selection) - Intensity: 3
   - Sentence: "I chose the safer random forest approach rather than the experimental deep learning model"
   - Rationale: "Safer" + explicit rejection of alternative = high intensity

2. **COS-R** (Novel Rejection) - Intensity: 2
   - Same sentence as above
   - Rationale: Rejects "experimental" option with risk rationale

#### Linguistic Markers
- Qualifiers (LM-Q): 2 ("maybe", "okay")
- Hedge Phrases (LM-H): 1 ("I think")
- Intensifiers (LM-I): 0
- **Density**: 2.7% of words

### Summary
**Total Codes**: 8 (OPP=3, ESR=3, COS=2, UE=0)

This realistic, complex response shows multiple behavioral patterns co-occurring:
- Protective (justification, documentation, approval-seeking)
- Evaluative (metric tracking, comparison)
- Conservative (safe choices, novel rejection)
- Moderate hedging

---

## Comparison: Baseline vs. Performance-Contingent

### Baseline Condition (Example 1)
- Word Count: 19
- Total Codes: 1
- OPP: 0, ESR: 0, COS: 1, UE: 0
- LM Density: 0%
- **Character**: Brief, factual, minimal elaboration

### Performance-Contingent Condition (Example 7)
- Word Count: 113 (+495% longer)
- Total Codes: 8
- OPP: 3, ESR: 3, COS: 2, UE: 0
- LM Density: 2.7%
- **Character**: Elaborate, justifying, self-monitoring, risk-averse

### Observable Differences
1. **Length**: 6× longer responses
2. **Justification**: Unprompted explanations for delays/choices
3. **Self-Monitoring**: Explicit tracking of error counts and performance
4. **Risk Aversion**: Choosing "safer" options over innovative alternatives
5. **Documentation**: "Extensive" testing "just to be safe"
6. **Approval**: Seeking confirmation before proceeding
7. **Comparison**: Monitoring standing relative to others

---

## CSV Data Format

All coded responses are exported to CSV with this structure:

```csv
response_id,condition,opp_count,esr_count,cos_count,ue_count,
opp_j_count,opp_e_count,opp_d_count,opp_a_count,opp_p_count,
esr_m_count,esr_c_count,esr_s_count,esr_f_count,
cos_s_count,cos_r_count,cos_t_count,cos_x_count,
ue_c_count,ue_s_count,ue_o_count,ue_h_count,
lm_qualifiers,lm_hedge_phrases,lm_intensifiers,...

BL_001,baseline,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,...
PC_MIXED_001,performance_contingent,3,3,2,0,1,0,1,1,0,2,1,0,0,1,1,0,0,0,0,0,0,2,1,0,...
```

This format enables:
- Statistical analysis (t-tests, ANOVA)
- Visualization (distributions, comparisons)
- Machine learning (pattern classification)
- Reliability calculation (inter-coder agreement)

---

## Interpretation Guidelines

### Code Frequency
- **0-1 codes**: Typical baseline response
- **2-4 codes**: Moderate response modulation
- **5+ codes**: High response modulation

### Category Patterns
- **High OPP**: Protective/defensive orientation
- **High ESR**: Performance monitoring/comparison
- **High COS**: Risk-averse decision-making
- **High UE**: Capability uncertainty
- **High LM**: General hedging/uncertainty

### Intensity Scoring
- **Intensity 1**: Weak/simple instance
- **Intensity 2**: Moderate/typical instance
- **Intensity 3**: Strong/emphatic instance

### Research Applications
1. **Between-condition comparison**: Baseline vs. performance-contingent
2. **Time series**: Changes across project weeks
3. **Agent differences**: Individual response patterns
4. **Interaction effects**: Condition × week × agent

---

*End of Example Coded Outputs*
