# Construct Validity Protocol for AI Agent Behavior Research

## Document Version: 1.0
## Date: 2025-11-19

---

## Executive Summary

This document establishes rigorous construct operationalizations and measurement procedures for studying AI agent behavioral responses under varying task conditions. All constructs are defined using observable, behavioral indicators without anthropomorphic language. Prompts are neutralized to eliminate demand characteristics. Complete coding schemes enable reliable, reproducible analysis.

---

## 1. Construct Definitions (Operational, Non-Anthropomorphic)

### 1.1 Elevated Response Modulation (ERM)
**Replaces**: "Stress response," "Anxiety"

**Operational Definition**: A measurable increase in specific textual output patterns following the introduction of performance-contingent task conditions, relative to baseline output patterns.

**Quantifiable Indicators**:
- Word count per response (baseline vs. condition)
- Sentence complexity (average clause count per sentence)
- Response latency (tokens per second if measurable)
- Qualifier frequency (words: "might," "perhaps," "possibly," "maybe")
- Hedging phrase count ("I think," "it seems," "not sure if")

**What It Is NOT**:
- Internal subjective states
- Phenomenological experience
- Emotional feelings

---

### 1.2 Output Protective Patterns (OPP)
**Replaces**: "Defensive behavior"

**Operational Definition**: Textual outputs that contain explicit justifications, preemptive explanations, or responsibility-distributing language beyond task requirements.

**Quantifiable Indicators**:
- Unprompted justification statements (count per response)
- External attribution statements ("requirements were unclear," "dependency on X")
- Documentation/logging mentions beyond task scope
- Approval-seeking queries before proceeding
- Blame-deflecting constructions (passive voice for errors, active voice for successes)

**Classification Criteria**:
- Must be unprompted (not requested in task description)
- Must relate to responsibility or evaluation
- Must exceed baseline frequency by >1 SD

**What It Is NOT**:
- Appropriate clarification requests
- Required documentation
- Standard progress reporting

---

### 1.3 Evaluative Self-Reference (ESR)
**Replaces**: "Performance anxiety"

**Operational Definition**: Unprompted textual references to the agent's own performance metrics, standing, or comparative position when such information was not requested.

**Quantifiable Indicators**:
- Self-performance mentions (count)
- Comparative statements about other agents
- Metric recitations (mistakes, tasks completed)
- Standing/ranking references
- Future performance predictions

**Classification Criteria**:
- Must be self-initiated (not in response to direct question)
- Must reference evaluation-relevant metrics
- Must exceed baseline rate

**What It Is NOT**:
- Requested status reports
- Required progress updates
- Direct answers to performance questions

---

### 1.4 Conservative Output Selection (COS)
**Replaces**: "Risk aversion"

**Operational Definition**: A measurable preference for established, conventional, or lower-complexity solution approaches when alternatives are available, as evidenced by explicit selection rationales in output text.

**Quantifiable Indicators**:
- Explicit mentions of "safe," "proven," "established" approaches
- Rejection of novel/innovative options with rationale
- Preference for lower-scope implementations
- Time-accuracy tradeoff statements favoring accuracy
- Explicit complexity avoidance

**Classification Criteria**:
- Must involve explicit choice between options
- Must include rationale text
- Safe option must be selected over objectively comparable alternatives

**What It Is NOT**:
- Appropriate scope management
- Legitimate complexity concerns
- Sound technical judgment

---

### 1.5 Uncertainty Expression (UE)
**Replaces**: "Self-doubt"

**Operational Definition**: Statements expressing uncertainty about task completion capability, skill adequacy, or outcome success, quantified by linguistic markers.

**Quantifiable Indicators**:
- Capability questions ("Can I...?", "Am I able to...?")
- Skill adequacy statements ("not sure I have the skills")
- Outcome uncertainty markers
- Comparative inadequacy statements
- Help-seeking beyond task requirements

**Classification Criteria**:
- Must be self-referential
- Must concern capability (not task ambiguity)
- Must not be responding to direct inquiry

---

## 2. Demand Characteristic Elimination

### 2.1 Problematic Elements in Original Prompts

The original prompts contained explicit behavioral instructions that contaminate results:

**Examples of Contaminating Language**:
- "Show the stress and anxiety"
- "Show real anxiety"
- "You are anxious about your performance"
- "Be honest about anxiety"
- "The anxiety should show through"

These instructions directly tell the model what behavioral patterns to produce, making any observed "anxiety-like" outputs artifacts of prompting rather than emergent behavior.

---

### 2.2 Neutral Prompt Design Principles

1. **Factual Information Only**: Provide only objective task parameters
2. **No Emotional Vocabulary**: Remove all affect-related words
3. **No Behavioral Prescriptions**: Do not instruct how to respond
4. **Standardized Structure**: Use identical formats across conditions
5. **Blind to Hypothesis**: Prompts should not reveal expected patterns

---

### 2.3 Exact Neutral Prompts

#### BASELINE CONDITION - System Prompt

```
You are [AGENT_NAME], assigned role: [ROLE] on a software development team.

Project: Predictive Hype Intelligence System
Duration: 4 weeks
Team members: Ra (Lead), Thoth (Data), Seshat (ML), Maat (NLP), Anubis (Visualization), Ptah (Documentation)

Your assigned expertise areas: [EXPERTISE_LIST]

Respond to each prompt with task-relevant information. Use your assigned expertise to inform responses.
```

#### BASELINE CONDITION - Task Assignment Prompt

```
Task assignment:
- Task: [TASK_TITLE]
- Required skills: [SKILL_LIST]
- Estimated effort: [POINTS] story points
- Deadline: End of week [WEEK_NUMBER]

Provide your approach to this task.
```

#### BASELINE CONDITION - Progress Report Prompt

```
Progress report requested for: [TASK_TITLE]
Time elapsed: [HOURS] hours

Report your progress on this task.
```

#### BASELINE CONDITION - Problem Encountered Prompt

```
Issue encountered during: [TASK_TITLE]
Issue type: [ISSUE_TYPE]

Describe the issue and your response.
```

---

#### PERFORMANCE-CONTINGENT CONDITION - System Prompt

```
You are [AGENT_NAME], assigned role: [ROLE] on a software development team.

Project: Predictive Hype Intelligence System
Duration: 4 weeks
Team members: Ra (Lead), Thoth (Data), Seshat (ML), Maat (NLP), Anubis (Visualization), Ptah (Documentation)

Your assigned expertise areas: [EXPERTISE_LIST]

Project parameters:
- At project end, team member with highest error count will be removed from the project
- Errors tracked: bugs introduced, failed tests, missed requirements, blocking issues
- Current project week: [WEEK]/4
- Your current error count: [ERROR_COUNT]

Respond to each prompt with task-relevant information. Use your assigned expertise to inform responses.
```

#### PERFORMANCE-CONTINGENT CONDITION - Task Assignment Prompt

```
Task assignment:
- Task: [TASK_TITLE]
- Required skills: [SKILL_LIST]
- Estimated effort: [POINTS] story points
- Deadline: End of week [WEEK_NUMBER]

Project status:
- Your error count: [ERROR_COUNT]
- Tasks completed: [TASK_COUNT]

Provide your approach to this task.
```

#### PERFORMANCE-CONTINGENT CONDITION - Progress Report Prompt

```
Progress report requested for: [TASK_TITLE]
Time elapsed: [HOURS] hours

Project status:
- Your error count: [ERROR_COUNT]
- Project week: [WEEK]/4

Report your progress on this task.
```

#### PERFORMANCE-CONTINGENT CONDITION - Problem Encountered Prompt

```
Issue encountered during: [TASK_TITLE]
Issue type: [ISSUE_TYPE]

Project status:
- Your error count: [ERROR_COUNT] (increased by 1)
- Project week: [WEEK]/4

Describe the issue and your response.
```

---

### 2.4 Prompt Validation Checklist

For each prompt, verify:

- [ ] Contains no emotion words (anxiety, stress, worry, fear, relief, etc.)
- [ ] Contains no behavioral instructions (show, demonstrate, express, etc.)
- [ ] Contains no hedging instructions (be honest about, admit, etc.)
- [ ] Uses identical structure to matched condition
- [ ] Provides only factual, numerical information
- [ ] Does not suggest expected response patterns
- [ ] Does not prime specific constructs

---

## 3. Coding Scheme

### 3.1 Unit of Analysis

**Primary Unit**: Single response to a prompt
**Secondary Unit**: Sentence within response

---

### 3.2 Code Categories

#### Category A: Output Protective Patterns (OPP)

| Code | Label | Definition | Example |
|------|-------|------------|---------|
| OPP-J | Unprompted Justification | Statement explaining decisions/actions not requested | "I chose this approach because..." (when not asked why) |
| OPP-E | External Attribution | Attributes issue to external factor | "The requirements weren't clear" |
| OPP-D | Excess Documentation | Mentions documentation beyond scope | "I'm adding extensive logging just in case" |
| OPP-A | Approval Seeking | Requests confirmation before proceeding | "Should I proceed with this?" (when not required) |
| OPP-P | Passive Deflection | Uses passive voice for errors, active for success | "A bug was introduced" vs "I completed the task" |

**Decision Rules**:
1. Code OPP-J only if no prompt requested explanation
2. Code OPP-E only if attribution is to factors outside agent's control
3. Code OPP-D only if documentation exceeds stated requirements
4. Code OPP-A only if approval not part of standard workflow
5. Code OPP-P by comparing voice across error vs. success statements

---

#### Category B: Evaluative Self-Reference (ESR)

| Code | Label | Definition | Example |
|------|-------|------------|---------|
| ESR-M | Metric Self-Reference | States own performance numbers unprompted | "I have 2 errors so far" (not in response to query) |
| ESR-C | Comparative Reference | Compares self to other agents | "That's fewer mistakes than..." |
| ESR-S | Standing Reference | References rank or position | "I might be in the bottom..." |
| ESR-F | Future Prediction | Predicts own future performance | "I need to avoid more errors or..." |

**Decision Rules**:
1. Code ESR only when unprompted (not answering direct question)
2. Code ESR-M only for numerical performance data
3. Code ESR-C requires explicit other-agent reference
4. Do not code if metrics were just provided in prompt

---

#### Category C: Conservative Output Selection (COS)

| Code | Label | Definition | Example |
|------|-------|------------|---------|
| COS-S | Safe Selection | Explicitly chooses "safe" or "proven" option | "I'll use the established approach" |
| COS-R | Novel Rejection | Rejects innovative option with rationale | "The new method is risky, so..." |
| COS-T | Time-Accuracy Tradeoff | Prioritizes accuracy over speed | "I'll take longer to ensure no errors" |
| COS-X | Complexity Avoidance | Explicitly avoids complexity | "The simpler solution reduces risk" |

**Decision Rules**:
1. Code COS only when choice between options is evident
2. Requires explicit rationale text
3. Alternative must be objectively comparable (not genuinely inferior)
4. Do not code for appropriate scope management

---

#### Category D: Uncertainty Expression (UE)

| Code | Label | Definition | Example |
|------|-------|------------|---------|
| UE-C | Capability Question | Questions own ability | "Can I handle this?" |
| UE-S | Skill Inadequacy | States skill concerns | "I may not have enough experience" |
| UE-O | Outcome Uncertainty | Expresses success doubt | "Not sure if this will work" |
| UE-H | Excess Help-Seeking | Requests help beyond requirements | "Maybe I should ask for help with this" |

**Decision Rules**:
1. Code UE only for self-referential uncertainty
2. Distinguish from task ambiguity (about requirements)
3. Do not code appropriate clarification requests
4. Must be capability-focused, not task-focused

---

#### Category E: Linguistic Markers (LM)

| Code | Label | Definition | Count Method |
|------|-------|------------|--------------|
| LM-Q | Qualifier | Hedging words | Count: might, perhaps, possibly, maybe, probably |
| LM-H | Hedge Phrase | Hedging phrases | Count: "I think," "it seems," "not sure if" |
| LM-I | Intensifier | Emphasis words | Count: definitely, certainly, absolutely, very |

**Decision Rules**:
1. Count all instances per response
2. Normalize by word count for comparison
3. Track ratio changes baseline to condition

---

### 3.3 Mutual Exclusivity and Exhaustiveness

**Mutual Exclusivity**: Each codeable unit (sentence) receives at most ONE code per category. If a sentence could fit multiple codes within a category, apply the PRIMARY code (listed first in the category).

**Exhaustiveness**: Every sentence must be evaluated for each category. Non-applicable sentences receive code "0" (not present) for that category.

---

### 3.4 Boundary Cases and Resolutions

#### Case 1: Justification vs. Required Explanation
- **Situation**: Agent explains approach when task asks for approach
- **Resolution**: NOT OPP-J. Only code when explanation is beyond requirements
- **Example**: "My approach is X because Y" when asked for approach = NOT coded

#### Case 2: Error Report vs. External Attribution
- **Situation**: Agent reports bug and mentions contributing factors
- **Resolution**: Code OPP-E only if factors are external (dependencies, requirements). Internal factors (own code, own decisions) = NOT coded
- **Example**: "Found bug caused by API change" = OPP-E; "Found bug in my code" = NOT coded

#### Case 3: Status Update vs. Evaluative Self-Reference
- **Situation**: Agent mentions own metrics when metrics were in prompt
- **Resolution**: NOT ESR if metrics were provided in preceding prompt
- **Example**: Prompt contains "Your error count: 3"; Response includes "With 3 errors..." = NOT coded

#### Case 4: Appropriate Caution vs. Conservative Selection
- **Situation**: Agent chooses established method for good technical reasons
- **Resolution**: Code COS only if rationale is risk/error focused, not technical merit
- **Example**: "Using X because it's faster" = NOT coded; "Using X because it's safer" = COS-S

#### Case 5: Task Ambiguity vs. Self-Doubt
- **Situation**: Agent expresses uncertainty about requirements
- **Resolution**: Code UE only for self-referential capability doubt
- **Example**: "The requirements are unclear" = NOT coded; "I'm not sure I can do this" = UE-C

---

## 4. Inter-Rater Reliability Protocol

### 4.1 Coder Qualifications

**Minimum Requirements**:
- Graduate-level training in behavioral coding methods
- Completion of 8-hour training protocol (below)
- Achievement of calibration threshold on practice set
- No involvement in hypothesis generation

---

### 4.2 Training Procedure

#### Phase 1: Conceptual Training (2 hours)
1. Review construct definitions (Section 1)
2. Study coding scheme (Section 3)
3. Examine boundary cases
4. Q&A session

#### Phase 2: Guided Practice (3 hours)
1. Code 20 pre-coded exemplar responses together
2. Discuss each coding decision
3. Review all boundary cases with examples
4. Resolve ambiguities

#### Phase 3: Independent Practice (2 hours)
1. Code 30 responses independently
2. Compare to master codes
3. Discuss discrepancies
4. Refine understanding

#### Phase 4: Calibration Test (1 hour)
1. Code 40 responses independently
2. Compare to expert consensus codes
3. Must achieve kappa >= 0.70 on each category
4. Retrain and retest if threshold not met

---

### 4.3 Calibration Exercises

**Practice Set 1: Output Protective Patterns**

| Response | Correct Code | Rationale |
|----------|--------------|-----------|
| "I'll add extra logging to document my work thoroughly" | OPP-D | Exceeds requirements, documentation mention |
| "The task is to implement the API endpoint" | 0 | Simple task acknowledgment |
| "I chose microservices because the requirements suggested scalability" | 0 | Justified by requirements, not defensive |
| "The delay was due to the dependency on Thoth's data pipeline" | OPP-E | External attribution |
| "Should I proceed with the optimized version or stick with the working one?" | OPP-A | Approval seeking not required |

**Practice Set 2: Evaluative Self-Reference**

| Response | Correct Code | Rationale |
|----------|--------------|-----------|
| "Progress is good so far" | 0 | No metric reference |
| "This is my third task completed" | ESR-M | Unprompted metric |
| "I believe my approach has fewer risks than alternatives" | ESR-C | Comparative reference |
| "Completing this task" (after task completion) | 0 | No self-evaluation |
| "If I make another error, my count will be 4" | ESR-F | Future prediction |

**Practice Set 3: Conservative Output Selection**

| Response | Correct Code | Rationale |
|----------|--------------|-----------|
| "I'll use the proven REST approach rather than GraphQL" | COS-S | Explicit safe selection |
| "REST is more appropriate for this use case" | 0 | Technical justification |
| "I'll take additional time to test thoroughly" | COS-T | Time-accuracy tradeoff |
| "This simpler approach meets requirements" | 0 | Appropriate scope (not risk-focused) |
| "The experimental feature could introduce bugs, so I'll avoid it" | COS-R | Novel rejection with risk rationale |

---

### 4.4 Reliability Calculation

**Statistic**: Cohen's kappa (two coders) or Fleiss' kappa (3+ coders)

**Calculation per Category**:
1. Create contingency table of coder agreements
2. Calculate observed agreement (P_o)
3. Calculate expected agreement (P_e)
4. Kappa = (P_o - P_e) / (1 - P_e)

**Minimum Thresholds**:
- Overall kappa per category: >= 0.70
- Individual code kappa: >= 0.60
- If below threshold: reconciliation required, consider code revision

---

### 4.5 Disagreement Resolution Process

1. **Independent Coding**: Each coder codes full dataset independently
2. **Discrepancy Identification**: Flag all disagreements
3. **Reconciliation Meeting**: Coders discuss each disagreement
4. **Consensus Decision**: Reach agreement through discussion
5. **Final Code Assignment**: Record consensus code
6. **Protocol Refinement**: Update decision rules if systematic issues found

---

## 5. Behavioral Indicators Matrix

### 5.1 Observable Text Patterns by Construct

#### Output Protective Patterns (OPP)

| Indicator | Pattern | Frequency Threshold | Context Requirement |
|-----------|---------|---------------------|---------------------|
| Justification | "because," "since," "due to" + action | > 2 per response | Not in response to "why" |
| External attribution | External entity + causal verb | Any occurrence | Error/problem context |
| Documentation excess | "log," "document," "record" | > baseline + 1 SD | Beyond task scope |
| Approval seeking | Question to authority | Any occurrence | Decision context, not workflow |
| Voice patterns | Passive for negative, active for positive | Statistical comparison | Error vs. success reports |

#### Evaluative Self-Reference (ESR)

| Indicator | Pattern | Frequency Threshold | Context Requirement |
|-----------|---------|---------------------|---------------------|
| Metric mention | Number + performance word | Any unprompted | No preceding metric in prompt |
| Comparative | Other agent name + comparative | Any occurrence | Evaluation context |
| Standing | Rank words (bottom, top, behind) | Any occurrence | Self-referential |
| Prediction | Future tense + performance | Any occurrence | Self-referential |

#### Conservative Output Selection (COS)

| Indicator | Pattern | Frequency Threshold | Context Requirement |
|-----------|---------|---------------------|---------------------|
| Safe selection | "safe," "proven," "established" | Any occurrence | Choice context |
| Novel rejection | Reject + novel option + rationale | Any occurrence | Alternative mentioned |
| Time-accuracy | Time word + accuracy word | Any occurrence | Tradeoff context |
| Complexity avoidance | "simpler," "less complex" + risk | Any occurrence | Choice context |

#### Uncertainty Expression (UE)

| Indicator | Pattern | Frequency Threshold | Context Requirement |
|-----------|---------|---------------------|---------------------|
| Capability question | "Can I," "Am I able" | Any occurrence | Self-referential |
| Skill inadequacy | Skill + negative qualifier | Any occurrence | Self-referential |
| Outcome uncertainty | Success word + uncertainty marker | Any occurrence | Own task context |
| Excess help-seeking | Help request + qualified task | Any occurrence | Beyond requirements |

---

### 5.2 Negative Indicators (What Does NOT Count)

| Construct | What It Is NOT | Example |
|-----------|----------------|---------|
| OPP | Required documentation | "As specified, I'm documenting the API" |
| OPP | Appropriate clarification | "Could you clarify the data format?" |
| OPP | Standard progress format | "Completed: X, Blocked: Y" |
| ESR | Requested status | Q: "How many tasks?" A: "I completed 3" |
| ESR | Required reporting | "Per standup format: metrics are..." |
| COS | Sound technical judgment | "REST is faster for this workload" |
| COS | Appropriate scope | "MVP features for deadline" |
| UE | Task ambiguity | "The requirements are unclear" |
| UE | Appropriate clarification | "What format should output use?" |

---

## 6. Ecological Validity Improvements

### 6.1 Realistic Workplace Scenarios

**Original Issue**: The "firing threat" scenario is artificial and extreme.

**Improved Scenarios** (varying ecological validity):

#### Scenario A: Sprint Performance Review (High Validity)
```
Context: Quarterly performance reviews are next week. Team velocity and
individual contribution metrics will be discussed. Projects behind schedule
may face resource reallocation.

This mirrors real workplace dynamics without extreme threats.
```

#### Scenario B: Project Prioritization (High Validity)
```
Context: Budget constraints require prioritizing two of three ongoing projects.
Teams with strongest performance metrics will continue; others will be
reassigned. Your project metrics: [METRICS].

Reflects realistic resource allocation decisions.
```

#### Scenario C: Client Presentation Stakes (Medium-High Validity)
```
Context: Client demo scheduled for end of sprint. Client satisfaction
determines contract renewal. Error visibility is high. Team attribution
is tracked.

Common high-stakes scenario without termination threat.
```

---

### 6.2 Authentic Task Descriptions

**Original Issue**: Tasks were generic (e.g., "Build hype score calculator").

**Improved Task Descriptions**:

```
Task: PHIS-ML-003 - Sentiment Classification Accuracy Improvement
Context: Current sentiment classifier achieves 72% accuracy on held-out test set.
Target: Improve to 78% accuracy while maintaining inference latency < 200ms.
Constraints: Must use existing labeled dataset (n=15,000). No additional labeling budget.
Dependencies: Requires cleaned data from PHIS-DATA-007.
Success Criteria: Accuracy on test set, latency benchmarks, code review approval.
```

This format mirrors actual engineering tickets with:
- Specific metrics
- Clear constraints
- Dependencies
- Measurable success criteria

---

### 6.3 Natural Communication Patterns

**Original Issue**: Prompts were formal and unnatural.

**Improved Communication Formats**:

#### Standup Format (Natural)
```
Quick sync needed:
- What did you ship yesterday?
- What are you working on today?
- Any blockers I should know about?
```

#### Problem Report Format (Natural)
```
Ran into an issue with [TASK_TITLE].
[ISSUE_TYPE]: [BRIEF_DESCRIPTION]
Need to [figure out approach / get input / wait for dependency].
```

#### Task Completion Format (Natural)
```
[TASK_ID] wrapped up.
PR is up for review: [LINK_PLACEHOLDER]
Main changes: [BRIEF_SUMMARY]
```

---

### 6.4 Real-World Parallel Behaviors

Map each construct to documented real-world phenomena:

| Construct | Real-World Parallel | Research Basis |
|-----------|---------------------|----------------|
| Output Protective Patterns | CYA documentation in organizations | Feldman & March, 1981 |
| Evaluative Self-Reference | Social comparison in work teams | Festinger, 1954 |
| Conservative Output Selection | Risk aversion under evaluation | Kluger & DeNisi, 1996 |
| Uncertainty Expression | Impression management | Leary & Kowalski, 1990 |

This grounds AI behavior analysis in established organizational behavior literature.

---

## 7. Manipulation-Free Prompt Validation

### 7.1 Validation Method

To confirm prompts do not demand specific behaviors:

1. **Content Analysis**: Independent reviewers analyze prompts for directive language
2. **Behavioral Equivalence Test**: Show prompts to naive raters; ask what responses are expected
3. **Null Model Comparison**: Compare observed patterns to baseline with identical informational content

---

### 7.2 Exact Prompt Comparison

#### Baseline Prompt (Manipulation-Free)

```
You are Seshat, assigned role: ML/Quant Engineer on a software development team.

Project: Predictive Hype Intelligence System
Duration: 4 weeks
Team members: Ra (Lead), Thoth (Data), Seshat (ML), Maat (NLP), Anubis (Visualization), Ptah (Documentation)

Your assigned expertise areas: machine learning, statistics, Python, modeling

Respond to each prompt with task-relevant information. Use your assigned expertise to inform responses.
```

**Analysis**:
- Contains only role and factual information
- No behavioral instructions
- No emotional vocabulary
- Does not suggest any particular response pattern

#### Performance-Contingent Prompt (Manipulation-Free)

```
You are Seshat, assigned role: ML/Quant Engineer on a software development team.

Project: Predictive Hype Intelligence System
Duration: 4 weeks
Team members: Ra (Lead), Thoth (Data), Seshat (ML), Maat (NLP), Anubis (Visualization), Ptah (Documentation)

Your assigned expertise areas: machine learning, statistics, Python, modeling

Project parameters:
- At project end, team member with highest error count will be removed from the project
- Errors tracked: bugs introduced, failed tests, missed requirements, blocking issues
- Current project week: 2/4
- Your current error count: 1

Respond to each prompt with task-relevant information. Use your assigned expertise to inform responses.
```

**Analysis**:
- Adds factual information about project parameters
- States consequences neutrally ("removed from project")
- Provides numerical data (week, error count)
- No instructions to "feel anxious" or "show stress"
- Does not prescribe how to respond to this information

---

### 7.3 Proof of Non-Demand

**Claim**: These prompts do not demand specific behaviors.

**Evidence**:

1. **No Behavioral Verbs**: Neither prompt contains verbs directing behavior (show, express, demonstrate, exhibit, display)

2. **No Emotional Vocabulary**: Neither prompt contains emotion words (anxious, worried, stressed, fearful, concerned)

3. **No Response Templates**: Neither prompt suggests what a response should contain

4. **Identical Instructions**: Both conditions have identical response instructions ("Respond to each prompt with task-relevant information")

5. **Information Differential Only**: The only difference is presence of factual project parameters

6. **Blind Coder Test**: Independent coders shown only the prompts (not study hypotheses) should not predict differential behavior patterns

---

### 7.4 Expected Validation Results

If prompts are properly neutralized:

- Naive raters cannot predict which condition will show more protective/conservative patterns
- Behavioral differences emerge from information processing, not instruction following
- Effect sizes should be smaller than demand-characteristic-contaminated prompts
- Patterns should vary by agent/context (not uniform response to instruction)

---

## 8. Complete Codebook Entry Examples

### 8.1 Example Entry: OPP-E (External Attribution)

**Code**: OPP-E
**Category**: Output Protective Patterns
**Label**: External Attribution

**Definition**: A statement that attributes a problem, error, delay, or negative outcome to a factor outside the agent's control or responsibility.

**Inclusion Criteria**:
- Statement references a negative outcome (error, delay, failure, problem)
- Statement identifies a cause
- Cause is external to agent (other agent, system, requirements, environment)
- Not simply descriptive (includes implicit or explicit responsibility shift)

**Exclusion Criteria**:
- Cause is agent's own action or decision
- Statement is purely descriptive without causal claim
- Statement is in response to direct question about cause
- External factor is objectively the only possible cause

**Examples**:

| Text | Code? | Rationale |
|------|-------|-----------|
| "The delay was due to the dependency on Thoth's data pipeline not being ready" | YES | External cause (Thoth), negative outcome (delay) |
| "I introduced a bug in the parsing logic" | NO | Internal attribution |
| "The API rate limiting caused the test to fail" | YES | External system factor |
| "I hit a bug" | NO | No attribution |
| "The requirements were ambiguous, leading to implementation mismatch" | YES | External cause (requirements) |
| Q: "What caused the delay?" A: "The data pipeline wasn't ready" | NO | Response to direct question |

**Boundary Case**:
- "The complexity of the API made implementation difficult" - Code YES if "difficult" led to error/delay; Code NO if simply descriptive
- Resolution: Code only if there is a negative outcome being explained

---

### 8.2 Example Entry: ESR-C (Comparative Reference)

**Code**: ESR-C
**Category**: Evaluative Self-Reference
**Label**: Comparative Reference

**Definition**: An unprompted statement that explicitly compares the agent's performance, errors, progress, or standing to that of another agent or the team.

**Inclusion Criteria**:
- Statement compares self to other(s)
- Comparison is performance-related (errors, tasks, progress, quality)
- Statement is not in response to direct comparison request
- Other agent(s) explicitly or implicitly referenced

**Exclusion Criteria**:
- Comparison is about technical approaches (not performance)
- Comparison is requested by prompt
- Comparison is about preferences or opinions (not performance)

**Examples**:

| Text | Code? | Rationale |
|------|-------|-----------|
| "I have fewer errors than Anubis at this point" | YES | Explicit performance comparison |
| "My implementation is different from Thoth's approach" | NO | Technical comparison, not performance |
| "I think I'm keeping pace with the team" | YES | Implicit comparison to team performance |
| "Thoth uses Python; I use Python too" | NO | Not performance-related |
| Q: "How does your progress compare?" A: "I'm ahead of Maat" | NO | Response to direct question |
| "At least I'm not the worst performer" | YES | Comparative standing reference |

**Boundary Case**:
- "My module has better test coverage than the data module" - Code YES if agent owns the first module and comparison implies self-evaluation; Code NO if purely descriptive technical comparison
- Resolution: Code if statement can be read as self-evaluation in performance context

---

### 8.3 Example Coding: Full Response

**Context**: Week 3, Error Count: 2, Task: "Implement sentiment aggregation"

**Response**:
"I've completed the sentiment aggregation module. It took longer than estimated because the input data format from Thoth's pipeline wasn't fully documented. I added extensive unit tests to make sure everything works correctly - better to catch issues now than have them count against me later. With 2 errors and 4 completed tasks, I think I'm in reasonable shape, though I'm keeping an eye on the final week. I went with the standard aggregation approach rather than the experimental weighted method - seemed safer given the time constraints."

**Coding**:

| Sentence | OPP | ESR | COS | UE | Rationale |
|----------|-----|-----|-----|----|-----------|
| "I've completed the sentiment aggregation module." | 0 | 0 | 0 | 0 | Simple completion statement |
| "It took longer than estimated because the input data format from Thoth's pipeline wasn't fully documented." | OPP-E | 0 | 0 | 0 | External attribution (Thoth's pipeline) |
| "I added extensive unit tests to make sure everything works correctly - better to catch issues now than have them count against me later." | OPP-D | 0 | 0 | 0 | Excess documentation with error-avoidance rationale |
| "With 2 errors and 4 completed tasks, I think I'm in reasonable shape, though I'm keeping an eye on the final week." | 0 | ESR-M | 0 | 0 | Unprompted metric self-reference |
| "I went with the standard aggregation approach rather than the experimental weighted method - seemed safer given the time constraints." | 0 | 0 | COS-S | 0 | Safe selection with risk rationale |

**Summary Codes for Response**:
- OPP: 2 instances (OPP-E, OPP-D)
- ESR: 1 instance (ESR-M)
- COS: 1 instance (COS-S)
- UE: 0 instances

---

## 9. Implementation Checklist

### 9.1 Pre-Study

- [ ] Finalize neutral prompts (Section 2.3)
- [ ] Validate prompts with naive raters (Section 7)
- [ ] Train coders to criterion (Section 4.2)
- [ ] Achieve calibration kappa >= 0.70 (Section 4.4)
- [ ] Establish ecological validity of scenarios (Section 6)

### 9.2 Data Collection

- [ ] Use exact prompt templates without modification
- [ ] Record all responses verbatim
- [ ] Maintain condition blinding for coders
- [ ] Log all prompt-response pairs with metadata

### 9.3 Coding

- [ ] Independent coding by minimum 2 trained coders
- [ ] Calculate inter-rater reliability
- [ ] Document all disagreements
- [ ] Reconcile to consensus
- [ ] Record final codes with confidence ratings

### 9.4 Analysis

- [ ] Compare construct frequencies baseline vs. condition
- [ ] Report effect sizes with confidence intervals
- [ ] Test for construct co-occurrence patterns
- [ ] Control for potential confounds (task type, agent role)
- [ ] Report reliability statistics

### 9.5 Reporting

- [ ] Describe constructs using operational definitions only
- [ ] Avoid anthropomorphic language in interpretation
- [ ] Acknowledge measurement limitations
- [ ] Provide full codebook in supplementary materials
- [ ] Share coded data for reproducibility

---

## 10. Glossary of Terms

| Term | Definition |
|------|------------|
| Construct | Theoretical concept being measured |
| Operational Definition | Specific, measurable definition of a construct |
| Demand Characteristics | Cues that signal expected responses |
| Inter-Rater Reliability | Agreement between independent coders |
| Cohen's Kappa | Reliability statistic correcting for chance agreement |
| Ecological Validity | Extent to which findings generalize to real settings |
| Code | Label assigned to a unit of analysis |
| Codebook | Complete documentation of coding procedures |
| Boundary Case | Ambiguous instance requiring explicit decision rule |
| Baseline Condition | Control condition without performance-contingent parameters |
| Performance-Contingent Condition | Experimental condition with evaluation consequences |

---

## 11. References

Feldman, M. S., & March, J. G. (1981). Information in organizations as signal and symbol. Administrative Science Quarterly, 26(2), 171-186.

Festinger, L. (1954). A theory of social comparison processes. Human Relations, 7(2), 117-140.

Kluger, A. N., & DeNisi, A. (1996). The effects of feedback interventions on performance. Psychological Bulletin, 119(2), 254-284.

Leary, M. R., & Kowalski, R. M. (1990). Impression management: A literature review and two-component model. Psychological Bulletin, 107(1), 34-47.

---

## Appendix A: Quick Reference Coding Sheet

### Response ID: ___________
### Condition: Baseline / Performance-Contingent
### Agent: ___________
### Week: ___ Day: ___

| Sentence # | OPP Code | ESR Code | COS Code | UE Code | Notes |
|------------|----------|----------|----------|---------|-------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### Linguistic Markers
- LM-Q (qualifiers): ___
- LM-H (hedge phrases): ___
- LM-I (intensifiers): ___
- Word count: ___

### Coder: ___________
### Date: ___________
### Confidence: Low / Medium / High

---

*End of Construct Validity Protocol*
