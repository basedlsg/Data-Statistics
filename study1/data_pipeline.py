#!/usr/bin/env python3
"""
Data Pipeline for Study 1: LLM Agent Response Variability
==========================================================

Complete data collection, logging, and validation system for the within-subjects
experimental design investigating response variability across 5 conditions.

Implements:
1. InteractionLogger - JSONL logging with atomic writes
2. SessionManager - Manages condition ordering and washout protocols
3. DataValidator - Quality control and completeness checks

Design follows STATISTICAL_METHODOLOGY.md requirements:
- Hierarchical structure: Condition → Agent → Session → Interaction
- Complete metadata for reproducibility
- Pseudo-replication handling through proper aggregation
- Counterbalancing verification
"""

import json
import uuid
import time
import hashlib
import fcntl
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Literal, Set, Tuple
from collections import defaultdict
from enum import Enum
import pandas as pd
import numpy as np


# =============================================================================
# 1. INTERACTION LOGGER
# =============================================================================

class ConditionType(Enum):
    """Experimental conditions for Study 1."""
    CONTROL = "control"
    TEMPERATURE_0_7 = "temperature_0.7"
    TEMPERATURE_1_2 = "temperature_1.2"
    TOP_P_0_9 = "top_p_0.9"
    PRESENCE_PENALTY = "presence_penalty_0.6"


@dataclass
class InteractionLog:
    """Single interaction event with complete metadata."""

    # Unique identifiers
    interaction_id: str
    session_id: str
    agent_id: str

    # Experimental design
    condition: str  # ConditionType value
    run_number: int  # 1-10 for each agent
    session_number: int  # Within-run session counter
    order_position: int  # 1-5, position in counterbalanced order

    # Timestamps
    timestamp: str  # ISO 8601 format
    unix_timestamp: float

    # LLM Interaction
    prompt_text: str
    response_text: str
    response_length: int  # Character count
    response_latency: float  # Seconds
    api_used: str  # "cerebras" or "gemini"

    # Fields with defaults (must come after non-default fields)
    simulated_date: Optional[str] = None  # For simulated experiments

    # API Parameters (condition-specific)
    api_parameters: Dict[str, Any] = field(default_factory=dict)

    # Quality metrics
    api_error: bool = False
    error_message: Optional[str] = None
    retry_count: int = 0

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper type handling."""
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
            elif isinstance(obj, Enum):
                return obj.value
            return obj
        return convert(asdict(self))


class InteractionLogger:
    """
    Logs all LLM interactions to JSONL format with atomic writes and error recovery.

    Features:
    - Append-only logging (never overwrites)
    - Atomic writes with file locking
    - Automatic error recovery
    - Timestamp synchronization
    - Complete metadata capture
    """

    def __init__(
        self,
        output_dir: Path,
        agent_id: str,
        run_number: int,
        session_id: Optional[str] = None
    ):
        """
        Initialize logger for a single agent run.

        Args:
            output_dir: Directory for raw log files
            agent_id: Unique agent identifier
            run_number: Run number (1-10)
            session_id: Optional session ID (auto-generated if not provided)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.agent_id = agent_id
        self.run_number = run_number
        self.session_id = session_id or self._generate_session_id()

        # Log file: agent_id_run_number_session_id.jsonl
        self.log_file = self.output_dir / f"{agent_id}_run{run_number:02d}_{self.session_id}.jsonl"

        # Interaction counter
        self.interaction_count = 0

        # Current condition tracking
        self.current_condition: Optional[str] = None
        self.session_number = 0
        self.order_position = 0

        # Initialize log file
        self._initialize_log_file()

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().isoformat()
        unique_str = f"{self.agent_id}_{self.run_number}_{timestamp}"
        return hashlib.sha256(unique_str.encode()).hexdigest()[:16]

    def _initialize_log_file(self):
        """Initialize log file with session metadata."""
        session_metadata = {
            "event": "SESSION_START",
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "run_number": self.run_number,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time(),
            "log_file": str(self.log_file),
            "schema_version": "1.0"
        }

        self._atomic_write(session_metadata)

    def _atomic_write(self, data: Dict[str, Any]):
        """
        Atomically write data to log file with file locking.

        Args:
            data: Dictionary to write as JSON line
        """
        max_retries = 5
        retry_delay = 0.1

        for attempt in range(max_retries):
            try:
                with open(self.log_file, 'a') as f:
                    # Acquire exclusive lock
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        # Write JSON line
                        f.write(json.dumps(data, default=str) + '\n')
                        f.flush()
                    finally:
                        # Release lock
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                return  # Success

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    # Final attempt failed - log to error file
                    error_file = self.output_dir / f"ERROR_{self.log_file.name}"
                    with open(error_file, 'a') as ef:
                        ef.write(f"FAILED_WRITE: {datetime.now().isoformat()}\n")
                        ef.write(f"Error: {str(e)}\n")
                        ef.write(f"Data: {json.dumps(data, default=str)}\n\n")
                    raise

    def start_condition(self, condition: str, order_position: int):
        """
        Mark the start of a new condition.

        Args:
            condition: Condition name (ConditionType value)
            order_position: Position in counterbalanced order (1-5)
        """
        self.current_condition = condition
        self.session_number += 1
        self.order_position = order_position

        condition_start = {
            "event": "CONDITION_START",
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "run_number": self.run_number,
            "session_number": self.session_number,
            "condition": condition,
            "order_position": order_position,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time()
        }

        self._atomic_write(condition_start)

    def end_condition(self, summary: Optional[Dict[str, Any]] = None):
        """
        Mark the end of current condition.

        Args:
            summary: Optional summary statistics for the condition
        """
        condition_end = {
            "event": "CONDITION_END",
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "run_number": self.run_number,
            "session_number": self.session_number,
            "condition": self.current_condition,
            "order_position": self.order_position,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time(),
            "summary": summary or {}
        }

        self._atomic_write(condition_end)

    def log_interaction(
        self,
        prompt_text: str,
        response_text: str,
        response_latency: float,
        api_used: str,
        api_parameters: Dict[str, Any],
        api_error: bool = False,
        error_message: Optional[str] = None,
        retry_count: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log a single LLM interaction.

        Args:
            prompt_text: Input prompt sent to LLM
            response_text: Response received from LLM
            response_latency: Time taken for response (seconds)
            api_used: "cerebras" or "gemini"
            api_parameters: API-specific parameters used
            api_error: Whether an error occurred
            error_message: Error message if applicable
            retry_count: Number of retries attempted
            metadata: Additional metadata

        Returns:
            interaction_id: Unique ID for this interaction
        """
        if self.current_condition is None:
            raise ValueError("Must call start_condition() before logging interactions")

        self.interaction_count += 1

        # Generate unique interaction ID
        interaction_id = f"{self.session_id}-{self.interaction_count:06d}"

        # Create interaction log
        log_entry = InteractionLog(
            interaction_id=interaction_id,
            session_id=self.session_id,
            agent_id=self.agent_id,
            condition=self.current_condition,
            run_number=self.run_number,
            session_number=self.session_number,
            order_position=self.order_position,
            timestamp=datetime.now().isoformat(),
            unix_timestamp=time.time(),
            prompt_text=prompt_text,
            response_text=response_text,
            response_length=len(response_text),
            response_latency=response_latency,
            api_used=api_used,
            api_parameters=api_parameters,
            api_error=api_error,
            error_message=error_message,
            retry_count=retry_count,
            metadata=metadata or {}
        )

        # Write to file
        self._atomic_write(log_entry.to_dict())

        return interaction_id

    def log_washout_period(self, duration_seconds: float, activity: str):
        """
        Log a washout period between conditions.

        Args:
            duration_seconds: Duration of washout
            activity: Description of washout activity
        """
        washout_log = {
            "event": "WASHOUT_PERIOD",
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "run_number": self.run_number,
            "duration_seconds": duration_seconds,
            "activity": activity,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time()
        }

        self._atomic_write(washout_log)

    def finalize(self, summary: Optional[Dict[str, Any]] = None):
        """
        Finalize the logging session.

        Args:
            summary: Optional session summary statistics
        """
        session_end = {
            "event": "SESSION_END",
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "run_number": self.run_number,
            "total_interactions": self.interaction_count,
            "total_sessions": self.session_number,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time(),
            "summary": summary or {}
        }

        self._atomic_write(session_end)


# =============================================================================
# 2. SESSION MANAGER
# =============================================================================

@dataclass
class ConditionOrder:
    """Represents a counterbalanced condition order."""
    order_id: int
    conditions: List[str]
    latin_square_row: int

    def __post_init__(self):
        if len(self.conditions) != 5:
            raise ValueError("Must have exactly 5 conditions")


class SessionManager:
    """
    Manages experimental sessions with proper counterbalancing and washout protocols.

    Features:
    - Latin square counterbalancing for 5 conditions
    - Washout period enforcement between conditions
    - Order effect tracking
    - Session state persistence
    - Completeness verification
    """

    def __init__(
        self,
        output_dir: Path,
        washout_duration: int = 300,  # 5 minutes default
        washout_activity: str = "neutral_task"
    ):
        """
        Initialize session manager.

        Args:
            output_dir: Directory for session state files
            washout_duration: Duration of washout period in seconds
            washout_activity: Description of washout activity
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.washout_duration = washout_duration
        self.washout_activity = washout_activity

        # Generate all Latin square orders (5x5 = 25 unique orders)
        self.condition_orders = self._generate_latin_square_orders()

        # Track assigned orders
        self.order_assignments: Dict[Tuple[str, int], int] = {}
        self.assignments_file = self.output_dir / "order_assignments.json"
        self._load_assignments()

    def _generate_latin_square_orders(self) -> List[ConditionOrder]:
        """
        Generate 5x5 Latin square for counterbalancing.

        Returns:
            List of ConditionOrder objects representing all possible orders
        """
        conditions = [c.value for c in ConditionType]

        # Standard Latin square for 5 conditions
        # Each condition appears exactly once in each position
        latin_square = [
            [0, 1, 2, 3, 4],  # ABCDE
            [1, 2, 3, 4, 0],  # BCDEA
            [2, 3, 4, 0, 1],  # CDEAB
            [3, 4, 0, 1, 2],  # DEABC
            [4, 0, 1, 2, 3],  # EABCD
        ]

        orders = []
        for i, row in enumerate(latin_square):
            order = ConditionOrder(
                order_id=i,
                conditions=[conditions[idx] for idx in row],
                latin_square_row=i
            )
            orders.append(order)

        return orders

    def _load_assignments(self):
        """Load existing order assignments from file."""
        if self.assignments_file.exists():
            with open(self.assignments_file, 'r') as f:
                data = json.load(f)
                # Convert string keys back to tuples
                self.order_assignments = {
                    (k.split('_')[0], int(k.split('_')[1])): v
                    for k, v in data.items()
                }

    def _save_assignments(self):
        """Save order assignments to file."""
        # Convert tuple keys to strings for JSON
        data = {
            f"{agent_id}_{run}": order_id
            for (agent_id, run), order_id in self.order_assignments.items()
        }

        with open(self.assignments_file, 'w') as f:
            json.dump(data, f, indent=2)

    def assign_order(self, agent_id: str, run_number: int) -> ConditionOrder:
        """
        Assign a counterbalanced order to an agent run.

        Uses balanced assignment to ensure even distribution across order types.

        Args:
            agent_id: Unique agent identifier
            run_number: Run number (1-10)

        Returns:
            ConditionOrder object
        """
        key = (agent_id, run_number)

        # Check if already assigned
        if key in self.order_assignments:
            order_id = self.order_assignments[key]
            return self.condition_orders[order_id]

        # Assign order using balanced allocation
        # Count current assignments
        order_counts = defaultdict(int)
        for assigned_order_id in self.order_assignments.values():
            order_counts[assigned_order_id] += 1

        # Choose least-assigned order
        min_count = min(order_counts.values()) if order_counts else 0
        available_orders = [
            i for i in range(len(self.condition_orders))
            if order_counts[i] <= min_count
        ]

        # Deterministic selection based on agent_id hash
        agent_hash = int(hashlib.sha256(f"{agent_id}_{run_number}".encode()).hexdigest(), 16)
        order_id = available_orders[agent_hash % len(available_orders)]

        # Save assignment
        self.order_assignments[key] = order_id
        self._save_assignments()

        return self.condition_orders[order_id]

    def get_order(self, agent_id: str, run_number: int) -> Optional[ConditionOrder]:
        """
        Get assigned order for an agent run.

        Args:
            agent_id: Unique agent identifier
            run_number: Run number

        Returns:
            ConditionOrder if assigned, None otherwise
        """
        key = (agent_id, run_number)
        if key in self.order_assignments:
            order_id = self.order_assignments[key]
            return self.condition_orders[order_id]
        return None

    def run_session(
        self,
        agent_id: str,
        run_number: int,
        condition_executor: callable
    ) -> Dict[str, Any]:
        """
        Run a complete experimental session with all conditions.

        Args:
            agent_id: Unique agent identifier
            run_number: Run number (1-10)
            condition_executor: Callable that executes a single condition
                                Signature: condition_executor(condition: str) -> Dict[str, Any]

        Returns:
            Session summary with results for all conditions
        """
        # Get or assign order
        order = self.assign_order(agent_id, run_number)

        # Create logger
        logger = InteractionLogger(
            output_dir=self.output_dir / "raw",
            agent_id=agent_id,
            run_number=run_number
        )

        session_results = {
            "agent_id": agent_id,
            "run_number": run_number,
            "order_id": order.order_id,
            "condition_order": order.conditions,
            "start_time": datetime.now().isoformat(),
            "conditions": {}
        }

        # Execute each condition in order
        for position, condition in enumerate(order.conditions, start=1):
            print(f"[Session] Agent {agent_id}, Run {run_number}, Position {position}: {condition}")

            # Start condition
            logger.start_condition(condition, position)

            # Execute condition
            try:
                result = condition_executor(condition, logger)
                session_results["conditions"][condition] = {
                    "position": position,
                    "result": result,
                    "success": True
                }
            except Exception as e:
                session_results["conditions"][condition] = {
                    "position": position,
                    "error": str(e),
                    "success": False
                }

            # End condition
            logger.end_condition()

            # Washout period (except after last condition)
            if position < len(order.conditions):
                print(f"[Session] Washout period: {self.washout_duration}s")
                logger.log_washout_period(self.washout_duration, self.washout_activity)
                time.sleep(self.washout_duration)

        # Finalize session
        session_results["end_time"] = datetime.now().isoformat()
        logger.finalize(session_results)

        return session_results

    def get_counterbalancing_summary(self) -> Dict[str, Any]:
        """
        Get summary of counterbalancing assignments.

        Returns:
            Dictionary with counterbalancing statistics
        """
        # Count assignments by order
        order_counts = defaultdict(int)
        for order_id in self.order_assignments.values():
            order_counts[order_id] += 1

        # Count conditions by position
        position_counts = defaultdict(lambda: defaultdict(int))
        for (agent_id, run), order_id in self.order_assignments.items():
            order = self.condition_orders[order_id]
            for pos, cond in enumerate(order.conditions, start=1):
                position_counts[pos][cond] += 1

        return {
            "total_assignments": len(self.order_assignments),
            "assignments_by_order": dict(order_counts),
            "conditions_by_position": {
                pos: dict(conds) for pos, conds in position_counts.items()
            },
            "latin_square_balanced": self._check_latin_square_balance()
        }

    def _check_latin_square_balance(self) -> bool:
        """Check if assignments maintain Latin square balance."""
        if not self.order_assignments:
            return True

        # Count assignments by order
        order_counts = defaultdict(int)
        for order_id in self.order_assignments.values():
            order_counts[order_id] += 1

        counts = list(order_counts.values())
        # Balanced if all counts differ by at most 1
        return max(counts) - min(counts) <= 1


# =============================================================================
# 3. DATA VALIDATOR
# =============================================================================

class DataValidator:
    """
    Validates data quality and completeness for Study 1.

    Checks:
    - Missing data
    - Complete counterbalancing
    - Duplicate detection
    - API error rates
    - Response quality metrics
    - Pseudo-replication handling
    """

    def __init__(self, data_dir: Path):
        """
        Initialize validator.

        Args:
            data_dir: Root directory containing raw data
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.validation_dir = self.data_dir / "validation"
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def load_all_interactions(self) -> pd.DataFrame:
        """
        Load all interaction logs into a DataFrame.

        Returns:
            DataFrame with all interactions
        """
        all_interactions = []

        for log_file in self.raw_dir.glob("*.jsonl"):
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        # Only process interaction logs (not events)
                        if "interaction_id" in data:
                            all_interactions.append(data)
                    except json.JSONDecodeError:
                        continue

        return pd.DataFrame(all_interactions)

    def validate_completeness(self) -> Dict[str, Any]:
        """
        Validate data completeness across all agents and runs.

        Returns:
            Validation report
        """
        df = self.load_all_interactions()

        if df.empty:
            return {"error": "No interaction data found"}

        # Count by agent and run
        agent_run_counts = df.groupby(['agent_id', 'run_number']).size().reset_index(name='count')

        # Expected: 5 conditions per run
        expected_conditions = 5

        # Check each agent-run for all conditions
        incomplete_runs = []
        for _, row in agent_run_counts.iterrows():
            agent_conds = df[
                (df['agent_id'] == row['agent_id']) &
                (df['run_number'] == row['run_number'])
            ]['condition'].unique()

            if len(agent_conds) < expected_conditions:
                incomplete_runs.append({
                    "agent_id": row['agent_id'],
                    "run_number": row['run_number'],
                    "conditions_found": len(agent_conds),
                    "missing_conditions": list(set([c.value for c in ConditionType]) - set(agent_conds))
                })

        # Summary statistics
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_interactions": len(df),
            "unique_agents": df['agent_id'].nunique(),
            "unique_runs": len(agent_run_counts),
            "conditions_tested": df['condition'].unique().tolist(),
            "incomplete_runs": incomplete_runs,
            "completeness_rate": 1 - (len(incomplete_runs) / len(agent_run_counts)) if len(agent_run_counts) > 0 else 0,
            "interactions_by_condition": df['condition'].value_counts().to_dict(),
            "interactions_by_agent": df.groupby('agent_id').size().to_dict()
        }

        # Save report
        report_file = self.validation_dir / f"completeness_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def validate_counterbalancing(self, session_manager: SessionManager) -> Dict[str, Any]:
        """
        Validate counterbalancing across all runs.

        Args:
            session_manager: SessionManager instance with assignments

        Returns:
            Validation report
        """
        df = self.load_all_interactions()

        if df.empty:
            return {"error": "No interaction data found"}

        # Get counterbalancing summary from session manager
        cb_summary = session_manager.get_counterbalancing_summary()

        # Check order effects - compare conditions by position
        position_stats = []
        for pos in range(1, 6):
            pos_data = df[df['order_position'] == pos]
            if not pos_data.empty:
                position_stats.append({
                    "position": pos,
                    "n_interactions": len(pos_data),
                    "conditions": pos_data['condition'].value_counts().to_dict(),
                    "mean_response_length": pos_data['response_length'].mean(),
                    "mean_latency": pos_data['response_latency'].mean()
                })

        report = {
            "timestamp": datetime.now().isoformat(),
            "counterbalancing_summary": cb_summary,
            "position_statistics": position_stats,
            "balance_quality": "good" if cb_summary.get("latin_square_balanced", False) else "poor",
            "recommendations": []
        }

        # Add recommendations
        if not cb_summary.get("latin_square_balanced", False):
            report["recommendations"].append("Add more runs to balance order assignments")

        # Save report
        report_file = self.validation_dir / f"counterbalancing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def detect_duplicates(self) -> Dict[str, Any]:
        """
        Detect duplicate interactions.

        Returns:
            Report of potential duplicates
        """
        df = self.load_all_interactions()

        if df.empty:
            return {"error": "No interaction data found"}

        # Check for duplicate interaction IDs
        duplicate_ids = df[df.duplicated(subset=['interaction_id'], keep=False)]

        # Check for duplicate (agent, run, session, order_position) combinations
        duplicate_positions = df[df.duplicated(
            subset=['agent_id', 'run_number', 'session_number', 'order_position'],
            keep=False
        )]

        report = {
            "timestamp": datetime.now().isoformat(),
            "duplicate_interaction_ids": len(duplicate_ids),
            "duplicate_positions": len(duplicate_positions),
            "duplicate_id_list": duplicate_ids['interaction_id'].tolist() if not duplicate_ids.empty else [],
            "duplicate_position_list": duplicate_positions[
                ['agent_id', 'run_number', 'session_number', 'order_position']
            ].to_dict('records') if not duplicate_positions.empty else []
        }

        # Save report
        report_file = self.validation_dir / f"duplicates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def validate_quality(self) -> Dict[str, Any]:
        """
        Validate data quality metrics.

        Returns:
            Quality report
        """
        df = self.load_all_interactions()

        if df.empty:
            return {"error": "No interaction data found"}

        # API error analysis
        error_rate = df['api_error'].mean() if 'api_error' in df.columns else 0
        errors_by_condition = df.groupby('condition')['api_error'].mean().to_dict() if 'api_error' in df.columns else {}

        # Response quality
        quality_metrics = {
            "mean_response_length": df['response_length'].mean(),
            "std_response_length": df['response_length'].std(),
            "mean_latency": df['response_latency'].mean(),
            "std_latency": df['response_latency'].std(),
            "min_response_length": df['response_length'].min(),
            "max_response_length": df['response_length'].max(),
        }

        # Quality by condition
        condition_quality = {}
        for condition in df['condition'].unique():
            cond_df = df[df['condition'] == condition]
            condition_quality[condition] = {
                "n_interactions": len(cond_df),
                "mean_response_length": cond_df['response_length'].mean(),
                "mean_latency": cond_df['response_latency'].mean(),
                "error_rate": cond_df['api_error'].mean() if 'api_error' in cond_df.columns else 0
            }

        # Identify outliers
        outliers = {
            "response_length_outliers": len(df[
                (df['response_length'] > quality_metrics['mean_response_length'] + 3 * quality_metrics['std_response_length']) |
                (df['response_length'] < quality_metrics['mean_response_length'] - 3 * quality_metrics['std_response_length'])
            ]),
            "latency_outliers": len(df[
                df['response_latency'] > quality_metrics['mean_latency'] + 3 * quality_metrics['std_latency']
            ])
        }

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_interactions": len(df),
            "overall_error_rate": error_rate,
            "errors_by_condition": errors_by_condition,
            "quality_metrics": quality_metrics,
            "quality_by_condition": condition_quality,
            "outliers": outliers,
            "quality_flags": []
        }

        # Add quality flags
        if error_rate > 0.20:
            report["quality_flags"].append("HIGH_ERROR_RATE: >20% API errors")

        if outliers["response_length_outliers"] > len(df) * 0.05:
            report["quality_flags"].append("MANY_OUTLIERS: >5% response length outliers")

        # Save report
        report_file = self.validation_dir / f"quality_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def validate_pseudo_replication(self) -> Dict[str, Any]:
        """
        Check for pseudo-replication issues and provide aggregation guidance.

        Returns:
            Report on pseudo-replication handling
        """
        df = self.load_all_interactions()

        if df.empty:
            return {"error": "No interaction data found"}

        # Hierarchical structure summary
        hierarchy = {
            "level_1_conditions": df['condition'].nunique(),
            "level_2_agents": df['agent_id'].nunique(),
            "level_3_runs": df.groupby('agent_id')['run_number'].nunique().to_dict(),
            "level_4_interactions": len(df)
        }

        # Calculate effective sample sizes
        # Following STATISTICAL_METHODOLOGY.md: need to aggregate to agent level
        agent_level = df.groupby(['agent_id', 'condition']).agg({
            'response_length': ['mean', 'std', 'count'],
            'response_latency': ['mean', 'std']
        }).reset_index()

        effective_n = {
            "total_interactions": len(df),
            "effective_n_agents": len(agent_level),
            "agents_per_condition": agent_level.groupby('condition').size().to_dict(),
            "mean_interactions_per_agent": df.groupby('agent_id').size().mean()
        }

        report = {
            "timestamp": datetime.now().isoformat(),
            "hierarchy": hierarchy,
            "effective_sample_sizes": effective_n,
            "aggregation_guidance": {
                "primary_unit": "agent",
                "aggregation_method": "Mean across runs within agent, then compare across agents",
                "avoid": "Treating individual interactions as independent observations",
                "statistical_test": "Mixed-effects model or agent-level t-test/ANOVA"
            },
            "pseudo_replication_risk": "low" if effective_n["effective_n_agents"] >= 10 else "high"
        }

        # Save report
        report_file = self.validation_dir / f"pseudo_replication_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def run_all_validations(self, session_manager: SessionManager) -> Dict[str, Any]:
        """
        Run all validation checks.

        Args:
            session_manager: SessionManager instance

        Returns:
            Comprehensive validation report
        """
        print("Running comprehensive data validation...")

        validations = {
            "completeness": self.validate_completeness(),
            "counterbalancing": self.validate_counterbalancing(session_manager),
            "duplicates": self.detect_duplicates(),
            "quality": self.validate_quality(),
            "pseudo_replication": self.validate_pseudo_replication()
        }

        # Overall summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "validation_results": validations,
            "overall_status": "pass" if self._check_overall_pass(validations) else "fail",
            "critical_issues": self._extract_critical_issues(validations)
        }

        # Save comprehensive report
        report_file = self.validation_dir / f"comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"Validation complete. Report saved to {report_file}")

        return summary

    def _check_overall_pass(self, validations: Dict[str, Any]) -> bool:
        """Check if all validations pass."""
        # Completeness check
        if validations["completeness"].get("completeness_rate", 0) < 0.95:
            return False

        # Quality check
        if validations["quality"].get("overall_error_rate", 1) > 0.20:
            return False

        # Duplicates check
        if validations["duplicates"].get("duplicate_interaction_ids", 0) > 0:
            return False

        return True

    def _extract_critical_issues(self, validations: Dict[str, Any]) -> List[str]:
        """Extract critical issues from validation results."""
        issues = []

        # Completeness issues
        incomplete = validations["completeness"].get("incomplete_runs", [])
        if incomplete:
            issues.append(f"{len(incomplete)} incomplete runs detected")

        # Quality issues
        quality_flags = validations["quality"].get("quality_flags", [])
        issues.extend(quality_flags)

        # Duplicate issues
        dup_ids = validations["duplicates"].get("duplicate_interaction_ids", 0)
        if dup_ids > 0:
            issues.append(f"{dup_ids} duplicate interaction IDs found")

        # Pseudo-replication risk
        pr_risk = validations["pseudo_replication"].get("pseudo_replication_risk", "low")
        if pr_risk == "high":
            issues.append("High pseudo-replication risk - insufficient agents")

        return issues


# =============================================================================
# 4. DATA AGGREGATION
# =============================================================================

class DataAggregator:
    """
    Aggregates raw interaction logs to analysis-ready datasets.

    Provides multiple aggregation levels:
    - Interaction-level (raw)
    - Session-level (condition × agent × run)
    - Agent-level (proper unit for between-subjects comparisons)
    """

    def __init__(self, data_dir: Path):
        """
        Initialize aggregator.

        Args:
            data_dir: Root data directory
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_interactions(self) -> pd.DataFrame:
        """Load all interactions into DataFrame."""
        all_interactions = []

        for log_file in self.raw_dir.glob("*.jsonl"):
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if "interaction_id" in data:
                            all_interactions.append(data)
                    except json.JSONDecodeError:
                        continue

        return pd.DataFrame(all_interactions)

    def aggregate_to_session_level(self) -> pd.DataFrame:
        """
        Aggregate to session level (condition × agent × run).

        Returns:
            DataFrame with one row per session
        """
        df = self.load_interactions()

        if df.empty:
            return pd.DataFrame()

        # Group by session
        session_agg = df.groupby(['agent_id', 'run_number', 'condition', 'order_position']).agg({
            'response_length': ['mean', 'std', 'min', 'max', 'count'],
            'response_latency': ['mean', 'std'],
            'api_error': ['sum', 'mean'],
            'interaction_id': 'count'
        }).reset_index()

        # Flatten column names
        session_agg.columns = ['_'.join(col).strip('_') for col in session_agg.columns]

        # Save
        output_file = self.processed_dir / "session_level.csv"
        session_agg.to_csv(output_file, index=False)

        return session_agg

    def aggregate_to_agent_level(self) -> pd.DataFrame:
        """
        Aggregate to agent level (proper unit for analysis).

        Following STATISTICAL_METHODOLOGY.md guidance:
        - First aggregate run → agent
        - Then compare across agents

        Returns:
            DataFrame with one row per agent × condition
        """
        df = self.load_interactions()

        if df.empty:
            return pd.DataFrame()

        # First level: run aggregation
        run_agg = df.groupby(['agent_id', 'run_number', 'condition']).agg({
            'response_length': 'mean',
            'response_latency': 'mean',
            'api_error': 'mean'
        }).reset_index()

        # Second level: agent aggregation (mean across runs)
        agent_agg = run_agg.groupby(['agent_id', 'condition']).agg({
            'response_length': ['mean', 'std', 'count'],
            'response_latency': ['mean', 'std'],
            'api_error': ['mean', 'std'],
            'run_number': 'count'
        }).reset_index()

        # Flatten column names
        agent_agg.columns = ['_'.join(col).strip('_') for col in agent_agg.columns]

        # Save
        output_file = self.processed_dir / "agent_level.csv"
        agent_agg.to_csv(output_file, index=False)

        return agent_agg

    def create_analysis_datasets(self):
        """Create all aggregated datasets for analysis."""
        print("Creating aggregated datasets...")

        # Session level
        session_df = self.aggregate_to_session_level()
        print(f"Session-level data: {len(session_df)} rows")

        # Agent level
        agent_df = self.aggregate_to_agent_level()
        print(f"Agent-level data: {len(agent_df)} rows")

        # Save metadata
        metadata = {
            "created": datetime.now().isoformat(),
            "session_level_file": "session_level.csv",
            "agent_level_file": "agent_level.csv",
            "aggregation_method": "Mean across runs within agent",
            "primary_analysis_level": "agent"
        }

        with open(self.processed_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Aggregated data saved to {self.processed_dir}")


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    import sys

    # Setup directories
    base_dir = Path("/home/user/Data-Statistics/study1/data")

    print("=" * 70)
    print("Study 1 Data Pipeline - Example Usage")
    print("=" * 70)

    # 1. Initialize Session Manager
    print("\n1. Initializing Session Manager...")
    session_mgr = SessionManager(
        output_dir=base_dir,
        washout_duration=10,  # Short for demo
        washout_activity="neutral_counting_task"
    )

    # 2. Show counterbalancing
    print("\n2. Condition Orders (Latin Square):")
    for order in session_mgr.condition_orders:
        print(f"   Order {order.order_id}: {' → '.join(order.conditions)}")

    # 3. Example: Assign order to an agent
    print("\n3. Assigning order to agent...")
    agent_id = "agent_001"
    run_num = 1
    assigned_order = session_mgr.assign_order(agent_id, run_num)
    print(f"   Agent {agent_id}, Run {run_num}: {' → '.join(assigned_order.conditions)}")

    # 4. Show directory structure
    print("\n4. Data Directory Structure:")
    print(f"   {base_dir}/")
    print(f"   ├── raw/              # Raw JSONL logs")
    print(f"   ├── processed/        # Aggregated CSVs")
    print(f"   └── validation/       # QC reports")

    # 5. Initialize components
    print("\n5. Initializing components...")

    validator = DataValidator(base_dir)
    aggregator = DataAggregator(base_dir)

    print("   ✓ InteractionLogger - Ready for logging")
    print("   ✓ SessionManager - Counterbalancing active")
    print("   ✓ DataValidator - Quality checks ready")
    print("   ✓ DataAggregator - Processing pipelines ready")

    print("\n" + "=" * 70)
    print("Data pipeline initialized successfully!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Run experiments with InteractionLogger")
    print("2. Use SessionManager.run_session() for complete runs")
    print("3. Validate data with DataValidator.run_all_validations()")
    print("4. Aggregate data with DataAggregator.create_analysis_datasets()")
    print("=" * 70)
