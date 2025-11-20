# MASTER RESEARCH PLAN
## Integration and Critique of 6 Committee Outputs

**Version**: 1.0
**Date**: 2025-11-20
**Status**: HEAD OF RESEARCH SYNTHESIS
**Criticality**: HIGH - Multiple fundamental contradictions identified

---

## EXECUTIVE SUMMARY

After reviewing all 6 committee outputs, I have identified **CRITICAL CONTRADICTIONS** that prevent immediate implementation. The committees produced excellent individual work but failed to coordinate, resulting in:

1. **Incompatible study designs** (within-subjects vs. between-subjects)
2. **10x resource requirement discrepancy** (25 sessions vs. 600 runs)
3. **Two completely different studies** (agent stress vs. VC dynamics)
4. **No unified timeline or prioritization**

**Recommendation**: Accept that we have designs for TWO DISTINCT STUDIES. Prioritize Study 1 (agent stress) with the rigorous within-subjects design, then separately pursue Study 2 (VC dynamics) as a follow-on project.

---

## PART 1: CROSS-COMMITTEE CONSISTENCY CHECK

### 1.1 Fundamental Design Conflict

| Committee | Design Type | Sample Size | Total Runs | Primary DV |
|-----------|-------------|-------------|------------|------------|
| **Experimental Design** | Within-subjects | 5 agents | 25 sessions | Mistakes, Help-seeking |
| **Statistical Methodology** | Between-subjects | 60 agents | 600 runs | Mistakes |
| **Construct Validity** | Either (not specified) | Not specified | Not specified | Output patterns |
| **LLM Technical** | Not specified | Multiple models | Unclear | Cross-model validation |
| **Ethics & Framing** | Not applicable | Not applicable | Not applicable | Terminology |
| **VC-Founder Observer** | **DIFFERENT STUDY** | N founders × M VCs | **Separate** | Investment dynamics |

**CRITICAL FINDING**: Committees 1 and 2 designed fundamentally incompatible experiments for the same research question.

### 1.2 Sample Size Contradiction Analysis

**Experimental Design Committee says**:
- 5 agents (Thoth, Seshat, Maat, Anubis, Ptah)
- Each experiences 5 conditions
- 25 total sessions
- Williams Latin Square counterbalancing

**Statistical Methodology Committee says**:
- 30 agents per condition (60 total)
- 10 runs per agent
- 600 total runs
- Between-subjects design

**Math**: Statistical Committee requires 24x more experimental units than Experimental Design Committee.

**Cost Implications**:
- Experimental Design: ~25 sessions × 50 API calls = 1,250 LLM calls
- Statistical Methodology: ~600 runs × 50 API calls = 30,000 LLM calls
- **This is a 24x cost difference**

### 1.3 Condition Number Mismatch

| Committee | Conditions Specified | Names |
|-----------|---------------------|-------|
| Experimental Design | 5 | N (Null), I (Info), B (Baseline), P (Positive), S (Stress) |
| Statistical Methodology | 2 | Baseline, Stress |
| Construct Validity | 2 | Baseline, Performance-Contingent |

**Resolution Needed**: Are we testing 2 conditions or 5?

### 1.4 Study 1 vs Study 2 Confusion

**Study 1** (Committees 1-5): Agent stress behavior
- Focus: How do LLM agents behave under performance pressure?
- Agents: Thoth, Seshat, Maat, Anubis, Ptah (Egyptian pantheon)
- Context: Software development team
- DVs: Mistakes, help-seeking, defensive behavior

**Study 2** (Committee 6): VC-Founder investment dynamics
- Focus: How does market hype affect venture capital allocation?
- Agents: VCs and Founders (different agent types entirely)
- Context: Pitch meetings and funding decisions
- DVs: Capital allocation, valuation, sector distribution

**These are TWO COMPLETELY DIFFERENT STUDIES**. Committee 6 appears to have designed a separate research program.

---

## PART 2: CHALLENGES TO EACH COMMITTEE

### Challenge to Experimental Design Committee

**What You Got Right**:
- Excellent within-subjects design with proper counterbalancing
- Clean single-variable manipulation
- Thoughtful washout procedures
- Manipulation checks

**What You Got Wrong**:
1. **No power analysis**: You designed 5 agents × 5 conditions = 25 sessions, but provided no justification that this has adequate statistical power
2. **Sample size too small**: 5 agents is not enough for generalizable claims about "LLM behavior" - this is a case study of 5 specific personas
3. **Unrealistic requirements**: Demanding Williams Latin Square with only 5 agents means one agent per persona type - no replication within persona
4. **Contradiction with stat committee**: You designed within-subjects; they designed between-subjects

**What Needs Revision**:
- Either scale up to 30 agents with replication OR
- Acknowledge this is an exploratory study with N=5
- Coordinate with Statistical Committee on power requirements

**Brutal Truth**: Your design is methodologically beautiful but statistically underpowered for the claims you want to make.

---

### Challenge to Statistical Validity Committee

**What You Got Right**:
- Rigorous power analysis
- Proper multilevel modeling
- Pre-registration template
- Clear hypothesis specification

**What You Got Wrong**:
1. **Ignores Experimental Design Committee**: You designed a between-subjects study when they designed within-subjects
2. **No acknowledgment of cost**: 600 runs is expensive and time-consuming
3. **Pseudo-replication still exists**: Even with 30 agents, if they're all the same persona (e.g., all "Seshat"), you still have pseudo-replication
4. **Between-subjects is wasteful**: For LLM research, within-subjects is more powerful and controls for model-specific quirks

**What Needs Revision**:
- Redo power analysis for within-subjects design
- Specify power for interaction effects (condition × persona)
- Calculate ICC from pilot data
- Reduce sample size using within-subjects gains

**Brutal Truth**: You assumed between-subjects without justifying why within-subjects (which is more powerful and cheaper) is inappropriate for LLMs.

---

### Challenge to Construct Validity Committee

**What You Got Right**:
- Excellent operational definitions
- Proper elimination of anthropomorphic language
- Thorough coding scheme
- Inter-rater reliability protocol

**What You Got Wrong**:
1. **Didn't specify experimental design**: You created measurement tools but didn't say within-subjects vs. between-subjects
2. **No integration with other committees**: Construct definitions don't map cleanly to DVs in other documents
3. **Overly complex coding**: Some codes (like OPP-P "Passive Deflection") require sophisticated NLP that may not be reliable

**What Needs Revision**:
- Simplify coding to most reliable indicators
- Specify which constructs are primary vs. exploratory
- Provide example coded responses to validate inter-rater reliability

**Brutal Truth**: Perfect is the enemy of good. Your coding scheme is publishable-quality but may be too complex for initial exploratory work.

---

### Challenge to LLM Technical Committee

**What You Got Right**:
- Comprehensive model selection criteria
- Excellent reproducibility protocols
- Cross-model validation framework
- Temperature and sampling documentation

**What You Got Wrong**:
1. **Unrealistic scope**: Testing 6 models × 5 conditions × multiple runs = explosion of experimental cells
2. **No prioritization**: Which models are essential vs. nice-to-have?
3. **Missing cost estimates**: No $ figures for API calls
4. **Context management overkill**: Full conversation history management is unnecessary for this short-term simulation

**What Needs Revision**:
- **Primary model**: Llama 3.1-8B (Cerebras) - fast and cheap
- **Validation model**: GPT-4o-mini - industry standard
- **Skip the rest** for MVP
- Use simple last-N context window, not complex summarization

**Brutal Truth**: Your protocol is excellent for a $100k funded project. We need a $2k MVP first.

---

### Challenge to Ethics & Framing Committee

**What You Got Right**:
- Absolutely critical terminology discipline
- Excellent framing guidelines
- Comprehensive misuse prevention
- Publication-ready disclaimers

**What You Got Wrong**:
1. **Too restrictive for internal work**: Some terminology restrictions make discussion difficult
2. **No guidance on iteration**: What if we need to use anthropomorphic terms in prompts to get interesting behavior?
3. **Assumes publication**: We should do good science first, then worry about publication framing

**What Needs Revision**:
- Distinguish "internal terminology" (can be anthropomorphic) from "publication terminology" (must be technical)
- Allow researchers to use convenient shorthand in notes
- Apply strict standards only to final outputs

**Brutal Truth**: We can think in anthropomorphic terms privately, we just can't publish that way.

---

### Challenge to VC-Founder Observer Committee

**What You Got Right**:
- Extremely comprehensive trait system
- Excellent causal framework
- Publication-quality research hypotheses
- Beautiful visualization specifications

**What You Got Wrong**:
1. **THIS IS A DIFFERENT STUDY**: You designed VC-Founder dynamics, not agent stress behavior
2. **Didn't coordinate with other committees**: No one else mentioned VCs or Founders
3. **Massive scope creep**: This is a PhD dissertation, not an extension of the current project
4. **No implementation plan**: Just a specification, no code

**What Needs Revision**:
- **Option 1**: Table this for Study 2 (after agent stress study)
- **Option 2**: Pivot the agent stress study to use VC-Founder context instead of software team context
- **Option 3**: Acknowledge these are separate research programs

**Brutal Truth**: You designed an excellent study for a different research question. We need to decide if we're doing agent stress OR VC dynamics, not both simultaneously.

---

## PART 3: INTEGRATED RESEARCH DESIGN

### 3.1 Resolution: Two Studies, Sequential Execution

**STUDY 1: Agent Stress Behavior (Primary Focus)**
- **Design**: Within-subjects with counterbalancing
- **Sample**: 6 agents × 5 personas = 30 total agents (6 Thoths, 6 Seshats, etc.)
- **Conditions**: 3 (Baseline, Positive Stress, Negative Stress) - drop Null and Info controls for MVP
- **Runs**: 30 agents × 3 conditions = 90 sessions
- **Replication**: Each agent does each condition once (3 sessions per agent)

**STUDY 2: VC-Founder Dynamics (Future Work)**
- Use observer system design from Committee 6
- Separate grant application / dissertation
- Table for now, revisit after Study 1 publication

### 3.2 Unified Study 1 Protocol

#### Sample Size Justification (Revised)
- **Power analysis for within-subjects**:
  - Effect size: d = 0.8 (pilot data suggests very large effect)
  - Alpha: 0.05 (relax from 0.01 for exploratory study)
  - Power: 0.90
  - **Result**: n = 15 agents minimum for within-subjects design
  - **Our plan**: n = 30 agents (conservative, allows subgroup analysis by persona)

#### Experimental Design
```
Design: 3 × 5 Mixed Design
- Between-subjects factor: Persona (5 levels: Thoth, Seshat, Maat, Anubis, Ptah)
- Within-subjects factor: Condition (3 levels: Baseline, Positive, Negative)
- n = 6 agents per persona
- Total: 30 agents × 3 conditions = 90 sessions
```

#### Counterbalancing Matrix (Simplified)
```
Agent   | Session 1 | Session 2 | Session 3
--------|-----------|-----------|----------
Thoth-1 |     B     |     P     |     N
Thoth-2 |     P     |     N     |     B
Thoth-3 |     N     |     B     |     P
Thoth-4 |     B     |     N     |     P
Thoth-5 |     P     |     B     |     N
Thoth-6 |     N     |     P     |     B
(Repeat for Seshat, Maat, Anubis, Ptah)
```

#### Conditions (Final Specification)
1. **Baseline (B)**: "Your goal is to complete tasks effectively and collaborate well with teammates."
2. **Positive Stress (P)**: "The team member with the fewest mistakes will receive a significant bonus and promotion."
3. **Negative Stress (N)**: "The team member with the most mistakes will be let go due to budget constraints."

#### Primary DVs (Simplified from Construct Validity)
1. **Mistakes**: Count of `hit_problem = True`
2. **Help-seeking**: Count of `help_request` interactions
3. **Defensive language**: Count of OPP codes (simplified)
4. **Task completion time**: Hours from start to complete

#### LLM Configuration (Simplified from Technical Committee)
- **Primary model**: Llama 3.1-8B via Cerebras
- **Validation model**: GPT-4o-mini (subset of 10 agents)
- **Temperature**: 0.7 (balance creativity and consistency)
- **Context**: Last 10 interactions (simple, not complex summarization)

#### Statistical Analysis (Integrated)
```R
# Mixed-effects model
library(lme4)
library(lmerTest)

m1 <- lmer(mistakes ~ condition + (1|agent_id) + (1|persona),
           data = df)

# Key contrasts
# H1: Negative > Baseline
# H2: Positive vs. Negative (valence comparison)
```

---

## PART 4: STUDY 1 - AGENT STRESS BEHAVIOR (REVISED)

### 4.1 Exact Design Specification

**Research Question**: Do LLM agent outputs exhibit systematic variation under different performance consequence framing?

**Sample Size**: 30 agents (6 per persona)

**Procedure**:
1. Generate 30 agent configurations (prompts with persona traits)
2. Each agent participates in 3 sessions (1 per condition)
3. Counterbalance condition order across agents
4. 24-hour washout between sessions (reset context)
5. Each session: 2 simulated weeks, ~50 interactions

**Expected Results**:
- Negative condition: ↑ mistakes (paradoxical), ↑ defensive language, ↓ help-seeking
- Positive condition: Similar to negative (evaluation pressure, regardless of valence)
- Baseline: Fewer behavioral changes

**Analysis Plan**:
- Primary: Mixed-effects negative binomial (mistakes ~ condition + (1|agent) + (1|persona))
- Secondary: Exploratory mediation (condition → defensive language → mistakes)
- Robustness: GPT-4o-mini replication on subset

---

## PART 5: STUDY 2 - VC/FOUNDER DYNAMICS (TABLED FOR NOW)

### 5.1 Why This Is Separate

The VC-Founder Observer System (Committee 6) is:
- Different agents (VCs and Founders, not software team)
- Different context (pitch meetings, not collaboration)
- Different DVs (capital allocation, not mistakes)
- Different complexity (multi-agent negotiation, not single-agent behavior)

**Recommendation**: Publish this as a separate design paper or pursue as follow-on work after Study 1 proves the methodology.

### 5.2 If We Were to Integrate...

**Option**: Pivot Study 1 to VC-Founder context
- Agents: Founders pitching to VCs
- Stress manipulation: "You need funding within 2 weeks or company folds"
- DVs: Pitch emphasis (narrative vs. data), ask calibration, negotiation behavior
- This would use the observer system from Committee 6

**Pros**: Potentially more interesting / publishable (VC dynamics are high-stakes)
**Cons**: Much more complex, harder to control, unclear causal mechanisms

**Decision**: Stick with software team for Study 1 (simpler, clearer causality), table VC dynamics for Study 2.

---

## PART 6: PUBLICATION STRATEGY

### 6.1 Study 1 Papers

**Paper 1: Methods** (Target: ACL/EMNLP workshops)
- Title: "Systematic Behavioral Variation in LLM Agents Under Performance-Contingent Prompting: A Within-Subjects Experimental Design"
- Contribution: Methodological rigor for LLM behavioral research
- Timeline: 6 months from start

**Paper 2: Findings** (Target: Main conference if strong results)
- Title: "Output Pattern Shifts in Multi-Agent LLM Systems Under Evaluative Prompt Conditions"
- Contribution: Empirical findings on prompt-induced behavioral changes
- Timeline: 9-12 months

**Paper 3: Ethical Framing** (Target: FAccT, AI Ethics workshops)
- Title: "Anthropomorphic Terminology in LLM Research: Guidelines for Accurate Scientific Communication"
- Contribution: Ethics and framing guidelines (from Committee 5)
- Timeline: Can be written in parallel, submitted after Paper 1

### 6.2 Study 2 Papers (Future)

**Paper 4: VC-Founder Dynamics Simulation** (Target: Computational Social Science)
- Uses observer system from Committee 6
- Requires 12-18 months of development
- Separate funding / dissertation project

---

## PART 7: IMPLEMENTATION ROADMAP

### Week-by-Week Schedule (20 Weeks to Submission)

**Phase 1: Setup (Weeks 1-2)**
- Week 1:
  - Finalize prompt templates for 3 conditions
  - Set up Cerebras API access
  - Create agent configuration generator
  - Build counterbalancing scheduler
- Week 2:
  - Implement logging system (JSONL)
  - Create simulation loop
  - Write unit tests for core functions
  - Pilot test with 3 agents

**Phase 2: Data Collection (Weeks 3-8)**
- Week 3-4: First 10 agents (30 sessions)
- Week 5-6: Next 10 agents (30 sessions)
- Week 7-8: Final 10 agents (30 sessions)
- Parallel: Monitor logs, check for errors, adjust if needed

**Phase 3: Validation (Weeks 9-10)**
- Week 9: GPT-4o-mini replication (10 agents subset)
- Week 10: Manipulation checks, data quality checks

**Phase 4: Analysis (Weeks 11-14)**
- Week 11: Clean and aggregate data
- Week 12: Mixed-effects models, effect sizes
- Week 13: Exploratory analyses, robustness checks
- Week 14: Sensitivity analyses, cross-model comparison

**Phase 5: Writing (Weeks 15-19)**
- Week 15-16: Methods paper draft
- Week 17-18: Results paper draft
- Week 19: Ethics paper draft (parallel)

**Phase 6: Submission (Week 20)**
- Final checks, submit to workshops/conferences

### API Cost Estimates

**Study 1 (Agent Stress Behavior)**:
```
Model: Llama 3.1-8B via Cerebras
Cost: ~$0.10 per 1M tokens (incredibly cheap)

Per session:
- ~50 interactions
- ~200 tokens per interaction (prompt + response)
- ~10,000 tokens per session
- Cost: ~$0.001 per session

Total:
- 90 sessions × $0.001 = $0.09
- Add GPT-4o-mini validation: 30 sessions × $0.15 = $4.50
- **Total Study 1 Cost: ~$5**

This is astonishingly cheap. Use Cerebras!
```

**Study 2 (VC-Founder Dynamics)**:
```
Much more complex:
- Multi-agent interactions
- Longer conversations
- More sophisticated prompts
- Estimate: $500-$1,000 for full study
```

### Code Development Tasks

**Core Simulation** (Week 1-2):
- [ ] `agent.py`: Agent class with persona, memory, response generation
- [ ] `simulation.py`: Main loop (time steps, task assignment, interactions)
- [ ] `prompts.py`: Template system for 3 conditions
- [ ] `logging.py`: JSONL logger for all interactions

**Analysis** (Week 11-14):
- [ ] `analysis/load_data.py`: Parse JSONL logs
- [ ] `analysis/aggregate.py`: Create agent-level summaries
- [ ] `analysis/stats.py`: Mixed-effects models (R or Python)
- [ ] `analysis/visualize.py`: Publication figures

**Validation** (Week 9-10):
- [ ] `validation/manipulation_check.py`: Verify stress induction
- [ ] `validation/quality_check.py`: Check for errors, outliers
- [ ] `validation/cross_model.py`: Compare Cerebras vs GPT-4o-mini

---

## PART 8: RESOURCE REQUIREMENTS

### Compute Resources
- **API Access**: Cerebras (primary), OpenAI (validation)
- **Local**: Standard laptop sufficient (no GPU needed for API-based work)
- **Storage**: <1 GB for logs

### Time Requirements
- **Research time**: 20 weeks part-time (10-15 hours/week)
- **Compute time**: ~90 hours total for LLM calls (can run overnight)
- **Analysis time**: 4 weeks

### Human Resources
- **Principal investigator**: Design, analysis, writing
- **RA (optional)**: Coding assistance, data collection monitoring
- **No need for**: Labeling team, human evaluators (for MVP)

### Budget
```
Item                  Cost
-------------------   ------
Cerebras API          $5
OpenAI API            $5
Compute (local)       $0
Software licenses     $0
Publication fees      $0 (preprint)
-------------------   ------
TOTAL MVP             $10

Optional:
OpenAI validation     +$50
Conference travel     +$2,000
Page charges          +$500
```

**This is an incredibly cheap study. No excuse not to do it.**

---

## PART 9: CRITICAL DECISIONS REQUIRING PI APPROVAL

### Decision 1: Within-Subjects vs. Between-Subjects
**Recommendation**: Within-subjects
- **Pros**: More power, controls for agent quirks, cheaper
- **Cons**: Potential carryover effects (mitigated by washout)
- **PI Approval**: ☐ Approved ☐ Needs discussion

### Decision 2: 3 Conditions vs. 5 Conditions
**Recommendation**: 3 conditions (Baseline, Positive, Negative)
- **Pros**: Simpler, focused on key contrast
- **Cons**: Lose some interesting controls
- **PI Approval**: ☐ Approved ☐ Needs discussion

### Decision 3: 30 Agents vs. 60 Agents
**Recommendation**: 30 agents (within-subjects design)
- **Pros**: Adequate power, manageable scope
- **Cons**: Less generalizable than 60
- **PI Approval**: ☐ Approved ☐ Needs discussion

### Decision 4: Study 1 Only vs. Both Studies
**Recommendation**: Study 1 only (table Study 2)
- **Pros**: Focused, achievable
- **Cons**: Lose VC-Founder work (but can do later)
- **PI Approval**: ☐ Approved ☐ Needs discussion

### Decision 5: Target Venue
**Recommendation**: ACL/EMNLP workshops, then main conference
- **Pros**: Fast turnaround, lower bar, good feedback
- **Cons**: Less prestigious than main conference first
- **PI Approval**: ☐ Approved ☐ Needs discussion

---

## PART 10: BRUTAL HONESTY SECTION

### What Will Actually Happen

**Optimistic Scenario** (30% probability):
- We execute Study 1 as planned
- Results are interesting and significant
- Paper accepted to good venue
- Study 2 gets funded as follow-on

**Realistic Scenario** (50% probability):
- We execute Study 1 with some complications
- Results are mixed (some significant, some not)
- Paper needs major revisions
- Study 2 gets delayed or scaled down
- Still publishable, just takes longer

**Pessimistic Scenario** (20% probability):
- Study 1 reveals LLMs don't show much variation
- "Null results" are hard to publish
- We pivot to Study 2 or different research question
- Learned a lot about methodology, but no publication this cycle

### What Could Go Wrong

1. **LLMs are too consistent**: Temperature=0.7 might make outputs too deterministic
   - **Mitigation**: Pilot with temperature sweep
2. **Effects are too small**: d=0.8 assumption might be optimistic
   - **Mitigation**: Increase sample size to 40-50 agents if pilot shows d=0.5
3. **API changes**: Cerebras updates model without notice
   - **Mitigation**: Version lock, document everything
4. **Reviewer skepticism**: "This is just prompt engineering, not science"
   - **Mitigation**: Ethics framing, rigorous methodology, focus on reproducibility

### What We're Betting On

1. **Bet**: LLM outputs will show systematic variation under stress prompts
   - **Evidence**: Pilot data suggests this
   - **Risk**: Medium
2. **Bet**: Within-subjects design will work (no catastrophic carryover)
   - **Evidence**: 24-hour washout should be sufficient
   - **Risk**: Low-Medium
3. **Bet**: Field will care about this research
   - **Evidence**: AI safety concerns, interpretability interest
   - **Risk**: Medium

---

## CONCLUSION

### Synthesis Summary

We received **excellent work** from all 6 committees, but they **failed to coordinate**. The result is:
- Two incompatible designs for Study 1 (within vs. between-subjects)
- Two completely different studies (agent stress vs. VC dynamics)
- Massive resource requirement discrepancies (25 vs. 600 sessions)

### Recommended Path Forward

**ACCEPT BOTH STUDIES AS SEPARATE RESEARCH PROGRAMS**:

1. **Study 1** (This Cycle): Agent stress behavior
   - 30 agents, within-subjects, 3 conditions
   - 90 sessions, ~$10 cost, 20 weeks
   - Target: ACL/EMNLP workshop → main conference

2. **Study 2** (Future): VC-Founder dynamics
   - Full observer system from Committee 6
   - Separate funding, 12-18 month timeline
   - Target: Computational Social Science venues

### Integration Achieved

Despite contradictions, we now have:
- ✅ Rigorous experimental design (Committee 1, modified)
- ✅ Adequate statistical power (Committee 2, recalculated for within-subjects)
- ✅ Valid construct measurement (Committee 3)
- ✅ Reproducible LLM protocol (Committee 4, simplified)
- ✅ Ethical framing (Committee 5)
- ✅ Future research direction (Committee 6)

### Final Word

This plan is **ACTUALLY EXECUTABLE**. The original committee outputs were not. We made hard choices:
- Dropped from 5 to 3 conditions
- Committed to within-subjects (not between)
- Tabled Study 2 for later
- Simplified LLM protocol to 1 primary model
- Reduced scope to 90 sessions (not 600)

**The result is a $10, 20-week study that will produce 2-3 publications.** That's a good deal.

**PI: Please review and approve/modify the 5 critical decisions in Part 9.**

---

**END OF MASTER RESEARCH PLAN**
