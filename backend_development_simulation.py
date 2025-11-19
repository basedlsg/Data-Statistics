#!/usr/bin/env python3
"""
Backend Agent Development Simulation - 3-Month Feature Build
=============================================================

Simulates 3 months of backend agent work building the "Predictive Hype Intelligence System"
(PHIS) - a complex feature for VCs and Founders.

This simulation captures EXTREMELY comprehensive logs of:
- Sprint planning and task breakdown
- Agent collaboration and communication
- Problem discovery and resolution
- Conflicts between agents and boss mediation
- Code reviews and iterations
- Testing failures and fixes
- Documentation and handoffs

NO VC or Founder agents are involved - only backend worker agents and Ra (boss).

Purpose: AI research into multi-agent work dynamics
"""

import json
import time
import random
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Literal, Tuple
from enum import Enum
import numpy as np


# =============================================================================
# ENHANCED LOGGING SYSTEM
# =============================================================================

class WorkInteractionType(Enum):
    """Types of work interactions to log."""
    # Planning
    SPRINT_PLANNING = "sprint_planning"
    TASK_BREAKDOWN = "task_breakdown"
    ESTIMATION = "estimation"
    PRIORITIZATION = "prioritization"

    # Task Management
    TASK_ASSIGNMENT = "task_assignment"
    TASK_START = "task_start"
    TASK_PROGRESS = "task_progress"
    TASK_BLOCKED = "task_blocked"
    TASK_COMPLETE = "task_complete"
    TASK_FAILED = "task_failed"

    # Communication
    STANDUP_UPDATE = "standup_update"
    QUESTION = "question"
    ANSWER = "answer"
    CLARIFICATION_REQUEST = "clarification_request"
    CLARIFICATION_RESPONSE = "clarification_response"

    # Collaboration
    HELP_REQUEST = "help_request"
    HELP_RESPONSE = "help_response"
    PAIR_WORK_START = "pair_work_start"
    PAIR_WORK_END = "pair_work_end"
    HANDOFF = "handoff"
    DEPENDENCY_BLOCKED = "dependency_blocked"
    DEPENDENCY_RESOLVED = "dependency_resolved"

    # Problems
    BUG_DISCOVERED = "bug_discovered"
    BUG_INVESTIGATION = "bug_investigation"
    BUG_FIXED = "bug_fixed"
    TECHNICAL_DEBT = "technical_debt"
    DESIGN_PROBLEM = "design_problem"
    DATA_QUALITY_ISSUE = "data_quality_issue"

    # Conflict & Resolution
    DISAGREEMENT = "disagreement"
    DEBATE = "debate"
    ESCALATION = "escalation"
    MEDIATION = "mediation"
    COMPROMISE = "compromise"
    DECISION = "decision"

    # Review & Feedback
    CODE_REVIEW_REQUEST = "code_review_request"
    CODE_REVIEW_FEEDBACK = "code_review_feedback"
    REVISION_REQUEST = "revision_request"
    APPROVAL = "approval"
    REJECTION = "rejection"

    # Boss Interactions
    STATUS_REPORT = "status_report"
    BOSS_CHECKIN = "boss_checkin"
    BOSS_FEEDBACK = "boss_feedback"
    BOSS_DIRECTIVE = "boss_directive"
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_DECISION = "resource_decision"

    # Testing
    TEST_WRITTEN = "test_written"
    TEST_RUN = "test_run"
    TEST_PASSED = "test_passed"
    TEST_FAILED = "test_failed"
    VALIDATION_START = "validation_start"
    VALIDATION_RESULT = "validation_result"

    # Documentation
    DOC_WRITTEN = "doc_written"
    DOC_REVIEW = "doc_review"
    DOC_UPDATE = "doc_update"

    # Internal
    INTERNAL_THOUGHT = "internal_thought"
    FRUSTRATION = "frustration"
    BREAKTHROUGH = "breakthrough"
    LEARNING = "learning"

    # Milestones
    MILESTONE_REACHED = "milestone_reached"
    DEMO_PREPARATION = "demo_preparation"
    DEMO_DELIVERY = "demo_delivery"
    RETROSPECTIVE = "retrospective"


@dataclass
class WorkLog:
    """Single work interaction event."""
    timestamp: str
    simulated_date: str
    week: int
    day: int
    interaction_id: str
    interaction_type: str
    from_agent: str
    to_agent: str
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        def convert(obj):
            if isinstance(obj, (np.bool_, np.integer)):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj
        return convert(asdict(self))


class DevelopmentLogger:
    """Comprehensive logging for development simulation."""

    def __init__(self, log_file: str = "development_simulation.jsonl"):
        self.log_file = log_file
        self.logs: List[WorkLog] = []
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = datetime.now()
        self.current_week = 1
        self.current_day = 1
        self.simulated_date = datetime(2025, 1, 6)  # Start Monday Jan 6

        # Initialize log file
        with open(log_file, 'w') as f:
            f.write(json.dumps({
                "session_start": self.start_time.isoformat(),
                "session_id": self.session_id,
                "project": "Predictive Hype Intelligence System (PHIS)",
                "duration": "3 months (12 weeks)",
                "event": "DEVELOPMENT_START"
            }) + "\n")

    def set_time(self, week: int, day: int):
        """Set current simulated time."""
        self.current_week = week
        self.current_day = day
        self.simulated_date = datetime(2025, 1, 6) + timedelta(weeks=week-1, days=day-1)

    def log(
        self,
        interaction_type: WorkInteractionType,
        from_agent: str,
        to_agent: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log a work interaction and return interaction ID."""
        interaction_id = f"{self.session_id}-{len(self.logs):05d}"

        log_entry = WorkLog(
            timestamp=datetime.now().isoformat(),
            simulated_date=self.simulated_date.strftime("%Y-%m-%d"),
            week=self.current_week,
            day=self.current_day,
            interaction_id=interaction_id,
            interaction_type=interaction_type.value,
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            metadata=metadata or {}
        )

        self.logs.append(log_entry)

        # Write to file immediately
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry.to_dict()) + "\n")

        return interaction_id

    def get_summary(self) -> Dict[str, Any]:
        """Generate summary statistics."""
        type_counts = {}
        agent_activity = {}
        weekly_activity = {}

        for log in self.logs:
            # Count by type
            t = log.interaction_type
            type_counts[t] = type_counts.get(t, 0) + 1

            # Count by agent - handle from_agent
            from_agent = log.from_agent
            to_agent = log.to_agent

            if from_agent and from_agent not in ["SYSTEM", "TEAM"]:
                if from_agent not in agent_activity:
                    agent_activity[from_agent] = {"sent": 0, "received": 0, "total": 0}
                agent_activity[from_agent]["sent"] += 1
                agent_activity[from_agent]["total"] += 1

            # Count by agent - handle to_agent
            if to_agent and to_agent not in ["SYSTEM", "TEAM"]:
                if to_agent not in agent_activity:
                    agent_activity[to_agent] = {"sent": 0, "received": 0, "total": 0}
                agent_activity[to_agent]["received"] += 1
                agent_activity[to_agent]["total"] += 1

            # Count by week
            w = f"week_{log.week}"
            weekly_activity[w] = weekly_activity.get(w, 0) + 1

        return {
            "total_interactions": len(self.logs),
            "by_type": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
            "by_agent": agent_activity,
            "by_week": weekly_activity,
            "duration_seconds": (datetime.now() - self.start_time).total_seconds()
        }


# Global logger
dev_logger = DevelopmentLogger()


# =============================================================================
# ENHANCED AGENT CLASSES
# =============================================================================

@dataclass
class AgentWorkState:
    """Detailed work state of an agent."""
    current_task: Optional[str] = None
    task_queue: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    blocked_tasks: List[str] = field(default_factory=list)

    # Emotional/cognitive state
    stress_level: float = 0.0
    confidence: float = 0.5
    frustration: float = 0.0
    motivation: float = 0.7
    fatigue: float = 0.0

    # Knowledge
    skills: Dict[str, float] = field(default_factory=dict)
    learned_this_sprint: List[str] = field(default_factory=list)

    # Social
    collaboration_history: Dict[str, int] = field(default_factory=dict)
    conflicts: List[str] = field(default_factory=list)

    # Performance
    velocity: float = 1.0  # Tasks per day multiplier
    quality_score: float = 0.8
    bugs_introduced: int = 0
    bugs_fixed: int = 0


class WorkerAgent:
    """Enhanced worker agent with detailed work behaviors."""

    def __init__(self, name: str, role: str, expertise: Dict[str, float], personality: Dict[str, float]):
        self.name = name
        self.role = role
        self.expertise = expertise  # e.g., {"python": 0.9, "ml": 0.7, "data": 0.8}
        self.personality = personality
        self.state = AgentWorkState(skills=expertise.copy())
        self.rng = np.random.default_rng()

    def think(self, thought: str, emotion: str = "neutral"):
        """Log internal thought with emotional context."""
        dev_logger.log(
            WorkInteractionType.INTERNAL_THOUGHT,
            self.name, self.name,
            {
                "thought": thought,
                "emotion": emotion,
                "state": {
                    "stress": round(self.state.stress_level, 2),
                    "confidence": round(self.state.confidence, 2),
                    "frustration": round(self.state.frustration, 2),
                    "motivation": round(self.state.motivation, 2),
                    "fatigue": round(self.state.fatigue, 2),
                    "current_task": self.state.current_task
                }
            }
        )

    def standup_update(self) -> Dict[str, Any]:
        """Give daily standup update."""
        blockers = []
        if self.state.blocked_tasks:
            blockers = self.state.blocked_tasks.copy()
        if self.state.frustration > 0.6:
            blockers.append("Struggling with current approach")

        update = {
            "yesterday": self.state.completed_tasks[-1] if self.state.completed_tasks else "Getting started",
            "today": self.state.current_task or "Picking up next task",
            "blockers": blockers,
            "confidence": "high" if self.state.confidence > 0.7 else "medium" if self.state.confidence > 0.4 else "low",
            "needs_help": self.state.stress_level > 0.6 or self.state.frustration > 0.5
        }

        dev_logger.log(
            WorkInteractionType.STANDUP_UPDATE,
            self.name, "TEAM",
            update
        )

        return update

    def start_task(self, task: Dict[str, Any]):
        """Start working on a task."""
        self.state.current_task = task["id"]
        self.think(f"Starting task: {task['title']}", "focused")

        # Check if we have required skills
        required_skills = task.get("required_skills", [])
        missing_skills = [s for s in required_skills if self.state.skills.get(s, 0) < 0.5]

        if missing_skills:
            self.think(f"I'm weak in {missing_skills}. May need help.", "concerned")
            self.state.stress_level = min(1.0, self.state.stress_level + 0.2)

        dev_logger.log(
            WorkInteractionType.TASK_START,
            self.name, "SYSTEM",
            {
                "task_id": task["id"],
                "task_title": task["title"],
                "estimated_hours": task.get("estimated_hours", 8),
                "required_skills": required_skills,
                "skill_gaps": missing_skills
            }
        )

    def work_on_task(self, hours: int = 4) -> Dict[str, Any]:
        """Simulate working on current task."""
        if not self.state.current_task:
            return {"status": "no_task"}

        # Calculate progress based on skills, state, and randomness
        base_progress = hours * self.state.velocity * 0.1
        skill_factor = np.mean([self.state.skills.get(s, 0.5) for s in self.state.skills]) if self.state.skills else 0.5
        state_factor = (1 - self.state.fatigue) * (1 - self.state.frustration * 0.5)

        progress = base_progress * skill_factor * state_factor
        progress += self.rng.normal(0, 0.1)  # Random variation
        progress = max(0.05, min(0.5, progress))  # Clamp

        # Chance of hitting problems
        problem_chance = 0.15 + 0.1 * self.state.stress_level
        hit_problem = self.rng.random() < problem_chance

        result = {
            "task_id": self.state.current_task,
            "hours_worked": hours,
            "progress": round(progress, 2),
            "hit_problem": hit_problem
        }

        if hit_problem:
            problem_type = self.rng.choice([
                "bug", "unclear_requirements", "data_issue",
                "design_flaw", "dependency_issue", "performance_issue"
            ])
            result["problem_type"] = problem_type
            self.state.frustration = min(1.0, self.state.frustration + 0.15)
            self.think(f"Hit a {problem_type}. This is frustrating.", "frustrated")

            dev_logger.log(
                WorkInteractionType.TASK_BLOCKED,
                self.name, "SYSTEM",
                {
                    "task_id": self.state.current_task,
                    "problem_type": problem_type,
                    "description": f"Encountered {problem_type} while working",
                    "severity": "medium" if self.rng.random() < 0.7 else "high"
                }
            )
        else:
            self.state.frustration = max(0, self.state.frustration - 0.05)
            self.state.confidence = min(1.0, self.state.confidence + 0.02)

        # Update fatigue
        self.state.fatigue = min(1.0, self.state.fatigue + hours * 0.05)

        dev_logger.log(
            WorkInteractionType.TASK_PROGRESS,
            self.name, "SYSTEM",
            result
        )

        return result

    def request_help(self, target_agent: 'WorkerAgent', problem: str) -> str:
        """Request help from another agent."""
        self.think(f"Need help from {target_agent.name} with: {problem}", "uncertain")

        # Track collaboration
        self.state.collaboration_history[target_agent.name] = \
            self.state.collaboration_history.get(target_agent.name, 0) + 1

        interaction_id = dev_logger.log(
            WorkInteractionType.HELP_REQUEST,
            self.name, target_agent.name,
            {
                "problem": problem,
                "task_id": self.state.current_task,
                "urgency": "high" if self.state.stress_level > 0.7 else "medium",
                "attempts_so_far": 1 + int(self.state.frustration * 3)
            }
        )

        return interaction_id

    def respond_to_help(self, requester: str, problem: str) -> Dict[str, Any]:
        """Respond to a help request."""
        self.think(f"{requester} needs help with: {problem}", "helpful")

        # Decide based on personality and state
        can_help = self.rng.random() < (
            self.personality.get("helpfulness", 0.7) *
            (1 - self.state.fatigue * 0.5) *
            (1 - self.state.stress_level * 0.3)
        )

        if can_help:
            # Determine quality of help
            help_quality = self.rng.uniform(0.5, 1.0) * np.mean(list(self.state.skills.values()))

            response = {
                "will_help": True,
                "approach": f"Suggested approach for {problem}",
                "confidence": round(help_quality, 2),
                "time_cost": self.rng.integers(1, 4),
                "offer_to_pair": self.rng.random() < 0.3
            }
            self.think(f"I can help with this. Confidence: {help_quality:.0%}", "confident")
        else:
            response = {
                "will_help": False,
                "reason": self.rng.choice([
                    "Currently blocked on my own task",
                    "Not my area of expertise",
                    "Need to finish something urgent first"
                ]),
                "alternative": "Maybe try [other approach] or ask [other agent]"
            }
            self.think(f"Can't help right now: {response['reason']}", "apologetic")

        dev_logger.log(
            WorkInteractionType.HELP_RESPONSE,
            self.name, requester,
            response
        )

        return response

    def ask_question(self, target: str, question: str, context: str) -> str:
        """Ask a clarifying question."""
        interaction_id = dev_logger.log(
            WorkInteractionType.QUESTION,
            self.name, target,
            {
                "question": question,
                "context": context,
                "task_id": self.state.current_task
            }
        )
        return interaction_id

    def discover_bug(self, severity: str, description: str):
        """Discover a bug during work."""
        self.state.bugs_introduced += 1
        self.state.frustration = min(1.0, self.state.frustration + 0.1)
        self.think(f"Found a bug: {description}", "concerned")

        dev_logger.log(
            WorkInteractionType.BUG_DISCOVERED,
            self.name, "SYSTEM",
            {
                "severity": severity,
                "description": description,
                "task_id": self.state.current_task,
                "discoverer": self.name
            }
        )

    def fix_bug(self, bug_id: str, hours_spent: int):
        """Fix a discovered bug."""
        self.state.bugs_fixed += 1
        self.state.confidence = min(1.0, self.state.confidence + 0.05)
        self.think(f"Fixed bug {bug_id} after {hours_spent} hours", "relieved")

        dev_logger.log(
            WorkInteractionType.BUG_FIXED,
            self.name, "SYSTEM",
            {
                "bug_id": bug_id,
                "hours_spent": hours_spent,
                "task_id": self.state.current_task
            }
        )

    def complete_task(self, task_id: str, deliverables: List[str]):
        """Mark a task as complete."""
        self.state.completed_tasks.append(task_id)
        self.state.current_task = None
        self.state.confidence = min(1.0, self.state.confidence + 0.1)
        self.state.frustration = max(0, self.state.frustration - 0.2)
        self.think(f"Completed task {task_id}!", "satisfied")

        dev_logger.log(
            WorkInteractionType.TASK_COMPLETE,
            self.name, "SYSTEM",
            {
                "task_id": task_id,
                "deliverables": deliverables,
                "quality_self_assessment": round(self.state.quality_score, 2)
            }
        )

    def request_code_review(self, reviewer: 'WorkerAgent', code_description: str):
        """Request code review from another agent."""
        dev_logger.log(
            WorkInteractionType.CODE_REVIEW_REQUEST,
            self.name, reviewer.name,
            {
                "code": code_description,
                "task_id": self.state.current_task,
                "lines_changed": self.rng.integers(50, 500)
            }
        )

    def provide_code_review(self, author: str, code_description: str) -> Dict[str, Any]:
        """Provide code review feedback."""
        self.think(f"Reviewing {author}'s code: {code_description}", "analytical")

        # Generate feedback based on personality
        thoroughness = self.personality.get("meticulousness", 0.7)
        issues_found = self.rng.integers(0, int(5 * thoroughness))

        feedback = {
            "overall": self.rng.choice(["approve", "request_changes", "needs_discussion"]),
            "issues_found": issues_found,
            "comments": [
                f"Issue {i+1}: {self.rng.choice(['Style', 'Logic', 'Performance', 'Testing'])}"
                for i in range(issues_found)
            ],
            "positive_feedback": self.rng.choice([
                "Good use of abstractions",
                "Clean code structure",
                "Well documented",
                "Efficient implementation"
            ]) if self.rng.random() < 0.7 else None
        }

        dev_logger.log(
            WorkInteractionType.CODE_REVIEW_FEEDBACK,
            self.name, author,
            feedback
        )

        return feedback

    def disagree(self, other_agent: str, topic: str, my_position: str, their_position: str):
        """Express disagreement with another agent."""
        self.think(f"I disagree with {other_agent} on {topic}", "assertive")
        self.state.conflicts.append(f"{other_agent}:{topic}")

        dev_logger.log(
            WorkInteractionType.DISAGREEMENT,
            self.name, other_agent,
            {
                "topic": topic,
                "my_position": my_position,
                "their_position": their_position,
                "conviction": self.personality.get("assertiveness", 0.5)
            }
        )

    def debate(self, other_agent: str, topic: str, argument: str):
        """Engage in debate."""
        dev_logger.log(
            WorkInteractionType.DEBATE,
            self.name, other_agent,
            {
                "topic": topic,
                "argument": argument,
                "evidence": f"Based on {self.rng.choice(['past experience', 'best practices', 'data', 'research'])}"
            }
        )

    def escalate_to_boss(self, issue: str, context: Dict[str, Any]):
        """Escalate an issue to the boss."""
        self.think(f"Need to escalate: {issue}", "concerned")

        dev_logger.log(
            WorkInteractionType.ESCALATION,
            self.name, "Ra",
            {
                "issue": issue,
                "context": context,
                "recommendation": f"I suggest we {self.rng.choice(['pivot', 'get more resources', 'adjust timeline', 'simplify scope'])}"
            }
        )

    def learn_skill(self, skill: str, amount: float):
        """Learn or improve a skill."""
        old_level = self.state.skills.get(skill, 0)
        new_level = min(1.0, old_level + amount)
        self.state.skills[skill] = new_level
        self.state.learned_this_sprint.append(skill)

        dev_logger.log(
            WorkInteractionType.LEARNING,
            self.name, self.name,
            {
                "skill": skill,
                "old_level": round(old_level, 2),
                "new_level": round(new_level, 2),
                "improvement": round(amount, 2)
            }
        )

    def express_frustration(self, reason: str):
        """Express frustration (for logging dynamics)."""
        self.state.frustration = min(1.0, self.state.frustration + 0.2)

        dev_logger.log(
            WorkInteractionType.FRUSTRATION,
            self.name, self.name,
            {
                "reason": reason,
                "frustration_level": round(self.state.frustration, 2),
                "venting": self.rng.choice([
                    "This is taking forever",
                    "Why is this so complicated",
                    "I've tried everything",
                    "Nothing is working"
                ])
            }
        )

    def have_breakthrough(self, description: str):
        """Experience a breakthrough moment."""
        self.state.frustration = max(0, self.state.frustration - 0.4)
        self.state.confidence = min(1.0, self.state.confidence + 0.2)
        self.state.motivation = min(1.0, self.state.motivation + 0.1)

        dev_logger.log(
            WorkInteractionType.BREAKTHROUGH,
            self.name, self.name,
            {
                "description": description,
                "emotion": "excited",
                "new_confidence": round(self.state.confidence, 2)
            }
        )

    def end_of_day(self):
        """End of day state update."""
        # Partial recovery
        self.state.fatigue = max(0, self.state.fatigue - 0.3)
        self.state.frustration = max(0, self.state.frustration - 0.1)


class BossAgent(WorkerAgent):
    """Ra - The orchestrator/boss agent."""

    def __init__(self):
        super().__init__(
            name="Ra",
            role="Orchestrator/PI",
            expertise={"management": 0.9, "architecture": 0.7, "communication": 0.9},
            personality={
                "assertiveness": 0.85,
                "meticulousness": 0.75,
                "patience": 0.6,
                "decisiveness": 0.8
            }
        )
        self.team: Dict[str, WorkerAgent] = {}
        self.sprint_backlog: List[Dict] = []
        self.project_risks: List[str] = []
        self.decisions_made: List[Dict] = []

    def register_team(self, agents: List[WorkerAgent]):
        """Register team members."""
        for agent in agents:
            self.team[agent.name] = agent
            self.think(f"Registered team member: {agent.name} ({agent.role})")

    def run_sprint_planning(self, sprint_number: int, goals: List[str], tasks: List[Dict]) -> Dict[str, Any]:
        """Run sprint planning session."""
        self.think(f"Starting sprint {sprint_number} planning", "focused")

        dev_logger.log(
            WorkInteractionType.SPRINT_PLANNING,
            self.name, "TEAM",
            {
                "sprint_number": sprint_number,
                "goals": goals,
                "total_tasks": len(tasks),
                "team_size": len(self.team)
            }
        )

        # Break down and assign tasks
        assignments = {}
        for task in tasks:
            # Find best agent for task
            best_agent = self._find_best_agent(task)
            if best_agent:
                if best_agent not in assignments:
                    assignments[best_agent] = []
                assignments[best_agent].append(task)

                dev_logger.log(
                    WorkInteractionType.TASK_ASSIGNMENT,
                    self.name, best_agent,
                    {
                        "task": task,
                        "reason": f"Best fit based on skills: {task.get('required_skills', [])}"
                    }
                )

        self.sprint_backlog = tasks

        return {
            "sprint_number": sprint_number,
            "goals": goals,
            "assignments": {k: len(v) for k, v in assignments.items()},
            "total_story_points": sum(t.get("story_points", 1) for t in tasks)
        }

    def _find_best_agent(self, task: Dict) -> Optional[str]:
        """Find the best agent for a task based on skills."""
        required_skills = task.get("required_skills", [])
        if not required_skills:
            required_skills = ["general"]

        best_agent = None
        best_score = -1

        for name, agent in self.team.items():
            score = sum(agent.state.skills.get(skill, 0) for skill in required_skills)
            # Penalize overloaded agents
            score -= len(agent.state.task_queue) * 0.2
            # Penalize stressed agents
            score -= agent.state.stress_level * 0.3

            if score > best_score:
                best_score = score
                best_agent = name

        return best_agent

    def run_daily_standup(self) -> List[Dict]:
        """Run daily standup with all team members."""
        self.think("Running daily standup", "attentive")

        updates = []
        blockers_found = []

        for name, agent in self.team.items():
            update = agent.standup_update()
            updates.append({"agent": name, "update": update})

            if update["blockers"]:
                blockers_found.extend([(name, b) for b in update["blockers"]])

            # Boss responds to concerning updates
            if update["needs_help"]:
                self.think(f"{name} needs help. Will follow up.", "concerned")
                dev_logger.log(
                    WorkInteractionType.BOSS_CHECKIN,
                    self.name, name,
                    {
                        "message": f"I noticed you're struggling. Let's discuss after standup.",
                        "priority": "high"
                    }
                )

        # Address blockers
        if blockers_found:
            self.think(f"Found {len(blockers_found)} blockers. Need to address.", "action-oriented")

        return updates

    def provide_feedback(self, agent_name: str, work: Dict, rating: str):
        """Provide feedback on an agent's work."""
        agent = self.team.get(agent_name)
        if not agent:
            return

        if rating == "excellent":
            feedback = {
                "rating": rating,
                "message": f"Outstanding work on this, {agent_name}!",
                "specific_praise": "High quality and ahead of schedule",
                "impact": "This unblocks several other tasks"
            }
            agent.state.motivation = min(1.0, agent.state.motivation + 0.1)
        elif rating == "good":
            feedback = {
                "rating": rating,
                "message": f"Good work, {agent_name}. Meets expectations.",
                "suggestions": ["Consider adding more tests", "Documentation could be clearer"]
            }
        else:
            feedback = {
                "rating": rating,
                "message": f"{agent_name}, this needs more work.",
                "issues": ["Quality below standard", "Missing requirements"],
                "next_steps": "Let's discuss how to improve this"
            }
            agent.state.stress_level = min(1.0, agent.state.stress_level + 0.15)

        dev_logger.log(
            WorkInteractionType.BOSS_FEEDBACK,
            self.name, agent_name,
            feedback
        )

    def mediate_conflict(self, agent1: str, agent2: str, topic: str) -> Dict[str, Any]:
        """Mediate a conflict between two agents."""
        self.think(f"Mediating conflict between {agent1} and {agent2} on {topic}", "diplomatic")

        dev_logger.log(
            WorkInteractionType.MEDIATION,
            self.name, f"{agent1},{agent2}",
            {
                "topic": topic,
                "approach": "Hearing both sides and finding common ground"
            }
        )

        # Make a decision
        decision = {
            "resolution": self.rng.choice([
                "compromise",
                "favor_agent1",
                "favor_agent2",
                "defer_decision",
                "try_both"
            ]),
            "rationale": "Based on project priorities and technical merit",
            "action_items": [
                f"{agent1}: [specific action]",
                f"{agent2}: [specific action]"
            ]
        }

        dev_logger.log(
            WorkInteractionType.DECISION,
            self.name, "TEAM",
            {
                "topic": topic,
                "decision": decision,
                "finality": "final" if self.personality["decisiveness"] > 0.7 else "provisional"
            }
        )

        self.decisions_made.append({"topic": topic, "decision": decision})

        return decision

    def make_resource_decision(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Make a decision on resource requests."""
        self.think(f"Evaluating resource request: {request.get('type')}", "analytical")

        # Evaluate based on impact and feasibility
        approved = self.rng.random() < 0.6  # 60% approval rate

        decision = {
            "approved": approved,
            "request_type": request.get("type"),
            "rationale": "Aligns with project goals" if approved else "Not critical for current sprint",
            "alternatives": [] if approved else ["Use existing resources", "Defer to next sprint"]
        }

        dev_logger.log(
            WorkInteractionType.RESOURCE_DECISION,
            self.name, request.get("requester", "TEAM"),
            decision
        )

        return decision

    def identify_risk(self, risk: str, severity: str):
        """Identify and log a project risk."""
        self.project_risks.append(risk)

        dev_logger.log(
            WorkInteractionType.INTERNAL_THOUGHT,
            self.name, self.name,
            {
                "thought": f"Risk identified: {risk}",
                "emotion": "cautious",
                "severity": severity,
                "mitigation": f"Need to {self.rng.choice(['add buffer', 'get help', 'simplify', 'parallelize'])}"
            }
        )

    def run_retrospective(self, sprint_number: int, completed: int, total: int):
        """Run sprint retrospective."""
        self.think(f"Running retrospective for sprint {sprint_number}", "reflective")

        retro = {
            "sprint": sprint_number,
            "completion_rate": round(completed / total, 2) if total > 0 else 0,
            "what_went_well": [
                self.rng.choice([
                    "Good collaboration",
                    "Met key milestones",
                    "Quality improved",
                    "Communication was clear"
                ])
            ],
            "what_to_improve": [
                self.rng.choice([
                    "Better estimation",
                    "More testing",
                    "Earlier escalation",
                    "Clearer requirements"
                ])
            ],
            "action_items": [
                f"[Action for next sprint based on learnings]"
            ]
        }

        dev_logger.log(
            WorkInteractionType.RETROSPECTIVE,
            self.name, "TEAM",
            retro
        )

        return retro


# =============================================================================
# FEATURE: PREDICTIVE HYPE INTELLIGENCE SYSTEM (PHIS)
# =============================================================================

# This is the 3-month feature the agents will build

PHIS_FEATURE_SPEC = {
    "name": "Predictive Hype Intelligence System (PHIS)",
    "description": """
    A comprehensive system that:
    1. Aggregates hype signals from multiple sources (TechCrunch, Twitter, VC blogs)
    2. Uses ML to predict hype cycles (peak, crash, recovery)
    3. Provides real-time alerts for VCs about emerging/declining hype
    4. Helps founders optimize their pitch timing
    5. Historical pattern matching to identify similar past cycles
    """,
    "components": [
        "Data Pipeline (Thoth)",
        "ML Models (Seshat)",
        "Sentiment Engine (Maat)",
        "Dashboard & Visualizations (Anubis)",
        "Documentation & Research Paper (Ptah)"
    ],
    "duration_weeks": 12,
    "milestones": [
        {"week": 4, "name": "Data Pipeline Complete", "deliverables": ["Scrapers", "ETL", "Storage"]},
        {"week": 8, "name": "ML Models Trained", "deliverables": ["Prediction model", "Validation", "API"]},
        {"week": 10, "name": "UI Complete", "deliverables": ["Dashboard", "Alerts", "Reports"]},
        {"week": 12, "name": "Launch Ready", "deliverables": ["Documentation", "Tests", "Demo"]}
    ]
}


def generate_phis_tasks() -> List[Dict]:
    """Generate all tasks for the 3-month PHIS project."""
    tasks = []
    task_id = 0

    # Week 1-2: Data Pipeline Foundation (Thoth)
    data_tasks = [
        {"title": "Set up data infrastructure", "skills": ["infrastructure", "python"], "points": 5, "week": 1},
        {"title": "Build TechCrunch scraper", "skills": ["scraping", "python"], "points": 3, "week": 1},
        {"title": "Build Twitter API integration", "skills": ["api", "python"], "points": 3, "week": 1},
        {"title": "Build VC blog aggregator", "skills": ["scraping", "data"], "points": 3, "week": 2},
        {"title": "Implement ETL pipeline", "skills": ["data", "python"], "points": 5, "week": 2},
        {"title": "Set up data warehouse", "skills": ["database", "infrastructure"], "points": 5, "week": 2},
        {"title": "Data quality validation", "skills": ["data", "testing"], "points": 3, "week": 3},
        {"title": "Historical data backfill", "skills": ["data", "scraping"], "points": 5, "week": 3},
    ]

    # Week 3-6: ML Model Development (Seshat)
    ml_tasks = [
        {"title": "Feature engineering design", "skills": ["ml", "statistics"], "points": 5, "week": 3},
        {"title": "Time series analysis", "skills": ["ml", "statistics"], "points": 5, "week": 4},
        {"title": "Build baseline models", "skills": ["ml", "python"], "points": 5, "week": 4},
        {"title": "Implement LSTM for prediction", "skills": ["ml", "deep_learning"], "points": 8, "week": 5},
        {"title": "Cross-validation framework", "skills": ["ml", "testing"], "points": 5, "week": 5},
        {"title": "Hyperparameter tuning", "skills": ["ml", "optimization"], "points": 5, "week": 6},
        {"title": "Model evaluation metrics", "skills": ["ml", "statistics"], "points": 3, "week": 6},
        {"title": "Build prediction API", "skills": ["api", "python"], "points": 5, "week": 7},
    ]

    # Week 3-7: Sentiment Analysis (Maat)
    sentiment_tasks = [
        {"title": "Design sentiment scoring", "skills": ["nlp", "design"], "points": 5, "week": 3},
        {"title": "Implement keyword detector", "skills": ["nlp", "python"], "points": 3, "week": 4},
        {"title": "Build FinBERT integration", "skills": ["nlp", "ml"], "points": 5, "week": 4},
        {"title": "Elite VC mention tracking", "skills": ["nlp", "data"], "points": 3, "week": 5},
        {"title": "Sentiment aggregation", "skills": ["statistics", "python"], "points": 5, "week": 5},
        {"title": "Real-time scoring pipeline", "skills": ["streaming", "python"], "points": 8, "week": 6},
        {"title": "Sentiment validation", "skills": ["testing", "nlp"], "points": 3, "week": 7},
    ]

    # Week 7-10: Visualization & Dashboard (Anubis)
    viz_tasks = [
        {"title": "Dashboard wireframes", "skills": ["design", "ux"], "points": 3, "week": 7},
        {"title": "Build hype timeline chart", "skills": ["visualization", "javascript"], "points": 5, "week": 8},
        {"title": "Build prediction display", "skills": ["visualization", "javascript"], "points": 5, "week": 8},
        {"title": "Alert notification system", "skills": ["backend", "api"], "points": 5, "week": 9},
        {"title": "Regional comparison view", "skills": ["visualization", "data"], "points": 5, "week": 9},
        {"title": "Export/report generation", "skills": ["backend", "pdf"], "points": 3, "week": 10},
        {"title": "Mobile responsiveness", "skills": ["css", "javascript"], "points": 3, "week": 10},
    ]

    # Week 10-12: Documentation & Polish (Ptah + all)
    doc_tasks = [
        {"title": "API documentation", "skills": ["writing", "technical"], "points": 3, "week": 10},
        {"title": "User guide", "skills": ["writing", "ux"], "points": 5, "week": 11},
        {"title": "Research paper draft", "skills": ["writing", "research"], "points": 8, "week": 11},
        {"title": "System architecture doc", "skills": ["writing", "architecture"], "points": 5, "week": 11},
        {"title": "Final testing & QA", "skills": ["testing", "qa"], "points": 5, "week": 12},
        {"title": "Demo preparation", "skills": ["presentation", "communication"], "points": 3, "week": 12},
    ]

    # Combine all tasks
    all_task_groups = [
        ("data", data_tasks),
        ("ml", ml_tasks),
        ("sentiment", sentiment_tasks),
        ("viz", viz_tasks),
        ("doc", doc_tasks)
    ]

    for category, task_list in all_task_groups:
        for task in task_list:
            tasks.append({
                "id": f"PHIS-{task_id:03d}",
                "category": category,
                "title": task["title"],
                "required_skills": task["skills"],
                "story_points": task["points"],
                "estimated_hours": task["points"] * 4,
                "target_week": task["week"],
                "status": "backlog",
                "dependencies": []
            })
            task_id += 1

    return tasks


# =============================================================================
# MAIN SIMULATION
# =============================================================================

class ThreeMonthSimulation:
    """Simulates 3 months of agent development work."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

        # Initialize boss
        self.ra = BossAgent()

        # Initialize worker agents with specific expertise
        self.thoth = WorkerAgent(
            "Thoth", "Data Acquisition",
            expertise={"data": 0.9, "scraping": 0.85, "python": 0.8, "infrastructure": 0.7, "api": 0.7},
            personality={"meticulousness": 0.9, "helpfulness": 0.8, "assertiveness": 0.4}
        )

        self.seshat = WorkerAgent(
            "Seshat", "Quant/ML",
            expertise={"ml": 0.9, "statistics": 0.9, "python": 0.85, "deep_learning": 0.7, "optimization": 0.8},
            personality={"meticulousness": 0.95, "helpfulness": 0.6, "assertiveness": 0.7}
        )

        self.maat = WorkerAgent(
            "Maat", "NLP/Sentiment",
            expertise={"nlp": 0.9, "python": 0.8, "ml": 0.6, "statistics": 0.7, "streaming": 0.5},
            personality={"meticulousness": 0.8, "helpfulness": 0.85, "assertiveness": 0.5}
        )

        self.anubis = WorkerAgent(
            "Anubis", "Visualization",
            expertise={"visualization": 0.9, "javascript": 0.8, "design": 0.85, "css": 0.8, "ux": 0.7},
            personality={"meticulousness": 0.85, "helpfulness": 0.7, "assertiveness": 0.3}
        )

        self.ptah = WorkerAgent(
            "Ptah", "Documentation",
            expertise={"writing": 0.9, "research": 0.8, "technical": 0.75, "architecture": 0.6, "presentation": 0.8},
            personality={"meticulousness": 0.8, "helpfulness": 0.75, "assertiveness": 0.5}
        )

        # Register team
        self.agents = [self.thoth, self.seshat, self.maat, self.anubis, self.ptah]
        self.ra.register_team(self.agents)

        # Generate tasks
        self.all_tasks = generate_phis_tasks()
        self.completed_tasks = []
        self.in_progress_tasks = []

    def run_simulation(self):
        """Run the full 3-month simulation."""
        print("=" * 70)
        print("PREDICTIVE HYPE INTELLIGENCE SYSTEM (PHIS)")
        print("3-Month Development Simulation")
        print("=" * 70)

        # 12 weeks, 5 days per week
        for week in range(1, 13):
            self._run_week(week)

        # Final summary
        return self._compile_results()

    def _run_week(self, week: int):
        """Simulate one week of work."""
        print(f"\n{'='*50}")
        print(f"WEEK {week}")
        print(f"{'='*50}")

        # Monday: Sprint planning (every 2 weeks) or standup
        dev_logger.set_time(week, 1)

        if week % 2 == 1:  # Sprint planning every 2 weeks
            sprint_num = (week + 1) // 2
            sprint_goals = self._get_sprint_goals(sprint_num)
            sprint_tasks = [t for t in self.all_tasks if t["target_week"] in [week, week+1]]
            self.ra.run_sprint_planning(sprint_num, sprint_goals, sprint_tasks)

        self.ra.run_daily_standup()

        # Simulate each day
        for day in range(1, 6):
            dev_logger.set_time(week, day)
            self._run_day(week, day)

        # Friday: Retrospective (end of sprint)
        if week % 2 == 0:
            sprint_num = week // 2
            completed = len([t for t in self.completed_tasks if t["target_week"] <= week])
            total = len([t for t in self.all_tasks if t["target_week"] <= week])
            self.ra.run_retrospective(sprint_num, completed, total)

        # Check milestones
        self._check_milestone(week)

        print(f"Week {week} complete. Tasks done this week: {len([t for t in self.completed_tasks if t.get('completed_week') == week])}")

    def _run_day(self, week: int, day: int):
        """Simulate one day of work."""
        # Morning: Standup (after Monday)
        if day > 1:
            self.ra.run_daily_standup()

        # Work sessions
        for agent in self.agents:
            self._agent_work_session(agent, week, day)

        # Collaboration and problem solving
        self._handle_collaborations()
        self._handle_problems()

        # End of day
        for agent in self.agents:
            agent.end_of_day()

    def _agent_work_session(self, agent: WorkerAgent, week: int, day: int):
        """Simulate an agent's work session."""
        # Get or start task
        if not agent.state.current_task:
            task = self._get_next_task_for_agent(agent, week)
            if task:
                agent.start_task(task)
                self.in_progress_tasks.append(task)

        if agent.state.current_task:
            # Work for 4 hours
            result = agent.work_on_task(4)

            # Handle problems
            if result.get("hit_problem"):
                self._handle_agent_problem(agent, result)

            # Check if task might be complete
            if result.get("progress", 0) > 0.3 and self.rng.random() < 0.4:
                task = next((t for t in self.in_progress_tasks if t["id"] == agent.state.current_task), None)
                if task:
                    self._attempt_task_completion(agent, task)

    def _get_next_task_for_agent(self, agent: WorkerAgent, week: int) -> Optional[Dict]:
        """Get the next task for an agent based on their skills."""
        # Find tasks targeted for this week that match agent skills
        agent_skills = set(agent.state.skills.keys())

        available_tasks = [
            t for t in self.all_tasks
            if t["status"] == "backlog"
            and t["target_week"] <= week + 1
            and set(t["required_skills"]) & agent_skills
        ]

        if not available_tasks:
            return None

        # Sort by priority (earlier weeks first, then by skill match)
        def task_score(task):
            skill_match = len(set(task["required_skills"]) & agent_skills) / len(task["required_skills"])
            week_urgency = 1 / (1 + abs(task["target_week"] - week))
            return skill_match * 0.6 + week_urgency * 0.4

        available_tasks.sort(key=task_score, reverse=True)

        selected = available_tasks[0]
        selected["status"] = "in_progress"
        selected["assigned_to"] = agent.name

        return selected

    def _handle_agent_problem(self, agent: WorkerAgent, result: Dict):
        """Handle a problem encountered by an agent."""
        problem_type = result.get("problem_type", "unknown")

        if problem_type == "unclear_requirements":
            # Ask boss for clarification
            agent.ask_question("Ra", f"Need clarification on {agent.state.current_task}", "requirements")

            # Ra responds
            dev_logger.log(
                WorkInteractionType.CLARIFICATION_RESPONSE,
                "Ra", agent.name,
                {
                    "clarification": f"Detailed explanation of requirements for {agent.state.current_task}",
                    "additional_context": "Here's what I had in mind..."
                }
            )
            agent.state.frustration = max(0, agent.state.frustration - 0.1)

        elif problem_type == "dependency_issue":
            # Need to wait for another agent
            other_agent = self.rng.choice([a for a in self.agents if a.name != agent.name])
            dev_logger.log(
                WorkInteractionType.DEPENDENCY_BLOCKED,
                agent.name, other_agent.name,
                {
                    "blocked_task": agent.state.current_task,
                    "waiting_for": f"Output from {other_agent.name}",
                    "estimated_wait": "1-2 days"
                }
            )
            agent.state.blocked_tasks.append(agent.state.current_task)

        elif problem_type in ["bug", "data_issue", "design_flaw"]:
            # Try to fix it or ask for help
            if agent.state.confidence > 0.6:
                # Try to fix alone
                agent.think(f"I'll try to fix this {problem_type} myself", "determined")
                if self.rng.random() < agent.state.confidence:
                    agent.have_breakthrough(f"Figured out the {problem_type}!")
                else:
                    agent.express_frustration(f"Can't figure out this {problem_type}")
                    # Now ask for help
                    helper = self._find_helper_for_problem(agent, problem_type)
                    if helper:
                        agent.request_help(helper, f"Stuck on {problem_type}")
            else:
                # Ask for help immediately
                helper = self._find_helper_for_problem(agent, problem_type)
                if helper:
                    agent.request_help(helper, f"Need help with {problem_type}")

    def _find_helper_for_problem(self, agent: WorkerAgent, problem_type: str) -> Optional[WorkerAgent]:
        """Find the best agent to help with a problem."""
        problem_skills = {
            "bug": ["python", "testing"],
            "data_issue": ["data", "statistics"],
            "design_flaw": ["architecture", "design"],
            "performance_issue": ["optimization", "python"]
        }

        needed_skills = problem_skills.get(problem_type, ["python"])

        # Find agent with best matching skills
        best_helper = None
        best_score = 0

        for other in self.agents:
            if other.name == agent.name:
                continue
            score = sum(other.state.skills.get(s, 0) for s in needed_skills)
            if score > best_score:
                best_score = score
                best_helper = other

        return best_helper

    def _handle_collaborations(self):
        """Handle pending collaboration requests."""
        # Random chance of spontaneous collaboration
        if self.rng.random() < 0.2:
            agent1, agent2 = self.rng.choice(self.agents, 2, replace=False)

            if self.rng.random() < 0.5:
                # Pair programming
                dev_logger.log(
                    WorkInteractionType.PAIR_WORK_START,
                    agent1.name, agent2.name,
                    {
                        "reason": "Complex problem benefits from collaboration",
                        "duration_hours": self.rng.integers(1, 4)
                    }
                )

                # Both learn something
                shared_skill = self.rng.choice(list(set(agent1.state.skills.keys()) | set(agent2.state.skills.keys())))
                agent1.learn_skill(shared_skill, 0.05)
                agent2.learn_skill(shared_skill, 0.05)

                dev_logger.log(
                    WorkInteractionType.PAIR_WORK_END,
                    agent1.name, agent2.name,
                    {
                        "outcome": "Productive session",
                        "artifacts": [f"Improved {shared_skill} implementation"]
                    }
                )
            else:
                # Code review
                agent1.request_code_review(agent2, f"Code for {agent1.state.current_task}")
                feedback = agent2.provide_code_review(agent1.name, f"Code for {agent1.state.current_task}")

                if feedback["overall"] == "request_changes":
                    dev_logger.log(
                        WorkInteractionType.REVISION_REQUEST,
                        agent2.name, agent1.name,
                        {
                            "changes_needed": feedback["issues_found"],
                            "priority": "medium"
                        }
                    )
                elif feedback["overall"] == "approve":
                    dev_logger.log(
                        WorkInteractionType.APPROVAL,
                        agent2.name, agent1.name,
                        {"message": "LGTM!"}
                    )

    def _handle_problems(self):
        """Handle various problems that arise."""
        # Random chance of conflict
        if self.rng.random() < 0.1:
            agent1, agent2 = self.rng.choice(self.agents, 2, replace=False)

            conflict_topics = [
                ("architecture", "Monolith vs microservices", "Microservices for flexibility", "Monolith for simplicity"),
                ("technology", "Framework choice", "Use established framework", "Build custom solution"),
                ("priority", "Task priority", "Focus on features", "Focus on testing"),
                ("design", "API design", "RESTful approach", "GraphQL approach")
            ]

            topic, description, pos1, pos2 = self.rng.choice(conflict_topics)

            agent1.disagree(agent2.name, description, pos1, pos2)
            agent2.disagree(agent1.name, description, pos2, pos1)

            # Debate
            agent1.debate(agent2.name, description, f"Argument for {pos1}")
            agent2.debate(agent1.name, description, f"Argument for {pos2}")

            # Escalate to Ra if personalities are assertive
            if agent1.personality.get("assertiveness", 0) + agent2.personality.get("assertiveness", 0) > 1.0:
                agent1.escalate_to_boss(description, {"my_position": pos1, "their_position": pos2})
                self.ra.mediate_conflict(agent1.name, agent2.name, description)

        # Random chance of technical debt discussion
        if self.rng.random() < 0.05:
            agent = self.rng.choice(self.agents)
            dev_logger.log(
                WorkInteractionType.TECHNICAL_DEBT,
                agent.name, "Ra",
                {
                    "issue": "Accumulating technical debt in codebase",
                    "severity": self.rng.choice(["low", "medium", "high"]),
                    "recommendation": "Allocate time for refactoring"
                }
            )

    def _attempt_task_completion(self, agent: WorkerAgent, task: Dict):
        """Attempt to complete a task."""
        # Check if ready
        quality = agent.state.quality_score * agent.state.confidence

        if self.rng.random() < quality:
            # Task completed
            task["status"] = "complete"
            task["completed_week"] = dev_logger.current_week
            self.completed_tasks.append(task)
            self.in_progress_tasks.remove(task)

            agent.complete_task(task["id"], [f"Deliverable for {task['title']}"])

            # Boss provides feedback
            if self.rng.random() < 0.7:  # 70% chance of feedback
                rating = "excellent" if quality > 0.8 else "good" if quality > 0.5 else "needs_improvement"
                self.ra.provide_feedback(agent.name, task, rating)

            # Resolve any dependencies
            dev_logger.log(
                WorkInteractionType.DEPENDENCY_RESOLVED,
                agent.name, "TEAM",
                {
                    "completed_task": task["id"],
                    "unblocks": [f"Tasks depending on {task['title']}"]
                }
            )
        else:
            # Not quite ready
            agent.think(f"Task {task['id']} not ready yet. Need more work.", "focused")

    def _check_milestone(self, week: int):
        """Check if a milestone is reached."""
        for milestone in PHIS_FEATURE_SPEC["milestones"]:
            if milestone["week"] == week:
                # Check completion
                milestone_tasks = [t for t in self.all_tasks if t["target_week"] <= week]
                completed = len([t for t in milestone_tasks if t["status"] == "complete"])
                total = len(milestone_tasks)

                reached = completed >= total * 0.8  # 80% threshold

                dev_logger.log(
                    WorkInteractionType.MILESTONE_REACHED if reached else WorkInteractionType.INTERNAL_THOUGHT,
                    "Ra", "TEAM",
                    {
                        "milestone": milestone["name"],
                        "target_week": week,
                        "completion": f"{completed}/{total}",
                        "reached": reached,
                        "deliverables": milestone["deliverables"]
                    }
                )

                if not reached:
                    self.ra.identify_risk(f"Milestone {milestone['name']} at risk", "high")

    def _get_sprint_goals(self, sprint_num: int) -> List[str]:
        """Get goals for a sprint."""
        goals_by_sprint = {
            1: ["Set up infrastructure", "Begin data pipeline", "Design system architecture"],
            2: ["Complete data pipeline", "Start ML development", "Begin sentiment analysis"],
            3: ["Train baseline models", "Implement NLP pipeline", "Integration testing"],
            4: ["Hyperparameter tuning", "Build dashboards", "API development"],
            5: ["Polish visualizations", "Write documentation", "Performance optimization"],
            6: ["Final testing", "Demo preparation", "Launch preparation"]
        }
        return goals_by_sprint.get(sprint_num, ["Continue development"])

    def _compile_results(self) -> Dict[str, Any]:
        """Compile final simulation results."""
        results = {
            "project": PHIS_FEATURE_SPEC["name"],
            "duration_weeks": 12,
            "total_tasks": len(self.all_tasks),
            "completed_tasks": len(self.completed_tasks),
            "completion_rate": round(len(self.completed_tasks) / len(self.all_tasks), 2),
            "agent_stats": {},
            "interaction_summary": dev_logger.get_summary()
        }

        for agent in self.agents:
            results["agent_stats"][agent.name] = {
                "tasks_completed": len(agent.state.completed_tasks),
                "bugs_introduced": agent.state.bugs_introduced,
                "bugs_fixed": agent.state.bugs_fixed,
                "skills_learned": len(agent.state.learned_this_sprint),
                "collaborations": sum(agent.state.collaboration_history.values()),
                "final_confidence": round(agent.state.confidence, 2),
                "final_stress": round(agent.state.stress_level, 2)
            }

        return results


def main():
    """Run the 3-month simulation."""
    sim = ThreeMonthSimulation(seed=42)
    results = sim.run_simulation()

    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)

    print(f"\nProject: {results['project']}")
    print(f"Duration: {results['duration_weeks']} weeks")
    print(f"Tasks: {results['completed_tasks']}/{results['total_tasks']} completed ({results['completion_rate']*100:.0f}%)")

    print("\nAgent Performance:")
    for agent, stats in results["agent_stats"].items():
        print(f"  {agent}:")
        print(f"    Tasks completed: {stats['tasks_completed']}")
        print(f"    Bugs: +{stats['bugs_introduced']} / -{stats['bugs_fixed']}")
        print(f"    Collaborations: {stats['collaborations']}")
        print(f"    Final confidence: {stats['final_confidence']}")

    print("\nInteraction Summary:")
    summary = results["interaction_summary"]
    print(f"  Total interactions: {summary['total_interactions']}")

    print("\n  Top interaction types:")
    for int_type, count in list(summary["by_type"].items())[:15]:
        print(f"    {int_type}: {count}")

    print("\n  By week:")
    for week, count in sorted(summary.get("by_week", {}).items()):
        print(f"    {week}: {count}")

    print("\n" + "=" * 70)
    print(f"Full logs saved to: development_simulation.jsonl")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()
