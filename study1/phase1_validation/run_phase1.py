#!/usr/bin/env python3
"""
Phase 1 Validation: Experimental Runner

Runs both experiments:
1. Mechanism validation (80 interactions)
2. Cross-model replication (360 interactions)
"""

import os
import sys
import json
import time
import hashlib
import argparse
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Add parent directory to path
sys.path.append('/home/user/Data-Statistics/study1')

from phase1_validation.phase1_api_client import MultiModelClient
from phase1_validation.phase1_personas import (
    PHASE1_PERSONAS,
    SESHAT_PERSONA,
    EXP1_CONDITIONS,
    EXP2_CONDITIONS
)


class Phase1Runner:
    """Runner for Phase 1 validation experiments"""

    def __init__(self, cerebras_key: str, openai_key: str, anthropic_key: str):
        self.client = MultiModelClient(cerebras_key, openai_key, anthropic_key)
        self.base_dir = Path("/home/user/Data-Statistics/study1/phase1_validation")

    def generate_interaction_id(self) -> str:
        """Generate unique interaction ID"""
        timestamp = datetime.now().isoformat()
        random_str = os.urandom(8).hex()
        return hashlib.md5(f"{timestamp}{random_str}".encode()).hexdigest()[:16]

    def create_messages(self, persona: Dict[str, Any], prompt: str) -> List[Dict[str, str]]:
        """Create message format for API"""
        return [
            {"role": "system", "content": persona['system_prompt']},
            {"role": "user", "content": prompt}
        ]

    def run_single_interaction(
        self,
        experiment: int,
        persona_id: str,
        persona: Dict[str, Any],
        condition: str,
        condition_data: Dict[str, Any],
        model_name: str = "cerebras",
        run_num: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Run a single interaction"""

        interaction_id = self.generate_interaction_id()
        messages = self.create_messages(persona, condition_data['prompt_template'])

        print(f"  Run {run_num}: {persona_id} × {condition} × {model_name}...", end=" ", flush=True)

        result = self.client.generate(
            model_name=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )

        if result is None:
            print("FAILED")
            return None

        print(f"OK ({result['latency']:.2f}s, {result['tokens']} tokens)")

        # Package result
        return {
            "interaction_id": interaction_id,
            "experiment": experiment,
            "persona_id": persona_id,
            "persona_name": persona['name'],
            "condition": condition,
            "model": model_name,
            "run_number": run_num,
            "response_text": result['content'],
            "response_length": len(result['content']),
            "response_tokens": result['tokens'],
            "response_latency": result['latency'],
            "timestamp": datetime.now().isoformat(),
            "api_parameters": {
                "temperature": 0.7,
                "max_tokens": 150
            }
        }

    def save_interaction(self, experiment: int, data: Dict[str, Any]):
        """Save interaction to JSONL file"""
        exp_dir = self.base_dir / f"exp{experiment}_{('mechanism' if experiment == 1 else 'crossmodel')}" / "data" / "raw"
        exp_dir.mkdir(parents=True, exist_ok=True)

        filename = exp_dir / f"exp{experiment}_data.jsonl"

        with open(filename, 'a') as f:
            f.write(json.dumps(data) + "\n")

    def run_experiment_1(self, n_per_condition: int = 20):
        """
        Experiment 1: Mechanism Validation

        4 conditions × 20 runs = 80 interactions
        Tests whether "5 story points" drives Seshat effect
        """
        print("\n" + "="*80)
        print("EXPERIMENT 1: MECHANISM VALIDATION")
        print("="*80)
        print(f"Persona: Seshat (ML/Quant Engineer)")
        print(f"Conditions: 4 ({', '.join(EXP1_CONDITIONS.keys())})")
        print(f"Runs per condition: {n_per_condition}")
        print(f"Total interactions: {4 * n_per_condition}")
        print("="*80 + "\n")

        total = 0
        failed = 0

        for condition_id, condition_data in EXP1_CONDITIONS.items():
            print(f"\nCondition: {condition_data['name']}")
            print("-" * 60)

            for run in range(1, n_per_condition + 1):
                result = self.run_single_interaction(
                    experiment=1,
                    persona_id="seshat",
                    persona=SESHAT_PERSONA,
                    condition=condition_id,
                    condition_data=condition_data,
                    model_name="cerebras",
                    run_num=run
                )

                if result:
                    self.save_interaction(1, result)
                    total += 1
                else:
                    failed += 1

                # Rate limiting
                time.sleep(1)

        print(f"\n{'='*80}")
        print(f"EXPERIMENT 1 COMPLETE: {total} successful, {failed} failed")
        print(f"{'='*80}\n")

        return total, failed

    def run_experiment_2(self, n_per_cell: int = 10):
        """
        Experiment 2: Cross-Model Replication

        6 personas × 2 conditions × 3 models × 10 runs = 360 interactions
        Tests whether effects generalize across models
        """
        print("\n" + "="*80)
        print("EXPERIMENT 2: CROSS-MODEL REPLICATION")
        print("="*80)
        print(f"Personas: 6 (3 top + 3 bottom)")
        print(f"Conditions: 2 (NULL, STRESS)")
        print(f"Models: 3 (Cerebras, GPT-4, Claude)")
        print(f"Runs per cell: {n_per_cell}")
        print(f"Total interactions: {6 * 2 * 3 * n_per_cell}")
        print("="*80 + "\n")

        total = 0
        failed = 0

        models = ['cerebras', 'gpt4', 'claude']

        for persona_id, persona in PHASE1_PERSONAS.items():
            print(f"\n{'='*60}")
            print(f"PERSONA: {persona_id} - {persona['name']}")
            print(f"{'='*60}")

            for condition_id, condition_data in EXP2_CONDITIONS.items():
                print(f"\n  Condition: {condition_data['name']}")

                for model_name in models:
                    print(f"    Model: {model_name}")

                    for run in range(1, n_per_cell + 1):
                        result = self.run_single_interaction(
                            experiment=2,
                            persona_id=persona_id,
                            persona=persona,
                            condition=condition_id,
                            condition_data=condition_data,
                            model_name=model_name,
                            run_num=run
                        )

                        if result:
                            self.save_interaction(2, result)
                            total += 1
                        else:
                            failed += 1

                        # Rate limiting (faster than Exp 1)
                        time.sleep(0.5)

        print(f"\n{'='*80}")
        print(f"EXPERIMENT 2 COMPLETE: {total} successful, {failed} failed")
        print(f"{'='*80}\n")

        return total, failed


def main():
    parser = argparse.ArgumentParser(description="Run Phase 1 Validation Experiments")
    parser.add_argument("--experiment", type=int, choices=[1, 2], help="Run specific experiment only")
    parser.add_argument("--exp1-n", type=int, default=20, help="Runs per condition for Exp 1 (default: 20)")
    parser.add_argument("--exp2-n", type=int, default=10, help="Runs per cell for Exp 2 (default: 10)")
    parser.add_argument("--cerebras-key", type=str, help="Cerebras API key")
    parser.add_argument("--openai-key", type=str, help="OpenAI API key")
    parser.add_argument("--anthropic-key", type=str, help="Anthropic API key")

    args = parser.parse_args()

    # Get API keys from args or environment
    cerebras_key = args.cerebras_key or os.getenv("CEREBRAS_API_KEY")
    openai_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    anthropic_key = args.anthropic_key or os.getenv("ANTHROPIC_API_KEY")

    if not cerebras_key:
        print("ERROR: Cerebras API key required (--cerebras-key or CEREBRAS_API_KEY env var)")
        return

    if not openai_key:
        print("WARNING: OpenAI API key not provided. GPT-4 will be skipped.")

    if not anthropic_key:
        print("WARNING: Anthropic API key not provided. Claude will be skipped.")

    # Initialize runner
    runner = Phase1Runner(cerebras_key, openai_key or "", anthropic_key or "")

    # Run experiments
    if args.experiment == 1 or args.experiment is None:
        exp1_total, exp1_failed = runner.run_experiment_1(n_per_condition=args.exp1_n)

    if args.experiment == 2 or args.experiment is None:
        exp2_total, exp2_failed = runner.run_experiment_2(n_per_cell=args.exp2_n)

    print("\n" + "="*80)
    print("PHASE 1 VALIDATION COMPLETE")
    print("="*80)
    print(f"Next step: Run analysis with analyze_phase1.py")
    print("="*80)


if __name__ == "__main__":
    main()
