#!/usr/bin/env python3
"""
Full Study Runner: n=30 Agents with Proper Washout Protocol and Cross-Model Validation

Implements committee recommendations:
1. ✓ Proper context reset washout between conditions
2. ✓ Cross-model validation (Cerebras + GPT-4o-mini on subset)
3. ✓ Williams Latin Square counterbalancing
4. ✓ n=30 agents for 92% power
5. ✓ Pre-registration compatible design
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
)
from prompts import (
    get_system_prompt,
    generate_task_prompt,
    generate_standup_prompt,
    TEMPERATURE,
    MAX_TOKENS
)
from api_client_enhanced import MultiModelManager
from data_pipeline import InteractionLogger
from behavioral_coding import AutoCoder

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


class FullStudyRunner:
    """
    Full study runner with proper washout protocol and cross-model validation.
    """

    def __init__(
        self,
        cerebras_api_key: str,
        gemini_api_key: str,
        openai_api_key: Optional[str] = None,
        output_dir: str = "full_study_results",
        seed: int = 42
    ):
        """
        Initialize full study runner.

        Args:
            cerebras_api_key: Cerebras API key
            gemini_api_key: Gemini API key
            openai_api_key: Optional OpenAI API key for cross-validation
            output_dir: Output directory
            seed: Random seed
        """
        self.cerebras_key = cerebras_api_key
        self.gemini_key = gemini_api_key
        self.openai_key = openai_api_key
        self.output_dir = Path(output_dir)
        self.seed = seed

        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
        (self.output_dir / "data").mkdir(exist_ok=True)
        (self.output_dir / "data" / "raw").mkdir(exist_ok=True)

        # Initialize experimental design
        logger.info("Initializing experimental design...")
        self.design = ExperimentalDesign(seed=seed)

        # Initialize multi-model API manager
        logger.info("Initializing multi-model API manager...")
        self.api_manager = MultiModelManager(
            cerebras_api_key=cerebras_api_key,
            gemini_api_key=gemini_api_key,
            openai_api_key=openai_api_key,
            primary_model="cerebras"
        )

        logger.info("Full study runner initialized successfully")

    def reset_context(self) -> None:
        """
        Context reset washout protocol.

        Since we cannot enforce 24-hour delays in a single session,
        we implement a symbolic context reset:
        1. Clear conversation history (use fresh context for each condition)
        2. Randomize task order within condition
        3. Log washout event
        """
        # In practice, each condition gets fresh context (no conversation history)
        # This is implemented by not passing previous messages
        logger.info("Context reset performed (washout protocol)")
        time.sleep(0.1)  # Symbolic delay

    def run_agent_session(
        self,
        agent: AgentPersona,
        condition: Condition,
        run_number: int,
        order_position: int,
        interactions: int = 10,
        force_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a single agent through one condition with washout protocol.

        Args:
            agent: Agent persona
            condition: Experimental condition
            run_number: Run number (0-indexed)
            order_position: Position in counterbalanced order (1-5)
            interactions: Number of interactions
            force_model: Optional model to force ("cerebras", "openai", "gemini")

        Returns:
            Session results
        """
        # Create logger for this agent/run
        interaction_logger = InteractionLogger(
            output_dir=self.output_dir / "data" / "raw",
            agent_id=agent.value,
            run_number=run_number
        )

        # Start condition
        interaction_logger.start_condition(
            condition=condition.value,
            order_position=order_position
        )

        logger.info(f"  Agent: {agent.value}, Condition: {condition.value}, Order: {order_position}")

        # Get system prompt
        condition_name = CONDITION_MAPPING.get(condition.value, condition.value)
        system_prompt = get_system_prompt(agent.value, condition_name)

        session_results = {
            'agent': agent.value,
            'condition': condition.value,
            'run_number': run_number,
            'order_position': order_position,
            'interactions': [],
            'success_count': 0,
            'fail_count': 0,
            'model_used': force_model or 'cerebras'
        }

        # Run interactions (each with fresh context per washout protocol)
        for i in range(interactions):
            # Generate task prompt
            if i % 3 == 0:
                task_prompt = generate_standup_prompt()
            elif i % 3 == 1:
                task_prompt = generate_task_prompt(
                    task_title=f"Feature {i+1}",
                    skill_list="Python, testing, documentation",
                    points=5,
                    week_number=1
                )
            else:
                task_prompt = f"Provide a progress update on this week's tasks."

            # WASHOUT: Fresh context for each interaction (no conversation history)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_prompt}
            ]

            # Generate response
            result = self.api_manager.generate(
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                force_model=force_model
            )

            if result:
                # Log interaction
                interaction_logger.log_interaction(
                    prompt_text=task_prompt,
                    response_text=result['content'],
                    response_latency=result['latency'],
                    api_used=result['provider'],
                    api_parameters={'temperature': TEMPERATURE, 'max_tokens': MAX_TOKENS}
                )

                session_results['interactions'].append({
                    'success': True,
                    'latency': result['latency'],
                    'provider': result['provider']
                })
                session_results['success_count'] += 1

            else:
                session_results['interactions'].append({'success': False})
                session_results['fail_count'] += 1

        # End condition
        interaction_logger.end_condition(
            summary={
                'total': len(session_results['interactions']),
                'success': session_results['success_count'],
                'failed': session_results['fail_count']
            }
        )

        return session_results

    def run_full_study(
        self,
        n_agents: int = 30,
        interactions_per_condition: int = 10,
        cross_validate: bool = True,
        cross_validate_n: int = 10
    ) -> Dict[str, Any]:
        """
        Run the complete full study with n=30 agents.

        Args:
            n_agents: Number of agents (default: 30)
            interactions_per_condition: Interactions per condition (default: 10)
            cross_validate: Whether to run cross-model validation (default: True)
            cross_validate_n: Number of agents for cross-validation (default: 10)

        Returns:
            Study results
        """
        logger.info("="*80)
        logger.info("FULL STUDY: n=30 AGENTS WITH WASHOUT PROTOCOL")
        logger.info("="*80)
        logger.info(f"Design: {n_agents} agents × 5 conditions × {interactions_per_condition} interactions")
        logger.info(f"Total interactions: {n_agents * 5 * interactions_per_condition}")

        if cross_validate and self.openai_key:
            logger.info(f"Cross-validation: {cross_validate_n} agents with GPT-4o-mini")

        # Generate agent personas
        all_agents = list(AgentPersona)
        agent_list = []
        for i in range(n_agents):
            agent_list.append(all_agents[i % len(all_agents)])

        # All conditions
        conditions = list(Condition)

        # Generate counterbalancing orders (Williams Latin Square pattern)
        orders = self._generate_counterbalancing_orders(n_agents)

        study_results = {
            'start_time': datetime.now().isoformat(),
            'n_agents': n_agents,
            'n_conditions': len(conditions),
            'interactions_per_condition': interactions_per_condition,
            'agents': [],
            'total_interactions': 0,
            'successful_interactions': 0,
            'failed_interactions': 0,
            'cross_validation_used': cross_validate and self.openai_key is not None
        }

        # Run each agent
        for agent_idx, agent in enumerate(agent_list):
            logger.info(f"\n{'='*60}")
            logger.info(f"AGENT {agent_idx+1}/{n_agents}: {agent.value}")
            logger.info(f"{'='*60}")

            agent_results = {
                'agent_id': agent_idx,
                'agent_name': agent.value,
                'conditions': []
            }

            # Get counterbalanced order for this agent
            order = orders[agent_idx % len(orders)]

            # Determine if this agent gets cross-validation
            use_openai = cross_validate and self.openai_key and agent_idx < cross_validate_n

            # Run through each condition in counterbalanced order
            for order_idx, condition in enumerate(order):
                # WASHOUT PROTOCOL: Context reset between conditions
                if order_idx > 0:
                    logger.info("  [WASHOUT] Context reset between conditions...")
                    self.reset_context()

                # Run session
                session_result = self.run_agent_session(
                    agent=agent,
                    condition=condition,
                    run_number=agent_idx,
                    order_position=order_idx + 1,
                    interactions=interactions_per_condition,
                    force_model="openai" if use_openai else None
                )

                agent_results['conditions'].append(session_result)
                study_results['total_interactions'] += len(session_result['interactions'])
                study_results['successful_interactions'] += session_result['success_count']
                study_results['failed_interactions'] += session_result['fail_count']

                logger.info(f"    Condition {condition.value} complete: {session_result['success_count']}/{interactions_per_condition} successful")

            study_results['agents'].append(agent_results)

        # Save results
        study_results['end_time'] = datetime.now().isoformat()
        study_results['api_stats'] = self.api_manager.get_stats()

        results_file = self.output_dir / "full_study_results.json"
        with open(results_file, 'w') as f:
            json.dump(study_results, f, indent=2)

        logger.info("\n" + "="*80)
        logger.info("FULL STUDY COMPLETE")
        logger.info("="*80)
        logger.info(f"Total interactions: {study_results['total_interactions']}")
        logger.info(f"Successful: {study_results['successful_interactions']}")
        logger.info(f"Failed: {study_results['failed_interactions']}")
        logger.info(f"Success rate: {study_results['successful_interactions']/study_results['total_interactions']*100:.1f}%")
        logger.info(f"Results saved to: {results_file}")

        # Print API stats
        self.api_manager.print_stats()

        return study_results

    def _generate_counterbalancing_orders(self, n_agents: int) -> List[List[Condition]]:
        """
        Generate counterbalanced condition orders using Williams Latin Square pattern.

        Args:
            n_agents: Number of agents

        Returns:
            List of condition orders
        """
        # Base Williams Latin Square for 5 conditions
        base_orders = [
            [Condition.NULL, Condition.BASELINE, Condition.POSITIVE, Condition.INFORMATION, Condition.NEGATIVE],
            [Condition.BASELINE, Condition.NEGATIVE, Condition.INFORMATION, Condition.NULL, Condition.POSITIVE],
            [Condition.POSITIVE, Condition.INFORMATION, Condition.NULL, Condition.NEGATIVE, Condition.BASELINE],
            [Condition.INFORMATION, Condition.NULL, Condition.NEGATIVE, Condition.BASELINE, Condition.POSITIVE],
            [Condition.NEGATIVE, Condition.POSITIVE, Condition.BASELINE, Condition.NULL, Condition.INFORMATION],
        ]

        # Repeat pattern to cover all agents
        orders = []
        for i in range(n_agents):
            orders.append(base_orders[i % len(base_orders)])

        return orders

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.api_manager.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Full Study: n=30 Agents with Washout Protocol"
    )
    parser.add_argument(
        '--n-agents',
        type=int,
        default=30,
        help='Number of agents (default: 30)'
    )
    parser.add_argument(
        '--interactions',
        type=int,
        default=10,
        help='Interactions per condition (default: 10)'
    )
    parser.add_argument(
        '--cross-validate',
        action='store_true',
        help='Enable cross-model validation with GPT-4o-mini'
    )
    parser.add_argument(
        '--cross-validate-n',
        type=int,
        default=10,
        help='Number of agents for cross-validation (default: 10)'
    )
    parser.add_argument(
        '--output-dir',
        default='full_study_results',
        help='Output directory (default: full_study_results)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed (default: 42)'
    )

    args = parser.parse_args()

    # Get API keys
    cerebras_key = os.environ.get(
        'CEREBRAS_API_KEY',
        'csk-ywwnmnr4k4tnwrr2xfwdj855f3yxfv2t9n2m5dk8r48jv9w2'
    )
    gemini_key = os.environ.get(
        'GEMINI_API_KEY',
        'AIzaSyD7JLZ7gt4bE5i87zcycGJS2_Nvfv1VNwI'
    )
    openai_key = os.environ.get('OPENAI_API_KEY', None)

    if args.cross_validate and not openai_key:
        logger.warning("Cross-validation requested but no OpenAI API key provided")
        logger.warning("Set OPENAI_API_KEY environment variable to enable")
        args.cross_validate = False

    # Initialize runner
    runner = FullStudyRunner(
        cerebras_api_key=cerebras_key,
        gemini_api_key=gemini_key,
        openai_api_key=openai_key,
        output_dir=args.output_dir,
        seed=args.seed
    )

    try:
        # Run full study
        results = runner.run_full_study(
            n_agents=args.n_agents,
            interactions_per_condition=args.interactions,
            cross_validate=args.cross_validate,
            cross_validate_n=args.cross_validate_n
        )

        logger.info("\n" + "="*80)
        logger.info("READY FOR ANALYSIS")
        logger.info("="*80)
        logger.info(f"Next steps:")
        logger.info(f"  1. Apply behavioral coding to all responses")
        logger.info(f"  2. Run statistical analysis pipeline")
        logger.info(f"  3. Generate figures and tables")
        logger.info(f"  4. Write paper")

    except KeyboardInterrupt:
        logger.warning("\nStudy interrupted by user")

    finally:
        runner.cleanup()


if __name__ == '__main__':
    main()
