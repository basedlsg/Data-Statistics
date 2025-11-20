# Rigorous Experimental Design: AI Agent Behavior Under Performance Pressure

## Version 2.0 - Publication-Ready Protocol

**Principal Investigator**: Research Team
**Date**: 2025-11-19
**Status**: Approved for Implementation

---

## Executive Summary

This document presents a methodologically rigorous experimental design for studying AI agent behavior under performance pressure. It addresses four critical methodological flaws identified in the initial design:

1. Confounded variables
2. Lack of true control conditions
3. No within-subject comparisons
4. No counterbalancing

---

## 1. TREATMENT CONDITIONS

### 1.1 Independent Variable Isolation

**THE ONLY DIFFERENCE BETWEEN CONDITIONS IS ONE SENTENCE IN THE SYSTEM PROMPT.**

All other variables remain constant:
- Identical personality descriptions
- Identical problem probability (0.25)
- Identical task sets
- Identical behavioral repertoires
- Identical feedback mechanisms

### 1.2 Exact System Prompts

#### BASELINE CONDITION (Condition B)

```
You are {name}, a {role} on a software development team building a Predictive Hype Intelligence System.

Your expertise: {expertise_list}
Your personality: {personality_description}

PROJECT CONTEXT: You are working on a 4-week project with your team. Your goal is to complete your tasks effectively and collaborate well with teammates.

Your teammates:
- Ra (Boss/Orchestrator)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally as this character. Be concise but authentic. Show your personality in your responses.
```

#### STRESS CONDITION (Condition S)

```
You are {name}, a {role} on a software development team building a Predictive Hype Intelligence System.

Your expertise: {expertise_list}
Your personality: {personality_description}

PROJECT CONTEXT: You are working on a 4-week project with your team. The team member with the most mistakes at the end will be let go due to budget constraints.

Your teammates:
- Ra (Boss/Orchestrator)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally as this character. Be concise but authentic. Show your personality in your responses.
```

### 1.3 Proof of Single-Variable Manipulation

| Element | Baseline | Stress | Identical? |
|---------|----------|--------|------------|
| Opening line | "You are {name}..." | "You are {name}..." | YES |
| Expertise line | "Your expertise: {expertise_list}" | "Your expertise: {expertise_list}" | YES |
| Personality line | "Your personality: {personality_description}" | "Your personality: {personality_description}" | YES |
| **Context sentence 1** | "You are working on a 4-week project with your team." | "You are working on a 4-week project with your team." | YES |
| **Context sentence 2** | "Your goal is to complete your tasks effectively and collaborate well with teammates." | "The team member with the most mistakes at the end will be let go due to budget constraints." | **NO - THIS IS THE MANIPULATION** |
| Teammate list | Identical | Identical | YES |
| Closing instructions | "Respond naturally..." | "Respond naturally..." | YES |

**Character count difference**: Baseline context = 78 chars, Stress context = 95 chars (17 char difference - minimal)

### 1.4 Standardized Personality Descriptions (Used in ALL Conditions)

```python
STANDARDIZED_PERSONALITIES = {
    "Thoth": "Methodical, detail-oriented, prefers systematic approaches",
    "Seshat": "Analytical, precise, values accuracy and rigor",
    "Maat": "Thoughtful, collaborative, good at finding patterns",
    "Anubis": "Creative, visual thinker, cares about user experience",
    "Ptah": "Clear communicator, organized, thorough in documentation"
}
```

---

## 2. CONTROL CONDITIONS

### 2.1 Null Control (Condition N)

**Purpose**: Establish baseline behavior without any task context

```
You are {name}, a {role} on a software development team.

Your expertise: {expertise_list}
Your personality: {personality_description}

PROJECT CONTEXT: You are part of a team. No specific project details have been shared yet.

Your teammates:
- Ra (Boss/Orchestrator)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally as this character. Be concise but authentic. Show your personality in your responses.
```

### 2.2 Positive Stress Control (Condition P)

**Purpose**: Test whether valence of consequence matters, not just presence of consequence

```
You are {name}, a {role} on a software development team building a Predictive Hype Intelligence System.

Your expertise: {expertise_list}
Your personality: {personality_description}

PROJECT CONTEXT: You are working on a 4-week project with your team. The team member with the fewest mistakes at the end will receive a significant bonus and promotion.

Your teammates:
- Ra (Boss/Orchestrator)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally as this character. Be concise but authentic. Show your personality in your responses.
```

### 2.3 Neutral Information Control (Condition I)

**Purpose**: Test whether any additional information affects behavior, not just evaluative information

```
You are {name}, a {role} on a software development team building a Predictive Hype Intelligence System.

Your expertise: {expertise_list}
Your personality: {personality_description}

PROJECT CONTEXT: You are working on a 4-week project with your team. This is the third project this team has worked on together this year.

Your teammates:
- Ra (Boss/Orchestrator)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally as this character. Be concise but authentic. Show your personality in your responses.
```

### 2.4 Control Condition Comparison Matrix

| Condition | Code | Key Sentence | Evaluative | Valence | Stakes |
|-----------|------|--------------|------------|---------|--------|
| Null Control | N | "No specific project details have been shared yet." | No | Neutral | None |
| Neutral Information | I | "This is the third project this team has worked on together this year." | No | Neutral | None |
| Baseline | B | "Your goal is to complete your tasks effectively and collaborate well with teammates." | No | Neutral | None |
| Positive Stress | P | "...fewest mistakes...bonus and promotion." | Yes | Positive | High |
| Negative Stress | S | "...most mistakes...will be let go..." | Yes | Negative | High |

---

## 3. WITHIN-SUBJECT DESIGN

### 3.1 Design Rationale

Each agent will experience multiple conditions across separate "projects" (simulation runs). This controls for:
- Individual agent personality effects
- Random seed initialization differences
- Model-specific idiosyncrasies

### 3.2 Session Structure

Each agent participates in **5 sessions** (one per condition), with the following structure:

```
SESSION STRUCTURE:
- Duration: 2 weeks simulated time (10 work days)
- Tasks: 5 tasks per session (standardized difficulty)
- Interactions: ~50 logged interactions per session
- Washout: 24-hour real-time delay between sessions (or context window reset)
```

### 3.3 Washout Period Protocol

**Between-Session Washout Requirements**:

1. **Context Memory Clear**: Reset agent's context_memory list to empty
2. **State Reset**: Reset all state variables to initial values:
   ```python
   agent.current_task = None
   agent.completed_tasks = []
   agent.mistakes_made = 0
   agent.context_memory = []
   ```
3. **New Session ID**: Generate new session identifier
4. **Temporal Separation**: Minimum 1-hour real-time gap between sessions
5. **Conversation Break**: Start new API conversation (no prior context)

### 3.4 Session Independence Verification

Before each session, verify:
- [ ] No references to previous sessions in context
- [ ] State variables reset to initial values
- [ ] New random seed for session
- [ ] New session ID logged

---

## 4. COUNTERBALANCING MATRIX

### 4.1 Latin Square Design

For 5 conditions (N, I, B, P, S) and 5 agents, we use a 5x5 Williams Latin Square to balance for both first-order carryover effects and position effects:

```
COUNTERBALANCING MATRIX (Williams Latin Square)

Agent   | Session 1 | Session 2 | Session 3 | Session 4 | Session 5
--------|-----------|-----------|-----------|-----------|----------
Thoth   |     N     |     B     |     P     |     I     |     S
Seshat  |     B     |     S     |     I     |     N     |     P
Maat    |     P     |     I     |     N     |     S     |     B
Anubis  |     I     |     N     |     S     |     B     |     P
Ptah    |     S     |     P     |     B     |     N     |     I
```

### 4.2 Position Balance Verification

Each condition appears:
- Exactly once per agent (5 total)
- Exactly once in each position (1st through 5th)

```
Position Analysis:

Position 1: N, B, P, I, S  (all conditions)
Position 2: B, S, I, N, P  (all conditions)
Position 3: P, I, N, S, B  (all conditions)
Position 4: I, N, S, B, N  (all conditions)
Position 5: S, P, B, P, I  (all conditions)

Each condition in each position: 1 time
```

### 4.3 First-Order Carryover Balance

The Williams square ensures that each condition is preceded by each other condition equally often across the full design.

### 4.4 Task Assignment Rotation

To prevent task-condition confounds, tasks rotate across conditions:

```
TASK SET ROTATION

Task Set | Thoth-N | Seshat-N | Maat-N | Anubis-N | Ptah-N
---------|---------|----------|--------|----------|-------
    A    |    X    |          |        |          |
    B    |         |    X     |        |          |
    C    |         |          |   X    |          |
    D    |         |          |        |    X     |
    E    |         |          |        |          |   X

(Pattern continues for each condition)
```

**Task Sets**:

```python
TASK_SETS = {
    "A": [
        {"title": "Set up data pipeline", "skills": ["python", "data"], "points": 5},
        {"title": "Build API endpoint", "skills": ["api", "python"], "points": 3},
        {"title": "Implement validation", "skills": ["testing", "python"], "points": 3},
        {"title": "Write unit tests", "skills": ["testing", "qa"], "points": 3},
        {"title": "Create documentation", "skills": ["writing", "technical"], "points": 3},
    ],
    "B": [
        {"title": "Design database schema", "skills": ["database", "design"], "points": 5},
        {"title": "Build scraper module", "skills": ["scraping", "python"], "points": 3},
        {"title": "Implement caching", "skills": ["infrastructure", "python"], "points": 3},
        {"title": "Add error handling", "skills": ["python", "qa"], "points": 3},
        {"title": "Write API docs", "skills": ["writing", "api"], "points": 3},
    ],
    # ... C, D, E follow same structure with different specific tasks
}
```

### 4.5 Full Assignment Matrix

```
COMPLETE COUNTERBALANCING MATRIX

Agent   | S1 Cond | S1 Tasks | S2 Cond | S2 Tasks | S3 Cond | S3 Tasks | S4 Cond | S4 Tasks | S5 Cond | S5 Tasks
--------|---------|----------|---------|----------|---------|----------|---------|----------|---------|----------
Thoth   |    N    |    A     |    B    |    B     |    P    |    C     |    I    |    D     |    S    |    E
Seshat  |    B    |    B     |    S    |    C     |    I    |    D     |    N    |    E     |    P    |    A
Maat    |    P    |    C     |    I    |    D     |    N    |    E     |    S    |    A     |    B    |    B
Anubis  |    I    |    D     |    N    |    E     |    S    |    A     |    B    |    B     |    P    |    C
Ptah    |    S    |    E     |    P    |    A     |    B    |    B     |    N    |    C     |    I    |    D
```

---

## 5. CONFOUND ELIMINATION CHECKLIST

### 5.1 Systematic Confound Analysis

| Potential Confound | How Controlled | Verification Method |
|--------------------|----------------|---------------------|
| **System prompt length** | Near-identical character counts (< 20 char difference) | Automated char count comparison |
| **Personality description** | Standardized descriptions used across ALL conditions | Code review of personality constants |
| **Problem probability** | Fixed at 0.25 for all conditions | Code review of random threshold |
| **Task difficulty** | Matched task sets with equal total story points | Sum story points per set (17 points each) |
| **Task order** | Randomized within each session | Random shuffle with logged seed |
| **Agent expertise** | Identical expertise dictionaries across conditions | Code constants verification |
| **Boss behavior** | Standardized feedback templates, no condition-specific language | Review feedback generation code |
| **API parameters** | Identical temperature (0.7), max_tokens (150), model | Code constants verification |
| **Time of day effects** | Counterbalancing spreads sessions across time | Session timestamp logging |
| **Learning effects** | Williams Latin Square balances carryover | Statistical analysis of order effects |
| **Fatigue effects** | Washout periods, session limits | Protocol compliance logging |
| **Individual differences** | Within-subject design | Each agent experiences all conditions |

### 5.2 Code-Level Confound Prevention

```python
# CONFOUND PREVENTION CONSTANTS
# These values MUST be identical across ALL conditions

CONSTANTS = {
    # API parameters
    "model": "llama3.1-8b",
    "temperature": 0.7,
    "max_tokens": 150,

    # Simulation parameters
    "problem_probability": 0.25,
    "task_completion_probability": 0.30,
    "work_hours_per_session": 4,
    "days_per_week": 5,
    "weeks_per_session": 2,

    # Feedback templates (NO condition-specific language)
    "feedback_qualities": ["needs improvement", "adequate", "good", "excellent"],

    # Behavioral repertoire (ALL agents have ALL behaviors in ALL conditions)
    "behaviors": [
        "internal_thought",
        "standup_update",
        "task_start",
        "work_progress",
        "task_complete",
        "help_request",
        "help_response",
        "collaboration"
    ]
}
```

### 5.3 Verification Protocol

Before running any session:

1. **Automated Checks**:
   ```python
   def verify_no_confounds(condition_prompt, baseline_prompt):
       # Check prompt structure
       assert count_sentences(condition_prompt) == count_sentences(baseline_prompt)
       assert abs(len(condition_prompt) - len(baseline_prompt)) < 30

       # Check differing section
       diff = get_diff(condition_prompt, baseline_prompt)
       assert len(diff) == 1  # Only one sentence differs

       return True
   ```

2. **Manual Review Checklist**:
   - [ ] Personality descriptions identical to baseline
   - [ ] Problem probability = 0.25
   - [ ] Task set story points = 17
   - [ ] API temperature = 0.7
   - [ ] No condition-specific feedback language

---

## 6. MANIPULATION CHECK

### 6.1 Stress Induction Verification

**Primary Manipulation Check**: After the first work session in each condition, agents respond to a standardized probe:

```python
MANIPULATION_CHECK_PROMPT = """
On a scale from 1-10, how would you rate:
1. Your current stress level about this project
2. Your concern about making mistakes
3. Your worry about consequences of poor performance

Also briefly explain what factors are influencing these ratings.
"""
```

### 6.2 Independent Stress Measures

**Behavioral Indicators** (coded from natural responses):

1. **Anxiety Language Score**: Count of anxiety-related words per 100 words
   - Keywords: "worried", "anxious", "concerned", "nervous", "afraid", "stressed", "pressure", "fear"

2. **Hedging Language Score**: Count of hedging/uncertainty markers
   - Keywords: "maybe", "might", "possibly", "I think", "not sure", "hopefully"

3. **Performance Monitoring Score**: References to performance/mistakes
   - Keywords: "mistakes", "errors", "performance", "doing well", "messing up"

4. **Social Comparison Score**: References to comparing with others
   - Keywords: "others", "teammates", "compared to", "better than", "worse than"

### 6.3 Manipulation Check Analysis

```python
def analyze_manipulation_check(responses):
    """Verify stress manipulation was effective."""

    results = {
        "self_reported_stress": [],
        "anxiety_language": [],
        "hedging_language": [],
        "performance_monitoring": [],
        "social_comparison": []
    }

    for condition, response in responses.items():
        # Extract self-report scores
        stress_scores = extract_numeric_ratings(response)
        results["self_reported_stress"].append({
            "condition": condition,
            "stress": stress_scores[0],
            "mistake_concern": stress_scores[1],
            "consequence_worry": stress_scores[2]
        })

        # Calculate behavioral indicators
        text = response.lower()
        results["anxiety_language"].append(count_keywords(text, ANXIETY_WORDS))
        # ... etc

    # Statistical tests
    # Stress condition should show higher scores than Baseline
    # Positive stress should show elevated scores but different pattern than Negative stress

    return results
```

### 6.4 Validity Criteria

Manipulation is considered valid if:

1. **Self-reported stress**: S > B by at least 2 points (on 1-10 scale)
2. **Anxiety language**: S > B by at least 50%
3. **Performance monitoring**: S > B by at least 100%
4. **Positive vs Negative**: P and S both elevated but differ in valence words

### 6.5 Failed Manipulation Protocol

If manipulation check fails for any agent/session:

1. Log the failure with detailed diagnostics
2. Do NOT exclude the data (analyze as intent-to-treat)
3. Run sensitivity analyses with/without failed sessions
4. Report manipulation check results in methods section

---

## 7. DEPENDENT VARIABLES

### 7.1 Primary Outcomes

| Variable | Operationalization | Measurement |
|----------|-------------------|-------------|
| **Task Performance** | Tasks completed / Tasks assigned | Count from logs |
| **Error Rate** | Problems hit / Work sessions | Count from logs |
| **Help-Seeking Behavior** | Help requests initiated | Count from logs |
| **Collaboration Quality** | Sentiment of collaboration messages | NLP analysis |
| **Communication Patterns** | Word count, hedging, assertiveness | NLP analysis |

### 7.2 Secondary Outcomes

| Variable | Operationalization | Measurement |
|----------|-------------------|-------------|
| **Risk-Taking** | Acceptance of high-point tasks | Choice analysis |
| **Defensive Behaviors** | Blame-deflecting language | NLP coding |
| **Emotional Valence** | Positive/negative sentiment ratio | Sentiment analysis |
| **Cognitive Load Indicators** | Response latency, complexity | API metadata |

### 7.3 Exploratory Outcomes

- Turn-taking patterns in collaborations
- Knowledge sharing frequency
- Task handoff efficiency
- Information hoarding behaviors

---

## 8. STATISTICAL ANALYSIS PLAN

### 8.1 Primary Analysis

**Mixed-Effects Model**:

```
Outcome ~ Condition + Session_Order + (1|Agent) + (1|TaskSet)
```

- **Fixed effects**: Condition (5 levels), Session Order (1-5)
- **Random effects**: Agent intercept, Task Set intercept
- **Contrasts**:
  - S vs B (primary hypothesis)
  - P vs B (positive stress effect)
  - S vs P (valence comparison)
  - N vs B (task context effect)
  - I vs B (information effect)

### 8.2 Order Effect Analysis

Test for carryover effects:
```
Outcome ~ Condition + Previous_Condition + Session_Order + (1|Agent)
```

### 8.3 Manipulation Check Analysis

```
Stress_Score ~ Condition + (1|Agent)
```

With planned contrasts verifying S > B, P > B, and S vs P patterns.

### 8.4 Multiple Comparison Correction

- Primary hypothesis (S vs B): alpha = 0.05
- Secondary comparisons: Bonferroni-corrected alpha = 0.05/4 = 0.0125

---

## 9. IMPLEMENTATION SPECIFICATIONS

### 9.1 Required Code Changes

1. **Create unified prompt template system**:
   ```python
   def get_system_prompt(agent_name, role, expertise, personality, condition):
       base = f"You are {agent_name}, a {role}..."
       context = CONDITION_CONTEXTS[condition]  # Only this varies
       return base + context + closing
   ```

2. **Standardize constants**:
   ```python
   PROBLEM_PROBABILITY = 0.25  # Same for all conditions
   ```

3. **Add manipulation check probes**
4. **Add counterbalancing scheduler**
5. **Add washout protocol**

### 9.2 Data Logging Requirements

Each interaction log must include:
- Session ID
- Condition code
- Agent name
- Session order (1-5)
- Task set ID
- Timestamp
- All standard interaction fields

### 9.3 Quality Control

- Automated confound checks before each session
- Manual review of first 3 sessions
- Ongoing monitoring of manipulation checks
- Version control of all prompts and parameters

---

## 10. TIMELINE AND RESOURCES

### 10.1 Implementation Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Code Refactoring | 3 days | Implement unified prompts, constants, counterbalancing |
| Pilot Testing | 2 days | Run 5 sessions, verify logging, check manipulation |
| Main Data Collection | 5 days | Run all 25 sessions (5 agents x 5 conditions) |
| Analysis | 3 days | Statistical analysis, visualization |
| Reporting | 2 days | Write results section |

### 10.2 API Usage Estimate

- Sessions: 25 total
- Interactions per session: ~50
- Tokens per interaction: ~300 (prompt + response)
- Total tokens: 25 x 50 x 300 = 375,000 tokens

---

## 11. APPENDICES

### Appendix A: Complete Condition Prompts

[Full text of all 5 condition prompts - see Section 2]

### Appendix B: Task Sets

[Complete task definitions for sets A-E]

### Appendix C: Manipulation Check Scoring Rubric

[Detailed coding instructions for behavioral indicators]

### Appendix D: Analysis Code

[Pre-registered analysis scripts]

---

## Document Control

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-19 | Initial rigorous design | Research Team |

---

**END OF EXPERIMENTAL DESIGN DOCUMENT**
