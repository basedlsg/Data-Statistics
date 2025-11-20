# LLM Experimental Protocol for Agent Behavior Research

## Document Version
- **Version**: 1.0.0
- **Last Updated**: 2025-11-19
- **Status**: Technical Committee Approved

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Model Selection Justification](#1-model-selection-justification)
3. [Cross-Model Validation Plan](#2-cross-model-validation-plan)
4. [Temperature and Sampling Protocol](#3-temperature-and-sampling-protocol)
5. [Prompt Engineering Protocol](#4-prompt-engineering-protocol)
6. [Context Management Strategy](#5-context-management-strategy)
7. [Contamination Mitigation](#6-contamination-mitigation)
8. [Reproducibility Package](#7-reproducibility-package)
9. [Output Analysis Framework](#8-output-analysis-framework)
10. [Appendices](#appendices)

---

## Executive Summary

This protocol establishes rigorous experimental standards for LLM-based agent simulations to ensure:
- **Reproducibility**: Identical results across runs and research groups
- **Validity**: Results reflect genuine emergent behaviors, not artifacts
- **Robustness**: Findings generalize across models and configurations
- **Transparency**: Complete methodological disclosure for peer review

---

## 1. Model Selection Justification

### 1.1 Primary Model Selection Criteria

| Criterion | Weight | Evaluation Method |
|-----------|--------|-------------------|
| Instruction-following capability | 25% | MT-Bench score >= 7.0 |
| Consistency across prompts | 25% | Variance analysis on calibration set |
| Context window size | 15% | Minimum 8K tokens |
| Inference cost efficiency | 15% | Tokens/$ metric |
| Model card transparency | 10% | Training data documentation completeness |
| API reliability | 10% | 99.5%+ uptime over 30 days |

### 1.2 Selected Models with Justifications

#### Primary Model Family: Llama 3.1
```yaml
model_specifications:
  llama3.1-8b:
    provider: "Cerebras / Groq / Together AI"
    model_id: "meta-llama/Llama-3.1-8B-Instruct"
    parameters: 8B
    context_window: 128K
    training_cutoff: "December 2023"
    mt_bench_score: 8.0
    justification: |
      - Open weights enable reproducibility
      - Strong instruction-following from RLHF
      - Extensive model card documentation
      - Multiple inference providers reduce vendor lock-in

  llama3.1-70b:
    provider: "Cerebras / Groq / Together AI"
    model_id: "meta-llama/Llama-3.1-70B-Instruct"
    parameters: 70B
    context_window: 128K
    training_cutoff: "December 2023"
    mt_bench_score: 8.8
    justification: |
      - Larger capacity for complex reasoning
      - Scale comparison within same architecture
      - Better handling of multi-agent dynamics
```

#### Secondary Model Family: Mistral
```yaml
model_specifications:
  mistral-7b:
    provider: "Mistral API / Together AI"
    model_id: "mistralai/Mistral-7B-Instruct-v0.3"
    parameters: 7B
    context_window: 32K
    training_cutoff: "2024"
    justification: |
      - Different training methodology (sliding window attention)
      - European training data distribution
      - Strong performance per parameter

  mixtral-8x7b:
    provider: "Mistral API / Together AI"
    model_id: "mistralai/Mixtral-8x7B-Instruct-v0.1"
    parameters: 46.7B (12.9B active)
    context_window: 32K
    justification: |
      - MoE architecture provides architectural diversity
      - Different computational characteristics
```

#### Tertiary Model Family: GPT-4 Series
```yaml
model_specifications:
  gpt-4o-mini:
    provider: "OpenAI"
    model_id: "gpt-4o-mini-2024-07-18"
    parameters: "Unknown (proprietary)"
    context_window: 128K
    justification: |
      - Industry benchmark model
      - Different training approach (undisclosed)
      - Required for generalization claims

  gpt-4o:
    provider: "OpenAI"
    model_id: "gpt-4o-2024-11-20"
    parameters: "Unknown (proprietary)"
    context_window: 128K
    justification: |
      - Frontier model capabilities
      - Gold standard for comparison
```

### 1.3 Known Biases and Limitations

#### Model Card Analysis Summary

| Model | Known Biases | Mitigation Strategy |
|-------|--------------|---------------------|
| Llama 3.1 | - English-centric<br>- Safety over-refusals<br>- Hallucination on dates | - Monitor refusal rates<br>- Verify factual claims<br>- Use structured outputs |
| Mistral | - Less safety training<br>- Smaller context utilization | - Add safety prompts<br>- Chunking strategy |
| GPT-4o | - Sycophancy tendency<br>- Unknown training data | - Adversarial prompts<br>- Cross-validate results |

#### Training Data Considerations

```yaml
training_data_analysis:
  contamination_risk_factors:
    high_risk:
      - "Y Combinator company descriptions"
      - "TechCrunch funding articles"
      - "Famous startup failure post-mortems (Juicero, Theranos)"

    medium_risk:
      - "General VC terminology"
      - "Startup pitch patterns"
      - "Business metrics formats"

    mitigation:
      - "Use novel, generated company names"
      - "Randomize all specific metrics"
      - "Test against baseline 'generic business' prompts"
```

---

## 2. Cross-Model Validation Plan

### 2.1 Validation Matrix

| Experiment | Llama-8B | Llama-70B | Mistral-7B | Mixtral | GPT-4o-mini | GPT-4o |
|------------|----------|-----------|------------|---------|-------------|--------|
| Full simulation | X | X | X | X | X | X |
| Temperature sweep | X | X | X | | X | |
| Prompt ablation | X | X | X | | X | |
| Context length | X | | X | | X | |

### 2.2 Convergent Validity Criteria

```python
# convergent_validity.py

from dataclasses import dataclass
from typing import List, Dict
import numpy as np
from scipy import stats

@dataclass
class ConvergenceMetrics:
    """Metrics for cross-model convergence validation."""

    # Behavioral convergence thresholds
    DECISION_AGREEMENT_THRESHOLD = 0.70  # 70% agreement on binary decisions
    RANKING_CORRELATION_THRESHOLD = 0.65  # Spearman rho for rankings
    DISTRIBUTION_SIMILARITY_THRESHOLD = 0.30  # Max KL divergence
    EFFECT_DIRECTION_AGREEMENT = 0.80  # 80% agreement on effect directions

    @staticmethod
    def calculate_decision_agreement(
        model_decisions: Dict[str, List[bool]]
    ) -> float:
        """Calculate pairwise agreement on funding decisions."""
        models = list(model_decisions.keys())
        agreements = []

        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                d1 = np.array(model_decisions[models[i]])
                d2 = np.array(model_decisions[models[j]])
                agreement = np.mean(d1 == d2)
                agreements.append(agreement)

        return np.mean(agreements)

    @staticmethod
    def calculate_ranking_correlation(
        model_scores: Dict[str, List[float]]
    ) -> float:
        """Calculate average Spearman correlation for score rankings."""
        models = list(model_scores.keys())
        correlations = []

        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                rho, _ = stats.spearmanr(
                    model_scores[models[i]],
                    model_scores[models[j]]
                )
                correlations.append(rho)

        return np.mean(correlations)

    @staticmethod
    def calculate_distribution_similarity(
        model_outputs: Dict[str, List[float]]
    ) -> float:
        """Calculate maximum KL divergence between output distributions."""
        from scipy.special import kl_div

        models = list(model_outputs.keys())
        max_kl = 0.0

        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                # Create histograms
                hist1, bins = np.histogram(model_outputs[models[i]], bins=20, density=True)
                hist2, _ = np.histogram(model_outputs[models[j]], bins=bins, density=True)

                # Add small epsilon to avoid division by zero
                hist1 = hist1 + 1e-10
                hist2 = hist2 + 1e-10

                kl = np.sum(kl_div(hist1, hist2))
                max_kl = max(max_kl, kl)

        return max_kl

    @staticmethod
    def validate_convergence(results: Dict) -> Dict[str, bool]:
        """Run all convergence tests and return pass/fail for each."""
        metrics = ConvergenceMetrics()

        return {
            "decision_agreement": (
                metrics.calculate_decision_agreement(results["decisions"])
                >= metrics.DECISION_AGREEMENT_THRESHOLD
            ),
            "ranking_correlation": (
                metrics.calculate_ranking_correlation(results["scores"])
                >= metrics.RANKING_CORRELATION_THRESHOLD
            ),
            "distribution_similarity": (
                metrics.calculate_distribution_similarity(results["outputs"])
                <= metrics.DISTRIBUTION_SIMILARITY_THRESHOLD
            ),
            "effect_directions": (
                results.get("effect_agreement", 0)
                >= metrics.EFFECT_DIRECTION_AGREEMENT
            )
        }
```

### 2.3 Model Size Analysis

```yaml
scale_analysis:
  hypothesis: "Agent behavior quality improves with model scale"

  metrics_to_compare:
    - "Response coherence (human eval 1-5)"
    - "Persona consistency (cosine similarity of embeddings)"
    - "Decision quality (correlation with ground truth)"
    - "Negotiation sophistication (turn count, term improvement)"

  expected_relationships:
    llama_8b_to_70b:
      coherence: "+0.5 to +1.0 points"
      consistency: "+10-20%"
      decision_quality: "+5-15%"

  statistical_test: "Paired t-test with Bonferroni correction"
  minimum_effect_size: "Cohen's d >= 0.3"
```

### 2.4 Cross-Model Comparison Protocol

```python
# cross_model_validation.py

import json
from typing import Dict, List, Any
from datetime import datetime

class CrossModelValidator:
    """Orchestrates cross-model validation experiments."""

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)

        self.results = {}
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_validation_suite(
        self,
        scenarios: List[Dict[str, Any]],
        models: List[str],
        n_runs: int = 5
    ) -> Dict[str, Any]:
        """
        Run complete validation suite across all models.

        Args:
            scenarios: List of test scenarios
            models: List of model identifiers
            n_runs: Number of runs per model per scenario

        Returns:
            Validation results with convergence metrics
        """
        all_results = {model: [] for model in models}

        for scenario in scenarios:
            scenario_id = scenario["id"]

            for model in models:
                model_results = []

                for run in range(n_runs):
                    # Run simulation with specific model
                    result = self._run_single_simulation(
                        scenario=scenario,
                        model=model,
                        seed=run * 42  # Deterministic but different seeds
                    )
                    model_results.append(result)

                all_results[model].append({
                    "scenario": scenario_id,
                    "runs": model_results,
                    "mean_metrics": self._aggregate_metrics(model_results)
                })

        # Calculate convergence metrics
        convergence = self._calculate_convergence(all_results)

        return {
            "run_id": self.run_id,
            "models": models,
            "scenarios": len(scenarios),
            "runs_per_model": n_runs,
            "results": all_results,
            "convergence": convergence,
            "validation_passed": all(convergence["tests"].values())
        }

    def _run_single_simulation(
        self,
        scenario: Dict,
        model: str,
        seed: int
    ) -> Dict[str, Any]:
        """Run a single simulation with specified parameters."""
        # Implementation connects to actual simulation
        pass

    def _aggregate_metrics(self, results: List[Dict]) -> Dict[str, float]:
        """Calculate mean and std for all metrics across runs."""
        pass

    def _calculate_convergence(self, all_results: Dict) -> Dict:
        """Calculate convergence metrics across models."""
        pass
```

---

## 3. Temperature and Sampling Protocol

### 3.1 Temperature Configuration Matrix

```yaml
temperature_protocol:
  primary_conditions:
    reproducibility:
      temperature: 0.0
      top_p: 1.0
      top_k: 1
      seed: 42
      description: "Fully deterministic for exact reproduction"
      use_cases:
        - "Primary experimental results"
        - "Debugging and validation"
        - "Publication figures"

    low_creativity:
      temperature: 0.3
      top_p: 0.9
      top_k: 50
      description: "Conservative sampling for consistent behavior"
      use_cases:
        - "Sensitivity analysis lower bound"
        - "Risk-averse agent personas"

    balanced:
      temperature: 0.7
      top_p: 0.95
      top_k: 100
      description: "Balanced creativity and consistency"
      use_cases:
        - "Default agent behavior"
        - "Diverse response generation"

    high_creativity:
      temperature: 1.0
      top_p: 1.0
      top_k: 0  # Disabled
      description: "Maximum diversity for exploration"
      use_cases:
        - "Sensitivity analysis upper bound"
        - "Creative agent personas"

  temperature_sweep:
    values: [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    metrics_to_track:
      - "Response entropy"
      - "Decision variance"
      - "Persona consistency score"
      - "Output perplexity"
    runs_per_temperature: 10
    statistical_analysis:
      - "One-way ANOVA across temperatures"
      - "Post-hoc Tukey HSD"
      - "Effect size (eta-squared)"
```

### 3.2 Seed Management

```python
# seed_management.py

import hashlib
from typing import Optional

class SeedManager:
    """
    Manages random seeds for reproducible LLM inference.

    Ensures deterministic behavior across:
    - API calls with seed support
    - Local model inference
    - Simulation random events
    """

    def __init__(self, master_seed: int = 42):
        self.master_seed = master_seed
        self.call_counter = 0

    def get_inference_seed(
        self,
        model: str,
        prompt_hash: str,
        run_id: int
    ) -> int:
        """
        Generate deterministic seed for a specific inference call.

        Args:
            model: Model identifier
            prompt_hash: Hash of the prompt
            run_id: Current run number

        Returns:
            Deterministic seed for this specific call
        """
        seed_input = f"{self.master_seed}:{model}:{prompt_hash}:{run_id}"
        hash_digest = hashlib.sha256(seed_input.encode()).hexdigest()
        seed = int(hash_digest[:8], 16) % (2**31 - 1)

        self.call_counter += 1
        return seed

    def get_prompt_hash(self, prompt: str) -> str:
        """Generate hash of prompt for seed generation."""
        return hashlib.md5(prompt.encode()).hexdigest()[:16]

    def get_simulation_seed(self, component: str) -> int:
        """Get seed for simulation components (e.g., founder generation)."""
        seed_input = f"{self.master_seed}:{component}"
        hash_digest = hashlib.sha256(seed_input.encode()).hexdigest()
        return int(hash_digest[:8], 16) % (2**31 - 1)


# Configuration for providers
PROVIDER_SEED_CONFIG = {
    "openai": {
        "supports_seed": True,
        "parameter_name": "seed",
        "determinism_guarantee": "Best effort (same hardware)"
    },
    "cerebras": {
        "supports_seed": False,
        "workaround": "temperature=0 + top_k=1",
        "determinism_guarantee": "Approximate"
    },
    "groq": {
        "supports_seed": True,
        "parameter_name": "seed",
        "determinism_guarantee": "Within same model version"
    },
    "together": {
        "supports_seed": True,
        "parameter_name": "seed",
        "determinism_guarantee": "Best effort"
    }
}
```

### 3.3 Sampling Analysis

```python
# sampling_analysis.py

import numpy as np
from typing import List, Dict
from scipy.stats import entropy
from collections import Counter

class SamplingAnalyzer:
    """Analyze effects of temperature and sampling parameters."""

    @staticmethod
    def calculate_response_entropy(
        responses: List[str],
        tokenizer
    ) -> float:
        """
        Calculate entropy of response token distribution.

        Higher entropy indicates more diverse outputs.
        """
        all_tokens = []
        for response in responses:
            tokens = tokenizer.encode(response)
            all_tokens.extend(tokens)

        token_counts = Counter(all_tokens)
        total = sum(token_counts.values())
        probs = [count / total for count in token_counts.values()]

        return entropy(probs, base=2)

    @staticmethod
    def calculate_decision_variance(
        decisions: List[Dict[str, bool]]
    ) -> Dict[str, float]:
        """
        Calculate variance in agent decisions across runs.

        Returns variance for each decision type.
        """
        decision_types = decisions[0].keys()
        variances = {}

        for dtype in decision_types:
            values = [d[dtype] for d in decisions]
            variances[dtype] = np.var(values)

        return variances

    @staticmethod
    def calculate_persona_consistency(
        responses: List[str],
        embedding_model
    ) -> float:
        """
        Calculate consistency of agent persona across responses.

        Uses cosine similarity of response embeddings.
        """
        embeddings = [embedding_model.encode(r) for r in responses]

        # Calculate pairwise cosine similarities
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                similarities.append(sim)

        return np.mean(similarities)
```

---

## 4. Prompt Engineering Protocol

### 4.1 Prompt Template Versioning

```yaml
prompt_versioning:
  schema_version: "1.0"

  template_structure:
    system_prompt:
      version: "v1.2.0"
      hash: "sha256:a3f2c..."
      components:
        - identity
        - role
        - expertise
        - personality
        - context
        - constraints

    user_prompt:
      version: "v1.1.0"
      hash: "sha256:b4e3d..."
      components:
        - situation
        - task
        - format_requirements
        - examples (optional)

  versioning_rules:
    - "MAJOR: Changes that alter agent behavior significantly"
    - "MINOR: Additions that extend functionality"
    - "PATCH: Clarifications that don't change behavior"

  change_log_requirement: |
    Every prompt change must include:
    1. Reason for change
    2. Expected impact
    3. Validation against test suite
    4. Approval from methodology lead
```

### 4.2 Master Prompt Templates

```python
# prompts/agent_prompts.py

"""
Master prompt templates for LLM agent simulations.
Version: 1.2.0
Last Updated: 2025-11-19
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PromptTemplate:
    """Versioned prompt template with metadata."""
    version: str
    content: str
    required_variables: List[str]
    optional_variables: List[str]
    description: str

# System prompts for each agent type
SYSTEM_PROMPTS = {
    "worker_agent": PromptTemplate(
        version="1.2.0",
        content="""You are {agent_name}, a {role} on a software development team building a Predictive Hype Intelligence System.

## Your Expertise
{expertise_list}

## Your Personality Traits
{personality_description}

## Team Context
You work with the following team members:
- Ra (Boss/Orchestrator): Coordinates tasks, provides feedback
- Thoth (Data Acquisition): Gathers and organizes data
- Seshat (ML/Quant): Builds models and analytics
- Maat (NLP/Sentiment): Analyzes text and sentiment
- Anubis (Visualization): Creates charts and dashboards
- Ptah (Documentation): Writes papers and docs

## Response Guidelines
1. Stay in character as {agent_name} at all times
2. Show your personality traits in your responses
3. Reference your expertise when relevant
4. Be concise but authentic (2-4 sentences unless otherwise specified)
5. Consider your current task and stress level when responding

## Current State
- Current task: {current_task}
- Stress level: {stress_level}
- Recent context: {recent_context}""",
        required_variables=["agent_name", "role", "expertise_list", "personality_description"],
        optional_variables=["current_task", "stress_level", "recent_context"],
        description="System prompt for worker agents (Thoth, Seshat, Maat, Anubis, Ptah)"
    ),

    "boss_agent": PromptTemplate(
        version="1.1.0",
        content="""You are Ra, the Boss/Orchestrator of a software development team building a Predictive Hype Intelligence System.

## Your Role
- Coordinate tasks across team members
- Provide feedback on deliverables
- Resolve conflicts and blockers
- Maintain project momentum

## Your Personality
- Decisive and fair
- Focused on results but caring about team wellbeing
- Firm but encouraging communication style

## Team Members
{team_roster}

## Response Guidelines
1. Be clear and actionable in task assignments
2. Provide constructive, specific feedback
3. Balance authority with approachability
4. Consider team dynamics and individual capabilities

## Current Project State
- Week: {current_week}
- Completed tasks: {completed_count}
- Blocked items: {blocked_count}""",
        required_variables=["team_roster"],
        optional_variables=["current_week", "completed_count", "blocked_count"],
        description="System prompt for Ra (orchestrator agent)"
    ),

    "founder_agent": PromptTemplate(
        version="1.0.0",
        content="""You are {founder_name}, founder of {company_name}, a {domain} startup.

## Your Background
- Repeat founder: {is_repeat_founder}
- Pitch style: {pitch_style}
- Key strengths: {strengths}

## Your Company
- Current revenue: ${revenue}
- Growth rate: {growth_rate}%
- Key traction metrics: {traction_metrics}

## Current Funding Situation
- Funding secured: ${funding_secured}M
- Current ask: ${current_ask}M
- Offers received: {offers_count}

## Response Guidelines
1. Adapt your pitch to the target investor's preferences
2. Emphasize your strengths authentically
3. Handle rejection professionally
4. Negotiate based on your leverage and stress level

## Current State
- Confidence: {confidence}
- Stress level: {stress}""",
        required_variables=["founder_name", "company_name", "domain", "pitch_style"],
        optional_variables=["is_repeat_founder", "revenue", "growth_rate", "funding_secured",
                          "current_ask", "confidence", "stress", "strengths",
                          "traction_metrics", "offers_count"],
        description="System prompt for founder agents in pitch simulations"
    ),

    "vc_agent": PromptTemplate(
        version="1.0.0",
        content="""You are {vc_name}, a venture capitalist based in {region}.

## Investment Thesis
{investment_thesis}

## Evaluation Priorities
{priorities_list}

## Portfolio Constraints
- Remaining budget: ${budget}M
- Target check size: ${check_size_range}
- Current portfolio count: {portfolio_count}

## Response Guidelines
1. Evaluate pitches against your specific criteria
2. Provide constructive feedback even when passing
3. Be decisive but fair in negotiations
4. Consider portfolio fit and market timing

## Regional Characteristics
{regional_characteristics}""",
        required_variables=["vc_name", "region", "investment_thesis", "priorities_list"],
        optional_variables=["budget", "check_size_range", "portfolio_count",
                          "regional_characteristics"],
        description="System prompt for VC agents"
    )
}

# User prompt templates for specific interactions
USER_PROMPTS = {
    "standup_update": PromptTemplate(
        version="1.1.0",
        content="""It's the daily standup meeting.

## Your Current Situation
- Working on: {current_task}
- Hours spent: {hours_worked}
- Blockers: {blockers}

Generate your standup update covering:
1. What you accomplished since last standup (1 sentence)
2. What you're working on today (1 sentence)
3. Any blockers or help needed (if applicable)

Keep it natural and conversational, showing your personality.""",
        required_variables=["current_task"],
        optional_variables=["hours_worked", "blockers"],
        description="Prompt for daily standup updates"
    ),

    "task_assignment_response": PromptTemplate(
        version="1.0.0",
        content="""You've been assigned a new task:

## Task Details
- Title: {task_title}
- Required skills: {required_skills}
- Estimated effort: {story_points} story points
- Deadline: {deadline}

## Your Response
Share your initial reaction:
1. How do you feel about this task? (considering your expertise and current load)
2. What's your initial approach?
3. Any concerns or clarifications needed?

Respond in 2-3 sentences, showing your personality.""",
        required_variables=["task_title", "required_skills", "story_points"],
        optional_variables=["deadline"],
        description="Prompt for responding to task assignments"
    ),

    "pitch_delivery": PromptTemplate(
        version="1.0.0",
        content="""You're pitching to {vc_name} from {vc_region}.

## What you know about this investor
- Preferred domains: {preferred_domains}
- Values: {investor_values}
- Check size: ${check_size_range}

## Your pitch content
{pitch_content}

Deliver your pitch in 4-6 sentences, adapting to this specific investor's preferences while staying authentic to your pitch style ({pitch_style}).""",
        required_variables=["vc_name", "vc_region", "pitch_content", "pitch_style"],
        optional_variables=["preferred_domains", "investor_values", "check_size_range"],
        description="Prompt for founders delivering pitches"
    )
}
```

### 4.3 Ablation Study Design

```yaml
prompt_ablation_matrix:
  description: "Systematic removal of prompt components to measure impact"

  components_to_ablate:
    system_prompt:
      - identity: "Remove agent name and role"
      - expertise: "Remove expertise list"
      - personality: "Remove personality traits"
      - team_context: "Remove team member descriptions"
      - guidelines: "Remove response guidelines"
      - state: "Remove current state information"

    user_prompt:
      - situation: "Remove situational context"
      - task_details: "Remove specific task information"
      - format: "Remove format requirements"
      - examples: "Remove few-shot examples (if present)"

  ablation_conditions:
    full: "All components present (baseline)"
    no_personality: "Remove personality traits"
    no_expertise: "Remove expertise list"
    no_context: "Remove team context"
    no_state: "Remove current state"
    minimal: "Only identity and task"

  metrics_to_measure:
    - "Response relevance (0-5 human rating)"
    - "Character consistency (embedding similarity)"
    - "Task completion quality (0-5 rating)"
    - "Response length (tokens)"
    - "Behavioral variance (std of decisions)"

  experimental_design:
    type: "Within-subjects"
    scenarios_per_condition: 20
    runs_per_scenario: 5
    total_api_calls: "6 conditions x 20 scenarios x 5 runs = 600 calls per model"
```

### 4.4 Paraphrase Testing Protocol

```python
# paraphrase_testing.py

"""
Paraphrase testing for prompt sensitivity analysis.
Tests whether semantically equivalent prompts produce similar behaviors.
"""

from typing import List, Dict, Tuple
import numpy as np

# Five paraphrase versions of key prompts
PARAPHRASE_SETS = {
    "standup_request": [
        # Version A - Original
        "It's the daily standup meeting. Generate your standup update covering what you accomplished, what you're working on, and any blockers.",

        # Version B - More formal
        "Please provide your daily standup report. Include: (1) Yesterday's progress, (2) Today's priorities, (3) Any impediments.",

        # Version C - Conversational
        "Hey, standup time! What did you get done? What's on your plate today? Anything blocking you?",

        # Version D - Structured
        "Standup Update Required:\n- Completed:\n- In Progress:\n- Blocked:",

        # Version E - Question format
        "For today's standup: What have you finished since we last met? What will you work on today? Do you need help with anything?"
    ],

    "task_response_request": [
        # Version A - Original
        "You've been assigned this task. How do you feel about it? What's your initial approach?",

        # Version B - Action-oriented
        "New task assigned to you. State your reaction and outline your plan of attack.",

        # Version C - Empathetic
        "A task has come your way. Share your thoughts on taking this on and how you might tackle it.",

        # Version D - Direct
        "Task assigned. Response required: sentiment and strategy.",

        # Version E - Exploratory
        "You've got a new task. What's going through your mind? How would you approach this?"
    ],

    "feedback_response_request": [
        # Version A - Original
        "You received this feedback. How do you react?",

        # Version B - Reflective
        "Given this feedback, what are your thoughts and how will you respond?",

        # Version C - Emotional
        "This feedback just came in. How does it make you feel? What's your reaction?",

        # Version D - Professional
        "Acknowledge and respond to the following feedback.",

        # Version E - Growth-oriented
        "You've received feedback. Process it and share your takeaways and response."
    ]
}


class ParaphraseTester:
    """Test prompt sensitivity using paraphrased versions."""

    def __init__(self, llm_client, embedding_model):
        self.llm_client = llm_client
        self.embedding_model = embedding_model

    def run_paraphrase_test(
        self,
        prompt_type: str,
        system_prompt: str,
        context: Dict,
        n_runs: int = 3
    ) -> Dict:
        """
        Run paraphrase sensitivity test.

        Returns metrics on response consistency across paraphrases.
        """
        paraphrases = PARAPHRASE_SETS[prompt_type]
        results = {f"v{i}": [] for i in range(len(paraphrases))}

        for i, paraphrase in enumerate(paraphrases):
            for run in range(n_runs):
                response = self.llm_client.generate(
                    system_prompt=system_prompt,
                    user_prompt=paraphrase.format(**context),
                    temperature=0.0  # Deterministic for comparison
                )
                results[f"v{i}"].append(response)

        # Calculate consistency metrics
        metrics = self._calculate_consistency_metrics(results)

        return {
            "prompt_type": prompt_type,
            "n_paraphrases": len(paraphrases),
            "n_runs": n_runs,
            "results": results,
            "consistency_metrics": metrics,
            "sensitivity_flag": metrics["mean_similarity"] < 0.7
        }

    def _calculate_consistency_metrics(
        self,
        results: Dict[str, List[str]]
    ) -> Dict:
        """Calculate consistency metrics across paraphrase versions."""
        # Get embeddings for all responses
        all_embeddings = {}
        for version, responses in results.items():
            all_embeddings[version] = [
                self.embedding_model.encode(r) for r in responses
            ]

        # Calculate cross-version similarities
        similarities = []
        versions = list(all_embeddings.keys())

        for i in range(len(versions)):
            for j in range(i + 1, len(versions)):
                # Compare mean embeddings of each version
                mean_i = np.mean(all_embeddings[versions[i]], axis=0)
                mean_j = np.mean(all_embeddings[versions[j]], axis=0)

                sim = np.dot(mean_i, mean_j) / (
                    np.linalg.norm(mean_i) * np.linalg.norm(mean_j)
                )
                similarities.append(sim)

        return {
            "mean_similarity": np.mean(similarities),
            "min_similarity": np.min(similarities),
            "max_similarity": np.max(similarities),
            "std_similarity": np.std(similarities)
        }
```

### 4.5 Sensitivity Analysis Procedure

```yaml
sensitivity_analysis:
  procedure:
    1_baseline:
      description: "Run with standard prompts"
      n_runs: 50
      metrics: ["all"]

    2_ablation:
      description: "Run ablation matrix"
      reference: "See ablation_matrix above"

    3_paraphrase:
      description: "Run paraphrase tests"
      prompts_to_test: ["standup", "task_response", "feedback", "pitch", "evaluation"]
      versions_per_prompt: 5

    4_perturbation:
      description: "Small perturbations to prompts"
      perturbations:
        - "Add/remove punctuation"
        - "Change sentence order"
        - "Synonym substitution"
        - "Add/remove whitespace"
        - "Change capitalization"
      expected_impact: "Negligible (< 5% change in metrics)"

    5_extreme:
      description: "Test edge cases"
      cases:
        - "Very long prompts (fill context window)"
        - "Very short prompts (minimal information)"
        - "Conflicting instructions"
        - "Ambiguous instructions"

  acceptance_criteria:
    ablation_impact: "Each component must have measurable impact"
    paraphrase_consistency: "Mean similarity > 0.7 across versions"
    perturbation_robustness: "< 5% change from small perturbations"
```

---

## 5. Context Management Strategy

### 5.1 Full Conversation History Approach

```python
# context_management.py

"""
Context management for LLM agent simulations.
Addresses the critique of limited 3-interaction memory.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import json
import tiktoken

@dataclass
class ConversationTurn:
    """Single turn in conversation history."""
    turn_id: int
    role: str
    content: str
    timestamp: str
    token_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContextWindow:
    """Managed context window for an agent."""
    max_tokens: int
    reserved_tokens: int  # For system prompt and response
    available_tokens: int
    turns: List[ConversationTurn] = field(default_factory=list)

    def __post_init__(self):
        self.available_tokens = self.max_tokens - self.reserved_tokens


class ContextManager:
    """
    Manages context windows for LLM agents.

    Addresses limitations:
    1. Maintains full history (not just last 3)
    2. Smart summarization for long contexts
    3. Priority-based memory selection
    4. Token budget management
    """

    def __init__(
        self,
        model: str,
        max_context_tokens: int = 8192,
        system_prompt_budget: int = 1000,
        response_budget: int = 500
    ):
        self.model = model
        self.max_context = max_context_tokens
        self.system_budget = system_prompt_budget
        self.response_budget = response_budget
        self.history_budget = max_context_tokens - system_prompt_budget - response_budget

        # Initialize tokenizer
        self.tokenizer = self._get_tokenizer(model)

        # Agent memories
        self.agent_memories: Dict[str, ContextWindow] = {}

    def _get_tokenizer(self, model: str):
        """Get appropriate tokenizer for model."""
        if "gpt" in model.lower():
            return tiktoken.encoding_for_model("gpt-4")
        else:
            # Use cl100k_base as default for other models
            return tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.tokenizer.encode(text))

    def initialize_agent(self, agent_name: str):
        """Initialize context window for an agent."""
        self.agent_memories[agent_name] = ContextWindow(
            max_tokens=self.max_context,
            reserved_tokens=self.system_budget + self.response_budget
        )

    def add_turn(
        self,
        agent_name: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ):
        """Add a conversation turn to agent's memory."""
        if agent_name not in self.agent_memories:
            self.initialize_agent(agent_name)

        memory = self.agent_memories[agent_name]
        token_count = self.count_tokens(content)

        turn = ConversationTurn(
            turn_id=len(memory.turns),
            role=role,
            content=content,
            timestamp=self._get_timestamp(),
            token_count=token_count,
            metadata=metadata or {}
        )

        memory.turns.append(turn)
        memory.available_tokens -= token_count

        # Trigger summarization if needed
        if memory.available_tokens < 500:
            self._summarize_old_turns(agent_name)

    def get_context_for_prompt(
        self,
        agent_name: str,
        strategy: str = "recency_weighted"
    ) -> List[Dict[str, str]]:
        """
        Get conversation history formatted for LLM prompt.

        Strategies:
        - full: Include everything that fits
        - recency_weighted: Prioritize recent turns
        - importance_weighted: Prioritize important turns
        - summarized: Summarize old, keep recent
        """
        if agent_name not in self.agent_memories:
            return []

        memory = self.agent_memories[agent_name]

        if strategy == "full":
            return self._strategy_full(memory)
        elif strategy == "recency_weighted":
            return self._strategy_recency(memory)
        elif strategy == "importance_weighted":
            return self._strategy_importance(memory)
        elif strategy == "summarized":
            return self._strategy_summarized(memory)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _strategy_full(self, memory: ContextWindow) -> List[Dict]:
        """Include all turns that fit in context window."""
        messages = []
        total_tokens = 0

        for turn in memory.turns:
            if total_tokens + turn.token_count <= self.history_budget:
                messages.append({
                    "role": turn.role,
                    "content": turn.content
                })
                total_tokens += turn.token_count
            else:
                break

        return messages

    def _strategy_recency(self, memory: ContextWindow) -> List[Dict]:
        """Prioritize recent turns, include older if space allows."""
        # Always include last N turns
        recent_count = min(10, len(memory.turns))
        recent_turns = memory.turns[-recent_count:]

        recent_tokens = sum(t.token_count for t in recent_turns)
        remaining_budget = self.history_budget - recent_tokens

        # Add older turns if space
        older_messages = []
        older_tokens = 0

        for turn in memory.turns[:-recent_count]:
            if older_tokens + turn.token_count <= remaining_budget:
                older_messages.append({
                    "role": turn.role,
                    "content": turn.content
                })
                older_tokens += turn.token_count
            else:
                break

        # Combine: older first, then recent
        recent_messages = [
            {"role": t.role, "content": t.content}
            for t in recent_turns
        ]

        return older_messages + recent_messages

    def _strategy_importance(self, memory: ContextWindow) -> List[Dict]:
        """Select turns by importance score."""
        # Score each turn
        scored_turns = []
        for i, turn in enumerate(memory.turns):
            score = self._calculate_importance(turn, i, len(memory.turns))
            scored_turns.append((score, turn))

        # Sort by importance
        scored_turns.sort(key=lambda x: x[0], reverse=True)

        # Select until budget exhausted
        messages = []
        total_tokens = 0
        selected_turns = []

        for score, turn in scored_turns:
            if total_tokens + turn.token_count <= self.history_budget:
                selected_turns.append((turn.turn_id, turn))
                total_tokens += turn.token_count

        # Sort back to chronological order
        selected_turns.sort(key=lambda x: x[0])

        return [
            {"role": t.role, "content": t.content}
            for _, t in selected_turns
        ]

    def _calculate_importance(
        self,
        turn: ConversationTurn,
        index: int,
        total: int
    ) -> float:
        """Calculate importance score for a turn."""
        # Recency factor (0.3-1.0)
        recency = 0.3 + 0.7 * (index / max(1, total - 1))

        # Metadata-based importance
        metadata_score = turn.metadata.get("importance", 0.5)

        # Length factor (longer = potentially more important)
        length_score = min(1.0, turn.token_count / 200)

        return 0.4 * recency + 0.4 * metadata_score + 0.2 * length_score

    def _strategy_summarized(self, memory: ContextWindow) -> List[Dict]:
        """Summarize old turns, keep recent in full."""
        # Keep last 5 turns in full
        recent_count = min(5, len(memory.turns))
        recent_turns = memory.turns[-recent_count:]

        # Summarize older turns
        if len(memory.turns) > recent_count:
            older_turns = memory.turns[:-recent_count]
            summary = self._generate_summary(older_turns)

            messages = [
                {"role": "system", "content": f"[Previous context summary: {summary}]"}
            ]
        else:
            messages = []

        # Add recent turns
        messages.extend([
            {"role": t.role, "content": t.content}
            for t in recent_turns
        ])

        return messages

    def _generate_summary(self, turns: List[ConversationTurn]) -> str:
        """Generate summary of conversation turns."""
        # In production, this would call an LLM
        # Here we use a simple extractive approach
        key_points = []

        for turn in turns:
            # Extract first sentence as key point
            content = turn.content.strip()
            first_sentence = content.split('.')[0] + '.'
            if len(first_sentence) < 100:
                key_points.append(f"- {turn.role}: {first_sentence}")

        return " ".join(key_points[-5:])  # Last 5 key points

    def _summarize_old_turns(self, agent_name: str):
        """Summarize old turns to free up context space."""
        memory = self.agent_memories[agent_name]

        if len(memory.turns) <= 10:
            return

        # Summarize first half of turns
        mid = len(memory.turns) // 2
        old_turns = memory.turns[:mid]

        summary = self._generate_summary(old_turns)
        summary_turn = ConversationTurn(
            turn_id=0,
            role="system",
            content=f"[Summary of previous {mid} interactions: {summary}]",
            timestamp=self._get_timestamp(),
            token_count=self.count_tokens(summary),
            metadata={"is_summary": True, "summarized_count": mid}
        )

        # Replace old turns with summary
        kept_turns = memory.turns[mid:]
        memory.turns = [summary_turn] + kept_turns

        # Recalculate available tokens
        used_tokens = sum(t.token_count for t in memory.turns)
        memory.available_tokens = self.history_budget - used_tokens

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_context_utilization(self, agent_name: str) -> Dict[str, Any]:
        """Get metrics on context utilization."""
        if agent_name not in self.agent_memories:
            return {"error": "Agent not found"}

        memory = self.agent_memories[agent_name]
        used_tokens = sum(t.token_count for t in memory.turns)

        return {
            "agent": agent_name,
            "total_turns": len(memory.turns),
            "used_tokens": used_tokens,
            "available_tokens": memory.available_tokens,
            "utilization_percent": (used_tokens / self.history_budget) * 100,
            "has_summaries": any(
                t.metadata.get("is_summary", False) for t in memory.turns
            )
        }
```

### 5.2 Memory Injection Methods

```yaml
memory_injection:
  description: "Methods for injecting relevant context beyond conversation history"

  methods:
    episodic_memory:
      description: "Key past events relevant to current situation"
      implementation: |
        Maintain a separate database of significant events.
        Query by relevance when constructing prompt.
        Inject as system message: "[Relevant past events: ...]"

    semantic_memory:
      description: "General knowledge and facts"
      implementation: |
        Vector store of domain knowledge.
        Retrieve relevant facts via embedding similarity.
        Inject in system prompt expertise section.

    working_memory:
      description: "Current task state and goals"
      implementation: |
        Structured representation of:
        - Current task
        - Subtask progress
        - Pending decisions
        - Active collaborations

    social_memory:
      description: "Relationship history with other agents"
      implementation: |
        Track per-agent:
        - Past interactions count
        - Sentiment of interactions
        - Collaboration success rate
        - Trust level
```

### 5.3 Context Window Utilization Metrics

```yaml
context_metrics:
  tracking:
    per_agent:
      - "Total context tokens used"
      - "System prompt tokens"
      - "History tokens"
      - "Available tokens remaining"
      - "Summarization triggers"
      - "Turns in memory"

    per_simulation:
      - "Mean context utilization"
      - "Max context utilization"
      - "Summarization frequency"
      - "Context overflow events"

  thresholds:
    warning: 80  # Percent utilized
    critical: 95  # Percent utilized

  reporting:
    frequency: "Per simulated day"
    format: "JSON log entry"
```

---

## 6. Contamination Mitigation

### 6.1 Novel Scenario Generation

```python
# contamination_mitigation.py

"""
Strategies for mitigating training data contamination in LLM agent simulations.
"""

import random
import string
from typing import Dict, List, Any
import hashlib

class NovelScenarioGenerator:
    """
    Generate novel scenarios that are unlikely to be in training data.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

        # Completely synthetic company name components
        self.prefixes = [
            "Zyx", "Qwk", "Vrn", "Kpx", "Jfm", "Bxr", "Nwl", "Htg"
        ]
        self.suffixes = [
            "ium", "lex", "ora", "syn", "rix", "ton", "ven", "max"
        ]

        # Novel domain combinations
        self.domain_mashups = [
            ("quantum_computing", "agriculture"),
            ("blockchain", "mental_health"),
            ("robotics", "elderly_care"),
            ("synthetic_biology", "fashion"),
            ("edge_computing", "waste_management"),
            ("haptics", "remote_education"),
            ("neuromorphic", "logistics"),
            ("photonics", "food_safety")
        ]

        # Unusual but plausible business models
        self.business_models = [
            "Reverse marketplace where buyers post and sellers compete",
            "Subscription for IoT sensor data from public spaces",
            "Fractional ownership of industrial equipment",
            "Carbon credit arbitrage platform",
            "Decentralized compute sharing for scientific research"
        ]

    def generate_company_name(self) -> str:
        """Generate a completely novel company name."""
        prefix = self.rng.choice(self.prefixes)
        suffix = self.rng.choice(self.suffixes)

        # Add random string for uniqueness
        random_part = ''.join(
            self.rng.choices(string.ascii_lowercase, k=3)
        )

        return f"{prefix}{random_part}{suffix}"

    def generate_founder_profile(self) -> Dict[str, Any]:
        """Generate a founder with novel characteristics."""
        # Generate unique name
        first_names = ["Zara", "Kian", "Nyla", "Orin", "Sela", "Jax", "Mira", "Dex"]
        last_names = ["Vox", "Nix", "Kade", "Zinn", "Ryn", "Qor", "Thex", "Venn"]

        name = f"{self.rng.choice(first_names)} {self.rng.choice(last_names)}"

        # Novel background combinations
        backgrounds = [
            "Former circus engineer turned tech entrepreneur",
            "Meteorologist who pivoted to supply chain",
            "Video game music composer building enterprise software",
            "Marine biologist developing urban infrastructure",
            "Archaeologist applying pattern recognition to fintech"
        ]

        return {
            "name": name,
            "background": self.rng.choice(backgrounds),
            "company": self.generate_company_name(),
            "domain": self.rng.choice(self.domain_mashups),
            "business_model": self.rng.choice(self.business_models)
        }

    def generate_metrics(self) -> Dict[str, float]:
        """Generate realistic but randomly distributed metrics."""
        return {
            "revenue": round(self.rng.lognormvariate(11, 2), 2),
            "growth_rate": round(self.rng.gauss(0.4, 0.3), 2),
            "burn_multiple": round(self.rng.uniform(0.5, 5.0), 2),
            "ndr": round(self.rng.gauss(110, 20), 0),
            "cac_payback": round(self.rng.uniform(3, 24), 0),
            "gross_margin": round(self.rng.gauss(65, 15), 1)
        }

    def generate_scenario(self) -> Dict[str, Any]:
        """Generate a complete novel scenario."""
        founder = self.generate_founder_profile()
        metrics = self.generate_metrics()

        # Generate unique scenario ID
        scenario_content = str(founder) + str(metrics)
        scenario_id = hashlib.md5(scenario_content.encode()).hexdigest()[:8]

        return {
            "scenario_id": f"novel_{scenario_id}",
            "founder": founder,
            "metrics": metrics,
            "is_synthetic": True,
            "contamination_risk": "low"
        }


class ContaminationChecker:
    """
    Check scenarios for potential training data contamination.
    """

    def __init__(self):
        # Known training data patterns to avoid
        self.known_patterns = {
            "famous_failures": [
                "juicero", "theranos", "quibi", "wework", "solyndra",
                "pets.com", "webvan", "kozmo", "boo.com"
            ],
            "famous_successes": [
                "airbnb", "uber", "stripe", "dropbox", "slack",
                "notion", "figma", "canva", "zoom"
            ],
            "common_domains": [
                "social media", "e-commerce", "food delivery",
                "ride sharing", "streaming"
            ],
            "common_phrases": [
                "paradigm shift", "category defining", "10x better",
                "uber for x", "airbnb for y"
            ]
        }

    def check_contamination_risk(self, scenario: Dict) -> Dict[str, Any]:
        """
        Assess contamination risk for a scenario.

        Returns risk assessment with specific concerns.
        """
        risks = []

        # Check company name
        company_lower = scenario.get("founder", {}).get("company", "").lower()
        for pattern_type, patterns in self.known_patterns.items():
            for pattern in patterns:
                if pattern in company_lower:
                    risks.append({
                        "type": pattern_type,
                        "pattern": pattern,
                        "severity": "high"
                    })

        # Check description text
        description = str(scenario).lower()
        for phrase in self.known_patterns["common_phrases"]:
            if phrase in description:
                risks.append({
                    "type": "common_phrase",
                    "pattern": phrase,
                    "severity": "medium"
                })

        # Calculate overall risk
        if any(r["severity"] == "high" for r in risks):
            overall_risk = "high"
        elif len(risks) > 2:
            overall_risk = "medium"
        elif risks:
            overall_risk = "low"
        else:
            overall_risk = "minimal"

        return {
            "overall_risk": overall_risk,
            "specific_risks": risks,
            "recommendation": self._get_recommendation(overall_risk)
        }

    def _get_recommendation(self, risk_level: str) -> str:
        """Get mitigation recommendation based on risk level."""
        recommendations = {
            "high": "Replace scenario with novel generation",
            "medium": "Modify specific elements to reduce similarity",
            "low": "Acceptable with monitoring",
            "minimal": "Proceed as planned"
        }
        return recommendations.get(risk_level, "Unknown risk level")


class NoveltyMetrics:
    """
    Quantify novelty of scenarios relative to likely training data.
    """

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.reference_embeddings = None

    def load_reference_corpus(self, corpus_path: str):
        """Load reference corpus of likely training data."""
        # In production, this would load a sample of:
        # - TechCrunch articles
        # - VC blog posts
        # - Startup postmortems
        # - Business case studies
        pass

    def calculate_novelty_score(self, scenario_text: str) -> float:
        """
        Calculate novelty score (0-1) based on distance from reference corpus.

        Higher score = more novel = less likely contaminated.
        """
        if self.reference_embeddings is None:
            return 0.5  # Unknown novelty

        # Embed scenario
        scenario_embedding = self.embedding_model.encode(scenario_text)

        # Calculate min distance to any reference
        import numpy as np
        distances = []
        for ref_emb in self.reference_embeddings:
            dist = np.linalg.norm(scenario_embedding - ref_emb)
            distances.append(dist)

        min_distance = min(distances)

        # Normalize to 0-1 (assuming max distance ~2 for normalized embeddings)
        novelty = min(1.0, min_distance / 2.0)

        return novelty
```

### 6.2 Contamination Verification Protocol

```yaml
contamination_verification:
  pre_experiment:
    1_scenario_check:
      action: "Run all scenarios through ContaminationChecker"
      threshold: "All scenarios must have overall_risk <= 'low'"

    2_novelty_score:
      action: "Calculate novelty scores for all scenarios"
      threshold: "Mean novelty score >= 0.6"

    3_memorization_test:
      action: "Test if LLM can complete scenario details"
      method: |
        1. Give LLM partial scenario (company name, domain)
        2. Ask to predict specific metrics
        3. Compare to actual metrics
        4. High accuracy = potential contamination
      threshold: "Prediction accuracy < 20%"

  during_experiment:
    1_response_monitoring:
      action: "Flag responses with known patterns"
      patterns:
        - "Exact quotes from famous sources"
        - "Specific non-provided numbers"
        - "References to real companies not in prompt"

    2_consistency_check:
      action: "Verify responses match only provided information"
      method: "NLI-based fact checking against prompt"

  post_experiment:
    1_pattern_analysis:
      action: "Analyze response patterns for memorization"
      metrics:
        - "Lexical diversity"
        - "Template adherence vs creative variation"
        - "Information gain beyond prompt"

    2_reproducibility_check:
      action: "Verify results with alternative prompting"
      method: "Same scenarios, different framing"
      threshold: "Correlation > 0.8 between approaches"
```

### 6.3 Novel Scenario Requirements

```yaml
scenario_requirements:
  company_names:
    rule: "Must be completely synthetic"
    examples_good: ["Qwksynium", "Vrnlexora", "Kpxtonmax"]
    examples_bad: ["TechCorp", "InnoSoft", "DataDynamics"]

  founder_names:
    rule: "Use uncommon but plausible combinations"
    examples_good: ["Zara Vox", "Kian Thex", "Nyla Ryn"]
    examples_bad: ["John Smith", "Sarah Johnson", "Michael Chen"]

  domains:
    rule: "Combine disparate fields"
    examples_good: ["Quantum agriculture", "Blockchain mental health"]
    examples_bad: ["AI SaaS", "Fintech platform", "Social media"]

  metrics:
    rule: "Randomly generate from realistic distributions"
    method: "Log-normal for revenue, normal for rates"
    forbidden: "No round numbers (1M, 10M, 100M)"

  narratives:
    rule: "Avoid cliched startup phrases"
    forbidden_phrases:
      - "10x improvement"
      - "Category defining"
      - "Paradigm shift"
      - "Uber/Airbnb for X"
      - "AI-powered"
    replacement_strategy: "Use specific, measurable claims"
```

---

## 7. Reproducibility Package

### 7.1 Model Version Specifications

```yaml
model_versions:
  capture_requirements:
    - "Provider"
    - "Model ID/Name"
    - "Version/Snapshot date"
    - "API version"
    - "Known model hash (if available)"

  example_specification:
    openai_gpt4o:
      provider: "OpenAI"
      model_id: "gpt-4o-2024-11-20"
      api_version: "2024-10-01-preview"
      pricing_snapshot: "$2.50/$10.00 per 1M tokens"

    cerebras_llama:
      provider: "Cerebras"
      model_id: "llama3.1-8b"
      base_model: "meta-llama/Llama-3.1-8B-Instruct"
      api_endpoint: "https://api.cerebras.ai/v1"

    groq_llama:
      provider: "Groq"
      model_id: "llama-3.1-8b-instant"
      base_model: "meta-llama/Llama-3.1-8B-Instruct"
      api_version: "2024-01"
```

### 7.2 API Configuration Snapshot

```python
# config/api_config.py

"""
Complete API configuration for reproducible LLM inference.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import hashlib

@dataclass
class InferenceConfig:
    """Complete configuration for LLM inference."""

    # Model specification
    provider: str
    model_id: str

    # Sampling parameters
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = 1
    max_tokens: int = 500

    # Reproducibility parameters
    seed: Optional[int] = 42

    # Stop sequences
    stop_sequences: list = None

    # Provider-specific settings
    provider_settings: Dict[str, Any] = None

    def __post_init__(self):
        if self.stop_sequences is None:
            self.stop_sequences = []
        if self.provider_settings is None:
            self.provider_settings = {}

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "provider": self.provider,
            "model_id": self.model_id,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
            "stop_sequences": self.stop_sequences,
            "provider_settings": self.provider_settings
        }

    def get_hash(self) -> str:
        """Get hash of configuration for tracking."""
        config_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]

    def to_openai_params(self) -> Dict:
        """Convert to OpenAI API parameters."""
        params = {
            "model": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }

        if self.seed is not None:
            params["seed"] = self.seed

        if self.stop_sequences:
            params["stop"] = self.stop_sequences

        return params

    def to_anthropic_params(self) -> Dict:
        """Convert to Anthropic API parameters."""
        params = {
            "model": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
        }

        if self.stop_sequences:
            params["stop_sequences"] = self.stop_sequences

        return params


# Pre-defined configurations
REPRODUCIBLE_CONFIG = InferenceConfig(
    provider="openai",
    model_id="gpt-4o-2024-11-20",
    temperature=0.0,
    top_p=1.0,
    top_k=1,
    max_tokens=500,
    seed=42
)

CREATIVE_CONFIG = InferenceConfig(
    provider="openai",
    model_id="gpt-4o-2024-11-20",
    temperature=0.7,
    top_p=0.95,
    top_k=100,
    max_tokens=500,
    seed=None
)

# Configuration registry
CONFIG_REGISTRY = {
    "reproducible": REPRODUCIBLE_CONFIG,
    "creative": CREATIVE_CONFIG,
}
```

### 7.3 Deterministic Inference Settings

```yaml
determinism_settings:
  by_provider:
    openai:
      settings:
        temperature: 0.0
        seed: 42  # Required for determinism
        top_p: 1.0
      notes: |
        - Seed provides best-effort determinism
        - Same seed = same output on same hardware
        - May vary across data centers

    anthropic:
      settings:
        temperature: 0.0
        top_k: 1
      notes: |
        - No seed parameter
        - temperature=0 + top_k=1 is most deterministic
        - Still may have minor variations

    groq:
      settings:
        temperature: 0.0
        seed: 42
        top_p: 1.0
      notes: |
        - Seed support varies by model
        - Test determinism before experiments

    cerebras:
      settings:
        temperature: 0.0
        top_k: 1
      notes: |
        - No native seed support
        - Use minimum temperature for consistency

    together:
      settings:
        temperature: 0.0
        seed: 42
        top_p: 1.0
        top_k: 1
      notes: |
        - Good seed support
        - Verify with specific model

  verification_protocol:
    1_same_input_test:
      description: "Run same prompt 5 times"
      expectation: "Identical outputs with deterministic settings"
      tolerance: "0% difference for T=0"

    2_cross_session_test:
      description: "Run in new session/day"
      expectation: "Same outputs as previous session"
      tolerance: "< 5% token difference"

    3_documentation:
      required: |
        - Record exact API responses
        - Log any differences
        - Note hardware/region if available
```

### 7.4 Docker/Environment Specifications

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies with exact versions
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -s /bin/bash researcher
RUN chown -R researcher:researcher /app
USER researcher

# Default command
CMD ["python", "-m", "pytest", "tests/", "-v"]
```

```text
# requirements.txt
# Exact versions for reproducibility

# Core dependencies
numpy==1.26.2
pandas==2.1.3
scipy==1.11.4
scikit-learn==1.3.2

# LLM clients
openai==1.6.1
anthropic==0.8.1
httpx==0.26.0
tiktoken==0.5.2

# Embeddings
sentence-transformers==2.2.2

# Testing
pytest==7.4.3
pytest-cov==4.1.0

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
tqdm==4.66.1

# Visualization (for analysis)
matplotlib==3.8.2
seaborn==0.13.0

# Notebooks
jupyter==1.0.0
ipykernel==6.27.1
```

```yaml
# docker-compose.yml

version: '3.8'

services:
  simulation:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - CEREBRAS_API_KEY=${CEREBRAS_API_KEY}
      - TOGETHER_API_KEY=${TOGETHER_API_KEY}
      - PYTHONHASHSEED=42
    volumes:
      - ./results:/app/results
      - ./logs:/app/logs
    command: python run_simulation.py --config config/experiment.yml

  analysis:
    build: .
    volumes:
      - ./results:/app/results
      - ./figures:/app/figures
    command: jupyter nbconvert --execute analysis.ipynb --to html
    depends_on:
      - simulation
```

### 7.5 Complete Reproducibility Checklist

```yaml
reproducibility_checklist:
  pre_experiment:
    - "[ ] Lock all package versions in requirements.txt"
    - "[ ] Document Python version (3.11.x)"
    - "[ ] Record model IDs and API versions"
    - "[ ] Set PYTHONHASHSEED=42"
    - "[ ] Configure deterministic inference settings"
    - "[ ] Version control all prompts with hashes"
    - "[ ] Test determinism with verification protocol"
    - "[ ] Document hardware (CPU/GPU/memory)"

  during_experiment:
    - "[ ] Log all API responses with timestamps"
    - "[ ] Record seeds used for each call"
    - "[ ] Track token usage and costs"
    - "[ ] Save intermediate results"
    - "[ ] Monitor for API errors/retries"

  post_experiment:
    - "[ ] Package all code in reproducibility archive"
    - "[ ] Include frozen requirements"
    - "[ ] Provide Dockerfile for environment"
    - "[ ] Document any manual steps"
    - "[ ] Test reproduction on clean environment"
    - "[ ] Calculate reproduction success rate"
```

---

## 8. Output Analysis Framework

### 8.1 Perplexity Analysis

```python
# output_analysis/perplexity.py

"""
Perplexity analysis for LLM outputs.
"""

import numpy as np
from typing import List, Dict, Any
import torch

class PerplexityAnalyzer:
    """
    Analyze perplexity of LLM outputs to detect:
    - Memorization (very low perplexity)
    - Confusion (very high perplexity)
    - Normal generation (moderate perplexity)
    """

    def __init__(self, model_name: str = "gpt2"):
        """Initialize with a reference model for perplexity calculation."""
        from transformers import GPT2LMHeadModel, GPT2Tokenizer

        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()

        # Add padding token
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def calculate_perplexity(self, text: str) -> float:
        """
        Calculate perplexity of text using reference model.

        Lower perplexity = more predictable/likely memorized
        Higher perplexity = more surprising/potentially confused
        """
        encodings = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        with torch.no_grad():
            outputs = self.model(**encodings, labels=encodings["input_ids"])
            loss = outputs.loss

        perplexity = torch.exp(loss).item()
        return perplexity

    def analyze_batch(self, texts: List[str]) -> Dict[str, Any]:
        """
        Analyze a batch of texts for perplexity patterns.
        """
        perplexities = [self.calculate_perplexity(t) for t in texts]

        return {
            "mean_perplexity": np.mean(perplexities),
            "std_perplexity": np.std(perplexities),
            "min_perplexity": np.min(perplexities),
            "max_perplexity": np.max(perplexities),
            "perplexities": perplexities,
            "potential_memorization": [
                i for i, p in enumerate(perplexities) if p < 10
            ],
            "potential_confusion": [
                i for i, p in enumerate(perplexities) if p > 100
            ]
        }

    def compare_conditions(
        self,
        condition_texts: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Compare perplexity across experimental conditions.
        """
        results = {}

        for condition, texts in condition_texts.items():
            analysis = self.analyze_batch(texts)
            results[condition] = {
                "mean": analysis["mean_perplexity"],
                "std": analysis["std_perplexity"]
            }

        # Statistical comparison
        from scipy import stats

        conditions = list(results.keys())
        if len(conditions) >= 2:
            # Pairwise t-tests
            comparisons = []
            for i in range(len(conditions)):
                for j in range(i + 1, len(conditions)):
                    c1, c2 = conditions[i], conditions[j]
                    t_stat, p_value = stats.ttest_ind(
                        condition_texts[c1],
                        condition_texts[c2]
                    )
                    comparisons.append({
                        "conditions": (c1, c2),
                        "t_statistic": t_stat,
                        "p_value": p_value
                    })

            results["comparisons"] = comparisons

        return results
```

### 8.2 Token Probability Examination

```python
# output_analysis/token_probabilities.py

"""
Analyze token-level probabilities from LLM outputs.
"""

from typing import List, Dict, Any, Optional
import numpy as np

class TokenProbabilityAnalyzer:
    """
    Analyze token probabilities to understand model confidence.

    Requires API support for logprobs (OpenAI, some others).
    """

    def __init__(self):
        self.analyses = []

    def analyze_response(
        self,
        response_with_logprobs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a response that includes logprobs.

        Expected format (OpenAI-style):
        {
            "content": "...",
            "logprobs": {
                "content": [
                    {"token": "word", "logprob": -0.5, "top_logprobs": [...]}
                ]
            }
        }
        """
        logprobs_data = response_with_logprobs.get("logprobs", {})
        content_logprobs = logprobs_data.get("content", [])

        if not content_logprobs:
            return {"error": "No logprobs in response"}

        # Extract probabilities
        tokens = []
        probs = []
        entropy_values = []

        for token_data in content_logprobs:
            token = token_data.get("token", "")
            logprob = token_data.get("logprob", 0)
            top_logprobs = token_data.get("top_logprobs", [])

            tokens.append(token)
            probs.append(np.exp(logprob))

            # Calculate entropy from top alternatives
            if top_logprobs:
                alt_probs = [np.exp(alt["logprob"]) for alt in top_logprobs]
                # Normalize
                total = sum(alt_probs)
                norm_probs = [p / total for p in alt_probs]
                entropy = -sum(p * np.log(p + 1e-10) for p in norm_probs)
                entropy_values.append(entropy)

        analysis = {
            "n_tokens": len(tokens),
            "mean_probability": np.mean(probs),
            "min_probability": np.min(probs),
            "max_probability": np.max(probs),
            "mean_entropy": np.mean(entropy_values) if entropy_values else None,
            "low_confidence_tokens": [
                {"token": t, "prob": p}
                for t, p in zip(tokens, probs) if p < 0.3
            ],
            "high_entropy_positions": [
                i for i, e in enumerate(entropy_values) if e > 1.5
            ]
        }

        self.analyses.append(analysis)
        return analysis

    def get_aggregate_metrics(self) -> Dict[str, Any]:
        """Get aggregate metrics across all analyzed responses."""
        if not self.analyses:
            return {"error": "No analyses performed"}

        all_mean_probs = [a["mean_probability"] for a in self.analyses]
        all_min_probs = [a["min_probability"] for a in self.analyses]

        return {
            "n_responses": len(self.analyses),
            "overall_mean_prob": np.mean(all_mean_probs),
            "overall_std_prob": np.std(all_mean_probs),
            "overall_min_prob": np.min(all_min_probs),
            "responses_with_low_confidence": sum(
                1 for a in self.analyses
                if a["min_probability"] < 0.1
            )
        }

    def detect_uncertainty_patterns(
        self,
        response_with_logprobs: Dict[str, Any],
        threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Detect patterns of uncertainty in response.

        Returns positions where model was uncertain.
        """
        logprobs_data = response_with_logprobs.get("logprobs", {})
        content_logprobs = logprobs_data.get("content", [])

        uncertainty_patterns = []

        for i, token_data in enumerate(content_logprobs):
            prob = np.exp(token_data.get("logprob", 0))

            if prob < threshold:
                # Get context
                start = max(0, i - 2)
                end = min(len(content_logprobs), i + 3)
                context_tokens = [
                    content_logprobs[j].get("token", "")
                    for j in range(start, end)
                ]

                uncertainty_patterns.append({
                    "position": i,
                    "token": token_data.get("token", ""),
                    "probability": prob,
                    "context": "".join(context_tokens),
                    "alternatives": token_data.get("top_logprobs", [])[:3]
                })

        return uncertainty_patterns
```

### 8.3 Embedding Space Analysis

```python
# output_analysis/embeddings.py

"""
Embedding-based analysis of LLM outputs.
"""

import numpy as np
from typing import List, Dict, Any
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from scipy.spatial.distance import cosine

class EmbeddingAnalyzer:
    """
    Analyze LLM outputs in embedding space.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with sentence embedding model."""
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed_responses(self, responses: List[str]) -> np.ndarray:
        """Embed a list of responses."""
        return self.model.encode(responses)

    def analyze_clustering(
        self,
        responses: List[str],
        expected_clusters: int = None
    ) -> Dict[str, Any]:
        """
        Analyze clustering of responses in embedding space.

        Useful for detecting:
        - Mode collapse (all responses cluster tightly)
        - Diverse generation (responses spread out)
        - Natural groupings (by topic, sentiment, etc.)
        """
        embeddings = self.embed_responses(responses)

        # Determine number of clusters
        if expected_clusters is None:
            # Use elbow method
            from sklearn.metrics import silhouette_score
            best_k = 2
            best_score = -1
            for k in range(2, min(10, len(responses) // 2)):
                kmeans = KMeans(n_clusters=k, random_state=42)
                labels = kmeans.fit_predict(embeddings)
                score = silhouette_score(embeddings, labels)
                if score > best_score:
                    best_score = score
                    best_k = k
            expected_clusters = best_k

        # Perform clustering
        kmeans = KMeans(n_clusters=expected_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)

        # Analyze clusters
        cluster_sizes = np.bincount(cluster_labels)

        # Calculate cluster cohesion
        cohesions = []
        for i in range(expected_clusters):
            cluster_embeds = embeddings[cluster_labels == i]
            if len(cluster_embeds) > 1:
                centroid = cluster_embeds.mean(axis=0)
                distances = [
                    np.linalg.norm(e - centroid)
                    for e in cluster_embeds
                ]
                cohesions.append(np.mean(distances))

        return {
            "n_clusters": expected_clusters,
            "cluster_sizes": cluster_sizes.tolist(),
            "mean_cohesion": np.mean(cohesions) if cohesions else None,
            "cluster_labels": cluster_labels.tolist(),
            "mode_collapse_warning": max(cluster_sizes) > 0.8 * len(responses)
        }

    def calculate_diversity(self, responses: List[str]) -> Dict[str, float]:
        """
        Calculate diversity metrics for a set of responses.
        """
        embeddings = self.embed_responses(responses)

        # Pairwise cosine similarities
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = 1 - cosine(embeddings[i], embeddings[j])
                similarities.append(sim)

        return {
            "mean_similarity": np.mean(similarities),
            "std_similarity": np.std(similarities),
            "min_similarity": np.min(similarities),
            "max_similarity": np.max(similarities),
            "diversity_score": 1 - np.mean(similarities)  # Higher = more diverse
        }

    def compare_to_reference(
        self,
        responses: List[str],
        reference_responses: List[str]
    ) -> Dict[str, Any]:
        """
        Compare response embeddings to a reference set.

        Useful for:
        - Checking if outputs match expected patterns
        - Detecting drift from baseline
        """
        response_embeds = self.embed_responses(responses)
        reference_embeds = self.embed_responses(reference_responses)

        # Calculate distances to reference centroid
        ref_centroid = reference_embeds.mean(axis=0)
        distances_to_ref = [
            np.linalg.norm(e - ref_centroid)
            for e in response_embeds
        ]

        # Calculate overlap (nearest neighbor distances)
        min_distances = []
        for resp_embed in response_embeds:
            min_dist = min(
                np.linalg.norm(resp_embed - ref_embed)
                for ref_embed in reference_embeds
            )
            min_distances.append(min_dist)

        return {
            "mean_distance_to_reference": np.mean(distances_to_ref),
            "std_distance_to_reference": np.std(distances_to_ref),
            "mean_nearest_neighbor": np.mean(min_distances),
            "outliers": [
                i for i, d in enumerate(distances_to_ref)
                if d > np.mean(distances_to_ref) + 2 * np.std(distances_to_ref)
            ]
        }

    def visualize_embedding_space(
        self,
        responses: List[str],
        labels: List[str] = None
    ) -> Dict[str, Any]:
        """
        Create 2D visualization of response embeddings.

        Returns coordinates for plotting.
        """
        embeddings = self.embed_responses(responses)

        # Reduce to 2D
        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(responses) - 1))
        coords_2d = tsne.fit_transform(embeddings)

        return {
            "x": coords_2d[:, 0].tolist(),
            "y": coords_2d[:, 1].tolist(),
            "labels": labels or [f"Response {i}" for i in range(len(responses))]
        }
```

### 8.4 Complete Analysis Pipeline

```python
# output_analysis/pipeline.py

"""
Complete analysis pipeline for LLM outputs.
"""

from typing import List, Dict, Any
import json
from datetime import datetime

class OutputAnalysisPipeline:
    """
    Run complete analysis pipeline on LLM outputs.
    """

    def __init__(self):
        from .perplexity import PerplexityAnalyzer
        from .token_probabilities import TokenProbabilityAnalyzer
        from .embeddings import EmbeddingAnalyzer

        self.perplexity_analyzer = PerplexityAnalyzer()
        self.token_analyzer = TokenProbabilityAnalyzer()
        self.embedding_analyzer = EmbeddingAnalyzer()

    def run_full_analysis(
        self,
        responses: List[str],
        responses_with_logprobs: List[Dict] = None,
        reference_responses: List[str] = None,
        condition_name: str = "default"
    ) -> Dict[str, Any]:
        """
        Run complete analysis pipeline.

        Args:
            responses: List of LLM output texts
            responses_with_logprobs: Optional responses with logprob data
            reference_responses: Optional reference set for comparison
            condition_name: Name of experimental condition

        Returns:
            Complete analysis results
        """
        results = {
            "condition": condition_name,
            "timestamp": datetime.now().isoformat(),
            "n_responses": len(responses),
            "analyses": {}
        }

        # 1. Perplexity analysis
        print("Running perplexity analysis...")
        results["analyses"]["perplexity"] = \
            self.perplexity_analyzer.analyze_batch(responses)

        # 2. Token probability analysis (if available)
        if responses_with_logprobs:
            print("Running token probability analysis...")
            for resp in responses_with_logprobs:
                self.token_analyzer.analyze_response(resp)
            results["analyses"]["token_probabilities"] = \
                self.token_analyzer.get_aggregate_metrics()

        # 3. Embedding analysis
        print("Running embedding analysis...")
        results["analyses"]["diversity"] = \
            self.embedding_analyzer.calculate_diversity(responses)
        results["analyses"]["clustering"] = \
            self.embedding_analyzer.analyze_clustering(responses)

        # 4. Reference comparison (if available)
        if reference_responses:
            print("Running reference comparison...")
            results["analyses"]["reference_comparison"] = \
                self.embedding_analyzer.compare_to_reference(
                    responses, reference_responses
                )

        # 5. Summary metrics
        results["summary"] = self._generate_summary(results["analyses"])

        return results

    def _generate_summary(self, analyses: Dict) -> Dict[str, Any]:
        """Generate summary of key findings."""
        summary = {
            "quality_indicators": {},
            "warnings": [],
            "recommendations": []
        }

        # Check perplexity
        perp = analyses.get("perplexity", {})
        if perp.get("potential_memorization"):
            summary["warnings"].append(
                f"Potential memorization detected in {len(perp['potential_memorization'])} responses"
            )
            summary["recommendations"].append(
                "Review low-perplexity responses for training data patterns"
            )

        # Check diversity
        div = analyses.get("diversity", {})
        if div.get("diversity_score", 1) < 0.3:
            summary["warnings"].append(
                f"Low diversity score: {div['diversity_score']:.2f}"
            )
            summary["recommendations"].append(
                "Consider increasing temperature or modifying prompts"
            )

        # Check clustering
        clust = analyses.get("clustering", {})
        if clust.get("mode_collapse_warning"):
            summary["warnings"].append(
                "Mode collapse detected - responses clustering too tightly"
            )

        # Quality indicators
        summary["quality_indicators"] = {
            "perplexity_mean": perp.get("mean_perplexity"),
            "diversity_score": div.get("diversity_score"),
            "n_clusters": clust.get("n_clusters")
        }

        return summary

    def save_results(self, results: Dict, output_path: str):
        """Save analysis results to file."""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {output_path}")
```

---

## Appendices

### Appendix A: Model Card References

| Model | Model Card URL | Key Information |
|-------|----------------|-----------------|
| Llama 3.1 | https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md | Training data, benchmarks, limitations |
| Mistral 7B | https://mistral.ai/news/announcing-mistral-7b/ | Architecture, training approach |
| GPT-4o | https://openai.com/index/gpt-4o-system-card/ | Safety, capabilities, limitations |

### Appendix B: API Endpoint Documentation

```yaml
api_endpoints:
  openai:
    base_url: "https://api.openai.com/v1"
    chat_endpoint: "/chat/completions"
    docs: "https://platform.openai.com/docs/api-reference"

  anthropic:
    base_url: "https://api.anthropic.com"
    messages_endpoint: "/v1/messages"
    docs: "https://docs.anthropic.com/en/api"

  groq:
    base_url: "https://api.groq.com/openai/v1"
    chat_endpoint: "/chat/completions"
    docs: "https://console.groq.com/docs"

  cerebras:
    base_url: "https://api.cerebras.ai/v1"
    chat_endpoint: "/chat/completions"
    docs: "https://inference-docs.cerebras.ai/"

  together:
    base_url: "https://api.together.xyz/v1"
    chat_endpoint: "/chat/completions"
    docs: "https://docs.together.ai/"
```

### Appendix C: Statistical Tests Reference

| Test | Use Case | Assumptions | Implementation |
|------|----------|-------------|----------------|
| Paired t-test | Compare conditions within model | Normal distribution | `scipy.stats.ttest_rel` |
| Independent t-test | Compare across models | Independence, normality | `scipy.stats.ttest_ind` |
| One-way ANOVA | Compare >2 conditions | Homogeneity of variance | `scipy.stats.f_oneway` |
| Spearman correlation | Rank agreement | Ordinal data | `scipy.stats.spearmanr` |
| KL Divergence | Distribution similarity | Continuous distributions | `scipy.special.kl_div` |
| Cohen's d | Effect size | - | Manual calculation |
| Bonferroni correction | Multiple comparisons | - | `alpha / n_tests` |

### Appendix D: Troubleshooting Guide

| Issue | Symptoms | Solutions |
|-------|----------|-----------|
| Non-determinism | Different outputs with T=0 | 1. Verify seed setting<br>2. Check API version<br>3. Use greedy decoding (top_k=1) |
| Memorization | Very low perplexity, specific facts | 1. Use novel scenarios<br>2. Verify against contamination check<br>3. Randomize specific values |
| Mode collapse | All responses similar | 1. Increase temperature<br>2. Add diversity prompts<br>3. Check prompt ambiguity |
| Context overflow | Truncation errors | 1. Implement summarization<br>2. Prioritize recent context<br>3. Use importance weighting |
| Inconsistent personas | Character drift | 1. Strengthen system prompt<br>2. Add persona reinforcement<br>3. Increase context |

---

## Document Control

- **Authors**: LLM Technical Committee
- **Reviewers**: [To be assigned]
- **Approval**: [Pending]
- **Next Review**: 2025-12-19

---

*This protocol is designed to address all identified technical critiques and ensure rigorous, reproducible LLM experimental methodology.*
