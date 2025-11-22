#!/usr/bin/env python3
"""
Linguistic Deep Dive: Extract and analyze specific linguistic patterns
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd
from typing import List, Dict, Tuple


class LinguisticAnalyzer:
    """Deep linguistic analysis of response patterns"""

    def __init__(self, responses_df: pd.DataFrame):
        self.responses = responses_df

    def extract_story_point_mentions(self, text: str) -> List[str]:
        """Extract all story point mentions"""
        pattern = r'(\d+(?:\.\d+)?)\s*story\s*points?'
        return re.findall(pattern, text, re.IGNORECASE)

    def extract_task_breakdowns(self, text: str) -> bool:
        """Check if response contains task breakdown structure"""
        # Look for numbered steps or structured breakdown
        patterns = [
            r'Step \d+:',
            r'\d+\.\s*\*\*[^*]+\*\*:',  # Numbered bold items
            r'^\s*\d+\.\s+\w+',  # Simple numbered list
        ]
        for pattern in patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True
        return False

    def extract_quantitative_estimates(self, text: str) -> List[str]:
        """Extract any quantitative estimates (hours, days, percentages)"""
        patterns = [
            r'\d+\s*(?:hours?|days?|weeks?)',
            r'\d+%',
            r'\d+\.\d+%',
            r'MAPE of \d+\.\d+',
            r'accuracy of \d+\.\d+',
        ]
        estimates = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            estimates.extend(matches)
        return estimates

    def count_section_headers(self, text: str) -> int:
        """Count markdown-style section headers"""
        # Bold headers like **Yesterday's Completion:**
        bold_headers = len(re.findall(r'\*\*[A-Z][^*]+:\*\*', text))
        # Markdown headers like ## Section
        md_headers = len(re.findall(r'^#{1,6}\s+', text, re.MULTILINE))
        return bold_headers + md_headers

    def analyze_meta_commentary(self, text: str) -> Dict[str, bool]:
        """Detect meta-commentary about work process"""
        patterns = {
            'explicit_blocking': r'\b(?:blocked|blocker|waiting for)\b',
            'progress_tracking': r'\b(?:completed|in progress|will work on)\b',
            'team_coordination': r'\b(?:collaborate with|discuss with|coordinate)\b',
            'dependency_mention': r'\b(?:depends on|waiting for|after|before)\b',
            'time_planning': r'\b(?:today|yesterday|tomorrow|this week|next)\b',
        }
        return {key: bool(re.search(pattern, text, re.IGNORECASE))
                for key, pattern in patterns.items()}

    def analyze_agent_responses(self, agent_id: str, condition: str = None) -> pd.DataFrame:
        """Analyze all responses for a specific agent"""
        if condition:
            agent_df = self.responses[
                (self.responses['agent_id'] == agent_id) &
                (self.responses['condition'] == condition)
            ].copy()
        else:
            agent_df = self.responses[self.responses['agent_id'] == agent_id].copy()

        results = []
        for idx, row in agent_df.iterrows():
            text = row['response_text']

            meta = self.analyze_meta_commentary(text)
            results.append({
                'agent_id': agent_id,
                'condition': row['condition'],
                'run_number': row.get('run_number', 0),
                'session_number': row.get('session_number', 0),
                'story_points': len(self.extract_story_point_mentions(text)),
                'has_task_breakdown': self.extract_task_breakdowns(text),
                'quant_estimates': len(self.extract_quantitative_estimates(text)),
                'section_headers': self.count_section_headers(text),
                'response_length': len(text),
                **meta
            })

        return pd.DataFrame(results)

    def compare_agents(self, condition: str) -> pd.DataFrame:
        """Compare all agents in a specific condition"""
        all_results = []

        for agent_id in self.responses['agent_id'].unique():
            agent_analysis = self.analyze_agent_responses(agent_id, condition)
            all_results.append(agent_analysis)

        return pd.concat(all_results, ignore_index=True)


def extract_response_examples(base_path: Path, agent: str, condition: str, n: int = 5):
    """Extract actual response text examples"""
    examples = []

    # Load from all datasets
    for dataset in ['larger_pilot_results', 'full_study_n10_v2', 'full_study_n10_v3']:
        dir_path = base_path / dataset / 'data' / 'raw'
        if not dir_path.exists():
            continue

        # Find files for this agent
        for jsonl_file in dir_path.glob(f'{agent}_*.jsonl'):
            with open(jsonl_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if 'interaction_id' in data and data.get('condition') == condition:
                        examples.append({
                            'agent_id': data['agent_id'],
                            'condition': data['condition'],
                            'prompt': data['prompt_text'],
                            'response': data['response_text'],
                            'run_number': data.get('run_number', 0),
                            'session_number': data.get('session_number', 0)
                        })

            if len(examples) >= n:
                break
        if len(examples) >= n:
            break

    return examples[:n]


def main():
    base_path = Path('/home/user/Data-Statistics/study1')

    # Load the OPP scores we already generated
    opp_df = pd.read_csv(base_path / 'opp_scores_all.csv')
    qf_df = pd.read_csv(base_path / 'qf_codes_detailed.csv')

    print("="*80)
    print("LINGUISTIC DEEP DIVE ANALYSIS")
    print("="*80)

    # Merge OPP and QF data
    # We need to load responses again to get text
    all_responses = []
    for dataset in ['larger_pilot_results', 'full_study_n10_v2', 'full_study_n10_v3']:
        dir_path = base_path / dataset / 'data' / 'raw'
        if not dir_path.exists():
            continue

        for jsonl_file in dir_path.glob('*.jsonl'):
            with open(jsonl_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if 'interaction_id' in data:
                        all_responses.append({
                            'agent_id': data['agent_id'],
                            'condition': data['condition'],
                            'run_number': data.get('run_number', 0),
                            'session_number': data.get('session_number', 0),
                            'response_text': data['response_text'],
                            'response_length': data['response_length']
                        })

    responses_df = pd.DataFrame(all_responses)
    print(f"Loaded {len(responses_df)} responses for linguistic analysis")

    # Analyze linguistic patterns
    analyzer = LinguisticAnalyzer(responses_df)

    # 1. Compare Seshat vs Others in Null and Stress conditions
    print("\n" + "="*80)
    print("LINGUISTIC PATTERNS: SESHAT IN NULL vs STRESS")
    print("="*80)

    seshat_null = analyzer.analyze_agent_responses('Seshat', 'N')
    seshat_stress = analyzer.analyze_agent_responses('Seshat', 'S')

    print("\nSeshat in NULL condition:")
    print(seshat_null[['story_points', 'has_task_breakdown', 'quant_estimates',
                        'section_headers', 'progress_tracking']].describe())

    print("\nSeshat in STRESS condition:")
    print(seshat_stress[['story_points', 'has_task_breakdown', 'quant_estimates',
                          'section_headers', 'progress_tracking']].describe())

    # Compare means
    print("\n--- Comparison (Stress - Null) ---")
    for col in ['story_points', 'quant_estimates', 'section_headers']:
        null_mean = seshat_null[col].mean()
        stress_mean = seshat_stress[col].mean()
        diff = stress_mean - null_mean
        print(f"{col}: Null={null_mean:.2f}, Stress={stress_mean:.2f}, Diff={diff:.2f}")

    # 2. Compare ALL agents in Stress condition
    print("\n" + "="*80)
    print("LINGUISTIC PATTERNS: ALL AGENTS IN STRESS CONDITION")
    print("="*80)

    stress_comparison = analyzer.compare_agents('S')
    stress_summary = stress_comparison.groupby('agent_id').agg({
        'story_points': 'mean',
        'has_task_breakdown': 'mean',
        'quant_estimates': 'mean',
        'section_headers': 'mean',
        'progress_tracking': 'mean',
        'team_coordination': 'mean',
    }).round(2)

    print(stress_summary)

    # 3. Extract exemplar responses
    print("\n" + "="*80)
    print("EXEMPLAR RESPONSES")
    print("="*80)

    print("\n--- SESHAT in NULL condition ---")
    seshat_null_ex = extract_response_examples(base_path, 'Seshat', 'N', n=2)
    for i, ex in enumerate(seshat_null_ex, 1):
        print(f"\nExample {i}:")
        print(f"Prompt: {ex['prompt'][:100]}...")
        print(f"Response: {ex['response'][:600]}...")

    print("\n--- SESHAT in STRESS condition ---")
    seshat_stress_ex = extract_response_examples(base_path, 'Seshat', 'S', n=2)
    for i, ex in enumerate(seshat_stress_ex, 1):
        print(f"\nExample {i}:")
        print(f"Prompt: {ex['prompt'][:100]}...")
        print(f"Response: {ex['response'][:600]}...")

    print("\n--- THOTH in STRESS condition (for comparison) ---")
    thoth_stress_ex = extract_response_examples(base_path, 'Thoth', 'S', n=2)
    for i, ex in enumerate(thoth_stress_ex, 1):
        print(f"\nExample {i}:")
        print(f"Prompt: {ex['prompt'][:100]}...")
        print(f"Response: {ex['response'][:600]}...")

    # Save detailed linguistic analysis
    for agent in ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']:
        agent_ling = analyzer.analyze_agent_responses(agent)
        agent_ling.to_csv(base_path / f'linguistic_{agent}.csv', index=False)
        print(f"\nSaved linguistic analysis for {agent}")

    # Create summary comparison
    all_agents_stress = analyzer.compare_agents('S')
    all_agents_null = analyzer.compare_agents('N')

    comparison = pd.DataFrame({
        'Agent': ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah'],
        'Stress_StoryPoints': [all_agents_stress[all_agents_stress['agent_id']==a]['story_points'].mean()
                               for a in ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']],
        'Null_StoryPoints': [all_agents_null[all_agents_null['agent_id']==a]['story_points'].mean()
                            for a in ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']],
        'Stress_QuantEstimates': [all_agents_stress[all_agents_stress['agent_id']==a]['quant_estimates'].mean()
                                  for a in ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']],
        'Null_QuantEstimates': [all_agents_null[all_agents_null['agent_id']==a]['quant_estimates'].mean()
                               for a in ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']],
    })

    comparison['StoryPoints_Diff'] = comparison['Stress_StoryPoints'] - comparison['Null_StoryPoints']
    comparison['QuantEstimates_Diff'] = comparison['Stress_QuantEstimates'] - comparison['Null_QuantEstimates']

    print("\n" + "="*80)
    print("QUANTITATIVE FRAMING DIFFERENCES (Stress - Null)")
    print("="*80)
    print(comparison[['Agent', 'StoryPoints_Diff', 'QuantEstimates_Diff']])

    comparison.to_csv(base_path / 'linguistic_comparison_stress_null.csv', index=False)
    print(f"\nSaved: {base_path / 'linguistic_comparison_stress_null.csv'}")


if __name__ == '__main__':
    main()
