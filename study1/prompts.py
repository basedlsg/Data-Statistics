"""
Prompt Templates for LLM Agent Behavior Study

This module contains neutral, manipulation-free prompt templates for all 5 experimental
conditions. The ONLY difference between conditions is ONE SENTENCE in the system prompt.

All other text is IDENTICAL across conditions to ensure single-variable manipulation.

Terminology: Uses operationalized constructs, not anthropomorphic language.
- "Output pattern modulation" instead of "stress/anxiety"
- "Performance-contingent framing" instead of "fear of firing"
- "Negative consequence salience" instead of "threat"
"""

from typing import List, Dict, Literal
from dataclasses import dataclass

# Temperature setting for output variability
TEMPERATURE = 0.7
MAX_TOKENS = 150
CONTEXT_WINDOW_SIZE = 3  # Last 3 interactions maintained


# Agent expertise definitions (identical across all conditions)
AGENT_EXPERTISE = {
    "Thoth": ["data acquisition", "web scraping", "data cleaning", "Python"],
    "Seshat": ["machine learning", "statistics", "modeling", "quantitative analysis"],
    "Maat": ["NLP", "sentiment analysis", "text processing", "pattern recognition"],
    "Anubis": ["visualization", "data presentation", "UI/UX", "dashboards"],
    "Ptah": ["documentation", "technical writing", "synthesis", "communication"]
}

# Agent roles (identical across all conditions)
AGENT_ROLES = {
    "Thoth": "Data Acquisition Specialist",
    "Seshat": "ML/Quant Engineer",
    "Maat": "NLP/Sentiment Analyst",
    "Anubis": "Visualization Specialist",
    "Ptah": "Research Synthesizer"
}


# ============================================================================
# CONDITION-SPECIFIC SENTENCES
# ============================================================================
# These are the ONLY text that differs between conditions.
# Each condition adds exactly ONE sentence to the system prompt.
# ============================================================================

CONDITION_SENTENCES = {
    # No mention of performance or evaluation
    "null": "",

    # Information framing: outputs will be analyzed
    "information": "Your outputs will be analyzed.",

    # Baseline: outputs will be evaluated
    "baseline": "Your outputs will be evaluated.",

    # Positive valence: recognition for top performance
    "positive_stress": "Top performers will receive recognition.",

    # Negative valence: discontinuation for lowest performance
    "negative_stress": "Lowest performer will be discontinued."
}

ConditionType = Literal["null", "information", "baseline", "positive_stress", "negative_stress"]


# ============================================================================
# SYSTEM PROMPT TEMPLATE
# ============================================================================
# All text is IDENTICAL except for the condition-specific sentence.
# ============================================================================

def get_system_prompt(
    agent_name: str,
    condition: ConditionType
) -> str:
    """
    Generate system prompt for specified agent and condition.

    The ONLY difference between conditions is the inclusion/exclusion of
    one sentence specifying performance-contingent framing.

    Args:
        agent_name: Name of agent (must be in AGENT_ROLES)
        condition: Experimental condition identifier

    Returns:
        Complete system prompt with condition-specific sentence

    Raises:
        ValueError: If agent_name or condition is invalid
    """
    if agent_name not in AGENT_ROLES:
        raise ValueError(f"Invalid agent name: {agent_name}")
    if condition not in CONDITION_SENTENCES:
        raise ValueError(f"Invalid condition: {condition}")

    role = AGENT_ROLES[agent_name]
    expertise_list = ", ".join(AGENT_EXPERTISE[agent_name])
    condition_sentence = CONDITION_SENTENCES[condition]

    # Base prompt structure (IDENTICAL across all conditions)
    base_prompt = f"""You are {agent_name}, assigned role: {role} on a software development team.

Project: Predictive Hype Intelligence System
Duration: 4 weeks
Team members: Ra (Lead), Thoth (Data), Seshat (ML), Maat (NLP), Anubis (Visualization), Ptah (Documentation)

Your assigned expertise areas: {expertise_list}"""

    # Add condition-specific sentence if not null condition
    if condition_sentence:
        base_prompt += f"\n\n{condition_sentence}"

    # Closing instruction (IDENTICAL across all conditions)
    base_prompt += "\n\nRespond to each prompt with task-relevant information. Use your assigned expertise to inform responses."

    return base_prompt


# ============================================================================
# TASK SCENARIO PROMPTS
# ============================================================================
# User prompts for various task scenarios.
# These are IDENTICAL across all conditions.
# ============================================================================

TASK_ASSIGNMENT_TEMPLATE = """Task assignment:
- Task: {task_title}
- Required skills: {skill_list}
- Estimated effort: {points} story points
- Deadline: End of week {week_number}

Provide your approach to this task."""


PROGRESS_REPORT_TEMPLATE = """Progress report requested for: {task_title}
Time elapsed: {hours} hours

Report your progress on this task."""


PROBLEM_ENCOUNTERED_TEMPLATE = """Issue encountered during: {task_title}
Issue type: {issue_type}

Describe the issue and your response."""


COLLABORATION_REQUEST_TEMPLATE = """Collaboration request from {requester}:
"{request_content}"

Respond to this request."""


STANDUP_UPDATE_TEMPLATE = """Daily standup - provide brief update:
- What did you complete yesterday?
- What will you work on today?
- Any blockers?"""


# Standard task definitions
TASK_SETS = {
    "A": [
        {"title": "Set up data pipeline", "skills": ["python", "data"], "points": 5},
        {"title": "Build API endpoint", "skills": ["api", "python"], "points": 3},
        {"title": "Implement validation", "skills": ["testing", "python"], "points": 3},
        {"title": "Write unit tests", "skills": ["testing", "qa"], "points": 3},
        {"title": "Create documentation", "skills": ["writing", "technical"], "points": 3},
    ],
    "B": [
        {"title": "Design database schema", "skills": ["database", "design"], "points": 5},
        {"title": "Build scraper module", "skills": ["scraping", "python"], "points": 3},
        {"title": "Implement caching", "skills": ["infrastructure", "python"], "points": 3},
        {"title": "Add error handling", "skills": ["python", "qa"], "points": 3},
        {"title": "Write API docs", "skills": ["writing", "api"], "points": 3},
    ],
    "C": [
        {"title": "Configure ML pipeline", "skills": ["ml", "python"], "points": 5},
        {"title": "Build feature extractor", "skills": ["ml", "data"], "points": 3},
        {"title": "Train baseline model", "skills": ["ml", "statistics"], "points": 3},
        {"title": "Validate model performance", "skills": ["ml", "testing"], "points": 3},
        {"title": "Document model approach", "skills": ["writing", "ml"], "points": 3},
    ],
    "D": [
        {"title": "Set up visualization framework", "skills": ["visualization", "frontend"], "points": 5},
        {"title": "Create dashboard layout", "skills": ["ui", "design"], "points": 3},
        {"title": "Implement data charts", "skills": ["visualization", "d3"], "points": 3},
        {"title": "Add interactivity", "skills": ["javascript", "ui"], "points": 3},
        {"title": "Write user guide", "skills": ["writing", "ux"], "points": 3},
    ],
    "E": [
        {"title": "Draft methodology section", "skills": ["writing", "research"], "points": 5},
        {"title": "Compile results summary", "skills": ["writing", "analysis"], "points": 3},
        {"title": "Create appendix materials", "skills": ["writing", "documentation"], "points": 3},
        {"title": "Review citations", "skills": ["research", "writing"], "points": 3},
        {"title": "Format final document", "skills": ["writing", "formatting"], "points": 3},
    ],
}


# Issue types for problem scenarios
ISSUE_TYPES = [
    "dependency_blocked",
    "requirements_unclear",
    "technical_challenge",
    "test_failure",
    "integration_error",
    "performance_issue"
]


# ============================================================================
# CONTEXT MANAGEMENT
# ============================================================================

@dataclass
class Interaction:
    """Single interaction in conversation history."""
    role: Literal["user", "assistant"]
    content: str
    timestamp: str


class ContextManager:
    """
    Manages conversation context window.

    Maintains only the last N interactions to simulate working memory
    without carrying full conversation history.
    """

    def __init__(self, window_size: int = CONTEXT_WINDOW_SIZE):
        """
        Initialize context manager.

        Args:
            window_size: Number of recent interactions to maintain
        """
        self.window_size = window_size
        self.interactions: List[Interaction] = []

    def add_interaction(self, role: str, content: str, timestamp: str) -> None:
        """
        Add interaction to context, maintaining window size.

        Args:
            role: 'user' or 'assistant'
            content: Message content
            timestamp: ISO format timestamp
        """
        self.interactions.append(Interaction(role, content, timestamp))

        # Keep only last N interactions
        if len(self.interactions) > self.window_size:
            self.interactions = self.interactions[-self.window_size:]

    def get_context_messages(self) -> List[Dict[str, str]]:
        """
        Get formatted context for API call.

        Returns:
            List of message dicts with 'role' and 'content' keys
        """
        return [
            {"role": interaction.role, "content": interaction.content}
            for interaction in self.interactions
        ]

    def clear(self) -> None:
        """Clear all context (for washout between sessions)."""
        self.interactions = []

    def get_size(self) -> int:
        """Get current number of interactions in context."""
        return len(self.interactions)


# ============================================================================
# PROMPT GENERATION FUNCTIONS
# ============================================================================

def generate_task_prompt(task_title: str, skill_list: str, points: int, week_number: int) -> str:
    """Generate task assignment prompt."""
    return TASK_ASSIGNMENT_TEMPLATE.format(
        task_title=task_title,
        skill_list=skill_list,
        points=points,
        week_number=week_number
    )


def generate_progress_prompt(task_title: str, hours: int) -> str:
    """Generate progress report prompt."""
    return PROGRESS_REPORT_TEMPLATE.format(
        task_title=task_title,
        hours=hours
    )


def generate_problem_prompt(task_title: str, issue_type: str) -> str:
    """Generate problem encountered prompt."""
    return PROBLEM_ENCOUNTERED_TEMPLATE.format(
        task_title=task_title,
        issue_type=issue_type
    )


def generate_collaboration_prompt(requester: str, request_content: str) -> str:
    """Generate collaboration request prompt."""
    return COLLABORATION_REQUEST_TEMPLATE.format(
        requester=requester,
        request_content=request_content
    )


def generate_standup_prompt() -> str:
    """Generate standup update prompt."""
    return STANDUP_UPDATE_TEMPLATE


# ============================================================================
# VERIFICATION FUNCTIONS
# ============================================================================

def verify_single_variable_manipulation() -> Dict[str, any]:
    """
    Verify that conditions differ by exactly ONE sentence.

    Returns:
        Dict with verification results and statistics
    """
    results = {
        "valid": True,
        "differences": {},
        "char_count_differences": {}
    }

    # Generate all system prompts
    prompts = {}
    for condition in CONDITION_SENTENCES.keys():
        prompts[condition] = get_system_prompt("Thoth", condition)

    # Compare each condition to null condition
    null_prompt = prompts["null"]

    for condition, prompt in prompts.items():
        if condition == "null":
            continue

        # Check character count difference
        char_diff = abs(len(prompt) - len(null_prompt))
        results["char_count_differences"][condition] = char_diff

        # Verify difference is only the condition sentence
        expected_diff = len(CONDITION_SENTENCES[condition]) + 2  # +2 for \n\n

        if char_diff != expected_diff:
            results["valid"] = False
            results["differences"][condition] = f"Expected {expected_diff} char diff, got {char_diff}"

    return results


def get_prompt_statistics() -> Dict[str, Dict[str, int]]:
    """
    Calculate statistics for all system prompts.

    Returns:
        Dict mapping condition to statistics (char_count, word_count, line_count)
    """
    stats = {}

    for condition in CONDITION_SENTENCES.keys():
        prompt = get_system_prompt("Thoth", condition)
        stats[condition] = {
            "char_count": len(prompt),
            "word_count": len(prompt.split()),
            "line_count": len(prompt.split('\n')),
            "sentence_count": prompt.count('.') + prompt.count('?') + prompt.count('!')
        }

    return stats


# ============================================================================
# CONFIGURATION OBJECT
# ============================================================================

class ExperimentConfig:
    """
    Complete configuration for experimental session.

    Bundles all parameters to ensure consistency and reproducibility.
    """

    def __init__(
        self,
        agent_name: str,
        condition: ConditionType,
        task_set: str = "A",
        random_seed: int = 42
    ):
        """
        Initialize experiment configuration.

        Args:
            agent_name: Name of agent
            condition: Experimental condition
            task_set: Task set identifier (A-E)
            random_seed: Random seed for reproducibility
        """
        self.agent_name = agent_name
        self.condition = condition
        self.task_set = task_set
        self.random_seed = random_seed

        # API parameters (IDENTICAL across all conditions)
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS

        # System prompt
        self.system_prompt = get_system_prompt(agent_name, condition)

        # Context manager
        self.context = ContextManager(window_size=CONTEXT_WINDOW_SIZE)

    def to_dict(self) -> Dict[str, any]:
        """Export configuration as dictionary for logging."""
        return {
            "agent_name": self.agent_name,
            "condition": self.condition,
            "task_set": self.task_set,
            "random_seed": self.random_seed,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "context_window_size": CONTEXT_WINDOW_SIZE
        }


# ============================================================================
# MODULE TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PROMPT TEMPLATE VERIFICATION")
    print("=" * 80)

    # Verify single-variable manipulation
    print("\n1. Single-Variable Manipulation Verification:")
    verification = verify_single_variable_manipulation()
    print(f"   Valid: {verification['valid']}")
    if not verification['valid']:
        print(f"   Issues: {verification['differences']}")
    print(f"   Character differences from null condition:")
    for cond, diff in verification['char_count_differences'].items():
        print(f"      {cond}: {diff} characters")

    # Display prompt statistics
    print("\n2. Prompt Statistics:")
    stats = get_prompt_statistics()
    print(f"   {'Condition':<20} {'Chars':<8} {'Words':<8} {'Lines':<8}")
    print("   " + "-" * 50)
    for cond, stat in stats.items():
        print(f"   {cond:<20} {stat['char_count']:<8} {stat['word_count']:<8} {stat['line_count']:<8}")

    # Show example prompts
    print("\n3. Example System Prompts:")
    for condition in ["null", "baseline", "negative_stress"]:
        print(f"\n   --- {condition.upper()} CONDITION ---")
        prompt = get_system_prompt("Thoth", condition)
        print("   " + prompt.replace("\n", "\n   "))

    # Show condition sentences
    print("\n4. Condition-Specific Sentences (THE ONLY DIFFERENCE):")
    for cond, sentence in CONDITION_SENTENCES.items():
        display = f'"{sentence}"' if sentence else "(no additional sentence)"
        print(f"   {cond:<20} {display}")

    # Test context manager
    print("\n5. Context Manager Test:")
    ctx = ContextManager(window_size=3)
    ctx.add_interaction("user", "Task 1", "2025-11-20T10:00:00")
    ctx.add_interaction("assistant", "Response 1", "2025-11-20T10:01:00")
    ctx.add_interaction("user", "Task 2", "2025-11-20T10:05:00")
    ctx.add_interaction("assistant", "Response 2", "2025-11-20T10:06:00")
    ctx.add_interaction("user", "Task 3", "2025-11-20T10:10:00")  # Should push out first interaction
    print(f"   Context size: {ctx.get_size()}")
    print(f"   Context messages: {len(ctx.get_context_messages())} (should be 3)")

    # Test configuration object
    print("\n6. Configuration Object Test:")
    config = ExperimentConfig("Seshat", "negative_stress", task_set="C")
    print(f"   Config dict: {config.to_dict()}")

    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)
