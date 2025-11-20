#!/usr/bin/env python3
"""
Study 1: Agent Stress Behavior - Main Simulation Runner
Integrates all components: experimental design, prompts, API, data pipeline, coding
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

# Add study1 directory to path
sys.path.insert(0, str(Path(__file__).parent))

from experimental_design import (
    ExperimentalDesign,
    Condition,
    AgentPersona,
    Session
)
from prompts import (
    get_system_prompt,
    generate_task_prompt,
    generate_standup_prompt,
    TEMPERATURE,
    MAX_TOKENS
)
from api_client import APIManager
from data_pipeline import InteractionLogger, SessionManager, DataValidator
from behavioral_coding import ResponseCoder, AutoCoder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Mapping between experimental_design.py Condition enum and prompts.py condition names
CONDITION_MAPPING = {
    "N": "null",
    "I": "information",
    "B": "baseline",
    "P": "positive_stress",
    "S": "negative_stress"
}


class SimulationRunner:
    """
    Main simulation runner that orchestrates the complete Study 1 experiment.
    """

    def __init__(
        self,
        cerebras_api_key: str,
        gemini_api_key: str,
        output_dir: str = "study1_results",
        seed: int = 42
    ):
        """
        Initialize simulation runner.

        Args:
            cerebras_api_key: Cerebras API key
            gemini_api_key: Google Gemini API key
            output_dir: Output directory for results
            seed: Random seed for reproducibility
        """
        self.cerebras_key = cerebras_api_key
        self.gemini_key = gemini_api_key
        self.output_dir = Path(output_dir)
        self.seed = seed

        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
        (self.output_dir / "data").mkdir(exist_ok=True)
        (self.output_dir / "coded").mkdir(exist_ok=True)

        # Initialize components
        logger.info("Initializing experimental design...")
        self.design = ExperimentalDesign(seed=seed)

        logger.info("Initializing API manager...")
        self.api_manager = APIManager(
            cerebras_api_key=cerebras_api_key,
            gemini_api_key=gemini_api_key
        )

        logger.info("Initializing behavioral coder...")
        self.coder = ResponseCoder()

        # Note: InteractionLogger will be created per agent/run in the simulation loops

        logger.info("Simulation runner initialized successfully")

    def run_pilot(
        self,
        n_agents: int = 2,
        interactions_per_condition: int = 5
    ) -> Dict[str, Any]:
        """
        Run a quick pilot study to test the full pipeline.

        Args:
            n_agents: Number of agents to test (default: 2)
            interactions_per_condition: Interactions per condition (default: 5)

        Returns:
            Dict with pilot results and validation report
        """
        logger.info("="*80)
        logger.info("STARTING PILOT STUDY")
        logger.info("="*80)
        logger.info(f"Agents: {n_agents}, Interactions/condition: {interactions_per_condition}")

        # Select agents for pilot
        all_agents = list(AgentPersona)
        pilot_agents = all_agents[:n_agents]

        # Select conditions (test all 5)
        conditions = list(Condition)

        pilot_results = {
            'start_time': datetime.now().isoformat(),
            'n_agents': n_agents,
            'n_conditions': len(conditions),
            'interactions_per_condition': interactions_per_condition,
            'agents': [],
            'total_interactions': 0,
            'successful_interactions': 0,
            'failed_interactions': 0,
            'api_stats': {}
        }

        # Run through each agent and condition
        for agent in pilot_agents:
            logger.info(f"\n{'='*60}")
            logger.info(f"AGENT: {agent.value}")
            logger.info(f"{'='*60}")

            agent_results = {
                'agent': agent.value,
                'conditions': []
            }

            # Create logger for this agent
            interaction_logger = InteractionLogger(
                output_dir=self.output_dir / "data" / "raw",
                agent_id=agent.value,
                run_number=0
            )

            for condition in conditions:
                logger.info(f"\n  Condition: {condition.value}")
                logger.info(f"  {'-'*50}")

                # Start condition
                interaction_logger.start_condition(
                    condition=condition.value,
                    order_position=conditions.index(condition) + 1  # 1-indexed
                )

                condition_results = {
                    'condition': condition.value,
                    'interactions': [],
                    'success_count': 0,
                    'fail_count': 0
                }

                # Get system prompt for this agent/condition
                condition_name = CONDITION_MAPPING.get(condition.value, condition.value)
                system_prompt = get_system_prompt(agent.value, condition_name)

                # Run multiple interactions
                for i in range(interactions_per_condition):
                    # Get task prompt (alternating between types for variety)
                    if i % 3 == 0:
                        task_prompt = generate_standup_prompt()
                    elif i % 3 == 1:
                        task_prompt = generate_task_prompt(
                            task_title=f"Feature Implementation {i+1}",
                            skill_list="Python, API design, testing",
                            points=5,
                            week_number=1
                        )
                    else:
                        task_prompt = f"What is your progress on this week's tasks? Please provide a brief update."

                    # Generate response via API
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": task_prompt}
                    ]

                    logger.info(f"    Interaction {i+1}/{interactions_per_condition}...")

                    start_time = time.time()
                    result = self.api_manager.generate(
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS
                    )
                    latency = time.time() - start_time

                    if result:
                        # Log successful interaction
                        interaction_logger.log_interaction(
                            prompt_text=task_prompt,
                            response_text=result['content'],
                            response_latency=result['latency'],
                            api_used=result['provider'],
                            api_parameters={'temperature': TEMPERATURE, 'max_tokens': MAX_TOKENS}
                        )

                        condition_results['interactions'].append({
                            'success': True,
                            'latency': result['latency'],
                            'provider': result['provider'],
                            'response_length': len(result['content'])
                        })
                        condition_results['success_count'] += 1
                        pilot_results['successful_interactions'] += 1

                        logger.info(f"      ✓ Success ({result['provider']}, {result['latency']:.2f}s)")
                    else:
                        # Log failure
                        condition_results['interactions'].append({
                            'success': False,
                            'latency': latency
                        })
                        condition_results['fail_count'] += 1
                        pilot_results['failed_interactions'] += 1

                        logger.error(f"      ✗ Failed after {latency:.2f}s")

                    pilot_results['total_interactions'] += 1

                # Log condition end
                interaction_logger.end_condition(
                    summary={
                        'total_interactions': len(condition_results['interactions']),
                        'successful': condition_results['success_count'],
                        'failed': condition_results['fail_count']
                    }
                )

                agent_results['conditions'].append(condition_results)

                logger.info(f"    Condition complete: {condition_results['success_count']}/{interactions_per_condition} successful")

            pilot_results['agents'].append(agent_results)

        # Get API stats
        pilot_results['api_stats'] = self.api_manager.get_stats()
        pilot_results['end_time'] = datetime.now().isoformat()

        # Save pilot results
        results_file = self.output_dir / "pilot_results.json"
        with open(results_file, 'w') as f:
            json.dump(pilot_results, f, indent=2)

        logger.info("\n" + "="*80)
        logger.info("PILOT STUDY COMPLETE")
        logger.info("="*80)
        logger.info(f"Total interactions: {pilot_results['total_interactions']}")
        logger.info(f"Successful: {pilot_results['successful_interactions']}")
        logger.info(f"Failed: {pilot_results['failed_interactions']}")
        logger.info(f"Success rate: {pilot_results['successful_interactions']/pilot_results['total_interactions']*100:.1f}%")
        logger.info(f"Results saved to: {results_file}")

        # Print API stats
        self.api_manager.print_stats()

        return pilot_results

    def run_full_study(
        self,
        n_agents: int = 30,
        n_runs: int = 10,
        interactions_per_condition: int = 10
    ) -> Dict[str, Any]:
        """
        Run the complete Study 1 experiment.

        Args:
            n_agents: Number of agents (default: 30)
            n_runs: Number of runs per agent (default: 10)
            interactions_per_condition: Interactions per condition (default: 10)

        Returns:
            Dict with complete study results
        """
        logger.info("="*80)
        logger.info("STARTING FULL STUDY")
        logger.info("="*80)
        logger.info(f"Design: {n_agents} agents × 5 conditions × {n_runs} runs × {interactions_per_condition} interactions")
        logger.info(f"Total planned interactions: {n_agents * 5 * n_runs * interactions_per_condition}")

        # Initialize session manager
        session_manager = SessionManager(
            output_dir=str(self.output_dir / "data")
        )

        # This is a simplified version - full implementation would follow
        # the counterbalancing and washout protocols from experimental_design.py

        logger.warning("Full study implementation requires washout protocols and counterbalancing")
        logger.warning("Use run_pilot() for testing the complete pipeline")

        return {
            'status': 'not_implemented',
            'message': 'Use run_pilot() for testing. Full study requires careful scheduling.'
        }

    def validate_data(self) -> Dict[str, Any]:
        """
        Run data validation on collected data.

        Returns:
            Validation report
        """
        logger.info("Running data validation...")

        validator = DataValidator()
        report = validator.validate_all(
            data_dir=str(self.output_dir / "data" / "raw")
        )

        # Save validation report
        report_file = self.output_dir / "validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Validation report saved to: {report_file}")

        return report

    def code_responses(self) -> str:
        """
        Run behavioral coding on all collected responses.

        Returns:
            Path to coded output CSV
        """
        logger.info("Coding all responses with 19-code behavioral scheme...")

        # Load all interactions from JSONL
        data_dir = self.output_dir / "data" / "raw"
        all_responses = []

        for jsonl_file in data_dir.glob("*.jsonl"):
            with open(jsonl_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if data.get('event_type') == 'INTERACTION':
                        all_responses.append({
                            'response_id': data.get('interaction_id', ''),
                            'response_text': data.get('response_text', ''),
                            'agent_name': data.get('agent_id', ''),
                            'condition': data.get('condition', ''),
                            'week': data.get('session_number', 0)
                        })

        logger.info(f"Found {len(all_responses)} responses to code")

        # Code all responses
        auto_coder = AutoCoder()
        coded_data = auto_coder.process_batch(
            responses=all_responses,
            output_path=str(self.output_dir / "coded" / "coded_responses.csv")
        )

        # Generate summary report
        auto_coder.print_summary_report(coded_data)

        output_path = self.output_dir / "coded" / "coded_responses.csv"
        logger.info(f"Coded data saved to: {output_path}")

        return str(output_path)

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.api_manager.close()


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Study 1: Agent Stress Behavior Simulation"
    )
    parser.add_argument(
        '--mode',
        choices=['pilot', 'full', 'validate', 'code'],
        default='pilot',
        help='Simulation mode (default: pilot)'
    )
    parser.add_argument(
        '--n-agents',
        type=int,
        default=2,
        help='Number of agents for pilot (default: 2)'
    )
    parser.add_argument(
        '--interactions',
        type=int,
        default=5,
        help='Interactions per condition (default: 5)'
    )
    parser.add_argument(
        '--output-dir',
        default='study1_results',
        help='Output directory (default: study1_results)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed (default: 42)'
    )

    args = parser.parse_args()

    # Get API keys from environment or hardcoded defaults
    cerebras_key = os.environ.get(
        'CEREBRAS_API_KEY',
        'csk-ywwnmnr4k4tnwrr2xfwdj855f3yxfv2t9n2m5dk8r48jv9w2'
    )
    gemini_key = os.environ.get(
        'GEMINI_API_KEY',
        'AIzaSyD7JLZ7gt4bE5i87zcycGJS2_Nvfv1VNwI'
    )

    # Initialize runner
    runner = SimulationRunner(
        cerebras_api_key=cerebras_key,
        gemini_api_key=gemini_key,
        output_dir=args.output_dir,
        seed=args.seed
    )

    try:
        if args.mode == 'pilot':
            results = runner.run_pilot(
                n_agents=args.n_agents,
                interactions_per_condition=args.interactions
            )

        elif args.mode == 'full':
            results = runner.run_full_study()

        elif args.mode == 'validate':
            results = runner.validate_data()

        elif args.mode == 'code':
            results = runner.code_responses()

        logger.info("\n" + "="*80)
        logger.info("SIMULATION COMPLETE")
        logger.info("="*80)

    except KeyboardInterrupt:
        logger.warning("\nSimulation interrupted by user")

    finally:
        runner.cleanup()


if __name__ == '__main__':
    main()
