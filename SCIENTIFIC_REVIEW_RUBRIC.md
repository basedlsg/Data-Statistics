# Scientific Review Rubric: VC Hype Simulation Project

## Multi-Perspective Committee Assessment
**Date**: December 2, 2025
**Project**: VC Hype Simulation / LLM Agent Behavior Research
**Review Type**: Pre-Submission Scientific Rigor Audit

---

## Executive Summary: The Four Perspectives

| Reviewer | Verdict | Overall Score | Key Issue |
|----------|---------|---------------|-----------|
| **Visionary CEO** | Needs Major Revision | 4/10 | "Beautiful machinery, no insight" |
| **Research Students** | Promising but Incomplete | 7/10 | Two incompatible studies |
| **Realist CTO** | Not Ready for Submission | 3/10 | Circular reasoning, unfalsifiable |
| **Design Committee** | Conditional Approval | 4/5 ⭐ | Study 1 proceed; Study 2 table |

---

## PART 1: VISIONARY CEO RUBRIC
### "What makes this insanely great?"

### Dimension 1: The "Reality Distortion Field" Test
*Does this make people WANT to believe it? Is the core insight memorable?*

| Criterion | Target | Current | Gap |
|-----------|--------|---------|-----|
| Surprising Finding | Something that contradicts intuition | Confirms stereotypes ("Bay Area likes charisma") | **CRITICAL** |
| Memorability | One sentence that stops conversation | Jargon-heavy abstracts | **HIGH** |
| Stakes | Why should anyone care? | Unclear beyond "educational use" | **HIGH** |

**What's Wrong**: The finding "regional VCs have different preferences" is not news. It's the financial equivalent of "water is wet."

**What Would Be Great**:
- "90% of early-stage VC decisions are regional copy-cat herds disguised as selection"
- "The same founder gets 3x different valuations by changing their pitch city"
- "Hype isn't irrational—it's an optimal learning strategy for VCs"

### Dimension 2: Simplicity Score
*Can you explain it in one sentence?*

| Rating | Current State |
|--------|---------------|
| **4/10** | Three metrics glued together with jargon |

**Current**: "Bay Area and LA ecosystems exhibit 2.5-3× higher hype elasticity..."
**Target**: "Change the city, change your funding outcome—geography matters more than your business."

### Dimension 3: Visual Impact
*Are the visualizations conference-worthy?*

| Rating | Current State |
|--------|---------------|
| **2/10** | Placeholder templates, no actual figures |

**Required Figures**:
1. **The Hype Effect** - Lines showing regional responses diverge under market sentiment
2. **The Founder Mismatch** - Same founder, wildly different outcomes by region
3. **Selection Frontier** - Where each region's "sweet spot" lies
4. **The Surprise** - Whatever finding emerges from actually running the simulation

### Dimension 4: Narrative Arc
*Does it tell a story with tension and resolution?*

| Rating | Current State |
|--------|---------------|
| **5/10** | Outline structure, no human stakes |

**Missing Elements**:
- **Protagonist**: Who are we rooting for?
- **Conflict**: What's at stake?
- **Discovery**: What don't we expect?
- **Resolution**: What changes if we're right?

### Dimension 5: Paradigm Disruption
*Does this challenge conventional wisdom?*

| Rating | Current State |
|--------|---------------|
| **2/10** | Reinforces conventional wisdom |

**The Shift Needed**:
- **OLD**: "Hype is irrational, VCs make mistakes"
- **NEW**: "Hype is locally rational—different regions optimize for different deal flows"

### Visionary CEO's Verdict:
> "You've built a perfect simulation of an uninteresting question. That's worse than building an imperfect simulation of a fascinating question. Find the insight that makes VCs uncomfortable about how they actually work."

---

## PART 2: RESEARCH STUDENTS RUBRIC
### "What's exciting and what needs work?"

### Dimension 1: Technical Completeness

| Component | Status | Score |
|-----------|--------|-------|
| Core simulation engine | ✅ Well-built, critical bugs fixed | 8.5/10 |
| Test suite | ✅ Comprehensive | 8/10 |
| Configuration system | ✅ YAML-editable, modular | 9/10 |
| Analysis notebook | ⚠️ Templates only, no figures | 4/10 |
| Paper results | ❌ "INSERT RESULTS HERE" | 2/10 |

### Dimension 2: Extensibility

| Rating | Evidence |
|--------|----------|
| **9/10** | Configuration-first architecture, clean design philosophy |

**What We Love**:
- YAML-editable parameters
- Modular class structure
- Clear separation of concerns
- Easy to add new regions (Seattle/Austin defined but not executed)

### Dimension 3: Reproducibility Checklist

| Item | Status |
|------|--------|
| Seeded RNG | ✅ |
| Pinned dependencies | ✅ |
| Detailed CHANGELOG | ✅ |
| Type hints | ✅ |
| Deterministic runs | ✅ |

**Score**: 9/10 - Someone could fork this repo tomorrow and get identical results

### Dimension 4: Literature Gap

| Status | Assessment |
|--------|------------|
| **6.5/10** | References classic papers but missing 2022-2025 sentiment/bubble work |

**Papers We Should Add**:
- Baker & Wurgler sentiment measurement updates
- Recent ABM validation standards (Windrum, Fagiolo)
- Gompers et al. on actual VC decision weights

### Dimension 5: Publication Readiness

| Venue | Ready? |
|-------|--------|
| Workshop paper | ✅ Ready |
| Conference paper | ⚠️ Needs figures + results |
| Top journal | ❌ Needs empirical validation |

### Critical Finding: Two Incompatible Studies!

The project contains TWO completely different research programs:

| Study | Design | Sample | Cost |
|-------|--------|--------|------|
| **Study 1**: LLM agent behavior | Within-subjects, 25 sessions | ~1,250 calls | ~$250 |
| **Study 2**: VC-Founder dynamics | Simulation-based | N/A | ~$0 |

**These are incompatible.** Must prioritize one.

### Research Students' Verdict:
> "You've built something really solid here! The foundation is excellent. Now comes the harder part: deciding what story to tell with it. Pick ONE study, finish it well, and ship it! 🚀"

---

## PART 3: REALIST CTO RUBRIC
### "What's actually wrong?"

### RED FLAGS: Tier 1 (Show-Stoppers)

| Flag | Severity | Evidence |
|------|----------|----------|
| **Circular reasoning** | CRITICAL | Weights hard-coded to ensure Bay Area > NYC > Boston |
| **No empirical calibration** | CRITICAL | All parameters are "stylized" (made up) |
| **Two incompatible designs** | CRITICAL | 24x cost difference between proposed studies |
| **No pre-registration** | CRITICAL | Document says "to be registered" (future tense) |
| **Unfalsifiable model** | CRITICAL | Any pattern can be explained by adjusting weights |
| **Parameters are guesses** | CRITICAL | "Will be replaced with exact figures when accessible" |

### Dimension 1: Methodological Soundness

| Rating | Assessment |
|--------|------------|
| **2/10** | Circular reasoning at core |

**The Core Problem**:
```
Assumption: Regional VCs have different weights
Model: Hard-code those weights
Result: Show regional differences exist
Conclusion: "We found regional differences!"
```
This is circular. The model is designed to produce the desired outcome.

### Dimension 2: Statistical Validity

| Rating | Assessment |
|--------|------------|
| **4/10** | Plans don't equal execution |

**Issues**:
- ICC assumed (0.15) but never validated
- Replication crisis: pilot effect (d=0.534) failed to replicate
- Multiple comparisons not controlled
- Model convergence untested

### Dimension 3: Falsifiability Test

| Rating | Assessment |
|--------|------------|
| **1/10** | Model is unfalsifiable by design |

**Critical Question**: What would constitute evidence AGAINST the model?

**Answer**: Nothing. You can always adjust weights to match any observed pattern.

### Dimension 4: Data Quality

| Rating | Assessment |
|--------|------------|
| **3/10** | Everything is "stylized" |

From `data/regions.yml`:
```yaml
bay_area:
  weights:
    charisma: 0.8    # ← Where did 0.8 come from?
    vision: 1.2      # ← Where did 1.2 come from?
```
**These numbers are invented.** No source. No validation.

### Dimension 5: Limitation Honesty

| Rating | Assessment |
|--------|------------|
| **6/10** | Documentation excellent, execution poor |

**The Gap**: Team KNOWS the problems but hasn't stopped the project.

Evidence:
- REVISION_PLAN authored but project continues as-is
- MASTER_RESEARCH_PLAN identifies contradictions but continues both designs
- Phase 1 experiment running despite acknowledged flaws

### CTO's Must-Fix Checklist

**Critical Path (4 weeks)**:
- [ ] Estimate w_region from real VC data (survey or revealed preference)
- [ ] Construct Hype(t) from Baker-Wurgler index, validate timing
- [ ] Obtain PitchBook/NVCA official numbers
- [ ] Pre-register on OSF with specific hypotheses

**High Priority (4-8 weeks)**:
- [ ] Explain why pilot effect disappeared (d=0.534 → 0.0)
- [ ] Calculate ICC from actual data
- [ ] Hold out 2023-2024 data; train on 2010-2022; make predictions

### CTO's Verdict:
> "You've built a beautiful toy that confirms your priors. The code works perfectly at doing something that means nothing. To be publishable, you need to stop assuming what VCs value and start measuring it."

---

## PART 4: RESEARCH DESIGN COMMITTEE RUBRIC
### "What does the literature say?"

### Dimension 1: Literature Positioning

**Study 1 (LLM Agent Behavior)** - Well-positioned
| Strength | Assessment |
|----------|------------|
| Novel question | Few labs have attempted rigorous LLM behavioral experimentation |
| Policy relevance | AI safety community cares about LLM behavior under pressure |
| Publication venues | Methods (ACL), Ethics (FAccT), Interpretability |

**Study 2 (VC Simulation)** - Needs grounding
| Weakness | Assessment |
|----------|------------|
| Lacks calibration | Hard-coded parameters, not estimated |
| Missing literature | No engagement with recent ABM validation standards |
| Validation gap | No out-of-sample testing |

### Dimension 2: Methodological Innovation

**Study 1 Contributions** (Novel):

1. **Within-Subjects LLM Design**: Single-variable manipulation with counterbalancing
2. **Non-Anthropomorphic Framework**: Complete terminology replacement protocol
3. **Pre-Registration Template**: Full analysis plan before data collection

**Study 2 Gaps**:
- No empirical parameter estimation
- No validation strategy
- Agent heterogeneity underspecified

### Dimension 3: Build vs. Don't Build

| Study | Recommendation | Rationale |
|-------|----------------|-----------|
| **Study 1** | ✅ PROCEED | $10 budget, 20-week timeline, fills genuine gap |
| **Study 2** | ⏸️ TABLE | Requires 18 months, ~$50K, data partnerships |

### Dimension 4: Ethical Considerations

| Safeguard | Status |
|-----------|--------|
| Terminology discipline | ✅ Mandatory anthropomorphic term replacement |
| Claim calibration | ✅ "CAN claim" vs "CANNOT claim" lists |
| Publication framing | ✅ Mandatory disclaimer about stochastic generators |
| Peer review strategy | ✅ Target venues with ethics expertise |

**Remaining Risk**: Downstream misrepresentation by media

### Dimension 5: Contribution Assessment

**Study 1 Contribution Tiers**:

| Tier | Contribution | Impact | Venue |
|------|--------------|--------|-------|
| 1 | Methodology for LLM behavioral research | ⭐⭐⭐⭐ | ACL/EMNLP workshop |
| 2 | Empirical findings on output variation | ⭐⭐⭐⭐ | Main conference |
| 3 | Ethical framing contribution | ⭐⭐⭐⭐ | FAccT |

### Recommended Reading (15 Essential Papers)

**Core LLM Behavioral Science**:
1. Park et al. (2023) - "Generative Agents" - foundational for agent-based LLM work
2. Santurkar et al. (2023) - "Whose Opinions Do Language Models Reflect?" - anthropomorphism critique
3. White et al. (2023) - "Prompt Pattern Catalog" - prompt sensitivity analysis

**Experimental Design**:
4. Lakens et al. (2018) - "Equivalence Testing" - statistical methods
5. Grimm et al. (2005) - "ODD Protocol" - ABM reproducibility

**Behavioral Economics (for Study 2)**:
6. Shiller (2017) - *Narrative Economics* - theoretical foundation
7. Baker & Wurgler (2006) - "Investor Sentiment" - sentiment measurement
8. Gompers et al. (2016) - "What Do Venture Capitalists Do?" - VC decision weights

**Agent-Based Modeling**:
9. Windrum et al. (2007) - "Empirical Validation of ABM" - validation standards
10. Fagiolo et al. (2019) - "Macroeconomic Policy in ABM" - calibration methods

### Design Committee's Verdict:
> "**APPROVE Study 1** for immediate execution with pre-registration. **TABLE Study 2** as separate 18-month project requiring data partnerships. The methodological foundation is excellent; now focus on one clear contribution."

---

## PART 5: SYNTHESIS & ACTION ITEMS

### The Fundamental Tension

| Perspective | Priority |
|-------------|----------|
| **Visionary CEO** | Find ONE surprising insight |
| **Research Students** | Finish what you started |
| **Realist CTO** | Get real data first |
| **Design Committee** | Pick ONE study, do it well |

### Unanimous Agreement

All four reviewers agree on these points:

1. **Technical infrastructure is excellent** - Code quality, reproducibility, documentation
2. **Two incompatible studies exist** - Must prioritize one
3. **Parameters are not grounded** - Need empirical calibration
4. **No actual results exist** - Paper has placeholders
5. **The question is not novel enough** - Need a surprising finding

### Recommended Path Forward

```
┌─────────────────────────────────────────────────────────┐
│  DECISION POINT: Which study to pursue?                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  OPTION A: Study 1 (LLM Agent Behavior)                │
│  ├── Timeline: 20 weeks                                 │
│  ├── Budget: ~$10                                       │
│  ├── Feasibility: HIGH                                  │
│  ├── Publication venues: ACL, FAccT, EMNLP             │
│  └── Recommendation: PROCEED                           │
│                                                         │
│  OPTION B: Study 2 (VC Simulation)                     │
│  ├── Timeline: 18 months                                │
│  ├── Budget: ~$50K (data acquisition)                  │
│  ├── Feasibility: LOW without partnerships             │
│  ├── Publication venues: Mgmt Science, JFE             │
│  └── Recommendation: TABLE                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Master Checklist

#### Phase 1: Decision (Week 1)
- [ ] **CHOOSE**: Study 1 OR Study 2 (not both)
- [ ] **DOCUMENT**: Decision rationale in CHANGELOG
- [ ] **COMMUNICATE**: Update all project documents

#### Phase 2: If Study 1 (Weeks 2-20)
- [ ] Lock final sample size (n=30 agents recommended)
- [ ] Pre-register on OSF before data collection
- [ ] Pilot temperature sweep (0.3, 0.7, 0.9)
- [ ] Execute experiment
- [ ] Write methods paper → ethics paper → empirical paper

#### Phase 2: If Study 2 (Months 1-18)
- [ ] Secure VC partnership OR survey approval
- [ ] Obtain PitchBook/NVCA data access
- [ ] Estimate w_region from real data
- [ ] Calibrate Hype(t) from Baker-Wurgler index
- [ ] Define validation targets
- [ ] Train on 2010-2022, predict 2023-2024
- [ ] Write results with empirical grounding

### The One Thing That Would Change Everything

Each reviewer offered their "silver bullet":

| Reviewer | Silver Bullet |
|----------|---------------|
| **Visionary CEO** | "Find the one statistic that stops people mid-conversation" |
| **Research Students** | "Finish analysis.ipynb with real figures" |
| **Realist CTO** | "Get actual VC decision data" |
| **Design Committee** | "Pre-register before collecting any more data" |

---

## SCORING RUBRIC TEMPLATE

Use this template to track progress:

### Scientific Rigor Score Card

| Dimension | Weight | Current | Target | Notes |
|-----------|--------|---------|--------|-------|
| **Insight Novelty** | 20% | 3/10 | 8/10 | Find surprising finding |
| **Methodological Soundness** | 25% | 2/10 | 8/10 | Fix circular reasoning |
| **Data Quality** | 20% | 3/10 | 7/10 | Get real parameters |
| **Visual Impact** | 10% | 2/10 | 8/10 | Create 4 figures |
| **Narrative Clarity** | 10% | 5/10 | 8/10 | Tell a human story |
| **Reproducibility** | 10% | 9/10 | 9/10 | ✅ Already excellent |
| **Ethical Safeguards** | 5% | 8/10 | 9/10 | ✅ Mostly in place |
| **WEIGHTED TOTAL** | 100% | **3.7/10** | **8.0/10** | |

### Publication Readiness Matrix

| Venue | Current Readiness | After Fixes |
|-------|-------------------|-------------|
| Internal presentation | ✅ Ready | ✅ |
| Workshop paper | ⚠️ Needs figures | ✅ Ready |
| Conference paper | ❌ Needs results | ✅ Ready |
| Top journal | ❌ Needs validation | ⚠️ Conditional |

---

## APPENDIX: DEBATE TRANSCRIPT

### The Great Debate: CEO vs. CTO

**CEO**: "We need to make this INTERESTING. The science community talks about paradigm shifts—where's ours?"

**CTO**: "Interesting doesn't mean correct. You can't paradigm-shift your way past circular reasoning."

**CEO**: "But if no one reads the paper, what's the point of being correct?"

**CTO**: "If the paper is wrong, what's the point of people reading it?"

**CEO**: "Fine. Then let's find something that's BOTH surprising AND defensible."

**CTO**: "Agreed. That requires actual data."

**CEO**: "And a story worth telling."

**CTO**: "And a story worth believing."

**Research Students**: "Can we just run the simulation and see what happens?!"

**Design Committee**: "Pre-register first."

**Everyone**: *sighs*

---

## Document Metadata

**Created By**: Multi-Agent Committee Review
**Perspectives Represented**:
- Visionary CEO (Wow Factor + Narrative)
- Research Students (Enthusiasm + Completion)
- Realist CTO (Rigor + Falsifiability)
- Design Committee (Literature + Best Practices)

**Files Analyzed**:
- `simulate.py` - Core simulation engine
- `hype_score.py` - Hype scoring rules
- `paper/main.md` - Draft paper
- `analysis.ipynb` - Analysis notebook
- `data/regions.yml` - Regional parameters
- `data/cases.csv` - Historical cases
- `MASTER_RESEARCH_PLAN.md` - Research plan
- `REVISION_PLAN.md` - Revision plan
- `STATISTICAL_METHODOLOGY.md` - Statistics guide
- `ETHICS_AND_FRAMING_GUIDELINES.md` - Ethics guide
- `CHANGELOG.md` - Project history

**Recommendation**: Address red flags, pick ONE study, execute with rigor, and find the surprising insight that makes this work matter.
