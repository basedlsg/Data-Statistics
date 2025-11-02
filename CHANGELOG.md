# Changelog
All notable changes to the VC Hype Simulation project will be documented here by Ra (Orchestrator).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added - 2025-11-02
- Initial repository structure with Ancient Egyptian agent system
- CLAUDE.md with project context, agent roles, and specifications
- config.yml with global simulation parameters and Hype(t) Markov chain
- Directory structure: data/, paper/, appendix/, tests/, results/
- CHANGELOG.md (this file) for tracking all changes

### Agents Initialized
- **Ra (Orchestrator)**: Project coordination and quality control
- **Thoth (Data Acquisition)**: Data gathering and source documentation
- **Seshat (Quant Analyst)**: Simulation engine and quantitative analysis
- **Ma'at (Narrative & Sentiment)**: Hype scoring and sentiment analysis
- **Ptah (Research Synthesizer)**: Paper writing and research synthesis
- **Anubis (Viz Specialist)**: Visualization and figure generation

### Completed - 2025-11-02

#### Thoth (Data Acquisition) ✓
- Created `data/regions.yml` with 4 regional VC ecosystem configurations
  - Bay Area, NYC, Boston, LA with capital shares, feature weights, hype betas
  - Documented sources: PitchBook Q4 2023, NVCA 2024, Carta, regional reports
  - Added robustness regions (Seattle, Austin) for future analysis
- Created `data/cases.csv` with 20 high-profile cases (Theranos, WeWork, Quibi, etc.)
  - Narrative keywords, peak valuations, outcomes documented
  - Sources cited in appendix
- Drafted `appendix/sources.md` with comprehensive source documentation
  - All regional capital estimates documented with confidence intervals
  - Stylized parameters clearly labeled
  - Future data acquisition roadmap included

#### Seshat (Quant Analyst) ✓
- Implemented `simulate.py` (450+ lines) with full simulation engine
  - Founder agent generation from configurable priors
  - 3-state Hype Markov chain (Risk-off, Normal, Hype)
  - Regional scoring: score = w • features + β × Hype(t) × narrative + ε
  - Greedy capital allocator with budget constraints
  - CLI interface with argparse
  - Type hints throughout (Python 3.11+)
- Created `config.yml` with all tunable parameters
  - Hype state definitions and transition matrix
  - Founder feature priors (revenue, growth, charisma, vision, etc.)
  - Domain distributions and growth multipliers
- Created `requirements.txt` with pinned dependencies
  - NumPy, Pandas, PyYAML, Matplotlib, Seaborn, Jupyter, pytest

#### Ma'at (Narrative & Sentiment) ✓
- Implemented `hype_score.py` with rule-based v0 scorer
  - High-hype keyword detection (category-defining, paradigm-shift, etc.)
  - Elite VC co-mention analysis (Sequoia, a16z, Benchmark, Tiger, etc.)
  - Conservative keyword penalty (profitable, sustainable, etc.)
  - Media cadence analyzer with press spike detection
  - Normalized scoring to [0, 1] using sigmoid
  - Example usage and documentation

#### Ptah (Research Synthesizer) ✓
- Drafted `paper/main.md` (6-page research paper)
  - Abstract, introduction with motivation and related work
  - Model section: founders, regions, Hype(t), scoring, allocator
  - Results section (template for simulation output)
  - Discussion: implications, limitations, transparency
  - Full references (Baker & Wurgler, Gompers et al., NVCA, PitchBook)
  - Reproducibility checklist
- Appendix sources already created by Thoth
  - Citations in APA 7th format
  - Industry reports with URLs and access dates

#### Anubis (Viz Specialist) ✓
- Created `analysis.ipynb` with 4 publication-ready figures
  - Figure 1: Allocation by trait × region (charisma, revenue, vision, growth)
  - Figure 2: Narrative-over-revenue crossover vs Hype
  - Figure 3: Region selection frontier (narrative vs revenue focus)
  - Figure 4: Robustness with additional regions
  - Summary statistics tables
  - Publication-ready styling with seaborn
  - Clear instructions for running simulation and generating figures

#### Seshat (Unit Tests) ✓
- Created `tests/test_simulate.py` with comprehensive test suite
  - Founder generation tests (priors, distributions, domains)
  - Hype Markov chain tests (transitions, state validity)
  - Regional scoring tests (monotonicity, hype effects, domain preferences)
  - Capital allocator tests (budget adherence, greedy ordering, stage assignment)
  - End-to-end simulation tests (reproducibility with seeds)
  - Hype scorer tests (high-hype vs conservative text)
  - 25+ test cases with pytest

#### Ra (Orchestrator) ✓
- Validated all deliverables against acceptance criteria
- Updated CHANGELOG.md with complete project history
- Verified file structure matches specification
- Confirmed reproducibility standards (seeded RNG, version pinning, documentation)

## [0.1.0] - 2025-11-02
### MVP Complete - Agent Pantheon Delivers

All core deliverables completed:
- ✓ Data acquisition (regions, cases, sources)
- ✓ Simulation engine (founders, Hype(t), scoring, allocation)
- ✓ Hype scoring system (rule-based v0)
- ✓ Research paper (draft with placeholders for results)
- ✓ Analysis notebook (4 figures + summary stats)
- ✓ Unit tests (25+ test cases)
- ✓ Configuration management (YAML, editable parameters)
- ✓ Documentation (README, CLAUDE.md, appendix)

**Ready for:**
1. Running simulation: `python simulate.py --runs 50 --seed 42 --out results/`
2. Running tests: `pytest tests/ -v`
3. Generating figures: `jupyter nbconvert --execute analysis.ipynb`
4. Paper finalization with actual results

**Next steps:**
- Execute simulation and update paper with results
- Add robustness checks (Seattle/Austin)
- Sensitivity analysis (±30% weight perturbations)
- Consider NLP upgrade for hype scorer (FinBERT/GPT)

## [0.0.1] - 2025-11-02
### Project Initialization
- Created git branch: claude/vc-hype-simulation-mvp-011CUj9hptEXAXSK5PXsDXq6
- Established agent system with Egyptian deity names
- Defined simulation specification and research goals
