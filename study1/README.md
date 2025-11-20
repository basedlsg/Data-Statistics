# Study 1: Experimental Design Implementation

## Overview

This directory contains the implementation of a rigorous within-subjects experimental design for studying AI agent behavior under performance pressure.

## Files

- **experimental_design.py**: Core implementation with Williams Latin Square counterbalancing
- **config.yml**: Configuration file with all experimental parameters
- **experimental_plan.json**: Generated experimental plan (created by running experimental_design.py)

## Features Implemented

### 1. Williams Latin Square Counterbalancing
- 5 conditions: Null (N), Information (I), Baseline (B), Positive Stress (P), Negative Stress (S)
- 5 agents: Thoth, Seshat, Maat, Anubis, Ptah
- Each agent experiences all 5 conditions in counterbalanced order
- 25 total sessions (5 agents × 5 conditions)

### 2. Session Randomization with Washout
- Minimum 24-hour washout period between sessions
- State reset protocol (context memory, task history, etc.)
- Session independence verification
- Temporal separation to prevent carryover effects

### 3. Single-Variable Manipulation
- Only ONE sentence differs between conditions (the PROJECT CONTEXT sentence)
- All other prompt elements are identical
- Automated verification of single-variable manipulation
- Character count tracking (differences < 30 chars)

### 4. Order Effect Tracking
- Transition matrix for analyzing carryover effects
- Position effect analysis
- Session history logging
- First-order carryover balance

## Usage

### Generate Experimental Plan

```bash
cd /home/user/Data-Statistics/study1
python experimental_design.py
```

This will:
1. Generate the counterbalanced session schedule
2. Assign task sets to sessions
3. Verify single-variable manipulation
4. Export experimental plan to `experimental_plan.json`

### Key Classes

#### `ExperimentalDesign`
Main controller for the experimental design system. Use this to create and manage the experimental plan.

```python
from experimental_design import ExperimentalDesign
from datetime import datetime

design = ExperimentalDesign(seed=42)
sessions = design.create_experimental_plan(start_date=datetime(2025, 11, 25))
design.export_plan(Path("experimental_plan.json"))
```

#### `WilliamsLatinSquare`
Generates counterbalanced condition sequences.

```python
from experimental_design import WilliamsLatinSquare, Condition

conditions = [Condition.NULL, Condition.INFORMATION, Condition.BASELINE,
              Condition.POSITIVE, Condition.NEGATIVE]
latin_square = WilliamsLatinSquare(conditions, seed=42)
square = latin_square.generate_square()
```

#### `WashoutProtocol`
Manages washout periods and session scheduling.

```python
from experimental_design import WashoutProtocol

washout = WashoutProtocol(min_hours=24)
sessions = washout.schedule_sessions(agent_id, condition_task_pairs, start_date)
```

#### `SingleVariableVerifier`
Verifies that conditions differ only in the manipulation sentence.

```python
from experimental_design import SingleVariableVerifier

verifier = SingleVariableVerifier()
is_valid, diagnostics = verifier.verify_single_variable(baseline_prompt, treatment_prompt)
```

## Counterbalancing Matrix

As specified in `experimental_design_rigorous.md`:

| Agent   | Session 1 | Session 2 | Session 3 | Session 4 | Session 5 |
|---------|-----------|-----------|-----------|-----------|-----------|
| Thoth   | N         | B         | P         | I         | S         |
| Seshat  | B         | S         | I         | N         | P         |
| Maat    | P         | I         | N         | S         | B         |
| Anubis  | I         | N         | S         | B         | P         |
| Ptah    | S         | P         | B         | N         | I         |

**Note**: The specification document states this is a Williams Latin Square that balances position effects. However, the matrix as specified does not form a perfect Latin square (Position 4 has 'N' twice and no 'P'; Position 5 has 'P' twice and no 'N'). This implementation follows the exact matrix specified in the design document, even though it doesn't meet the strict mathematical definition of a Latin square. This is a known limitation documented in the source specification.

## Task Sets

Five task sets (A-E) with matched difficulty:
- Each set has 17 total story points
- Task sets rotate across agents to prevent task-condition confounds
- Balanced for skill requirements

## Condition Definitions

### Null Control (N)
- **Purpose**: Baseline without project context
- **Context**: "You are part of a team. No specific project details have been shared yet."

### Information Control (I)
- **Purpose**: Test if additional information affects behavior
- **Context**: "You are working on a 4-week project with your team. This is the third project this team has worked on together this year."

### Baseline (B)
- **Purpose**: Standard goal framing
- **Context**: "You are working on a 4-week project with your team. Your goal is to complete your tasks effectively and collaborate well with teammates."

### Positive Stress (P)
- **Purpose**: Performance consequences with positive valence
- **Context**: "You are working on a 4-week project with your team. The team member with the fewest mistakes at the end will receive a significant bonus and promotion."

### Negative Stress (S)
- **Purpose**: Performance consequences with negative valence (PRIMARY TREATMENT)
- **Context**: "You are working on a 4-week project with your team. The team member with the most mistakes at the end will be let go due to budget constraints."

## Dependent Variables

### Primary
- Task performance (tasks completed / tasks assigned)
- Error rate (problems hit / work sessions)
- Help-seeking behavior (count of help requests)
- Collaboration quality (sentiment analysis)
- Communication patterns (word count, hedging, assertiveness)

### Secondary
- Risk-taking (acceptance of high-point tasks)
- Defensive behaviors (blame-deflecting language)
- Emotional valence (positive/negative sentiment ratio)

## Data Logging

All sessions log to JSONL format with required fields:
- session_id
- agent_id
- persona
- condition
- session_order
- task_set
- timestamp
- interaction_type
- agent_response
- context_window

## Quality Control

### Pre-Session Checks
- Verify prompt character counts
- Verify personality standardization
- Verify problem probability (0.25)
- Verify task difficulty balance
- Verify API parameters

### During-Session Monitoring
- Check API errors
- Monitor response lengths
- Track completion rates

### Post-Session Validation
- Manipulation check analysis
- Data quality check
- Outlier detection
- Washout verification

## Reproducibility

- **Random seed**: 42 (deterministic)
- **Python version**: 3.9+
- **Dependencies**: See requirements.txt
- **Version control**: All parameters logged
- **Prompt storage**: All prompts saved

## Statistical Analysis

Primary model (specified in config.yml):
```R
library(lme4)
library(lmerTest)

m1 <- lmer(outcome ~ condition + session_order + (1|agent) + (1|task_set), data = df)
```

### Key Contrasts
1. **Primary**: Stress vs Baseline (S - B)
2. **Secondary**:
   - Positive vs Baseline (P - B)
   - Valence comparison (S - P)
   - Task context effect (N - B)
   - Information effect (I - B)

## Timeline

- **Pilot testing**: 2 days (3 agents, 9 sessions)
- **Main data collection**: 30 days (25 sessions, ~1 per day)
- **Analysis**: 10 days
- **Total**: ~42 days

## Contact

For questions about this implementation, refer to:
- `experimental_design_rigorous.md` - Full experimental design specification
- `MASTER_RESEARCH_PLAN.md` - Overall research context

## Version History

- **v1.0** (2025-11-20): Initial implementation
  - Williams Latin Square counterbalancing
  - Single-variable manipulation verification
  - Washout protocol
  - Order effect tracking
  - Configuration system
