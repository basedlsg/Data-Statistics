# Phase 1 Validation: Setup and Execution Guide

## Overview

Phase 1 consists of two critical validation experiments:
- **Experiment 1**: Mechanism validation (80 interactions)
- **Experiment 2**: Cross-model replication (360 interactions)

**Total**: 440 interactions, ~$500-750, 4-6 weeks

## Prerequisites

### 1. Install Dependencies

```bash
pip install anthropic  # For Claude support
```

(Other dependencies already installed: openai, httpx, etc.)

### 2. API Keys Required

You'll need API keys for:

**Required (Experiment 1)**:
- Cerebras API key (for mechanism validation)

**Required (Experiment 2)**:
- Cerebras API key
- OpenAI API key (for GPT-4o-mini)
- Anthropic API key (for Claude 3.5 Sonnet)

### 3. Set API Keys

**Option A: Environment variables**
```bash
export CEREBRAS_API_KEY="your_cerebras_key_here"
export OPENAI_API_KEY="your_openai_key_here"
export ANTHROPIC_API_KEY="your_anthropic_key_here"
```

**Option B: Pass as arguments**
```bash
python run_phase1.py --cerebras-key "..." --openai-key "..." --anthropic-key "..."
```

## Running the Experiments

### Run Both Experiments (Full Phase 1)

```bash
cd /home/user/Data-Statistics/study1/phase1_validation
python run_phase1.py
```

This will run:
- Experiment 1: 4 conditions × 20 runs = 80 interactions
- Experiment 2: 6 personas × 2 conditions × 3 models × 10 runs = 360 interactions

### Run Experiment 1 Only (Mechanism Validation)

```bash
python run_phase1.py --experiment 1
```

This tests whether "5 story points" drives the Seshat effect.

**Critical test**: If this fails, no need to run Experiment 2.

### Run Experiment 2 Only (Cross-Model Replication)

```bash
python run_phase1.py --experiment 2
```

Tests whether effects generalize across Cerebras, GPT-4, and Claude.

### Adjust Sample Sizes

```bash
# Smaller pilot (faster, cheaper)
python run_phase1.py --exp1-n 10 --exp2-n 5

# Larger sample (more power)
python run_phase1.py --exp1-n 30 --exp2-n 15
```

## Output Files

Data is saved to:

```
phase1_validation/
├── exp1_mechanism/
│   └── data/
│       └── raw/
│           └── exp1_data.jsonl
└── exp2_crossmodel/
    └── data/
        └── raw/
            └── exp2_data.jsonl
```

## Analysis

After data collection, analyze results:

```bash
python analyze_phase1.py
```

This will:
1. Load and code all responses
2. Run statistical tests
3. Generate decision report
4. Provide GO/NO-GO recommendation for 50-persona study

## Expected Timeline

- **Days 1-2**: Run Experiment 1 (80 interactions, ~1-2 hours)
- **Day 3**: Analyze Experiment 1 results
- **Decision Point**: If mechanism validated → proceed to Exp 2
- **Days 4-7**: Run Experiment 2 (360 interactions, ~3-6 hours)
- **Days 8-10**: Analyze Experiment 2 results
- **Day 11**: Final decision report

## Decision Criteria

### GO (Proceed to 50-Persona Study)

**Requires ALL**:
✓ Mechanism validated (quantitative cue drives effect, p<0.05, d>0.4)
✓ Cross-model replication (persona effect in all 3 models)
✓ Generalizability (Model × Persona interaction small, η²<0.10)
✓ Rank order preserved (Top 3 > Bottom 3 in 2/3 models)

### NO-GO (Revise Theory)

**If ANY**:
✗ Mechanism fails (urgency drives effect, not quant cue)
✗ Effects don't replicate in GPT-4 or Claude
✗ Large Model × Persona interaction (model-specific)
✗ Rank order reverses across models

## Cost Estimates

**Experiment 1** (Cerebras only):
- 80 interactions × $0.50 = $40

**Experiment 2**:
- Cerebras: 120 × $0.50 = $60
- GPT-4: 120 × $1.50 = $180
- Claude: 120 × $1.50 = $180
- Subtotal: $420

**Total: ~$460**

(Actual costs may vary based on current API pricing)

## Troubleshooting

### SSL Errors

SSL verification is disabled for development. If you encounter SSL errors, they should be automatically handled.

### Rate Limiting

The script includes automatic retry with exponential backoff (1s, 2s, 4s, 8s).

If you hit rate limits:
- Increase sleep time in `run_phase1.py`
- Run experiments sequentially instead of in one session
- Use `--experiment 1` first, then `--experiment 2` later

### API Failures

If an API fails repeatedly:
- Check API key validity
- Check API account balance/credits
- Check API service status
- Review error logs

Failed interactions are logged and skipped (not retried indefinitely).

## Support

For questions or issues:
- Review protocol: `PHASE1_VALIDATION_PROTOCOL.md`
- Check logs in console output
- Examine raw JSONL files for data quality

## Pre-Registration

This protocol is pre-registered. See `PHASE1_VALIDATION_PROTOCOL.md` for complete experimental design, predictions, and analysis plan.

**No modifications to protocol after data collection begins.**
