#!/usr/bin/env python3
"""
Agent Interaction System - Multi-Agent Dynamics Research
=========================================================

This module implements a multi-agent system for studying agent dynamics:
- Backend agent interactions (search, collaboration, reporting)
- Boss agent (Ra) coordination and task assignment
- Founder-VC pitch interactions
- Funding decision dynamics

All interactions are logged in extreme detail for AI research purposes.
"""

import json
import time
import random
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional, Literal
from enum import Enum
import numpy as np


# =============================================================================
# LOGGING SYSTEM
# =============================================================================

class InteractionType(Enum):
    """Types of agent interactions to log."""
    TASK_ASSIGNMENT = "task_assignment"
    SEARCH_QUERY = "search_query"
    SEARCH_RESULT = "search_result"
    COLLABORATION_REQUEST = "collaboration_request"
    COLLABORATION_RESPONSE = "collaboration_response"
    REPORT_TO_BOSS = "report_to_boss"
    BOSS_FEEDBACK = "boss_feedback"
    PITCH_START = "pitch_start"
    PITCH_CONTENT = "pitch_content"
    VC_EVALUATION = "vc_evaluation"
    FUNDING_DECISION = "funding_decision"
    NEGOTIATION = "negotiation"
    INTERNAL_THOUGHT = "internal_thought"
    ERROR = "error"
    CONFLICT = "conflict"
    CONSENSUS = "consensus"


@dataclass
class InteractionLog:
    """Single interaction event."""
    timestamp: str
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


class AgentLogger:
    """Comprehensive logging system for agent interactions."""

    def __init__(self, log_file: str = "agent_interactions.jsonl"):
        self.log_file = log_file
        self.logs: List[InteractionLog] = []
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = datetime.now()

        # Initialize log file
        with open(log_file, 'w') as f:
            f.write(json.dumps({
                "session_start": self.start_time.isoformat(),
                "session_id": self.session_id,
                "event": "SESSION_START"
            }) + "\n")

    def log(
        self,
        interaction_type: InteractionType,
        from_agent: str,
        to_agent: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log an interaction and return interaction ID."""
        interaction_id = f"{self.session_id}-{len(self.logs):04d}"

        log_entry = InteractionLog(
            timestamp=datetime.now().isoformat(),
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
        """Generate summary statistics of interactions."""
        type_counts = {}
        agent_activity = {}

        for log in self.logs:
            # Count by type
            t = log.interaction_type
            type_counts[t] = type_counts.get(t, 0) + 1

            # Count by agent
            for agent in [log.from_agent, log.to_agent]:
                if agent not in agent_activity:
                    agent_activity[agent] = {"sent": 0, "received": 0}
            agent_activity[log.from_agent]["sent"] += 1
            agent_activity[log.to_agent]["received"] += 1

        return {
            "total_interactions": len(self.logs),
            "by_type": type_counts,
            "by_agent": agent_activity,
            "duration_seconds": (datetime.now() - self.start_time).total_seconds()
        }


# Global logger instance
logger = AgentLogger()


# =============================================================================
# BASE AGENT CLASS
# =============================================================================

@dataclass
class AgentState:
    """Internal state of an agent."""
    current_task: Optional[str] = None
    knowledge_base: Dict[str, Any] = field(default_factory=dict)
    pending_requests: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    stress_level: float = 0.0  # 0-1, affects behavior
    confidence: float = 0.5  # 0-1, affects decisions


class BaseAgent:
    """Base class for all agents in the system."""

    def __init__(self, name: str, role: str, personality: Dict[str, float]):
        self.name = name
        self.role = role
        self.personality = personality  # e.g., {"assertiveness": 0.7, "risk_tolerance": 0.3}
        self.state = AgentState()
        self.rng = np.random.default_rng()

        # Log agent creation
        logger.log(
            InteractionType.INTERNAL_THOUGHT,
            self.name, "SYSTEM",
            {
                "thought": f"Agent {name} initialized",
                "role": role,
                "personality": personality
            }
        )

    def think(self, thought: str, context: Dict = None):
        """Log internal thought process."""
        logger.log(
            InteractionType.INTERNAL_THOUGHT,
            self.name, self.name,
            {
                "thought": thought,
                "context": context or {},
                "state": {
                    "stress": self.state.stress_level,
                    "confidence": self.state.confidence,
                    "current_task": self.state.current_task
                }
            }
        )

    def search(self, query: str, search_space: str) -> Dict[str, Any]:
        """Perform a search operation."""
        # Log search initiation
        logger.log(
            InteractionType.SEARCH_QUERY,
            self.name, "KNOWLEDGE_BASE",
            {
                "query": query,
                "search_space": search_space,
                "confidence": self.state.confidence
            }
        )

        # Simulate search with some randomness
        self.think(f"Searching for '{query}' in {search_space}...")
        time.sleep(0.01)  # Simulate processing

        # Determine search success based on confidence and randomness
        success_prob = 0.5 + 0.3 * self.state.confidence
        found = self.rng.random() < success_prob

        result = {
            "found": found,
            "query": query,
            "results": [f"Result for {query}"] if found else [],
            "confidence_in_result": self.rng.uniform(0.3, 0.9) if found else 0.0
        }

        # Log search result
        logger.log(
            InteractionType.SEARCH_RESULT,
            "KNOWLEDGE_BASE", self.name,
            result
        )

        if not found:
            self.think(f"Search failed for '{query}'. May need to ask for help.")
            self.state.stress_level = min(1.0, self.state.stress_level + 0.1)
        else:
            self.state.confidence = min(1.0, self.state.confidence + 0.05)

        return result


# =============================================================================
# WORKER AGENTS (Egyptian Pantheon)
# =============================================================================

class ThothAgent(BaseAgent):
    """Data Acquisition Agent - Gathers and organizes data."""

    def __init__(self):
        super().__init__(
            name="Thoth",
            role="Data Acquisition",
            personality={
                "meticulousness": 0.9,
                "assertiveness": 0.4,
                "risk_tolerance": 0.2,
                "collaboration_tendency": 0.7
            }
        )
        self.data_sources = []

    def gather_data(self, data_type: str, source: str) -> Dict[str, Any]:
        """Gather data from a specified source."""
        self.think(f"Need to gather {data_type} from {source}")

        # Search for data
        result = self.search(data_type, source)

        if result["found"]:
            self.think(f"Successfully gathered {data_type}. Recording source for documentation.")
            self.data_sources.append({
                "type": data_type,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
        else:
            self.think(f"Failed to gather {data_type}. Will need to try alternative sources or ask Seshat for help.")

        return result

    def request_collaboration(self, target_agent: 'BaseAgent', task: str) -> str:
        """Request help from another agent."""
        self.think(f"Requesting collaboration from {target_agent.name} for: {task}")

        interaction_id = logger.log(
            InteractionType.COLLABORATION_REQUEST,
            self.name, target_agent.name,
            {
                "task": task,
                "urgency": self.state.stress_level,
                "context": {
                    "my_current_task": self.state.current_task,
                    "data_gathered_so_far": len(self.data_sources)
                }
            }
        )

        return interaction_id


class SeshatAgent(BaseAgent):
    """Quant Analyst Agent - Builds simulation engine."""

    def __init__(self):
        super().__init__(
            name="Seshat",
            role="Quant Analyst",
            personality={
                "meticulousness": 0.95,
                "assertiveness": 0.6,
                "risk_tolerance": 0.3,
                "collaboration_tendency": 0.5
            }
        )
        self.models_built = []

    def build_model(self, model_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Build a quantitative model."""
        self.think(f"Building model: {model_spec.get('name', 'unnamed')}")

        # Check if we have required data
        required_data = model_spec.get("required_data", [])
        missing_data = []

        for data_item in required_data:
            result = self.search(data_item, "internal_knowledge")
            if not result["found"]:
                missing_data.append(data_item)

        if missing_data:
            self.think(f"Missing data for model: {missing_data}. Need to coordinate with Thoth.")
            return {
                "success": False,
                "missing_data": missing_data,
                "recommendation": "Request data from Thoth"
            }

        # Build the model
        self.think("All data available. Proceeding with model construction.")
        model_result = {
            "success": True,
            "model_name": model_spec.get("name"),
            "parameters_estimated": self.rng.integers(5, 20),
            "validation_score": self.rng.uniform(0.6, 0.95)
        }

        self.models_built.append(model_result)
        self.state.confidence = min(1.0, self.state.confidence + 0.1)

        return model_result

    def respond_to_collaboration(self, request_from: str, task: str) -> Dict[str, Any]:
        """Respond to a collaboration request."""
        self.think(f"Received collaboration request from {request_from}: {task}")

        # Decide whether to help based on personality and current state
        help_probability = (
            self.personality["collaboration_tendency"] *
            (1 - self.state.stress_level) *
            (0.5 + 0.5 * self.state.confidence)
        )

        will_help = self.rng.random() < help_probability

        response = {
            "will_help": will_help,
            "reason": "Available and task aligns with expertise" if will_help else "Currently overloaded with other tasks",
            "estimated_time": self.rng.integers(1, 5) if will_help else None,
            "conditions": ["Need clear specifications", "Will require review"] if will_help else []
        }

        logger.log(
            InteractionType.COLLABORATION_RESPONSE,
            self.name, request_from,
            response
        )

        if will_help:
            self.think(f"Agreed to help {request_from}. Adding to my task queue.")
            self.state.pending_requests.append(task)
        else:
            self.think(f"Declined to help {request_from}. Too much on my plate.")

        return response


class MaatAgent(BaseAgent):
    """Narrative & Sentiment Agent - Analyzes hype and sentiment."""

    def __init__(self):
        super().__init__(
            name="Maat",
            role="Narrative & Sentiment",
            personality={
                "meticulousness": 0.7,
                "assertiveness": 0.5,
                "risk_tolerance": 0.4,
                "collaboration_tendency": 0.8
            }
        )
        self.sentiment_analyses = []

    def analyze_sentiment(self, text: str, context: str) -> Dict[str, Any]:
        """Analyze sentiment/hype in text."""
        self.think(f"Analyzing sentiment for: {context}")

        # Simulate sentiment analysis
        hype_score = self.rng.uniform(0, 1)
        confidence = self.rng.uniform(0.5, 0.9)

        analysis = {
            "context": context,
            "hype_score": hype_score,
            "confidence": confidence,
            "keywords_detected": self.rng.integers(0, 10),
            "elite_vc_mentions": self.rng.integers(0, 5)
        }

        self.sentiment_analyses.append(analysis)

        self.think(f"Sentiment analysis complete. Hype score: {hype_score:.2f}")

        return analysis


class AnubisAgent(BaseAgent):
    """Visualization Agent - Creates figures and visualizations."""

    def __init__(self):
        super().__init__(
            name="Anubis",
            role="Visualization",
            personality={
                "meticulousness": 0.85,
                "assertiveness": 0.3,
                "risk_tolerance": 0.2,
                "collaboration_tendency": 0.6
            }
        )
        self.figures_created = []

    def create_visualization(self, data: Dict, viz_type: str) -> Dict[str, Any]:
        """Create a visualization from data."""
        self.think(f"Creating {viz_type} visualization")

        # Check if data is sufficient
        if not data:
            self.think("No data provided. Need to request from Seshat or Thoth.")
            return {"success": False, "reason": "No data provided"}

        figure = {
            "type": viz_type,
            "data_points": len(data),
            "quality_score": self.rng.uniform(0.7, 1.0),
            "file_path": f"results/figure_{len(self.figures_created)+1}_{viz_type}.png"
        }

        self.figures_created.append(figure)
        self.think(f"Visualization complete: {figure['file_path']}")

        return {"success": True, "figure": figure}


class PtahAgent(BaseAgent):
    """Research Synthesizer Agent - Writes papers and documentation."""

    def __init__(self):
        super().__init__(
            name="Ptah",
            role="Research Synthesizer",
            personality={
                "meticulousness": 0.8,
                "assertiveness": 0.5,
                "risk_tolerance": 0.3,
                "collaboration_tendency": 0.7
            }
        )
        self.sections_written = []

    def write_section(self, section_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Write a section of the research paper."""
        self.think(f"Writing section: {section_name}")

        # Check for required inputs
        required = ["data", "analysis", "figures"]
        missing = [r for r in required if r not in inputs]

        if missing:
            self.think(f"Missing inputs for {section_name}: {missing}. Need to coordinate with team.")
            return {
                "success": False,
                "missing_inputs": missing,
                "section": section_name
            }

        section = {
            "name": section_name,
            "word_count": self.rng.integers(500, 2000),
            "citations": self.rng.integers(5, 15),
            "quality_score": self.rng.uniform(0.6, 0.9)
        }

        self.sections_written.append(section)
        self.think(f"Section {section_name} complete. {section['word_count']} words.")

        return {"success": True, "section": section}


# =============================================================================
# BOSS AGENT (Ra - Orchestrator)
# =============================================================================

class RaAgent(BaseAgent):
    """Orchestrator Agent - Coordinates all other agents."""

    def __init__(self):
        super().__init__(
            name="Ra",
            role="Orchestrator",
            personality={
                "meticulousness": 0.8,
                "assertiveness": 0.9,
                "risk_tolerance": 0.5,
                "collaboration_tendency": 0.6
            }
        )
        self.team = {}
        self.task_queue = []
        self.completed_tasks = []

    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator."""
        self.team[agent.name] = agent
        self.think(f"Registered agent: {agent.name} ({agent.role})")

    def assign_task(self, agent_name: str, task: Dict[str, Any]) -> str:
        """Assign a task to an agent."""
        if agent_name not in self.team:
            self.think(f"ERROR: Agent {agent_name} not found in team!")
            logger.log(
                InteractionType.ERROR,
                self.name, "SYSTEM",
                {"error": f"Agent {agent_name} not found", "task": task}
            )
            return None

        agent = self.team[agent_name]
        task_id = f"TASK-{len(self.task_queue):04d}"

        task["task_id"] = task_id
        task["assigned_to"] = agent_name
        task["assigned_at"] = datetime.now().isoformat()

        self.think(f"Assigning task {task_id} to {agent_name}: {task.get('description', 'No description')}")

        # Log the assignment
        logger.log(
            InteractionType.TASK_ASSIGNMENT,
            self.name, agent_name,
            task
        )

        # Update agent state
        agent.state.current_task = task_id
        self.task_queue.append(task)

        return task_id

    def receive_report(self, from_agent: str, report: Dict[str, Any]):
        """Receive a status report from an agent."""
        self.think(f"Receiving report from {from_agent}")

        logger.log(
            InteractionType.REPORT_TO_BOSS,
            from_agent, self.name,
            report
        )

        # Evaluate the report
        success = report.get("success", False)
        quality = report.get("quality_score", 0.5)

        # Provide feedback
        if success and quality > 0.7:
            feedback = {
                "assessment": "excellent",
                "message": f"Great work, {from_agent}! This meets our standards.",
                "next_steps": "Proceed to next task"
            }
            self.state.confidence = min(1.0, self.state.confidence + 0.05)
        elif success:
            feedback = {
                "assessment": "acceptable",
                "message": f"Good effort, {from_agent}. Some improvements needed.",
                "next_steps": "Minor revisions required",
                "revision_notes": ["Increase rigor", "Add more validation"]
            }
        else:
            feedback = {
                "assessment": "needs_work",
                "message": f"{from_agent}, this needs significant revision.",
                "next_steps": "Please address the issues and resubmit",
                "issues": report.get("issues", ["Unknown issues"])
            }
            self.state.stress_level = min(1.0, self.state.stress_level + 0.1)

        logger.log(
            InteractionType.BOSS_FEEDBACK,
            self.name, from_agent,
            feedback
        )

        return feedback

    def resolve_conflict(self, agent1: str, agent2: str, conflict: Dict[str, Any]):
        """Resolve a conflict between two agents."""
        self.think(f"Resolving conflict between {agent1} and {agent2}")

        logger.log(
            InteractionType.CONFLICT,
            "SYSTEM", self.name,
            {
                "agents": [agent1, agent2],
                "conflict": conflict
            }
        )

        # Make a decision based on assertiveness
        if self.rng.random() < self.personality["assertiveness"]:
            resolution = {
                "decision": "directive",
                "winner": agent1 if self.rng.random() < 0.5 else agent2,
                "rationale": "Executive decision to maintain project momentum"
            }
        else:
            resolution = {
                "decision": "compromise",
                "actions": [f"{agent1} handles part A", f"{agent2} handles part B"],
                "rationale": "Both approaches have merit; splitting responsibility"
            }

        logger.log(
            InteractionType.CONSENSUS,
            self.name, "TEAM",
            resolution
        )

        return resolution

    def run_coordination_cycle(self):
        """Run one coordination cycle with all agents."""
        self.think("Beginning coordination cycle")

        # Check on each agent
        for agent_name, agent in self.team.items():
            if agent.state.current_task:
                self.think(f"Checking on {agent_name}, working on {agent.state.current_task}")

                # Simulate progress check
                if agent.state.stress_level > 0.7:
                    self.think(f"{agent_name} appears stressed. May need support.")

                    # Offer help
                    logger.log(
                        InteractionType.COLLABORATION_REQUEST,
                        self.name, agent_name,
                        {
                            "type": "support_offer",
                            "message": "I noticed you might need help. What can I do?"
                        }
                    )


# =============================================================================
# FOUNDER AND VC AGENTS
# =============================================================================

@dataclass
class FounderProfile:
    """Profile of a founder agent."""
    id: int
    name: str
    company: str
    domain: str
    revenue: float
    growth: float
    charisma: float
    vision: float
    traction: float
    repeat_founder: bool
    pitch_style: str  # "visionary", "data_driven", "storyteller", "technical"


class FounderAgent(BaseAgent):
    """Founder agent that pitches to VCs."""

    def __init__(self, profile: FounderProfile):
        super().__init__(
            name=f"Founder_{profile.name}",
            role="Founder",
            personality={
                "assertiveness": 0.3 + 0.5 * profile.charisma,
                "risk_tolerance": 0.5 + 0.3 * profile.vision,
                "confidence": 0.4 + 0.4 * (1 if profile.repeat_founder else 0)
            }
        )
        self.profile = profile
        self.pitches_given = []
        self.offers_received = []
        self.funding_secured = 0.0

    def prepare_pitch(self, target_vc: str) -> Dict[str, Any]:
        """Prepare a pitch for a specific VC."""
        self.think(f"Preparing pitch for {target_vc}")

        # Adapt pitch based on style
        if self.profile.pitch_style == "visionary":
            emphasis = ["vision", "market_size", "moonshot_potential"]
            narrative_weight = 0.8
        elif self.profile.pitch_style == "data_driven":
            emphasis = ["revenue", "growth", "unit_economics"]
            narrative_weight = 0.3
        elif self.profile.pitch_style == "storyteller":
            emphasis = ["founding_story", "customer_testimonials", "mission"]
            narrative_weight = 0.7
        else:  # technical
            emphasis = ["technology", "IP", "technical_moat"]
            narrative_weight = 0.4

        pitch = {
            "target_vc": target_vc,
            "company": self.profile.company,
            "domain": self.profile.domain,
            "emphasis": emphasis,
            "narrative_weight": narrative_weight,
            "metrics": {
                "revenue": self.profile.revenue,
                "growth": self.profile.growth,
                "traction": self.profile.traction
            },
            "ask": self._calculate_ask()
        }

        self.think(f"Pitch prepared. Emphasizing {emphasis}. Ask: ${pitch['ask']}M")

        return pitch

    def _calculate_ask(self) -> float:
        """Calculate funding ask based on stage and confidence."""
        base_ask = 2.0  # $2M base

        # Adjust based on revenue
        if self.profile.revenue > 5_000_000:
            base_ask = 30.0
        elif self.profile.revenue > 500_000:
            base_ask = 12.0

        # Adjust based on confidence
        confidence_multiplier = 0.8 + 0.4 * self.state.confidence

        return round(base_ask * confidence_multiplier, 1)

    def deliver_pitch(self, vc_agent: 'VCAgent', pitch: Dict[str, Any]) -> str:
        """Deliver the pitch to a VC agent."""
        self.think(f"Delivering pitch to {vc_agent.name}")

        # Log pitch start
        logger.log(
            InteractionType.PITCH_START,
            self.name, vc_agent.name,
            {
                "company": self.profile.company,
                "founder_confidence": self.state.confidence,
                "founder_stress": self.state.stress_level
            }
        )

        # Log pitch content
        interaction_id = logger.log(
            InteractionType.PITCH_CONTENT,
            self.name, vc_agent.name,
            pitch
        )

        self.pitches_given.append({
            "vc": vc_agent.name,
            "interaction_id": interaction_id,
            "ask": pitch["ask"]
        })

        return interaction_id

    def receive_decision(self, vc_name: str, decision: Dict[str, Any]):
        """Receive and process funding decision."""
        self.think(f"Received decision from {vc_name}")

        if decision["funded"]:
            self.think(f"SUCCESS! {vc_name} is investing ${decision['amount']}M!")
            self.offers_received.append(decision)
            self.funding_secured += decision["amount"]
            self.state.confidence = min(1.0, self.state.confidence + 0.2)
            self.state.stress_level = max(0.0, self.state.stress_level - 0.3)
        else:
            self.think(f"Rejected by {vc_name}. Reason: {decision.get('reason', 'Not specified')}")
            self.state.stress_level = min(1.0, self.state.stress_level + 0.1)

            # Consider adjusting approach
            if self.state.stress_level > 0.5:
                self.think("Multiple rejections. May need to reconsider pitch strategy.")

    def negotiate(self, vc_agent: 'VCAgent', initial_offer: Dict[str, Any]) -> Dict[str, Any]:
        """Negotiate terms with a VC."""
        self.think(f"Negotiating with {vc_agent.name}. Initial offer: ${initial_offer['amount']}M at {initial_offer['valuation']}M valuation")

        # Decide on counter based on personality
        if self.personality["assertiveness"] > 0.6 and len(self.offers_received) > 0:
            # Have leverage, push back
            counter = {
                "type": "counter",
                "amount": initial_offer["amount"],
                "valuation": initial_offer["valuation"] * 1.2,
                "rationale": "We have other term sheets and believe our traction justifies higher valuation"
            }
            self.think("Countering with higher valuation due to competitive dynamics")
        elif self.state.stress_level > 0.7:
            # Desperate, accept quickly
            counter = {
                "type": "accept",
                "amount": initial_offer["amount"],
                "valuation": initial_offer["valuation"],
                "rationale": "Terms are acceptable"
            }
            self.think("Accepting offer to close round quickly")
        else:
            # Minor negotiation
            counter = {
                "type": "counter",
                "amount": initial_offer["amount"] * 1.1,
                "valuation": initial_offer["valuation"] * 1.1,
                "rationale": "Slight adjustment to terms"
            }
            self.think("Making modest counter-offer")

        logger.log(
            InteractionType.NEGOTIATION,
            self.name, vc_agent.name,
            counter
        )

        return counter


class VCAgent(BaseAgent):
    """VC agent that evaluates pitches and makes funding decisions."""

    def __init__(self, name: str, region: str, preferences: Dict[str, float]):
        super().__init__(
            name=name,
            role=f"VC ({region})",
            personality={
                "assertiveness": 0.7,
                "risk_tolerance": preferences.get("hype_beta", 0.5),
                "meticulousness": 0.8
            }
        )
        self.region = region
        self.preferences = preferences  # Feature weights
        self.budget = preferences.get("budget", 100.0)  # $M
        self.investments = []
        self.deals_seen = []

    def evaluate_pitch(self, pitch: Dict[str, Any], founder: FounderAgent) -> Dict[str, Any]:
        """Evaluate a pitch from a founder."""
        self.think(f"Evaluating pitch from {founder.name} for {pitch['company']}")

        # Calculate score based on preferences
        metrics = pitch["metrics"]

        # Base score from fundamentals
        fundamental_score = (
            self.preferences.get("revenue", 1.0) * np.log1p(metrics["revenue"]) / 10 +
            self.preferences.get("growth", 1.0) * metrics["growth"] +
            self.preferences.get("traction", 1.0) * metrics["traction"]
        )

        # Narrative score
        narrative_score = (
            self.preferences.get("charisma", 1.0) * founder.profile.charisma +
            self.preferences.get("vision", 1.0) * founder.profile.vision
        )

        # Domain preference
        domain_mult = self.preferences.get(f"domain_{pitch['domain']}", 1.0)

        # Total score
        total_score = (fundamental_score + narrative_score) * domain_mult

        # Add noise
        noise = self.rng.normal(0, 0.5)
        total_score += noise

        evaluation = {
            "company": pitch["company"],
            "fundamental_score": fundamental_score,
            "narrative_score": narrative_score,
            "domain_multiplier": domain_mult,
            "total_score": total_score,
            "threshold": 5.0,  # Minimum score to consider
            "passes_threshold": total_score > 5.0
        }

        self.think(f"Evaluation complete. Score: {total_score:.2f}. Threshold: 5.0. Pass: {evaluation['passes_threshold']}")

        # Log evaluation
        logger.log(
            InteractionType.VC_EVALUATION,
            self.name, founder.name,
            evaluation
        )

        self.deals_seen.append(evaluation)

        return evaluation

    def make_funding_decision(self, evaluation: Dict[str, Any], pitch: Dict[str, Any], founder: FounderAgent) -> Dict[str, Any]:
        """Make final funding decision."""
        self.think(f"Making funding decision for {pitch['company']}")

        # Check budget
        ask = pitch["ask"]
        if ask > self.budget:
            self.think(f"Ask ${ask}M exceeds remaining budget ${self.budget}M. Cannot fund.")
            decision = {
                "funded": False,
                "reason": "Insufficient budget",
                "ask": ask,
                "budget_remaining": self.budget
            }
        elif not evaluation["passes_threshold"]:
            self.think(f"Score {evaluation['total_score']:.2f} below threshold. Passing.")
            decision = {
                "funded": False,
                "reason": "Below investment threshold",
                "score": evaluation["total_score"],
                "feedback": self._generate_feedback(evaluation)
            }
        else:
            # Calculate investment amount and terms
            amount = min(ask, self.budget * 0.3)  # Max 30% of budget per deal
            valuation = amount * self.rng.uniform(3, 8)  # 3-8x multiple

            self.think(f"Deciding to invest ${amount}M at ${valuation}M valuation")

            decision = {
                "funded": True,
                "amount": amount,
                "valuation": valuation,
                "ownership": amount / valuation,
                "terms": ["Standard preferred", "Pro-rata rights", "Board seat" if amount > 5 else "Board observer"],
                "rationale": self._generate_rationale(evaluation, pitch)
            }

            # Update budget and investments
            self.budget -= amount
            self.investments.append({
                "company": pitch["company"],
                "founder": founder.name,
                "amount": amount,
                "valuation": valuation
            })

        # Log decision
        logger.log(
            InteractionType.FUNDING_DECISION,
            self.name, founder.name,
            decision
        )

        return decision

    def _generate_feedback(self, evaluation: Dict[str, Any]) -> str:
        """Generate feedback for rejected founders."""
        if evaluation["fundamental_score"] < 2:
            return "Need stronger revenue traction before we can invest"
        elif evaluation["narrative_score"] < 1:
            return "Would like to see a clearer vision for category leadership"
        else:
            return "Competitive space, looking for more differentiation"

    def _generate_rationale(self, evaluation: Dict[str, Any], pitch: Dict[str, Any]) -> str:
        """Generate rationale for investment decision."""
        reasons = []

        if evaluation["fundamental_score"] > 3:
            reasons.append("Strong fundamentals")
        if evaluation["narrative_score"] > 2:
            reasons.append("Compelling founder narrative")
        if evaluation["domain_multiplier"] > 1.2:
            reasons.append(f"High conviction in {pitch['domain']} thesis")

        return "; ".join(reasons) if reasons else "Meets investment criteria"

    def respond_to_negotiation(self, founder: FounderAgent, counter: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to founder's negotiation."""
        self.think(f"Responding to negotiation from {founder.name}")

        if counter["type"] == "accept":
            response = {
                "type": "close",
                "final_terms": counter
            }
            self.think("Founder accepted. Closing deal.")
        elif counter["valuation"] > self.investments[-1]["valuation"] * 1.3:
            response = {
                "type": "withdraw",
                "reason": "Valuation expectations too high"
            }
            self.think("Counter too aggressive. Walking away.")
            # Undo investment
            self.budget += self.investments[-1]["amount"]
            self.investments.pop()
        else:
            # Split the difference
            new_valuation = (counter["valuation"] + self.investments[-1]["valuation"]) / 2
            response = {
                "type": "final_offer",
                "amount": counter["amount"],
                "valuation": new_valuation
            }
            self.think(f"Counter-offering at ${new_valuation}M valuation")

        logger.log(
            InteractionType.NEGOTIATION,
            self.name, founder.name,
            response
        )

        return response


# =============================================================================
# SIMULATION RUNNER
# =============================================================================

class AgentSimulation:
    """Main simulation runner for agent interactions."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

        # Initialize boss agent
        self.ra = RaAgent()

        # Initialize worker agents
        self.thoth = ThothAgent()
        self.seshat = SeshatAgent()
        self.maat = MaatAgent()
        self.anubis = AnubisAgent()
        self.ptah = PtahAgent()

        # Register workers with boss
        for agent in [self.thoth, self.seshat, self.maat, self.anubis, self.ptah]:
            self.ra.register_agent(agent)

        # Initialize VC agents
        self.vcs = self._create_vc_agents()

        # Initialize founder agents
        self.founders = []

    def _create_vc_agents(self) -> Dict[str, VCAgent]:
        """Create VC agents for each region."""
        regions = {
            "bay_area": {
                "revenue": 0.6, "growth": 0.8, "charisma": 1.2, "vision": 1.5,
                "traction": 0.7, "hype_beta": 1.5, "domain_ai": 1.8, "domain_bio": 0.9,
                "budget": 100.0
            },
            "nyc": {
                "revenue": 1.4, "growth": 1.2, "charisma": 0.7, "vision": 0.6,
                "traction": 1.3, "hype_beta": 0.8, "domain_enterprise": 1.5, "domain_bio": 0.7,
                "budget": 50.0
            },
            "boston": {
                "revenue": 1.1, "growth": 1.0, "charisma": 0.5, "vision": 0.7,
                "traction": 1.4, "hype_beta": 0.5, "domain_bio": 2.0, "domain_consumer": 0.6,
                "budget": 30.0
            },
            "la": {
                "revenue": 0.8, "growth": 1.0, "charisma": 1.4, "vision": 1.2,
                "traction": 0.9, "hype_beta": 1.3, "domain_consumer": 1.7, "domain_ai": 0.8,
                "budget": 20.0
            }
        }

        vcs = {}
        for region, prefs in regions.items():
            vcs[region] = VCAgent(f"VC_{region}", region, prefs)

        return vcs

    def generate_founders(self, n: int) -> List[FounderAgent]:
        """Generate founder agents."""
        domains = ["ai", "bio", "consumer", "enterprise"]
        pitch_styles = ["visionary", "data_driven", "storyteller", "technical"]
        names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery"]

        founders = []
        for i in range(n):
            profile = FounderProfile(
                id=i,
                name=f"{self.rng.choice(names)}_{i}",
                company=f"Startup_{i}",
                domain=self.rng.choice(domains),
                revenue=float(self.rng.lognormal(11.5, 2.0)),
                growth=float(self.rng.normal(0.5, 0.3)),
                charisma=float(self.rng.normal(0, 1)),
                vision=float(self.rng.normal(0, 1)),
                traction=float(self.rng.normal(0, 1)),
                repeat_founder=bool(self.rng.random() < 0.15),
                pitch_style=self.rng.choice(pitch_styles)
            )
            founders.append(FounderAgent(profile))

        self.founders = founders
        return founders

    def run_backend_workflow(self):
        """Run backend agent workflow (Week 2-3 tasks)."""
        logger.log(
            InteractionType.INTERNAL_THOUGHT,
            "SYSTEM", "ALL",
            {"event": "Starting backend workflow simulation"}
        )

        # Ra assigns tasks
        self.ra.assign_task("Thoth", {
            "description": "Scrape TechCrunch for sentiment data",
            "priority": "high",
            "deadline": "Week 3"
        })

        self.ra.assign_task("Seshat", {
            "description": "Build sentiment analysis pipeline",
            "priority": "high",
            "deadline": "Week 3"
        })

        # Thoth starts gathering data
        self.thoth.gather_data("techcrunch_articles", "web_scraper")

        # Thoth needs help from Seshat
        collab_id = self.thoth.request_collaboration(
            self.seshat,
            "Need help parsing sentiment from scraped articles"
        )

        # Seshat responds
        self.seshat.respond_to_collaboration("Thoth", "sentiment parsing")

        # Maat analyzes sentiment
        self.maat.analyze_sentiment(
            "Sample article text about AI startup raising $100M",
            "TechCrunch article"
        )

        # Seshat builds model
        self.seshat.build_model({
            "name": "Hype Sentiment Model",
            "required_data": ["techcrunch_articles", "sentiment_labels"]
        })

        # Anubis creates visualization
        self.anubis.create_visualization(
            {"sample": "data"},
            "sentiment_timeline"
        )

        # Ptah writes documentation
        self.ptah.write_section(
            "Methodology",
            {"data": True, "analysis": True, "figures": True}
        )

        # Workers report to Ra
        self.ra.receive_report("Thoth", {
            "success": True,
            "quality_score": 0.75,
            "data_gathered": 1000,
            "issues": []
        })

        self.ra.receive_report("Seshat", {
            "success": True,
            "quality_score": 0.82,
            "model_accuracy": 0.78
        })

        # Ra runs coordination cycle
        self.ra.run_coordination_cycle()

    def run_pitch_simulation(self, n_founders: int = 10):
        """Run founder-VC pitch simulation."""
        logger.log(
            InteractionType.INTERNAL_THOUGHT,
            "SYSTEM", "ALL",
            {"event": f"Starting pitch simulation with {n_founders} founders"}
        )

        # Generate founders
        founders = self.generate_founders(n_founders)

        # Each founder pitches to each VC
        for founder in founders:
            for region, vc in self.vcs.items():
                # Prepare pitch
                pitch = founder.prepare_pitch(vc.name)

                # Deliver pitch
                founder.deliver_pitch(vc, pitch)

                # VC evaluates
                evaluation = vc.evaluate_pitch(pitch, founder)

                # VC makes decision
                decision = vc.make_funding_decision(evaluation, pitch, founder)

                # Founder receives decision
                founder.receive_decision(vc.name, decision)

                # If funded, negotiate
                if decision.get("funded"):
                    counter = founder.negotiate(vc, decision)
                    vc.respond_to_negotiation(founder, counter)

        return self._compile_results()

    def _compile_results(self) -> Dict[str, Any]:
        """Compile simulation results."""
        results = {
            "total_founders": len(self.founders),
            "total_pitches": sum(len(f.pitches_given) for f in self.founders),
            "total_funded": sum(1 for f in self.founders if f.funding_secured > 0),
            "total_capital_deployed": sum(f.funding_secured for f in self.founders),
            "by_region": {},
            "interaction_summary": logger.get_summary()
        }

        for region, vc in self.vcs.items():
            results["by_region"][region] = {
                "investments": len(vc.investments),
                "capital_deployed": sum(inv["amount"] for inv in vc.investments),
                "deals_seen": len(vc.deals_seen),
                "budget_remaining": vc.budget
            }

        return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Run the agent simulation."""
    print("=" * 60)
    print("AGENT INTERACTION SIMULATION")
    print("Multi-Agent Dynamics Research")
    print("=" * 60)

    # Initialize simulation
    sim = AgentSimulation(seed=42)

    # Run backend workflow (Week 2-3 tasks)
    print("\n[Phase 1] Backend Agent Workflow")
    print("-" * 40)
    sim.run_backend_workflow()

    # Run pitch simulation
    print("\n[Phase 2] Founder-VC Pitch Simulation")
    print("-" * 40)
    results = sim.run_pitch_simulation(n_founders=20)

    # Print results
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)
    print(f"Total Founders: {results['total_founders']}")
    print(f"Total Pitches: {results['total_pitches']}")
    print(f"Total Funded: {results['total_funded']}")
    print(f"Total Capital Deployed: ${results['total_capital_deployed']:.1f}M")

    print("\nBy Region:")
    for region, data in results["by_region"].items():
        print(f"  {region}: {data['investments']} investments, ${data['capital_deployed']:.1f}M deployed")

    print("\nInteraction Summary:")
    summary = results["interaction_summary"]
    print(f"  Total Interactions: {summary['total_interactions']}")
    print(f"  Duration: {summary['duration_seconds']:.1f}s")

    print("\n  By Type:")
    for int_type, count in sorted(summary["by_type"].items(), key=lambda x: -x[1]):
        print(f"    {int_type}: {count}")

    print("\n" + "=" * 60)
    print(f"Full interaction log saved to: agent_interactions.jsonl")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
