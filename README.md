# VC Hype Simulation

A research simulation modeling how market sentiment (Hype) affects venture capital allocation across regional ecosystems.

## Overview

This project simulates 4 VC ecosystems (Bay Area, NYC, Boston, LA) as capital-allocating agents evaluating a pool of 200 founder/companies under a tunable Hype(t) parameter. The simulation investigates when narrative-driven factors (charisma, vision, story) outweigh fundamental metrics (revenue, growth, traction) in funding decisions.

## Key Features

- **4 Regional VC Ecosystems**: Bay Area, NYC, Boston, LA with distinct investment preferences
- **Tunable Hype Parameter**: 3-state Markov chain (Risk-off, Normal, Hype) affecting allocation
- **200 Founder Agents**: Multi-dimensional feature vectors (revenue, growth, charisma, vision, domain, etc.)
- **Transparent Scoring**: `score = w_region • features + β_region * Hype(t) + ε`
- **Reproducible**: Deterministic random seeds, unit tests, full source attribution

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Simulation
```bash
python simulate.py --runs 50 --seed 42 --out results/
```

### Generate Figures
```bash
jupyter nbconvert --execute analysis.ipynb
```

### Run Tests
```bash
pytest tests/ -v
```

## Regional Investment Preferences

| Region | Focus | Hype Elasticity |
|--------|-------|-----------------|
| **Bay Area** | Vision, charisma, AI/infra, pre-revenue tolerance | High |
| **NYC** | Revenue, enterprise/fintech, fundamentals | Moderate |
| **Boston** | Bio/deeptech, science signals, repeat founders | Low |
| **LA** | Consumer/media, brand/story, narrative | High |

## Agent System

This project uses a multi-agent framework with Ancient Egyptian deity names:

- **Ra (Orchestrator)**: Coordinates tasks and maintains quality
- **Thoth (Data Acquisition)**: Gathers and documents data sources
- **Seshat (Quant Analyst)**: Builds simulation engine
- **Ma'at (Narrative & Sentiment)**: Analyzes hype and sentiment
- **Ptah (Research Synthesizer)**: Writes research paper
- **Anubis (Viz Specialist)**: Creates visualizations

See [CLAUDE.md](CLAUDE.md) for detailed agent responsibilities.

## Outputs

1. **Capital allocation by founder traits & domain**
2. **Narrative-over-revenue crossover analysis** as Hype increases
3. **Regional selection frontier** comparing ecosystem strategies
4. **Robustness checks** adding Seattle/Austin

## Data Sources

All data sources are documented in [appendix/sources.md](appendix/sources.md). Regional capital shares are based on:
- PitchBook (2023-2024 data)
- NVCA Yearbook 2024
- Carta State of Private Markets
- Public disclosures (when available)

Estimates are clearly labeled and will be replaced with exact figures when accessible.

## Project Structure

```
vc-hype-sim/
  simulate.py               # Core simulation loop
  config.yml                # Global parameters
  data/regions.yml          # Regional capital shares (editable)
  data/cases.csv            # Historical case studies
  hype_score.py             # Hype scoring logic
  analysis.ipynb            # Figures and analysis
  paper/main.md             # Research writeup
  appendix/sources.md       # Citations and sources
  tests/                    # Unit tests
  CHANGELOG.md              # Project changelog
  CLAUDE.md                 # Project context for Claude Code
```

## Citation

If you use this simulation in your research, please cite:
```
[To be added upon publication]
```

## License

MIT License - See LICENSE file for details

## Contributing

This project is managed through Claude Code with an orchestrator + worker agent pattern. See CLAUDE.md for contribution guidelines and agent roles.

## Reproducibility

- All random number generation uses fixed seeds (default: 42)
- Dependencies pinned in requirements.txt
- Unit tests for core logic in tests/
- Full CHANGELOG in CHANGELOG.md

## Contact

[To be added]

---

Built with Claude Code | Agent System: Ancient Egyptian Pantheon
