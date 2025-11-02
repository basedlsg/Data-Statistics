# VC Hype Simulation - Claude Code Project Context

## Project Overview
A one-file simulation modeling 4 VC ecosystems as capital-allocating agents and a pool of founders/companies pitching under a tunable Hype(t) knob. This research project investigates how market sentiment affects venture capital allocation across different regional ecosystems.

## Repository Structure
```
vc-hype-sim/
  simulate.py               # Core simulation loop (deterministic seed)
  config.yml                # Global params (N founders, Hype schedule)
  data/regions.yml          # Capital shares by region (editable)
  data/cases.csv            # Exemplar companies for context section
  hype_score.py             # Simple text-rule hype scorer (v0)
  analysis.ipynb            # Figures and visualizations
  paper/main.md             # 4–6 page writeup (camera-ready)
  appendix/sources.md       # Links, table of regional dollars
  tests/                    # Unit tests
  CHANGELOG.md              # Orchestrator maintains
  CLAUDE.md                 # This file - project context
```

## Agent System (Ancient Egyptian Pantheon)

### Ra (Orchestrator/PI)
**Role**: Supreme coordinator - routes tasks, sets acceptance criteria, reviews diffs, maintains CHANGELOG.md
**Responsibilities**:
- Open and assign tasks to worker agents
- Summarize diffs and validate deliverables
- Ensure reproducibility and citation standards
- Final quality control

### Thoth (Data Acquisition)
**Role**: God of knowledge and records - gathers and organizes data
**Responsibilities**:
- Draft `data/regions.yml` with capital weights by region (Bay Area, NYC, Boston, LA)
- Create `data/cases.csv` with high-profile cases (Juicero, Quibi, Beepi, etc.)
- Document all sources in `appendix/sources.md`
- Implement simple "hype score" rubric with keyword/co-mention tracking

### Seshat (Quant Analyst)
**Role**: Goddess of mathematics, wisdom, and astronomy - builds the simulation engine
**Responsibilities**:
- Implement `simulate.py` with founder generator, Hype(t), scoring, allocator
- Create `config.yml` with tunable parameters
- Write unit tests for scoring monotonicity and budget adherence
- Run sensitivity sweeps over Hype parameter

### Ma'at (Narrative & Sentiment)
**Role**: Goddess of truth and harmony - analyzes narrative and sentiment
**Responsibilities**:
- Create `hype_score.py` with transparent, rule-based v0
- Implement term counting, press cadence analysis
- Design keyword detector (e.g., "category-defining", "paradigm-shift")
- Track elite-investor co-mentions (Sequoia/Benchmark/Tiger)

### Ptah (Research Synthesizer)
**Role**: Creator god and craftsman - synthesizes findings into publication
**Responsibilities**:
- Draft `paper/main.md` (intro, methods, results, limitations)
- Write `appendix/sources.md` with exact citations
- Ensure every claim is footnoted or labeled "stylized"
- Maintain publication-ready quality

### Anubis (Viz Specialist)
**Role**: God of precision and measurement - creates visualizations
**Responsibilities**:
- Create `analysis.ipynb` with 4 core figures:
  1. Allocation by trait × region
  2. Narrative-over-revenue crossover vs Hype
  3. Region selection frontier
  4. Robustness with Seattle/Austin
- Ensure reproducible plots with clear labels
- Generate publication-quality figures

## Simulation Specification

### Investor Ecosystems (4 regions)
- **Bay Area**: ↑ vision, charisma, AI/infra; tolerant of pre-revenue
- **NYC**: ↑ revenue, enterprise/fintech; moderate hype elasticity
- **Boston**: ↑ bio/deeptech, science signals; lower hype elasticity
- **LA**: ↑ consumer/media, brand/story tilt

### Founder Features (N=200 default)
- revenue (continuous)
- growth (continuous)
- charisma (continuous, ~N(0,1))
- vision/story (continuous)
- repeat_founder (binary)
- domain (categorical: AI/bio/consumer/enterprise)
- traction_quality (continuous)
- geo_flex (continuous)

### Scoring Model
```
score = w_region • features + β_region * Hype(t) + ε
```
Where:
- `w_region`: region-specific feature weights
- `β_region`: region-specific hype sensitivity
- `Hype(t)`: 3-state Markov (Risk-off, Normal, Hype)
- `ε`: noise term

### Hype(t) States
- **Risk-off**: Low β weights, focus on fundamentals
- **Normal**: Baseline β weights
- **Hype**: ↑ β weights on charisma & vision, wider valuation spreads

### Allocator
Greedy/knapsack algorithm subject to regional budget and stage mix; funds top-scoring pitches until capital exhausted.

## Coding Style & Standards

### Python
- Use type hints throughout
- Docstrings for all functions (Google style)
- Black formatting (line length 100)
- pytest for unit tests
- Deterministic random seeds for reproducibility

### Data Files
- YAML for configuration (human-editable)
- CSV for tabular data (with header comments for sources)
- Markdown for documentation (GitHub-flavored)

### Acceptance Criteria
Every task must include:
1. Working code with type hints
2. Unit tests where applicable
3. Source documentation for data
4. Commit message explaining changes
5. Updates to CHANGELOG.md (by Ra)

## Commands for Claude Code

### Run simulation
```bash
python simulate.py --runs 50 --seed 42 --out results/
```

### Run tests
```bash
pytest tests/ -v
```

### Generate figures
```bash
jupyter nbconvert --execute analysis.ipynb
```

## Data Policy (Class-Safe MVP)
- Allow hard-coded but up-to-date capital share estimates in config
- Document sources in appendix (PitchBook, NVCA, Carta, etc.)
- Label estimates clearly; replace with exact numbers when available
- No proprietary data in public repo

## Reproducibility Requirements
1. Seeded random number generation
2. Version-pinned dependencies (requirements.txt)
3. Unit tests for core logic
4. CHANGELOG.md tracking all changes
5. Clear source attribution in appendix

## What Makes This Publishable
1. **Transparent mechanics**: One hype knob, one allocator
2. **Editable priors**: YAML configuration for easy experimentation
3. **Robustness checks**: Add Seattle/Austin to test generalization
4. **Reproducibility**: Seeded sim, unit tests, CHANGELOG
5. **Methodological transparency**: Citations to tooling (Claude Code usage patterns)
6. **Defensive science**: Every claim footnoted or labeled "stylized"

## Task Board Status
See TODO list managed by Ra (Orchestrator)

## Notes for Claude Code
- Break work into small diffs
- Checkpoint often with commits
- Workers propose test snippets and commit messages
- Orchestration loops on "diff + rationale + tests"
- Keep core logic pure Python (can be adapted to Artifacts/web later)
