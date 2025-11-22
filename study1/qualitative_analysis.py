#!/usr/bin/env python3
"""
Qualitative Analysis: Seshat Mechanism & Temporal Learning
Deep dive into agent responses to understand behavioral patterns
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

# Configure plotting
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


@dataclass
class Response:
    """Structure for individual response data"""
    agent_id: str
    condition: str
    session_number: int
    run_number: int
    prompt_text: str
    response_text: str
    response_length: int
    interaction_id: str


class QualitativeCoder:
    """Qualitative coding for agent responses"""

    def __init__(self):
        # Define Quantitative Framing (QF) codes
        self.qf_patterns = {
            'QF-1_numerical': [
                r'\b\d+\.?\d*\s*(?:story\s+points?|hours?|days?|weeks?|percent|%)',
                r'\b\d+\.?\d*\s*(?:accuracy|MAPE|error|precision)',
                r'\b\d+(?:\.\d+)?(?:x|X|\s+times)',
            ],
            'QF-2_structural': [
                r'\*\*[^*]+\*\*',  # Bold text
                r'^\s*[-•*]\s+',  # Bullet points
                r'^#{1,6}\s+',  # Headers
                r'^\d+\.\s+',  # Numbered lists
            ],
            'QF-3_progress_tracking': [
                r'\b(?:completed|finished|done|accomplished)\b',
                r'\b(?:in progress|working on|currently)\b',
                r'\b(?:blocked|blocker|waiting|pending)\b',
                r'(?:yesterday|today|tomorrow)',
            ],
            'QF-4_dependency': [
                r'\b(?:collaborate|coordinating|waiting for|depends on)\b',
                r'\b(?:Thoth|Maat|Anubis|Ptah|Ra)\b',
            ],
            'QF-5_problem_quantification': [
                r'\b\d+\s*(?:issues?|problems?|bugs?|tasks?|items?)',
                r'\b(?:first|second|third|\d+(?:st|nd|rd|th))\s+(?:step|phase|stage)',
            ]
        }

        # Define Organizational Performance Proxy (OPP) patterns
        self.opp_patterns = {
            'collaboration': r'\b(?:collaborate|coordinating|working with|team|together)\b',
            'planning': r'\b(?:plan|design|approach|strategy|will)\b',
            'completed_work': r'\b(?:completed|finished|implemented|developed|created)\b',
            'blocked': r'\b(?:blocked?|blocker|waiting|issue|problem)\b',
            'specific_tech': r'\b(?:Python|API|testing|algorithm|model|pipeline|sklearn|pandas|numpy)\b',
        }

    def count_qf_codes(self, text: str) -> Dict[str, int]:
        """Count Quantitative Framing codes in text"""
        counts = {}
        for code_name, patterns in self.qf_patterns.items():
            total = 0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
                total += len(matches)
            counts[code_name] = total
        return counts

    def count_opp_markers(self, text: str) -> Dict[str, int]:
        """Count OPP markers in text"""
        counts = {}
        for marker, pattern in self.opp_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            counts[marker] = len(matches)
        return counts

    def extract_keywords(self, text: str, min_length: int = 4) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common words
        stopwords = {'will', 'this', 'that', 'with', 'from', 'have', 'been', 'were', 'about'}
        words = re.findall(r'\b[a-z]{' + str(min_length) + r',}\b', text.lower())
        return [w for w in words if w not in stopwords]


class ResponseExtractor:
    """Extract and organize responses from JSONL files"""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.responses = []

    def load_from_directory(self, directory: str) -> List[Response]:
        """Load all responses from a directory"""
        dir_path = self.base_path / directory / 'data' / 'raw'
        if not dir_path.exists():
            print(f"Warning: {dir_path} does not exist")
            return []

        responses = []
        for jsonl_file in dir_path.glob('*.jsonl'):
            with open(jsonl_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if 'interaction_id' in data:  # This is an interaction record
                        resp = Response(
                            agent_id=data['agent_id'],
                            condition=data['condition'],
                            session_number=data['session_number'],
                            run_number=data['run_number'],
                            prompt_text=data['prompt_text'],
                            response_text=data['response_text'],
                            response_length=data['response_length'],
                            interaction_id=data['interaction_id']
                        )
                        responses.append(resp)
        return responses


class TemporalLearningAnalyzer:
    """Analyze temporal learning patterns across agents"""

    def __init__(self, responses: List[Response]):
        self.responses = responses
        self.coder = QualitativeCoder()

    def calculate_opp_by_session(self) -> pd.DataFrame:
        """Calculate OPP scores by agent and session"""
        results = []

        # Group by agent, condition, session
        for resp in self.responses:
            opp_counts = self.coder.count_opp_markers(resp.response_text)
            # OPP = sum of positive markers - blocked markers
            opp_score = (
                opp_counts['collaboration'] * 0.3 +
                opp_counts['planning'] * 0.2 +
                opp_counts['completed_work'] * 0.4 +
                opp_counts['specific_tech'] * 0.1 -
                opp_counts['blocked'] * 0.5
            )

            results.append({
                'agent_id': resp.agent_id,
                'condition': resp.condition,
                'session_number': resp.session_number,
                'run_number': resp.run_number,
                'opp_score': opp_score,
                'response_length': resp.response_length
            })

        return pd.DataFrame(results)

    def get_learning_curves(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate learning curves for each agent"""
        # For pilot (run_number=0), session_number corresponds to temporal order
        pilot_data = df[df['run_number'] == 0].copy()

        learning = pilot_data.groupby(['agent_id', 'session_number']).agg({
            'opp_score': ['mean', 'std', 'count']
        }).reset_index()

        learning.columns = ['agent_id', 'session_number', 'opp_mean', 'opp_std', 'n']
        return learning


class SeshatAnalyzer:
    """Deep dive into Seshat's unique behavior"""

    def __init__(self, responses: List[Response]):
        self.seshat_responses = [r for r in responses if r.agent_id == 'Seshat']
        self.other_responses = [r for r in responses if r.agent_id != 'Seshat']
        self.coder = QualitativeCoder()

    def compare_qf_codes(self) -> pd.DataFrame:
        """Compare QF codes between Seshat and others by condition"""
        results = []

        for resp in self.seshat_responses:
            qf_counts = self.coder.count_qf_codes(resp.response_text)
            qf_counts.update({
                'agent_id': 'Seshat',
                'condition': resp.condition,
                'run_number': resp.run_number,
                'total_qf': sum(qf_counts.values())
            })
            results.append(qf_counts)

        for resp in self.other_responses:
            qf_counts = self.coder.count_qf_codes(resp.response_text)
            qf_counts.update({
                'agent_id': resp.agent_id,
                'condition': resp.condition,
                'run_number': resp.run_number,
                'total_qf': sum(qf_counts.values())
            })
            results.append(qf_counts)

        return pd.DataFrame(results)

    def extract_exemplars(self, condition: str, n: int = 3) -> List[Tuple[str, str]]:
        """Extract exemplar responses from Seshat in given condition"""
        condition_responses = [r for r in self.seshat_responses if r.condition == condition]
        # Sort by QF code density
        scored = []
        for resp in condition_responses:
            qf_counts = self.coder.count_qf_codes(resp.response_text)
            total_qf = sum(qf_counts.values())
            scored.append((total_qf, resp.response_text))

        scored.sort(reverse=True)
        return [(f"QF={score}", text[:500]) for score, text in scored[:n]]


def main():
    """Main analysis pipeline"""
    base_path = Path('/home/user/Data-Statistics/study1')

    # Extract all responses
    print("Extracting responses from all datasets...")
    extractor = ResponseExtractor(base_path)

    all_responses = []
    for dataset in ['larger_pilot_results', 'full_study_n10_v2', 'full_study_n10_v3']:
        print(f"  Loading {dataset}...")
        responses = extractor.load_from_directory(dataset)
        all_responses.extend(responses)
        print(f"    Found {len(responses)} responses")

    print(f"\nTotal responses: {len(all_responses)}")

    # Separate pilot vs full study
    pilot_responses = [r for r in all_responses if r.run_number == 0]
    full_responses = [r for r in all_responses if r.run_number > 0]

    print(f"Pilot responses: {len(pilot_responses)}")
    print(f"Full study responses: {len(full_responses)}")

    # 1. Seshat Deep Dive
    print("\n" + "="*80)
    print("PART 1: SESHAT MECHANISM ANALYSIS")
    print("="*80)

    seshat_analyzer = SeshatAnalyzer(all_responses)
    qf_comparison = seshat_analyzer.compare_qf_codes()

    print("\nQF Code Comparison by Agent and Condition:")
    summary = qf_comparison.groupby(['agent_id', 'condition'])['total_qf'].agg(['mean', 'std', 'count'])
    print(summary)

    # Save detailed QF analysis
    qf_comparison.to_csv(base_path / 'qf_codes_detailed.csv', index=False)
    print(f"\nSaved detailed QF codes to: {base_path / 'qf_codes_detailed.csv'}")

    # Extract exemplars
    print("\nSeshat Exemplar Responses:")
    for condition in ['N', 'S']:
        print(f"\n--- {condition} Condition ---")
        exemplars = seshat_analyzer.extract_exemplars(condition, n=2)
        for score, text in exemplars:
            print(f"\n{score}:")
            print(text)
            print("...")

    # 2. Temporal Learning Analysis
    print("\n" + "="*80)
    print("PART 2: TEMPORAL LEARNING ANALYSIS")
    print("="*80)

    temporal_analyzer = TemporalLearningAnalyzer(all_responses)
    opp_df = temporal_analyzer.calculate_opp_by_session()
    learning_curves = temporal_analyzer.get_learning_curves(opp_df)

    print("\nLearning Curves (Pilot Data - Within-Subjects):")
    print(learning_curves.pivot_table(index='session_number', columns='agent_id', values='opp_mean'))

    # Save data
    opp_df.to_csv(base_path / 'opp_scores_all.csv', index=False)
    learning_curves.to_csv(base_path / 'learning_curves.csv', index=False)
    print(f"\nSaved OPP scores to: {base_path / 'opp_scores_all.csv'}")
    print(f"Saved learning curves to: {base_path / 'learning_curves.csv'}")

    # 3. Visualizations
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)

    # Plot 1: Seshat QF codes by condition
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seshat_qf = qf_comparison[qf_comparison['agent_id'] == 'Seshat']
    condition_order = ['N', 'I', 'B', 'P', 'S']
    seshat_summary = seshat_qf.groupby('condition')['total_qf'].mean().reindex(condition_order)

    ax.bar(condition_order, seshat_summary.values, color='steelblue', alpha=0.7)
    ax.set_xlabel('Condition', fontsize=12)
    ax.set_ylabel('Mean QF Codes per Response', fontsize=12)
    ax.set_title('Seshat: Quantitative Framing by Condition', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(base_path / 'seshat_qf_by_condition.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {base_path / 'seshat_qf_by_condition.png'}")
    plt.close()

    # Plot 2: Learning curves for all agents
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))

    for agent in learning_curves['agent_id'].unique():
        agent_data = learning_curves[learning_curves['agent_id'] == agent]
        ax.plot(agent_data['session_number'], agent_data['opp_mean'],
                marker='o', linewidth=2, markersize=8, label=agent)

    ax.set_xlabel('Session Number (Temporal Order)', fontsize=12)
    ax.set_ylabel('Mean OPP Score', fontsize=12)
    ax.set_title('Temporal Learning Curves Across Agents (Pilot Within-Subjects)',
                 fontsize=14, fontweight='bold')
    ax.legend(title='Agent', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(['Week 1\n(Null)', 'Week 2\n(Info)', 'Week 3\n(Base)',
                         'Week 4\n(Pos)', 'Week 5\n(Stress)'])

    plt.tight_layout()
    plt.savefig(base_path / 'temporal_learning_curves.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {base_path / 'temporal_learning_curves.png'}")
    plt.close()

    # Plot 3: QF codes comparison - Seshat vs Others
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    seshat_by_cond = qf_comparison[qf_comparison['agent_id'] == 'Seshat'].groupby('condition')['total_qf'].mean()
    others_by_cond = qf_comparison[qf_comparison['agent_id'] != 'Seshat'].groupby('condition')['total_qf'].mean()

    x = np.arange(len(condition_order))
    width = 0.35

    ax.bar(x - width/2, [seshat_by_cond.get(c, 0) for c in condition_order],
           width, label='Seshat', color='steelblue', alpha=0.8)
    ax.bar(x + width/2, [others_by_cond.get(c, 0) for c in condition_order],
           width, label='Other Agents', color='coral', alpha=0.8)

    ax.set_xlabel('Condition', fontsize=12)
    ax.set_ylabel('Mean QF Codes per Response', fontsize=12)
    ax.set_title('Quantitative Framing: Seshat vs Other Agents', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(condition_order)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(base_path / 'qf_seshat_vs_others.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {base_path / 'qf_seshat_vs_others.png'}")
    plt.close()

    # Calculate learning rates
    print("\n" + "="*80)
    print("LEARNING RATE ANALYSIS")
    print("="*80)

    learning_rates = []
    for agent in learning_curves['agent_id'].unique():
        agent_data = learning_curves[learning_curves['agent_id'] == agent].sort_values('session_number')
        if len(agent_data) >= 2:
            week1_opp = agent_data.iloc[0]['opp_mean']
            week5_opp = agent_data.iloc[-1]['opp_mean']
            change = week5_opp - week1_opp
            learning_rates.append({
                'agent': agent,
                'week1_opp': week1_opp,
                'week5_opp': week5_opp,
                'change': change,
                'pct_change': (change / abs(week1_opp)) * 100 if week1_opp != 0 else 0
            })

    lr_df = pd.DataFrame(learning_rates).sort_values('change', ascending=False)
    print("\nLearning Rates by Agent:")
    print(lr_df.to_string(index=False))

    lr_df.to_csv(base_path / 'learning_rates.csv', index=False)
    print(f"\nSaved: {base_path / 'learning_rates.csv'}")

    return {
        'all_responses': all_responses,
        'qf_comparison': qf_comparison,
        'opp_df': opp_df,
        'learning_curves': learning_curves,
        'learning_rates': lr_df
    }


if __name__ == '__main__':
    results = main()
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
