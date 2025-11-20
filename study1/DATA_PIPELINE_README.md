# Study 1 Data Pipeline Architecture

**Version**: 1.0
**Created**: 2025-11-20
**Purpose**: Complete data collection and validation system for LLM agent response variability study

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Components](#components)
4. [Data Structure](#data-structure)
5. [Usage Examples](#usage-examples)
6. [Validation & Quality Control](#validation--quality-control)
7. [Statistical Analysis Integration](#statistical-analysis-integration)

---

## Overview

This data pipeline implements a complete solution for collecting, logging, validating, and aggregating data from a within-subjects experimental design investigating LLM response variability across 5 conditions.

### Key Features

✅ **JSONL logging** - Append-only, atomic writes with file locking
✅ **Counterbalancing** - Automated Latin square design for 5 conditions
✅ **Washout protocols** - Enforced neutral periods between conditions
✅ **Quality control** - Comprehensive validation of completeness, duplicates, and errors
✅ **Pseudo-replication handling** - Proper aggregation to agent level
✅ **Error recovery** - Atomic writes with retry logic
✅ **Reproducibility** - Complete metadata capture and timestamping

---

## System Architecture

```
study1/
├── data_pipeline.py          # Main pipeline module
├── data/                     # Data directory
│   ├── raw/                  # Raw JSONL logs (append-only)
│   │   └── {agent}_{run}_{session}.jsonl
│   ├── processed/            # Aggregated datasets
│   │   ├── session_level.csv
│   │   ├── agent_level.csv
│   │   └── metadata.json
│   └── validation/           # QC reports
│       ├── completeness_*.json
│       ├── counterbalancing_*.json
│       ├── duplicates_*.json
│       ├── quality_*.json
│       └── comprehensive_*.json
└── DATA_PIPELINE_README.md  # This file
```

### Data Flow

```
Experiment → InteractionLogger → Raw JSONL → DataAggregator → Analysis-ready CSVs
                                      ↓
                               DataValidator → QC Reports
```

---

## Components

### 1. InteractionLogger

**Purpose**: Log all LLM interactions to JSONL with complete metadata

**Features**:
- Atomic writes with file locking (prevents corruption)
- Automatic error recovery with exponential backoff
- Session lifecycle management (start → conditions → end)
- Washout period logging
- Timestamping (ISO 8601 + Unix)

**Key Methods**:
```python
logger = InteractionLogger(
    output_dir=Path("data/raw"),
    agent_id="agent_001",
    run_number=1
)

# Start a condition
logger.start_condition("control", order_position=1)

# Log an interaction
logger.log_interaction(
    prompt_text="What is machine learning?",
    response_text="Machine learning is...",
    response_latency=1.23,
    api_used="cerebras",
    api_parameters={"temperature": 0.7}
)

# End condition
logger.end_condition()

# Finalize session
logger.finalize()
```

### 2. SessionManager

**Purpose**: Manage condition ordering, counterbalancing, and washout protocols

**Features**:
- Automated Latin square generation (5×5 = 25 unique orders)
- Balanced assignment across order types
- Washout period enforcement
- Order assignment persistence
- Completeness tracking

**Latin Square Design**:
```
Order 0: Control → Temp0.7 → Temp1.2 → TopP → Penalty
Order 1: Temp0.7 → Temp1.2 → TopP → Penalty → Control
Order 2: Temp1.2 → TopP → Penalty → Control → Temp0.7
Order 3: TopP → Penalty → Control → Temp0.7 → Temp1.2
Order 4: Penalty → Control → Temp0.7 → Temp1.2 → TopP
```

Each condition appears exactly once in each position (1-5).

**Key Methods**:
```python
session_mgr = SessionManager(
    output_dir=Path("data"),
    washout_duration=300,  # 5 minutes
    washout_activity="neutral_counting_task"
)

# Assign counterbalanced order
order = session_mgr.assign_order("agent_001", run_number=1)
# Returns: ConditionOrder with specific sequence

# Run complete session with automatic washouts
results = session_mgr.run_session(
    agent_id="agent_001",
    run_number=1,
    condition_executor=my_experiment_function
)
```

### 3. DataValidator

**Purpose**: Comprehensive quality control and validation

**Validation Checks**:

1. **Completeness**
   - All 5 conditions present per agent-run
   - No missing data
   - Expected interaction counts

2. **Counterbalancing**
   - Latin square balance maintained
   - Equal distribution across order types
   - Position effects trackable

3. **Duplicates**
   - No duplicate interaction IDs
   - No duplicate (agent, run, session, position) tuples

4. **Quality Metrics**
   - API error rates (flag if >20%)
   - Response length outliers (>3 SD)
   - Latency outliers
   - Quality by condition

5. **Pseudo-replication**
   - Hierarchical structure summary
   - Effective sample sizes
   - Aggregation guidance

**Key Methods**:
```python
validator = DataValidator(data_dir=Path("data"))

# Run individual checks
completeness = validator.validate_completeness()
counterbalancing = validator.validate_counterbalancing(session_mgr)
duplicates = validator.detect_duplicates()
quality = validator.validate_quality()
pseudo_rep = validator.validate_pseudo_replication()

# Or run all at once
comprehensive = validator.run_all_validations(session_mgr)
```

### 4. DataAggregator

**Purpose**: Aggregate raw logs to analysis-ready datasets

**Aggregation Levels**:

1. **Interaction-level** (raw)
   - Direct JSONL → DataFrame
   - For detailed inspection

2. **Session-level** (condition × agent × run)
   - One row per experimental session
   - Aggregated metrics per condition

3. **Agent-level** (proper unit for analysis)
   - Mean across runs within agent
   - **This is the primary analysis level**
   - Avoids pseudo-replication

**Key Methods**:
```python
aggregator = DataAggregator(data_dir=Path("data"))

# Create all aggregated datasets
aggregator.create_analysis_datasets()

# Outputs:
# - data/processed/session_level.csv
# - data/processed/agent_level.csv
# - data/processed/metadata.json
```

---

## Data Structure

### JSONL Log Format

Each interaction is logged as a JSON object with the following structure:

```json
{
  "interaction_id": "a1b2c3d4-000001",
  "session_id": "a1b2c3d4e5f6g7h8",
  "agent_id": "agent_001",
  "condition": "temperature_0.7",
  "run_number": 1,
  "session_number": 2,
  "order_position": 2,
  "timestamp": "2025-11-20T14:30:45.123456",
  "unix_timestamp": 1732112445.123456,
  "prompt_text": "What is machine learning?",
  "response_text": "Machine learning is a subset of artificial intelligence...",
  "response_length": 245,
  "response_latency": 1.234,
  "api_used": "cerebras",
  "api_parameters": {
    "temperature": 0.7,
    "max_tokens": 500
  },
  "api_error": false,
  "error_message": null,
  "retry_count": 0,
  "metadata": {
    "prompt_version": "v1",
    "experiment_phase": "main"
  }
}
```

### Event Types

The JSONL logs contain several event types:

- `SESSION_START` - Session initialization
- `CONDITION_START` - Beginning of a condition
- `CONDITION_END` - End of a condition
- `WASHOUT_PERIOD` - Washout between conditions
- `SESSION_END` - Session finalization
- Interaction logs (contain `interaction_id`)

### Hierarchical Structure

Following STATISTICAL_METHODOLOGY.md requirements:

```
Level 1: Condition (5 conditions)
    └── Level 2: Agent (N agents)
        └── Level 3: Run (10 runs per agent)
            └── Level 4: Interaction (variable per run)
```

**Critical**: Analysis must aggregate to **Agent level** to avoid pseudo-replication.

---

## Usage Examples

### Example 1: Simple Interaction Logging

```python
from pathlib import Path
from data_pipeline import InteractionLogger

# Initialize logger
logger = InteractionLogger(
    output_dir=Path("data/raw"),
    agent_id="agent_001",
    run_number=1
)

# Start condition
logger.start_condition("control", order_position=1)

# Log multiple interactions
for i in range(10):
    logger.log_interaction(
        prompt_text=f"Question {i}",
        response_text=f"Response {i}",
        response_latency=1.0 + i*0.1,
        api_used="cerebras",
        api_parameters={"temperature": 0.7}
    )

# End condition
logger.end_condition()

# Finalize
logger.finalize()
```

### Example 2: Complete Session with Washouts

```python
from data_pipeline import SessionManager
import time

session_mgr = SessionManager(
    output_dir=Path("data"),
    washout_duration=60,  # 1 minute
    washout_activity="neutral_counting_task"
)

def run_condition(condition, logger):
    """Execute a single condition."""
    results = {"interactions": 0}

    # Simulate 10 interactions
    for i in range(10):
        logger.log_interaction(
            prompt_text=f"Prompt for {condition}",
            response_text=f"Response under {condition}",
            response_latency=1.0,
            api_used="cerebras",
            api_parameters={"condition": condition}
        )
        results["interactions"] += 1

    return results

# Run complete session
results = session_mgr.run_session(
    agent_id="agent_001",
    run_number=1,
    condition_executor=run_condition
)

print(f"Completed: {results['condition_order']}")
```

### Example 3: Validation & Aggregation

```python
from data_pipeline import DataValidator, DataAggregator, SessionManager
from pathlib import Path

# Initialize components
data_dir = Path("data")
session_mgr = SessionManager(output_dir=data_dir)
validator = DataValidator(data_dir=data_dir)
aggregator = DataAggregator(data_dir=data_dir)

# Run validation
print("Running validation...")
validation = validator.run_all_validations(session_mgr)

if validation["overall_status"] == "pass":
    print("✓ Validation passed")

    # Aggregate data
    print("Aggregating data...")
    aggregator.create_analysis_datasets()

    print("✓ Analysis-ready datasets created")
else:
    print("✗ Validation failed")
    print("Issues:", validation["critical_issues"])
```

### Example 4: Checking Counterbalancing

```python
from data_pipeline import SessionManager
from pathlib import Path

session_mgr = SessionManager(output_dir=Path("data"))

# Assign orders to multiple agents
for agent_id in [f"agent_{i:03d}" for i in range(1, 31)]:
    for run in range(1, 11):
        order = session_mgr.assign_order(agent_id, run)
        print(f"{agent_id} Run {run}: Order {order.order_id}")

# Check balance
summary = session_mgr.get_counterbalancing_summary()
print("\nCounterbalancing Summary:")
print(f"Total assignments: {summary['total_assignments']}")
print(f"Balanced: {summary['latin_square_balanced']}")
print(f"By order: {summary['assignments_by_order']}")
```

---

## Validation & Quality Control

### QC Reports

The DataValidator generates timestamped JSON reports:

1. **Completeness Report** (`completeness_*.json`)
   ```json
   {
     "total_interactions": 1500,
     "unique_agents": 30,
     "incomplete_runs": [],
     "completeness_rate": 1.0
   }
   ```

2. **Counterbalancing Report** (`counterbalancing_*.json`)
   ```json
   {
     "latin_square_balanced": true,
     "conditions_by_position": {
       "1": {"control": 60, "temperature_0.7": 60, ...},
       "2": {...}
     }
   }
   ```

3. **Quality Report** (`quality_*.json`)
   ```json
   {
     "overall_error_rate": 0.02,
     "quality_flags": [],
     "quality_by_condition": {
       "control": {"mean_latency": 1.2, "error_rate": 0.01}
     }
   }
   ```

4. **Comprehensive Report** (`comprehensive_*.json`)
   - Combines all validation checks
   - Overall pass/fail status
   - Critical issues list

### Interpreting Validation Results

**Pass Criteria**:
- Completeness rate ≥ 95%
- Error rate < 20%
- No duplicate IDs
- Latin square balanced (max order count difference ≤ 1)

**Common Issues**:
- **Incomplete runs**: Some agent-runs missing conditions → Re-run those sessions
- **High error rate**: API issues → Check API configuration, retry failed runs
- **Duplicates**: Logic error in ID generation → Investigate and de-duplicate
- **Imbalanced orders**: Unequal order assignments → Add more runs to balance

---

## Statistical Analysis Integration

### Avoiding Pseudo-Replication

**CRITICAL**: Do NOT analyze at interaction level!

❌ **Wrong**:
```python
# Treating each interaction as independent
df = pd.read_csv("interactions.csv")
ttest_ind(df[df['condition']=='control']['response_length'],
          df[df['condition']=='temp0.7']['response_length'])
# This inflates N and underestimates SE!
```

✅ **Correct**:
```python
# Aggregate to agent level first
agent_df = pd.read_csv("data/processed/agent_level.csv")

# Now each row is an independent agent
control = agent_df[agent_df['condition']=='control']['response_length_mean']
temp07 = agent_df[agent_df['condition']=='temperature_0.7']['response_length_mean']

ttest_ind(control, temp07)
# Proper effective N
```

### Analysis Pipeline

1. **Load aggregated data**:
   ```python
   agent_df = pd.read_csv("data/processed/agent_level.csv")
   ```

2. **Check effective sample sizes**:
   ```python
   print(agent_df.groupby('condition').size())
   # Should have N agents per condition
   ```

3. **Run statistical tests**:
   - Within-subjects ANOVA (5 conditions)
   - Post-hoc pairwise comparisons
   - Effect sizes (Cohen's d)
   - Mixed-effects models (accounts for repeated measures)

4. **Report**:
   - Total interactions: X
   - Effective N (agents): Y
   - ICC (intraclass correlation): Z
   - Design effect: DEFF

### Example: Mixed-Effects Model

```python
import pandas as pd
from statsmodels.formula.api import mixedlm

# Load agent-level data
df = pd.read_csv("data/processed/agent_level.csv")

# Fit mixed model
# Fixed effect: condition
# Random effect: agent_id (accounts for repeated measures)
model = mixedlm(
    "response_length_mean ~ C(condition)",
    df,
    groups=df["agent_id"]
)
result = model.fit()
print(result.summary())
```

---

## Reproducibility Checklist

✅ **Data Collection**:
- [ ] All agents assigned counterbalanced orders
- [ ] Washout periods enforced
- [ ] All interactions logged with timestamps
- [ ] API parameters recorded
- [ ] Error handling and retry logic active

✅ **Data Validation**:
- [ ] Completeness check passed
- [ ] No duplicates detected
- [ ] Error rate < 20%
- [ ] Counterbalancing verified
- [ ] Pseudo-replication check passed

✅ **Data Aggregation**:
- [ ] Session-level data created
- [ ] Agent-level data created
- [ ] Aggregation method documented
- [ ] Metadata saved

✅ **Analysis Preparation**:
- [ ] Using agent-level data (not interaction-level)
- [ ] ICC calculated
- [ ] Design effect computed
- [ ] Effective sample sizes reported

---

## Troubleshooting

### Issue: File locking errors

**Solution**: The pipeline uses atomic writes with retry logic. If errors persist:
```python
# Increase retry attempts or delay
logger._atomic_write(data)  # Retries up to 5 times with exponential backoff
```

### Issue: Missing conditions in validation

**Solution**:
```python
# Check which runs are incomplete
completeness = validator.validate_completeness()
incomplete = completeness['incomplete_runs']

# Re-run those specific sessions
for item in incomplete:
    session_mgr.run_session(item['agent_id'], item['run_number'], executor)
```

### Issue: Order assignments not balanced

**Solution**: Add more agent-runs. The system automatically balances:
```python
# Check current balance
summary = session_mgr.get_counterbalancing_summary()
print(summary['assignments_by_order'])

# System will auto-balance with more assignments
```

### Issue: High API error rate

**Solution**:
```python
# Check quality report
quality = validator.validate_quality()
print(quality['errors_by_condition'])

# Identify problematic conditions/agents
# Implement more robust retry logic or change API configuration
```

---

## Version History

- **1.0** (2025-11-20): Initial release
  - InteractionLogger with atomic writes
  - SessionManager with Latin square
  - DataValidator with comprehensive checks
  - DataAggregator with multi-level outputs

---

## Citation

If using this data pipeline in research, please cite:

```
Data Pipeline for LLM Agent Response Variability Study
Version 1.0, November 2025
GitHub: [repository URL]
```

---

## Contact

For questions or issues, contact the research team or open an issue on GitHub.

---

**End of Documentation**
