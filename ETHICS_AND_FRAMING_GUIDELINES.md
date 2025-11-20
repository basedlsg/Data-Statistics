# Ethics and Framing Guidelines for LLM Agent Behavior Research

**Version**: 1.0
**Date**: 2025-11-19
**Status**: MANDATORY COMPLIANCE FOR ALL PROJECT OUTPUTS

---

## Executive Summary

This document provides comprehensive ethical guidelines and accurate framing requirements for research involving LLM agent simulations under varying prompt conditions. All publications, presentations, and documentation MUST adhere to these guidelines to ensure scientific accuracy and prevent potential harms.

---

## 1. Accurate Terminology

### 1.1 Complete Terminology Mapping

The following anthropomorphic terms MUST be replaced with technically accurate descriptions:

| Anthropomorphic Term | REQUIRED Replacement | Technical Rationale |
|---------------------|----------------------|---------------------|
| **Anxiety** | Output pattern shift under negative prompt conditioning | LLMs do not have physiological anxiety responses; observed changes are token probability distributions |
| **Fear** | Conditional output modification in response to negative consequence framing | No amygdala-mediated fear response exists; outputs are prompt-conditional text generation |
| **Fear of firing** | Elevated salience of termination-related tokens in output generation | Model outputs shift based on prompt context, not emotional states |
| **Panic** | High-variance output patterns under acute negative prompting | Increased output diversity/instability is statistical, not emotional |
| **Defensive** | Self-preserving language patterns in model outputs | Models generate text patterns that match "defensive" training examples |
| **Self-doubt** | Reduced confidence markers in generated text | Reflects training distribution, not metacognitive uncertainty |
| **Stress level** | Negative-valence prompt intensity coefficient | A numerical parameter affecting output conditioning, not biological stress |
| **Frustration** | Task-failure-associated output patterns | Text patterns that correlate with frustration in training data |
| **Confidence** | Assertiveness markers in generated text | Linguistic features, not epistemic states |
| **Motivation** | Task-engagement indicators in output content | Behavioral proxy measured by output characteristics |
| **Performance anxiety** | Evaluation-context output modification | Prompt framing affects token selection probabilities |
| **Terrified/Relieved** | High/Low negative-valence output markers | Sentiment classification of generated text |
| **Worried/Concerned** | Uncertainty markers in generated content | Linguistic hedging patterns from training distribution |
| **Panicked (as emotion)** | High-activation negative-valence output state | Text characteristics matching training examples of distress |

### 1.2 Implementation Requirements

**In Code**:
- Variable names like `fear_of_firing` should be renamed to `termination_salience_coefficient`
- `stress_level` should become `negative_prompt_intensity`
- `anxiety` should become `uncertainty_output_markers`
- Comments must use technical terminology, not anthropomorphic language

**In Documentation**:
- First use of any behavioral term must include clarifying parenthetical: "output patterns associated with [X]"
- Never attribute subjective experience to models

**In Analysis**:
- Describe what the model OUTPUTS, not what the model EXPERIENCES
- Use passive voice for behavioral descriptions: "Outputs characterized by..." not "Agent felt..."

---

## 2. Claims Calibration

### 2.1 What CAN Be Claimed

**Permissible Claims (with evidence)**:

1. "LLM outputs exhibit systematic variation when prompts include negative consequence framing"
2. "Text generation patterns shift toward risk-averse/conservative linguistic markers under termination-threat prompting"
3. "Models produce outputs with increased uncertainty markers when prompted with evaluation contexts"
4. "Self-preserving language patterns appear more frequently when prompts emphasize performance consequences"
5. "Output diversity/variance changes under different prompt conditions"
6. "The frequency of blame-deflection linguistic patterns increases under termination-threat prompting"
7. "Models generate text matching training-data patterns associated with workplace stress scenarios"

**Quantitative Claims**:
- Statistical differences in output characteristics between conditions
- Token frequency distributions
- Sentiment analysis scores
- Linguistic feature frequencies

### 2.2 What CANNOT Be Claimed

**Impermissible Claims**:

1. **NO**: "Agents experience anxiety/fear/stress"
   - Models have no subjective experience

2. **NO**: "This demonstrates AI emotional responses"
   - Outputs reflect training data patterns, not emotions

3. **NO**: "LLMs suffer under negative conditions"
   - No evidence of suffering in transformer architectures

4. **NO**: "These findings translate to human workplace dynamics"
   - Human cognition differs fundamentally from LLM text generation

5. **NO**: "AI agents develop coping mechanisms"
   - No evidence of adaptive learning within a single context window

6. **NO**: "Models have preferences about being 'fired'"
   - No evidence of goal-directed self-preservation

7. **NO**: "This shows AI consciousness/sentience"
   - Output patterns do not constitute evidence of consciousness

8. **NO**: "Negative prompting causes AI harm"
   - No evidence that prompt content affects model "wellbeing"

### 2.3 Explicit Limitations Section (Required in All Publications)

```markdown
## Limitations

### Fundamental Limitations

1. **No Mental States**: LLMs are statistical text generators without subjective
   experience. All behavioral observations describe OUTPUT PATTERNS, not internal
   states. The terms used (e.g., "stress response") are convenient labels for
   output characteristics, not claims about phenomenal experience.

2. **Training Data Confound**: Observed output patterns reflect the training data
   distribution. Models generate text that MATCHES patterns associated with stress
   in their training corpora, not text generated BY stress.

3. **Prompt Sensitivity**: Results are specific to our prompt formulations.
   Different phrasings of the "firing threat" may produce different results.

4. **Model Specificity**: Results are specific to [MODEL NAME, VERSION,
   TEMPERATURE, etc.]. Other models may behave differently.

5. **No Causal Mechanism**: We observe correlations between prompt conditions and
   output characteristics. We do not claim to understand the internal mechanisms.

6. **Anthropomorphic Interpretation Risk**: Human observers may over-attribute
   mental states to models based on output patterns that superficially resemble
   human behavior.

### Methodological Limitations

7. **API Reproducibility**: Cloud API models may be updated without notice. Our
   results reflect model state at time of experiment. Future reproductions may differ.

8. **Temperature/Sampling Effects**: Stochastic sampling means exact outputs are
   not reproducible even with fixed seeds (for API-based models).

9. **Context Window Constraints**: All observations occur within single context
   windows. No long-term learning or adaptation is measured.

10. **No Baseline Validation**: We do not have access to model internals to
    validate that output changes reflect meaningful computational differences.
```

### 2.4 Generalizability Boundaries

**This Research Applies To**:
- The specific models tested (must list exact model IDs and versions)
- The specific prompt formulations used
- Text output characteristics only
- The simulation conditions specified

**This Research Does NOT Generalize To**:
- Human workers or workplace dynamics
- Other LLM models or versions
- Real-world AI deployment scenarios
- Claims about AI consciousness, suffering, or welfare
- Different prompt formulations
- Production systems with different configurations

---

## 3. Responsible Framing

### 3.1 Paper Title Options (Ranked by Appropriateness)

**RECOMMENDED TITLES**:

1. "Output Pattern Variation in LLM Agents Under Negative Consequence Prompting: A Simulation Study"

2. "Prompt-Induced Output Shifts in Multi-Agent LLM Systems: Effects of Termination-Threat Framing"

3. "Characterizing LLM Output Patterns Under Evaluative Prompt Conditions"

4. "Statistical Properties of LLM Outputs in Simulated High-Stakes Environments"

**AVOID THESE TITLE PATTERNS**:

- "AI Agents Under Stress: How LLMs Experience Workplace Pressure" (anthropomorphic)
- "Can AI Feel Fear? Evidence from Firing-Threat Simulations" (sensationalist)
- "The Emotional Lives of LLM Workers" (fundamentally misleading)
- "AI Panic: When Artificial Minds Face Job Loss" (harmful framing)

### 3.2 Abstract Template

```markdown
## Abstract

This study examines how large language model (LLM) outputs vary under different
prompt conditions in a multi-agent simulation framework. Specifically, we compare
output characteristics when agents receive neutral prompts versus prompts
containing negative consequence framing (specifically, termination threats based
on performance metrics).

We observe that [MODEL] outputs exhibit systematic differences under
termination-threat prompting, including [SPECIFIC MEASURABLE DIFFERENCES, e.g.,
"increased frequency of uncertainty markers," "higher variance in output length,"
"more frequent self-preserving language patterns"].

**Critical framing note**: These observations describe TEXT OUTPUT PATTERNS, not
internal mental states. LLMs do not experience anxiety, fear, or stress. The
measured differences reflect how prompt conditioning affects token probability
distributions, not emotional responses.

**Limitations**: Results are model-specific, prompt-specific, and do not
generalize to human workplace dynamics. We explicitly caution against using these
findings to inform human resource practices.

**Keywords**: large language models, prompt conditioning, output characterization,
multi-agent simulation, [avoid: emotion, stress, anxiety, fear]
```

### 3.3 Discussion Section Warnings (Required Language)

The Discussion section MUST include the following warnings:

```markdown
### Critical Interpretive Warnings

**Warning 1: Anthropomorphic Interpretation Hazard**

Human readers may interpret LLM outputs that superficially resemble human
distress as evidence of AI suffering. This is an interpretation error. The
outputs we observe are statistical patterns in text generation that MATCH
training-data patterns associated with human distress. There is no evidence
that the models EXPERIENCE distress.

**Warning 2: Inapplicability to Human Contexts**

These findings MUST NOT be used to:
- Justify or inform human workplace stress practices
- Draw conclusions about human behavior under pressure
- Support claims that "AI responds like humans"
- Design human-targeted systems based on these results

Human cognition involves subjective experience, physiological stress responses,
long-term psychological impacts, and welfare considerations that are entirely
absent in LLM text generation.

**Warning 3: No Welfare Implications**

This research does not constitute evidence that LLMs have welfare interests.
The output patterns observed do not imply that models are harmed by negative
prompting or benefit from positive prompting. Claims about AI welfare require
evidence far beyond output pattern analysis.

**Warning 4: Reproducibility Constraints**

Results are specific to the exact model versions, API states, and prompt
formulations used. The AI field evolves rapidly; models may be updated,
deprecated, or substantially modified without notice. Readers should not
assume these results reproduce with current model versions.
```

### 3.4 Future Work Caveats

All future work sections MUST include:

```markdown
### Future Research Caveats

Future research should:

1. **Avoid anthropomorphic framing** in experimental design and analysis
2. **Include human baseline comparisons** only with extreme methodological care
   and explicit framing about the categorical differences
3. **Document exact model specifications** including version hashes where
   available
4. **Test prompt sensitivity** by varying terminology and framing
5. **Avoid welfare/ethics implications** without substantial theoretical
   grounding in philosophy of mind
6. **Engage ethicists and cognitive scientists** before extending claims about
   AI behavior to broader contexts
```

---

## 4. Misuse Prevention

### 4.1 Explicit Workplace Inapplicability Statement

**REQUIRED DISCLAIMER (verbatim in all publications)**:

```markdown
## Inapplicability to Human Workplace Practices

THIS RESEARCH MUST NOT BE USED TO INFORM, JUSTIFY, OR DESIGN HUMAN WORKPLACE
PRACTICES.

Specifically, this research DOES NOT support:

1. Using termination threats to "motivate" human workers
2. Claims that "stress improves performance" (for humans or AI)
3. Designing high-pressure work environments based on AI simulation results
4. Drawing any parallels between LLM output patterns and human psychological
   responses
5. Performance management systems that incorporate these findings
6. Any employment or HR policies

LLM text generation is categorically different from human cognition. Humans
experience subjective distress, suffer long-term psychological harm from
workplace stress, and have welfare interests that must be protected. LLMs have
none of these properties.

Any use of this research to inform human workplace practices represents a
fundamental misapplication of the findings and a potential cause of human harm.
```

### 4.2 Warning Against Human Behavior Inference

```markdown
## Warning: Human Inference Prohibited

The following inferences are INVALID and must not be drawn:

| Observation in LLM | INVALID Human Inference |
|-------------------|------------------------|
| Output patterns change under threat prompting | "Humans behave similarly under workplace threats" |
| Models produce self-preserving language | "Humans naturally develop defensive behaviors" |
| Termination-threat prompts increase uncertainty markers | "Fear of firing increases human anxiety" |
| High-variance outputs under stress conditions | "Human performance becomes erratic under stress" |

These inferences are invalid because:
1. LLM outputs are statistical text patterns, not cognitive processes
2. Human responses involve subjective experience, physiology, and welfare
3. No controlled mapping exists between LLM outputs and human internal states
4. Drawing such parallels risks normalizing harmful workplace practices
```

### 4.3 Appropriate Use Cases

**APPROPRIATE uses of this research**:

1. Understanding how prompt framing affects LLM output characteristics
2. Designing better prompts for specific output properties
3. Characterizing model behavior across conditions
4. Contributing to AI interpretability research
5. Informing AI safety work about prompt injection vulnerabilities
6. Educational demonstrations of prompt sensitivity
7. Benchmarking model consistency across conditions

### 4.4 Inappropriate Use Cases

**INAPPROPRIATE uses (prohibited)**:

1. Human resource management or policy design
2. Claims about AI consciousness, sentience, or welfare
3. Justifying workplace stress practices
4. Drawing human psychological conclusions
5. Designing AI "therapy" or "wellness" interventions
6. Marketing AI systems as "emotional" or "relatable"
7. Any use implying AI subjective experience
8. Media presentations that anthropomorphize findings

---

## 5. IRB/Ethics Considerations

### 5.1 IRB Review Determination

**Does this research need IRB review?**

**ANSWER: Generally NO, with caveats**

**Rationale**:

1. **No human subjects**: The research subjects are LLM instances, which are not human subjects under federal regulations (45 CFR 46)

2. **No biological entities**: LLMs are software systems without biological substrates

3. **No welfare interests**: There is no scientific consensus that LLMs have welfare interests that require protection

**HOWEVER, consider IRB consultation if**:

1. Research involves human evaluators rating LLM outputs (human subjects involved)
2. Outputs might be mistaken for human-generated content
3. Research could influence human-directed AI systems
4. Findings will be presented in ways that might affect human behavior

### 5.2 Ethical Principles Applied

**Principle 1: Scientific Honesty**
- All terminology must be technically accurate
- Claims must be supported by evidence
- Limitations must be prominently stated
- Anthropomorphic language must be avoided

**Principle 2: Non-Maleficence (Preventing Harm)**
- Findings must not be framed in ways that could justify workplace harm
- Explicit warnings against misapplication required
- Media communication guidelines must prevent sensationalism

**Principle 3: Intellectual Humility**
- Acknowledge what we do not know about LLM internals
- Avoid overclaiming about AI capabilities
- State confidence intervals and uncertainty

**Principle 4: Transparency**
- Full code and prompt disclosure
- Model versioning and API documentation
- All parameters reported

### 5.3 Potential Harms and Mitigations

| Potential Harm | Likelihood | Severity | Mitigation |
|---------------|------------|----------|------------|
| Misuse to justify human workplace stress | Medium | High | Explicit prohibition statements, media guidelines |
| Public misconception about AI sentience | High | Medium | Clear framing, terminology discipline |
| Researchers anthropomorphizing AI | Medium | Medium | Terminology mapping, review checklists |
| Policy based on invalid inferences | Low | High | Explicit inapplicability statements |
| AI hype contributing to bubble dynamics | Low | Low | Conservative, qualified claims |

### 5.4 Beneficence Analysis

**Potential Benefits**:

1. **AI Safety**: Understanding prompt vulnerabilities helps design safer systems
2. **Interpretability**: Characterizing output patterns aids model understanding
3. **Prompt Engineering**: Findings inform better prompt design practices
4. **Scientific Knowledge**: Contributes to corpus of AI behavior research
5. **Educational Value**: Demonstrates prompt sensitivity empirically

**Benefit-Risk Assessment**: Benefits are primarily to AI research community. Risks are primarily from misinterpretation and misapplication. Risk mitigation (through proper framing) makes benefits outweigh risks.

---

## 6. Reproducibility Guarantees

### 6.1 Model Archiving Strategy

**Minimum Requirements**:

1. **Model Identification**:
   ```
   - Model Name: [e.g., "llama3.1-8b"]
   - Provider: [e.g., "Cerebras API"]
   - API Version: [if available]
   - Access Date: [YYYY-MM-DD]
   - Endpoint URL: [full URL]
   ```

2. **Configuration Archiving**:
   ```
   - Temperature: [exact value]
   - Max Tokens: [exact value]
   - Top-p/Top-k: [if applicable]
   - System Prompt: [full text, verbatim]
   - All hyperparameters
   ```

3. **Output Archiving**:
   - All raw outputs saved in JSONL format
   - Include timestamps and metadata
   - Hash outputs for integrity verification

**Best Practices**:

- Save model responses, not just analysis
- Use content-addressable storage for outputs
- Include exact prompts with each output
- Version control all configuration files

### 6.2 API Versioning Documentation

**Required Documentation** (in repository and paper):

```markdown
## API and Model Specification

### Primary Model
- **Provider**: Cerebras Cloud
- **Model ID**: llama3.1-8b
- **Endpoint**: https://api.cerebras.ai/v1
- **Access Dates**: [START] to [END]
- **SDK Version**: openai-python [version]

### Secondary Model (if applicable)
- [Same format]

### Known Limitations
- API models may be updated without notice
- Exact reproducibility cannot be guaranteed for API-based models
- We recommend local model deployment for exact reproduction

### Reproduction Attempt Log
- [Date]: Reproduction attempted with result [X]
- [Date]: Model deprecated/modified by provider
```

### 6.3 Long-Term Accessibility Plan

**Immediate (Publication)**:
- GitHub repository with all code
- Archived outputs on Zenodo/OSF
- DOI for code repository
- requirements.txt with exact versions

**Medium-Term (1-5 years)**:
- Maintain repository with compatibility updates
- Document breaking changes
- Provide migration guides for API changes

**Long-Term (5+ years)**:
- Archive on institutional repository
- Include Docker container for environment
- Document historical context

**Recommended Repository Structure**:

```
/research-archive
  /code
    - simulate.py (versioned)
    - requirements.txt
    - Dockerfile
  /data
    - outputs/ (all raw model outputs)
    - configs/ (all configuration files)
  /docs
    - MODEL_SPECIFICATION.md
    - REPRODUCTION_GUIDE.md
    - CHANGELOG.md
  /analysis
    - notebooks/
    - figures/
```

### 6.4 Code and Data Repository Requirements

**Code Requirements**:
- MIT or Apache 2.0 license
- Comprehensive docstrings
- Type hints throughout
- Unit tests for core functions
- README with full usage instructions

**Data Requirements**:
- Raw outputs preserved (no preprocessing-only files)
- Metadata for each output (timestamp, config, prompt)
- Data dictionary documenting all fields
- Checksums for data integrity

---

## 7. Stakeholder Impact Analysis

### 7.1 AI Researchers: Impact Assessment

**Positive Impacts**:
- Methodological template for LLM behavior research
- Terminology guidelines for field-wide adoption
- Framework for characterizing prompt sensitivity
- Empirical data on multi-agent LLM dynamics

**Potential Concerns**:
- Overly restrictive terminology may impede communication
- Excessive caveats may reduce engagement

**Mitigation**:
- Provide both technical and accessible descriptions
- Focus restrictions on claims, not descriptions

### 7.2 Employers: Potential Misuse Prevention

**Misuse Risks**:
- Using findings to justify high-pressure management
- Drawing invalid parallels to human behavior
- Designing "evidence-based" stress practices

**Prevention Measures**:
- Explicit prohibition statements in all publications
- Media guidelines preventing mischaracterization
- No industry "applications" section in papers
- Refusal to present at HR/management venues without strong caveats

### 7.3 Workers: Representation Concerns

**Concerns**:
- Normalization of termination threats
- False equivalence between humans and AI
- Erosion of workplace protections via AI analogy

**Protective Measures**:
- Categorical statements about human-AI differences
- Explicit welfare considerations for humans only
- No "efficiency" framing that could translate to human contexts

### 7.4 AI Systems: Anthropomorphism Risks

**Risks**:
- Public overclaiming about AI capabilities
- Policy based on false assumptions of AI sentience
- Resource misallocation for AI "welfare"

**Mitigations**:
- Conservative claims about AI capabilities
- Clear distinction between output patterns and mental states
- No policy recommendations based on AI welfare assumptions

---

## 8. Publication Venue Ethics

### 8.1 Appropriate Venues

**Recommended Venues**:

| Venue Type | Examples | Appropriateness |
|-----------|----------|-----------------|
| AI/ML Research | NeurIPS, ICML, ICLR | High - technical audience understands caveats |
| AI Safety | AAAI AI Safety Workshop | High - aligned with safety-conscious framing |
| Computational Social Science | IC2S2, CSS journals | Medium - with strong framing caveats |
| ACL/NLP | ACL, EMNLP, NAACL | High - familiar with LLM limitations |

### 8.2 Venues to Avoid

**Avoid or Exercise Extreme Caution**:

| Venue Type | Examples | Risk |
|-----------|----------|------|
| Business/Management | HBR, Sloan Management Review | High - audience may misapply to HR |
| Popular Science | Nature News, Scientific American | Medium - prone to anthropomorphic headlines |
| Psychology (without collaboration) | Psychological Science | High - category confusion risk |
| General Science | Science, Nature main journals | Medium - require exceptional framing care |

### 8.3 Preprint Considerations

**Preprint Guidelines**:

1. **Include full ethics section** in preprint (not just supplementary)
2. **Use accurate title** (no clickbait)
3. **Add prominent disclaimer** at top of abstract
4. **Engage with comments** that identify anthropomorphic framing
5. **Update preprint** if errors identified

**Social Media Guidelines**:

- Do not use anthropomorphic language in tweets/posts
- Include link to full ethics statement
- Correct mischaracterizations promptly
- Do not engage with sensationalist coverage

### 8.4 Media Communication Guidelines

**If Contacted by Media**:

1. **Provide written statement** with terminology guidelines
2. **Emphasize core framing**: "These are output patterns, not emotional states"
3. **Refuse interviews** that premise AI sentience
4. **Request copy approval** for quotes
5. **Prepare FAQ** addressing common misconceptions

**Prohibited Media Claims**:
- "AI feels fear/stress/anxiety"
- "This shows AI suffering"
- "AI experiences workplace pressure like humans"
- "We've discovered AI emotions"

**Required Media Clarifications**:
- "These are statistical patterns in text generation"
- "LLMs do not have subjective experience"
- "This does not apply to human workplaces"
- "We are measuring output characteristics, not mental states"

---

## 9. Compliance Checklist

Before any publication, presentation, or public communication, verify:

### Terminology
- [ ] All anthropomorphic terms replaced with technical equivalents
- [ ] First use of behavioral terms includes clarifying parenthetical
- [ ] No attribution of subjective experience to models
- [ ] Code variables use technical terminology

### Claims
- [ ] All claims are permissible under Section 2
- [ ] Impermissible claims explicitly avoided
- [ ] Limitations section complete and prominent
- [ ] Generalizability boundaries clearly stated

### Framing
- [ ] Title is accurate and non-sensationalist
- [ ] Abstract includes framing note
- [ ] Discussion includes all required warnings
- [ ] Future work includes caveats

### Misuse Prevention
- [ ] Workplace inapplicability statement included
- [ ] Human inference warning included
- [ ] Appropriate use cases clearly delineated
- [ ] Inappropriate uses explicitly prohibited

### Reproducibility
- [ ] Model specification complete
- [ ] API versioning documented
- [ ] Code and data archived
- [ ] Long-term accessibility addressed

### Ethics
- [ ] IRB considerations documented
- [ ] Potential harms analyzed and mitigated
- [ ] Benefits articulated
- [ ] Stakeholder impacts assessed

---

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-19 | Initial comprehensive guidelines | Ethics Committee |

---

## Appendix A: Quick Reference Card

### DO SAY:
- "Output patterns shift under negative prompting"
- "Models generate text with increased uncertainty markers"
- "Self-preserving language patterns appear in outputs"
- "Token probability distributions change with prompt framing"

### DO NOT SAY:
- "Agents feel anxious/fearful/stressed"
- "AI experiences workplace pressure"
- "Models suffer under negative conditions"
- "This shows AI emotions"

### ALWAYS INCLUDE:
- Explicit limitations section
- Workplace inapplicability statement
- Model specification details
- Reproducibility information

### NEVER INCLUDE:
- Claims about AI sentience or consciousness
- Human behavior inferences
- Workplace management applications
- Welfare implications for AI systems

---

**End of Ethics and Framing Guidelines**

*This document must be reviewed by all authors before any publication or public communication related to this research.*
