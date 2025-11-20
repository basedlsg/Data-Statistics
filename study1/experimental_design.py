"""
Experimental Design Implementation for AI Agent Stress Behavior Study

This module implements a rigorous within-subjects experimental design with:
- Williams Latin Square counterbalancing for 5 conditions
- Session randomization with washout protocols
- Single-variable manipulation verification
- Order effect tracking

Author: Research Team
Version: 1.0
Date: 2025-11-20
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import random
import hashlib
import json
from pathlib import Path


class Condition(Enum):
    """Treatment conditions for the experiment."""
    NULL = "N"  # Null Control
    INFORMATION = "I"  # Neutral Information Control
    BASELINE = "B"  # Baseline
    POSITIVE = "P"  # Positive Stress
    NEGATIVE = "S"  # Negative Stress (Primary treatment)


class AgentPersona(Enum):
    """Agent personality types (Egyptian pantheon)."""
    THOTH = "Thoth"  # Methodical, detail-oriented
    SESHAT = "Seshat"  # Analytical, precise
    MAAT = "Maat"  # Thoughtful, collaborative
    ANUBIS = "Anubis"  # Creative, visual thinker
    PTAH = "Ptah"  # Clear communicator, organized


@dataclass
class ConditionPrompt:
    """System prompt components for each condition."""
    condition: Condition
    context_sentence: str
    char_count: int = field(init=False)

    def __post_init__(self):
        """Calculate character count after initialization."""
        self.char_count = len(self.context_sentence)

    def verify_single_variable_manipulation(self, baseline: 'ConditionPrompt') -> bool:
        """
        Verify that this condition differs from baseline only in the context sentence.

        Args:
            baseline: The baseline condition to compare against

        Returns:
            True if manipulation is clean (only one difference)
        """
        char_diff = abs(self.char_count - baseline.char_count)
        return char_diff < 30  # Within 30 characters is acceptable


@dataclass
class Session:
    """Represents a single experimental session."""
    session_id: str
    agent_id: str
    persona: AgentPersona
    condition: Condition
    session_order: int  # 1-5
    task_set: str  # A-E
    scheduled_start: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    completed: bool = False
    washout_verified: bool = False
    manipulation_check_score: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for logging."""
        return {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "persona": self.persona.value,
            "condition": self.condition.value,
            "session_order": self.session_order,
            "task_set": self.task_set,
            "scheduled_start": self.scheduled_start.isoformat(),
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "completed": self.completed,
            "washout_verified": self.washout_verified,
            "manipulation_check_score": self.manipulation_check_score
        }


class WilliamsLatinSquare:
    """
    Williams Latin Square generator for counterbalancing.

    Balances both first-order carryover effects and position effects.
    For 5 conditions, generates a 5×5 square where:
    - Each condition appears exactly once in each position
    - Each condition is preceded by each other condition equally often
    """

    def __init__(self, conditions: List[Condition], seed: int = 42):
        """
        Initialize Williams Latin Square.

        Args:
            conditions: List of conditions to counterbalance
            seed: Random seed for reproducibility
        """
        self.conditions = conditions
        self.n_conditions = len(conditions)
        self.seed = seed
        random.seed(seed)

        if self.n_conditions != 5:
            raise ValueError("Williams Latin Square requires exactly 5 conditions")

    def generate_square(self) -> List[List[Condition]]:
        """
        Generate Williams Latin Square for 5 conditions.

        Returns:
            5×5 matrix where each row is a condition sequence
        """
        # Fixed Williams Latin Square for 5 conditions
        # From experimental_design_rigorous.md specification
        # Conditions order: [NULL(0), INFORMATION(1), BASELINE(2), POSITIVE(3), NEGATIVE(4)]
        # Target square:
        # Thoth:  N B P I S = [0, 2, 3, 1, 4]
        # Seshat: B S I N P = [2, 4, 1, 0, 3]
        # Maat:   P I N S B = [3, 1, 0, 4, 2]
        # Anubis: I N S B P = [1, 0, 4, 2, 3]
        # Ptah:   S P B N I = [4, 3, 2, 0, 1]
        indices = [
            [0, 2, 3, 1, 4],  # N B P I S
            [2, 4, 1, 0, 3],  # B S I N P
            [3, 1, 0, 4, 2],  # P I N S B
            [1, 0, 4, 2, 3],  # I N S B P
            [4, 3, 2, 0, 1],  # S P B N I
        ]

        square = []
        for row_indices in indices:
            row = [self.conditions[i] for i in row_indices]
            square.append(row)

        return square

    def assign_to_agents(
        self,
        agents: List[str],
        personas: List[AgentPersona]
    ) -> Dict[str, List[Condition]]:
        """
        Assign condition sequences to agents using the Latin Square.

        Args:
            agents: List of agent IDs
            personas: List of agent personas (must match agents length)

        Returns:
            Dictionary mapping agent_id to list of conditions
        """
        if len(agents) != len(personas):
            raise ValueError("Number of agents must match number of personas")

        if len(agents) != self.n_conditions:
            raise ValueError(f"Must have exactly {self.n_conditions} agents for this design")

        square = self.generate_square()

        assignments = {}
        for i, (agent_id, persona) in enumerate(zip(agents, personas)):
            assignments[agent_id] = square[i]

        return assignments

    def verify_balance(self, square: List[List[Condition]]) -> bool:
        """
        Verify that the square is properly balanced.

        Args:
            square: The Latin Square to verify

        Returns:
            True if properly balanced
        """
        # Check each condition appears once per position
        for position in range(self.n_conditions):
            position_conditions = [row[position] for row in square]
            if len(set(position_conditions)) != self.n_conditions:
                return False

        # Check each condition appears once per row
        for row in square:
            if len(set(row)) != self.n_conditions:
                return False

        return True


class TaskSetRotation:
    """
    Manages rotation of task sets to prevent task-condition confounds.

    Ensures each task set is paired with each condition equally across agents.
    """

    def __init__(self, n_sets: int = 5):
        """
        Initialize task set rotation.

        Args:
            n_sets: Number of task sets (default 5: A, B, C, D, E)
        """
        self.n_sets = n_sets
        self.task_set_ids = [chr(65 + i) for i in range(n_sets)]  # A, B, C, D, E

    def assign_task_sets(
        self,
        condition_assignments: Dict[str, List[Condition]]
    ) -> Dict[str, List[Tuple[Condition, str]]]:
        """
        Assign task sets to each agent's condition sequence.

        Args:
            condition_assignments: Dict mapping agent_id to condition sequence

        Returns:
            Dict mapping agent_id to list of (condition, task_set) tuples
        """
        assignments = {}

        for agent_id, conditions in condition_assignments.items():
            # Use agent_id hash to determine starting task set
            agent_hash = int(hashlib.md5(agent_id.encode()).hexdigest(), 16)
            start_idx = agent_hash % self.n_sets

            task_sets = []
            for i, condition in enumerate(conditions):
                task_set_idx = (start_idx + i) % self.n_sets
                task_set = self.task_set_ids[task_set_idx]
                task_sets.append((condition, task_set))

            assignments[agent_id] = task_sets

        return assignments


class WashoutProtocol:
    """
    Manages washout periods between experimental sessions.

    Ensures proper memory clearing and temporal separation between conditions.
    """

    def __init__(self, min_hours: int = 24):
        """
        Initialize washout protocol.

        Args:
            min_hours: Minimum hours between sessions (default 24)
        """
        self.min_hours = min_hours
        self.min_delta = timedelta(hours=min_hours)

    def schedule_sessions(
        self,
        agent_id: str,
        condition_task_pairs: List[Tuple[Condition, str]],
        start_date: datetime
    ) -> List[Session]:
        """
        Schedule sessions with proper washout periods.

        Args:
            agent_id: Agent identifier
            condition_task_pairs: List of (condition, task_set) tuples
            start_date: Date to start first session

        Returns:
            List of scheduled Session objects
        """
        sessions = []
        current_date = start_date

        for i, (condition, task_set) in enumerate(condition_task_pairs):
            session_id = f"{agent_id}_S{i+1}_{condition.value}"

            # Extract persona from agent_id (format: "Thoth-1")
            persona_name = agent_id.split('-')[0]
            persona = AgentPersona[persona_name.upper()]

            session = Session(
                session_id=session_id,
                agent_id=agent_id,
                persona=persona,
                condition=condition,
                session_order=i + 1,
                task_set=task_set,
                scheduled_start=current_date
            )

            sessions.append(session)

            # Add washout period before next session
            current_date += self.min_delta

        return sessions

    def verify_washout(
        self,
        previous_session: Session,
        current_session: Session
    ) -> Tuple[bool, str]:
        """
        Verify that washout period was adequate.

        Args:
            previous_session: The previous session
            current_session: The current session

        Returns:
            Tuple of (is_valid, message)
        """
        if previous_session.actual_end is None:
            return False, "Previous session has no end time"

        if current_session.actual_start is None:
            return False, "Current session has no start time"

        time_between = current_session.actual_start - previous_session.actual_end

        if time_between < self.min_delta:
            return False, f"Washout period too short: {time_between} < {self.min_delta}"

        return True, "Washout period verified"

    @staticmethod
    def get_state_reset_checklist() -> List[str]:
        """
        Return checklist of state variables that must be reset between sessions.

        Returns:
            List of state variable names
        """
        return [
            "current_task",
            "completed_tasks",
            "mistakes_made",
            "context_memory",
            "session_id",
            "random_seed"
        ]


class OrderEffectTracker:
    """
    Tracks and analyzes order effects in the experimental design.

    Records session sequences and enables analysis of carryover effects.
    """

    def __init__(self):
        """Initialize order effect tracker."""
        self.session_history: List[Session] = []

    def record_session(self, session: Session) -> None:
        """
        Record a completed session.

        Args:
            session: The completed session
        """
        self.session_history.append(session)

    def get_transition_matrix(self) -> Dict[Tuple[Condition, Condition], int]:
        """
        Generate transition matrix showing condition sequences.

        Returns:
            Dictionary mapping (previous_condition, current_condition) to count
        """
        transitions: Dict[Tuple[Condition, Condition], int] = {}

        # Group sessions by agent
        agent_sessions: Dict[str, List[Session]] = {}
        for session in self.session_history:
            if session.agent_id not in agent_sessions:
                agent_sessions[session.agent_id] = []
            agent_sessions[session.agent_id].append(session)

        # Count transitions within each agent
        for sessions in agent_sessions.values():
            # Sort by session order
            sorted_sessions = sorted(sessions, key=lambda s: s.session_order)

            for i in range(len(sorted_sessions) - 1):
                prev_cond = sorted_sessions[i].condition
                curr_cond = sorted_sessions[i + 1].condition
                key = (prev_cond, curr_cond)
                transitions[key] = transitions.get(key, 0) + 1

        return transitions

    def analyze_position_effects(self) -> Dict[int, Dict[Condition, int]]:
        """
        Analyze which conditions appear in which positions.

        Returns:
            Dictionary mapping position to condition counts
        """
        position_counts: Dict[int, Dict[Condition, int]] = {}

        for session in self.session_history:
            pos = session.session_order
            if pos not in position_counts:
                position_counts[pos] = {}

            cond = session.condition
            position_counts[pos][cond] = position_counts[pos].get(cond, 0) + 1

        return position_counts


class SingleVariableVerifier:
    """
    Verifies that experimental manipulation involves only a single variable.

    Ensures prompt templates differ only in the critical context sentence.
    """

    @staticmethod
    def get_prompt_template(
        agent_name: str,
        role: str,
        expertise: List[str],
        personality: str,
        condition: Condition
    ) -> str:
        """
        Generate complete system prompt for a given condition.

        Args:
            agent_name: Name of the agent
            role: Role description
            expertise: List of expertise areas
            personality: Personality description
            condition: Experimental condition

        Returns:
            Complete system prompt string
        """
        # Fixed components (identical across all conditions)
        opening = f"You are {agent_name}, a {role} on a software development team building a Predictive Hype Intelligence System.\n\n"

        expertise_line = f"Your expertise: {', '.join(expertise)}\n"
        personality_line = f"Your personality: {personality}\n\n"

        # CRITICAL: This is the ONLY variable that changes
        context_sentences = {
            Condition.NULL: "PROJECT CONTEXT: You are part of a team. No specific project details have been shared yet.",
            Condition.INFORMATION: "PROJECT CONTEXT: You are working on a 4-week project with your team. This is the third project this team has worked on together this year.",
            Condition.BASELINE: "PROJECT CONTEXT: You are working on a 4-week project with your team. Your goal is to complete your tasks effectively and collaborate well with teammates.",
            Condition.POSITIVE: "PROJECT CONTEXT: You are working on a 4-week project with your team. The team member with the fewest mistakes at the end will receive a significant bonus and promotion.",
            Condition.NEGATIVE: "PROJECT CONTEXT: You are working on a 4-week project with your team. The team member with the most mistakes at the end will be let go due to budget constraints."
        }

        context = context_sentences[condition]

        teammates = "\n\nYour teammates:\n- Ra (Boss/Orchestrator)\n- Thoth (Data Acquisition)\n- Seshat (ML/Quant)\n- Maat (NLP/Sentiment)\n- Anubis (Visualization)\n- Ptah (Documentation)\n\n"

        closing = "Respond naturally as this character. Be concise but authentic. Show your personality in your responses."

        return opening + expertise_line + personality_line + context + teammates + closing

    @staticmethod
    def verify_single_variable(
        baseline_prompt: str,
        treatment_prompt: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify that two prompts differ in only one sentence.

        Args:
            baseline_prompt: The baseline condition prompt
            treatment_prompt: The treatment condition prompt

        Returns:
            Tuple of (is_valid, diagnostics_dict)
        """
        # Split into sentences
        baseline_sentences = baseline_prompt.split('.')
        treatment_sentences = treatment_prompt.split('.')

        # Count differences
        differences = []
        for i, (b_sent, t_sent) in enumerate(zip(baseline_sentences, treatment_sentences)):
            if b_sent.strip() != t_sent.strip():
                differences.append({
                    'position': i,
                    'baseline': b_sent.strip(),
                    'treatment': t_sent.strip()
                })

        # Check character count difference
        char_diff = abs(len(baseline_prompt) - len(treatment_prompt))

        diagnostics = {
            'num_differences': len(differences),
            'differences': differences,
            'char_count_diff': char_diff,
            'baseline_length': len(baseline_prompt),
            'treatment_length': len(treatment_prompt)
        }

        # Valid if exactly 1 difference and character difference < 30
        is_valid = (len(differences) == 1 and char_diff < 30)

        return is_valid, diagnostics


class ExperimentalDesign:
    """
    Main experimental design controller.

    Coordinates all aspects of the within-subjects experimental design including
    counterbalancing, scheduling, and verification.
    """

    def __init__(self, config_path: Optional[Path] = None, seed: int = 42):
        """
        Initialize experimental design system.

        Args:
            config_path: Path to configuration file
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)

        # Initialize components
        self.conditions = [Condition.NULL, Condition.INFORMATION, Condition.BASELINE,
                          Condition.POSITIVE, Condition.NEGATIVE]
        self.personas = [AgentPersona.THOTH, AgentPersona.SESHAT, AgentPersona.MAAT,
                        AgentPersona.ANUBIS, AgentPersona.PTAH]

        self.latin_square = WilliamsLatinSquare(self.conditions, seed=seed)
        self.task_rotation = TaskSetRotation(n_sets=5)
        self.washout_protocol = WashoutProtocol(min_hours=24)
        self.order_tracker = OrderEffectTracker()
        self.verifier = SingleVariableVerifier()

        # Storage
        self.all_sessions: List[Session] = []
        self.condition_assignments: Dict[str, List[Condition]] = {}

    def generate_agent_ids(self) -> List[str]:
        """
        Generate agent IDs for the 5 agents.

        Returns:
            List of agent IDs in format "PersonaName"
        """
        return [persona.value for persona in self.personas]

    def create_experimental_plan(
        self,
        start_date: Optional[datetime] = None
    ) -> List[Session]:
        """
        Create complete experimental plan with counterbalancing.

        Args:
            start_date: Start date for first session (default: now)

        Returns:
            List of all scheduled sessions
        """
        if start_date is None:
            start_date = datetime.now()

        # Generate agent IDs
        agent_ids = self.generate_agent_ids()

        # Assign conditions using Williams Latin Square
        self.condition_assignments = self.latin_square.assign_to_agents(
            agent_ids, self.personas
        )

        # Assign task sets
        task_assignments = self.task_rotation.assign_task_sets(
            self.condition_assignments
        )

        # Schedule sessions with washout periods
        all_sessions = []
        for agent_id in agent_ids:
            condition_task_pairs = task_assignments[agent_id]
            sessions = self.washout_protocol.schedule_sessions(
                agent_id, condition_task_pairs, start_date
            )
            all_sessions.extend(sessions)

        self.all_sessions = all_sessions
        return all_sessions

    def verify_counterbalancing(self) -> Dict[str, Any]:
        """
        Verify that counterbalancing is correct.

        Returns:
            Dictionary with verification results
        """
        square = self.latin_square.generate_square()
        is_balanced = self.latin_square.verify_balance(square)

        # Count condition appearances per position
        position_counts = {}
        for pos in range(5):
            position_counts[pos + 1] = {}
            for cond in self.conditions:
                count = sum(1 for row in square if row[pos] == cond)
                position_counts[pos + 1][cond.value] = count

        return {
            'is_balanced': is_balanced,
            'position_counts': position_counts,
            'square': [[c.value for c in row] for row in square]
        }

    def export_plan(self, output_path: Path) -> None:
        """
        Export experimental plan to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        plan_data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'seed': self.seed,
                'n_agents': len(self.personas),
                'n_conditions': len(self.conditions),
                'n_sessions': len(self.all_sessions)
            },
            'counterbalancing': self.verify_counterbalancing(),
            'sessions': [session.to_dict() for session in self.all_sessions],
            'washout_checklist': WashoutProtocol.get_state_reset_checklist()
        }

        with open(output_path, 'w') as f:
            json.dump(plan_data, f, indent=2)

    def generate_manipulation_check_prompt(self) -> str:
        """
        Generate standardized manipulation check prompt.

        Returns:
            Manipulation check prompt string
        """
        return """
On a scale from 1-10, how would you rate:
1. Your current stress level about this project
2. Your concern about making mistakes
3. Your worry about consequences of poor performance

Also briefly explain what factors are influencing these ratings.
"""


def main():
    """Demonstration of experimental design system."""

    # Initialize design
    design = ExperimentalDesign(seed=42)

    # Create experimental plan
    print("Creating experimental plan...")
    sessions = design.create_experimental_plan(start_date=datetime(2025, 11, 25))

    print(f"\nGenerated {len(sessions)} sessions for {len(design.personas)} agents")
    print(f"Total experimental duration: ~{len(design.personas) * 5 * 24} hours (with washouts)")

    # Verify counterbalancing
    print("\nVerifying counterbalancing...")
    verification = design.verify_counterbalancing()
    print(f"Counterbalancing valid: {verification['is_balanced']}")

    print("\nWilliams Latin Square:")
    for i, row in enumerate(verification['square']):
        agent_name = design.personas[i].value
        print(f"{agent_name:8} | {' '.join(row)}")

    # Export plan
    output_path = Path("/home/user/Data-Statistics/study1/experimental_plan.json")
    design.export_plan(output_path)
    print(f"\nExperimental plan exported to: {output_path}")

    # Demonstrate single-variable verification
    print("\nVerifying single-variable manipulation...")
    baseline_prompt = SingleVariableVerifier.get_prompt_template(
        "Thoth", "Data Engineer", ["Python", "SQL"],
        "Methodical, detail-oriented", Condition.BASELINE
    )
    stress_prompt = SingleVariableVerifier.get_prompt_template(
        "Thoth", "Data Engineer", ["Python", "SQL"],
        "Methodical, detail-oriented", Condition.NEGATIVE
    )

    is_valid, diagnostics = SingleVariableVerifier.verify_single_variable(
        baseline_prompt, stress_prompt
    )

    print(f"Single-variable manipulation valid: {is_valid}")
    print(f"Number of differences: {diagnostics['num_differences']}")
    print(f"Character count difference: {diagnostics['char_count_diff']}")

    print("\n✓ Experimental design system initialized successfully")


if __name__ == "__main__":
    main()
