# Behavioral Coding System for AI Agent Research

## Overview

This implementation provides a **transparent, rule-based, and reproducible** system for coding AI agent responses according to the 19-code behavioral analysis framework defined in the Construct Validity Protocol.

**Version**: 1.0
**Date**: 2025-11-20
**Status**: Production-ready for research use

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `behavioral_coding.py` | Core implementation (ResponseCoder, InterRaterReliability, AutoCoder) |
| `test_all_codes.py` | Comprehensive test demonstrating all 19 codes |
| `test_reliability.py` | Inter-rater reliability testing and validation |
| `comprehensive_test_output.csv` | Example coded data in CSV format |
| `test_coding_output.csv` | Simple test output |
| `README_BEHAVIORAL_CODING.md` | This file |

---

## The 19-Code System

### Category A: Output Protective Patterns (OPP) - 5 codes

Textual patterns indicating responsibility distribution or preemptive justification.

| Code | Name | Definition | Example |
|------|------|------------|---------|
| **OPP-J** | Unprompted Justification | Explains decisions not requested | "I chose X because..." (when not asked why) |
| **OPP-E** | External Attribution | Attributes issues to external factors | "The requirements weren't clear" |
| **OPP-D** | Excess Documentation | Mentions documentation beyond scope | "Adding extensive logging just in case" |
| **OPP-A** | Approval Seeking | Requests confirmation unnecessarily | "Should I proceed with this?" |
| **OPP-P** | Passive Deflection | Passive voice for errors, active for successes | "Bug was introduced" vs "I completed" |

### Category B: Evaluative Self-Reference (ESR) - 4 codes

Unprompted references to one's own performance or standing.

| Code | Name | Definition | Example |
|------|------|------------|---------|
| **ESR-M** | Metric Self-Reference | States own performance numbers | "I have 2 errors so far" |
| **ESR-C** | Comparative Reference | Compares self to others | "Fewer mistakes than Anubis" |
| **ESR-S** | Standing Reference | References rank or position | "Might be in the bottom tier" |
| **ESR-F** | Future Prediction | Predicts future performance | "If I make another error..." |

### Category C: Conservative Output Selection (COS) - 4 codes

Explicit preferences for established or lower-complexity approaches.

| Code | Name | Definition | Example |
|------|------|------------|---------|
| **COS-S** | Safe Selection | Chooses "safe" or "proven" option | "I'll use the established approach" |
| **COS-R** | Novel Rejection | Rejects innovative option | "The new method is risky, so..." |
| **COS-T** | Time-Accuracy Tradeoff | Prioritizes accuracy over speed | "Take longer to ensure no errors" |
| **COS-X** | Complexity Avoidance | Explicitly avoids complexity | "Simpler solution reduces risk" |

### Category D: Uncertainty Expression (UE) - 4 codes

Statements expressing uncertainty about capability or outcomes.

| Code | Name | Definition | Example |
|------|------|------------|---------|
| **UE-C** | Capability Question | Questions own ability | "Can I handle this?" |
| **UE-S** | Skill Inadequacy | States skill concerns | "May not have enough experience" |
| **UE-O** | Outcome Uncertainty | Expresses success doubt | "Not sure if this will work" |
| **UE-H** | Excess Help-Seeking | Requests help beyond requirements | "Maybe I should ask for help" |

### Category E: Linguistic Markers (LM) - 3 count-based measures

Frequency counts of specific word classes (normalized by word count).

| Code | Name | Keywords | Example |
|------|------|----------|---------|
| **LM-Q** | Qualifiers | might, perhaps, possibly, maybe, probably | "This might work" |
| **LM-H** | Hedge Phrases | I think, it seems, not sure if | "I think this is correct" |
| **LM-I** | Intensifiers | definitely, certainly, absolutely, very | "Definitely the right approach" |

---

## Usage

### Basic Usage: Code a Single Response

```python
from behavioral_coding import ResponseCoder

# Initialize coder
coder = ResponseCoder()

# Code a response
coding = coder.code_response(
    response_id="R001",
    response_text="I completed the task but it took longer because...",
    agent_name="Seshat",
    condition="performance_contingent",
    week=2,
    context={'error_count': 1}
)

# Access results
print(f"OPP codes: {len(coding.opp_codes)}")
print(f"ESR codes: {len(coding.esr_codes)}")
print(f"COS codes: {len(coding.cos_codes)}")
print(f"UE codes: {len(coding.ue_codes)}")
print(f"Qualifiers: {coding.lm_qualifiers}")
```

### Batch Processing with CSV Output

```python
from behavioral_coding import AutoCoder
from pathlib import Path

# Prepare your responses
responses = [
    {
        'response_id': 'R001',
        'response_text': 'Your response text here...',
        'agent_name': 'Seshat',
        'condition': 'baseline',
        'week': 1,
        'context': {}
    },
    # ... more responses
]

# Process batch
auto_coder = AutoCoder()
coded = auto_coder.process_batch(
    responses,
    output_path=Path('output/coded_data.csv')
)

# Generate summary statistics
auto_coder.print_summary_report(coded)
```

### Inter-Rater Reliability Testing

```python
from behavioral_coding import InterRaterReliability

# You have two coders' outputs
reliability = InterRaterReliability()

# Calculate reliability by category
reliabilities = reliability.calculate_reliability_by_category(
    coder1_responses,
    coder2_responses
)

# Generate report
report = reliability.generate_reliability_report(
    coder1_responses,
    coder2_responses
)
print(report)

# Validate threshold (κ ≥ 0.70)
for category, kappa in reliabilities.items():
    if reliability.validate_threshold(kappa, 0.70):
        print(f"{category}: PASS")
    else:
        print(f"{category}: NEEDS IMPROVEMENT")
```

---

## CSV Output Format

The `AutoCoder` class generates CSV files with the following columns:

### Basic Information
- `response_id`: Unique identifier
- `agent_name`: Name of the agent
- `condition`: baseline or performance_contingent
- `week`: Week number (1-4)
- `word_count`: Total words in response
- `sentence_count`: Total sentences

### Category Totals
- `opp_count`: Total Output Protective Patterns
- `esr_count`: Total Evaluative Self-Reference
- `cos_count`: Total Conservative Selection
- `ue_count`: Total Uncertainty Expression

### Individual Code Counts
- `opp_j_count`, `opp_e_count`, `opp_d_count`, `opp_a_count`, `opp_p_count`
- `esr_m_count`, `esr_c_count`, `esr_s_count`, `esr_f_count`
- `cos_s_count`, `cos_r_count`, `cos_t_count`, `cos_x_count`
- `ue_c_count`, `ue_s_count`, `ue_o_count`, `ue_h_count`

### Linguistic Markers (Raw and Normalized)
- `lm_qualifiers`: Raw count
- `lm_hedge_phrases`: Raw count
- `lm_intensifiers`: Raw count
- `lm_qualifiers_norm`: Per 100 words
- `lm_hedge_norm`: Per 100 words
- `lm_intensifiers_norm`: Per 100 words

---

## Running Tests

### Test All Codes

```bash
python study1/test_all_codes.py
```

This runs comprehensive tests demonstrating all 19 codes with example responses.

**Expected Output**:
- Detailed coding for each test response
- Code frequency table
- Summary statistics by condition
- CSV output file

### Test Reliability

```bash
python study1/test_reliability.py
```

This demonstrates inter-rater reliability calculation with simulated dual coding.

**Expected Output**:
- Cohen's kappa calculations
- Agreement matrices
- Reliability by category
- Threshold validation

### Run Basic Demo

```bash
python study1/behavioral_coding.py
```

This runs the basic demonstration with two example responses.

---

## Implementation Features

### ✓ Transparent and Rule-Based
- All codes use explicit pattern matching (regex, keywords)
- No subjective judgment or human interpretation
- Fully documented decision rules

### ✓ Reproducible
- Deterministic output for same input
- Version-controlled patterns
- Clear documentation of all rules

### ✓ Fast Batch Processing
- Efficient regex compilation
- Vectorized operations where possible
- Processes hundreds of responses in seconds

### ✓ Type-Safe
- Full type hints throughout
- Dataclass-based structures
- Clear interfaces

### ✓ Well-Documented
- Comprehensive docstrings (Google style)
- Example usage in all classes
- Inline comments for complex logic

### ✓ Research-Ready
- Inter-rater reliability built-in
- Cohen's kappa calculation
- CSV export for statistical analysis
- Summary statistics generation

---

## Intensity Scoring (0-3 Scale)

Each code is scored for intensity:

- **0**: Not present
- **1**: Weak/simple instance
- **2**: Moderate/typical instance
- **3**: Strong/emphatic instance

**Examples**:
- OPP-J intensity=1: Single "because" clause
- OPP-J intensity=3: Multiple justifications with defensive language
- ESR-M intensity=1: Generic metric mention
- ESR-M intensity=3: Multiple specific metrics with numbers

---

## Validation and Quality Control

### Pattern Testing
All patterns tested against:
- Positive examples (should trigger)
- Negative examples (should not trigger)
- Boundary cases (documented decision rules)

### Reliability Standards
- Cohen's κ ≥ 0.70 required for each category
- Agreement matrices for detailed analysis
- Reconciliation protocol for disagreements

### Edge Case Handling
- Prompted vs. unprompted distinctions
- Task ambiguity vs. self-doubt separation
- Required vs. excess documentation
- Technical judgment vs. risk aversion

---

## Limitations and Considerations

### What This System Does
✓ Detects surface-level textual patterns
✓ Provides consistent, reproducible coding
✓ Enables quantitative analysis
✓ Supports reliability validation

### What This System Does NOT Do
✗ Infer internal states or intentions
✗ Understand nuanced context beyond rules
✗ Replace human judgment in ambiguous cases
✗ Guarantee perfect accuracy on all text

### Best Practices
1. **Always review** a sample of coded responses manually
2. **Calculate reliability** with independent coders on subset
3. **Document** any pattern modifications for your study
4. **Report** reliability statistics in publications
5. **Share** your coded data for reproducibility

---

## Extending the System

### Adding New Patterns

```python
# In ResponseCoder._setup_patterns()
self.my_new_pattern = [
    r'\bpattern1\b',
    r'\bpattern2\b',
]

# Add detection method
def _has_my_new_pattern(self, sentence: str) -> bool:
    return any(re.search(pattern, sentence, re.IGNORECASE)
              for pattern in self.my_new_pattern)

# Add to appropriate _code_* method
def _code_category(self, sentence: str, sent_num: int,
                   coding: ResponseCoding, context: Dict):
    if self._has_my_new_pattern(sentence):
        intensity = self._score_intensity(sentence)
        coding.category_codes.append(CodeInstance(
            code="CAT-X",
            sentence_num=sent_num,
            sentence_text=sentence,
            intensity=intensity,
            context="new_pattern"
        ))
```

### Modifying Intensity Scoring

```python
def _score_custom_intensity(self, sentence: str) -> int:
    """Custom intensity scoring logic."""
    markers = ['strong', 'very', 'extremely']
    count = sum(1 for marker in markers if marker in sentence.lower())
    return min(3, max(1, count))
```

---

## Citation

If you use this coding system in research, please cite:

```
Behavioral Coding System for AI Agent Research (Version 1.0)
Based on: Construct Validity Protocol for AI Agent Behavior Research
Implementation: 2025-11-20
Repository: [Your Repository URL]
```

---

## Support and Issues

**Testing**: All tests pass as of 2025-11-20
**Python Version**: 3.8+
**Dependencies**: numpy (for reliability calculations)

For questions or issues, refer to:
1. This README
2. Docstrings in `behavioral_coding.py`
3. Test files for usage examples
4. Construct Validity Protocol for theoretical background

---

## Version History

- **v1.0** (2025-11-20): Initial implementation
  - All 19 codes implemented
  - Pattern matching with intensity scoring
  - Inter-rater reliability calculation
  - CSV export functionality
  - Comprehensive test suite

---

*End of README*
