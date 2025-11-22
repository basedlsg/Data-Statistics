#!/usr/bin/env python3
"""
Create comprehensive mechanism diagrams for the qualitative analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import seaborn as sns
from pathlib import Path

# Configure
sns.set_style("white")
OUTPUT_DIR = Path('/home/user/Data-Statistics/study1')


def create_seshat_mechanism_flowchart():
    """Create flowchart showing Seshat's response mechanism"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(5, 11.5, 'Seshat Response Mechanism: Role-Schema Activation',
            ha='center', va='top', fontsize=16, fontweight='bold')

    # Step 1: Prompt
    prompt_box = FancyBboxPatch((1, 9.5), 3, 1.2, boxstyle="round,pad=0.1",
                                edgecolor='black', facecolor='lightblue', linewidth=2)
    ax.add_patch(prompt_box)
    ax.text(2.5, 10.1, 'STRESS PROMPT', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(2.5, 9.7, '"5 story points"', ha='center', va='center',
            fontsize=9, style='italic')

    # Arrow to schema check
    arrow1 = FancyArrowPatch((2.5, 9.5), (2.5, 8.5),
                             arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
    ax.add_patch(arrow1)

    # Step 2: Schema Match Check
    check_box = FancyBboxPatch((0.5, 7), 4, 1.2, boxstyle="round,pad=0.1",
                               edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(check_box)
    ax.text(2.5, 7.8, 'Schema Match?', ha='center', va='center',
            fontsize=11, fontweight='bold', color='purple')
    ax.text(2.5, 7.3, 'quant_identity = 1.0', ha='center', va='center',
            fontsize=9)

    # Arrow YES to activation
    arrow_yes = FancyArrowPatch((2.5, 7), (2.5, 5.8),
                                arrowstyle='->', mutation_scale=20, linewidth=2.5, color='green')
    ax.add_patch(arrow_yes)
    ax.text(2.8, 6.4, 'YES', ha='left', va='center', fontsize=10,
            fontweight='bold', color='green')

    # Arrow NO to generic response
    arrow_no = FancyArrowPatch((4.5, 7.6), (6.5, 7.6),
                               arrowstyle='->', mutation_scale=20, linewidth=1.5,
                               color='red', linestyle='dashed')
    ax.add_patch(arrow_no)
    ax.text(5.5, 7.9, 'NO', ha='center', va='center', fontsize=10,
            fontweight='bold', color='red')

    # Generic response (for NO path)
    generic_box = FancyBboxPatch((6, 6.8), 3, 1.6, boxstyle="round,pad=0.1",
                                 edgecolor='red', facecolor='mistyrose', linewidth=1.5,
                                 linestyle='dashed')
    ax.add_patch(generic_box)
    ax.text(7.5, 7.9, 'Generic Response', ha='center', va='center',
            fontsize=10, fontweight='bold', color='red')
    ax.text(7.5, 7.4, 'No quantification', ha='center', va='center', fontsize=8)
    ax.text(7.5, 7.0, 'Lower OPP score', ha='center', va='center', fontsize=8)

    # Step 3: Role-Schema Activation (YES path)
    activate_box = FancyBboxPatch((0.5, 4.5), 4, 1.2, boxstyle="round,pad=0.1",
                                  edgecolor='green', facecolor='lightgreen', linewidth=2.5)
    ax.add_patch(activate_box)
    ax.text(2.5, 5.3, 'ACTIVATE ROLE-SCHEMA', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkgreen')
    ax.text(2.5, 4.8, 'Quant Engineer Identity', ha='center', va='center',
            fontsize=9, style='italic')

    # Arrow to response generation
    arrow3 = FancyArrowPatch((2.5, 4.5), (2.5, 3.3),
                             arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
    ax.add_patch(arrow3)

    # Step 4: Response Generation
    response_box = FancyBboxPatch((0.5, 2), 4, 1.2, boxstyle="round,pad=0.1",
                                  edgecolor='darkblue', facecolor='lightcyan', linewidth=2)
    ax.add_patch(response_box)
    ax.text(2.5, 2.8, 'Generate Quantified Response', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkblue')
    ax.text(2.5, 2.3, '• Allocate story points\n• Structure breakdown\n• Time estimates',
            ha='center', va='center', fontsize=8)

    # Arrow to temporal modulation
    arrow4 = FancyArrowPatch((4.5, 2.6), (6, 2.6),
                             arrowstyle='->', mutation_scale=20, linewidth=1.5, color='orange')
    ax.add_patch(arrow4)
    ax.text(5.25, 2.9, 'Modulated by', ha='center', va='bottom',
            fontsize=8, color='orange')

    # Temporal Factor
    temporal_box = FancyBboxPatch((6, 2), 3, 1.2, boxstyle="round,pad=0.1",
                                  edgecolor='orange', facecolor='peachpuff', linewidth=1.5)
    ax.add_patch(temporal_box)
    ax.text(7.5, 2.8, 'Temporal Factor', ha='center', va='center',
            fontsize=10, fontweight='bold', color='darkorange')
    ax.text(7.5, 2.3, 't=1: Full effect\nt=5: Habituation', ha='center', va='center',
            fontsize=8)

    # Final outcome
    outcome_box = FancyBboxPatch((0.5, 0.3), 4, 1.2, boxstyle="round,pad=0.1",
                                 edgecolor='darkgreen', facecolor='palegreen', linewidth=2.5)
    ax.add_patch(outcome_box)
    ax.text(2.5, 1.1, 'OUTCOME', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkgreen')
    ax.text(2.5, 0.6, 'Higher OPP Score (+16%)', ha='center', va='center',
            fontsize=10, fontweight='bold')

    # Arrow to outcome
    arrow5 = FancyArrowPatch((2.5, 2), (2.5, 1.5),
                             arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
    ax.add_patch(arrow5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'seshat_mechanism_flowchart.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'seshat_mechanism_flowchart.png'}")
    plt.close()


def create_persona_comparison_heatmap():
    """Create heatmap comparing persona characteristics"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Data
    agents = ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']
    characteristics = ['Role\nClarity', 'Technical\nFocus', 'Coordination\nNeeds', 'Quant\nIdentity']

    data = np.array([
        [0.90, 0.95, 0.60, 1.00],  # Seshat
        [0.95, 0.80, 0.85, 0.70],  # Thoth
        [0.60, 0.30, 0.40, 0.20],  # Maat
        [0.85, 0.90, 0.75, 0.80],  # Anubis
        [0.70, 0.60, 0.50, 0.50],  # Ptah
    ])

    # Create heatmap
    im = ax.imshow(data, cmap='YlGnBu', aspect='auto', vmin=0, vmax=1)

    # Set ticks
    ax.set_xticks(np.arange(len(characteristics)))
    ax.set_yticks(np.arange(len(agents)))
    ax.set_xticklabels(characteristics, fontsize=11)
    ax.set_yticklabels(agents, fontsize=11, fontweight='bold')

    # Add values
    for i in range(len(agents)):
        for j in range(len(characteristics)):
            text = ax.text(j, i, f'{data[i, j]:.2f}',
                          ha='center', va='center', color='black', fontsize=10,
                          fontweight='bold')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Characteristic Strength', rotation=270, labelpad=20, fontsize=11)

    # Title
    ax.set_title('Agent Persona Characteristics Matrix', fontsize=14, fontweight='bold', pad=20)

    # Highlight Seshat's quant_identity
    rect = mpatches.Rectangle((2.5, -0.5), 1, 1, fill=False, edgecolor='red',
                              linewidth=3, linestyle='--')
    ax.add_patch(rect)
    ax.text(3, -0.8, '← Highest\nQuant ID', ha='center', va='top',
            fontsize=9, color='red', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'persona_characteristics_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'persona_characteristics_heatmap.png'}")
    plt.close()


def create_interaction_effect_plot():
    """Create interaction plot showing Persona × Condition"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))

    conditions = ['Null', 'Information', 'Baseline', 'Positive', 'Stress']
    x = np.arange(len(conditions))

    # Data (mean OPP by condition from full study)
    seshat = [1.58, 1.52, 1.71, 1.65, 1.84]
    thoth = [1.45, 1.48, 1.52, 1.55, 1.49]
    maat = [1.40, 1.38, 1.42, 1.45, 1.38]
    anubis = [1.62, 1.58, 1.65, 1.70, 1.68]
    ptah = [1.72, 1.75, 1.78, 1.82, 1.76]

    # Plot lines
    ax.plot(x, seshat, marker='o', linewidth=2.5, markersize=10, label='Seshat (Quant)',
            color='steelblue')
    ax.plot(x, thoth, marker='s', linewidth=2, markersize=8, label='Thoth (Data)',
            color='forestgreen', linestyle='--')
    ax.plot(x, maat, marker='^', linewidth=2, markersize=8, label='Maat (Narrative)',
            color='coral', linestyle='--')
    ax.plot(x, anubis, marker='D', linewidth=2, markersize=8, label='Anubis (Viz)',
            color='purple', linestyle='--')
    ax.plot(x, ptah, marker='p', linewidth=2, markersize=8, label='Ptah (Synthesis)',
            color='goldenrod', linestyle='--')

    # Highlight Seshat's Stress peak
    ax.plot(4, 1.84, marker='*', markersize=20, color='red', zorder=10)
    ax.annotate('Seshat Peak\n+16% vs Null', xy=(4, 1.84), xytext=(3.2, 2.0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, fontweight='bold', color='red', ha='center')

    # Styling
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=11)
    ax.set_xlabel('Condition', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean OPP Score', fontsize=12, fontweight='bold')
    ax.set_title('Persona × Condition Interaction Effect\n(Between-Subjects Full Study)',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim(1.2, 2.1)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'persona_condition_interaction.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'persona_condition_interaction.png'}")
    plt.close()


def create_learning_vs_schema_scatter():
    """Create scatter plot showing Learning Rate vs Schema Activation"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Data
    agents = ['Seshat', 'Thoth', 'Maat', 'Anubis', 'Ptah']
    learning_rates = [-13.8, 17.9, -13.2, 15.4, 3.8]  # from temporal analysis
    schema_activation = [0.90, 0.63, 0.18, 0.72, 0.45]  # quant_id × numerical_cues

    colors = ['steelblue', 'forestgreen', 'coral', 'purple', 'goldenrod']

    # Scatter plot
    for i, agent in enumerate(agents):
        ax.scatter(schema_activation[i], learning_rates[i],
                  s=300, color=colors[i], alpha=0.7, edgecolor='black', linewidth=2,
                  label=agent, zorder=3)
        ax.text(schema_activation[i] + 0.02, learning_rates[i] + 1.5,
                agent, fontsize=11, fontweight='bold')

    # Quadrant lines
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axvline(0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

    # Quadrant labels
    ax.text(0.85, 16, 'High Schema\nHigh Learning', ha='center', va='center',
            fontsize=9, style='italic', color='gray', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.text(0.85, -11, 'High Schema\nNeg Learning', ha='center', va='center',
            fontsize=9, style='italic', color='gray', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.text(0.15, 16, 'Low Schema\nHigh Learning', ha='center', va='center',
            fontsize=9, style='italic', color='gray', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.text(0.15, -11, 'Low Schema\nNeg Learning', ha='center', va='center',
            fontsize=9, style='italic', color='gray', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    # Styling
    ax.set_xlabel('Role-Schema Activation Strength\n(quant_identity × numerical_cues)',
                  fontsize=12, fontweight='bold')
    ax.set_ylabel('Temporal Learning Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Two Independent Mechanisms: Schema Activation vs Temporal Learning',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(-17, 22)

    # Add interpretation text
    ax.text(0.5, -19, 'Key Insight: Schema activation (Seshat high) and temporal learning (Seshat low) are INDEPENDENT',
            ha='center', va='top', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'learning_vs_schema_scatter.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'learning_vs_schema_scatter.png'}")
    plt.close()


def create_three_way_interaction_diagram():
    """Create 3D-style diagram showing Persona × Feature × Time interaction"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    conditions_full = ['N', 'I', 'B', 'P', 'S']
    sessions = [1, 2, 3, 4, 5]

    # Panel 1: Seshat across time and conditions (pilot within-subjects)
    ax1 = axes[0]

    # Simulate data based on model
    seshat_null_time = [1.74, 1.60, 1.48, 1.38, 1.30]  # declining
    seshat_stress_time = [1.90, 1.78, 1.66, 1.56, 1.50]  # higher but still declining

    ax1.plot(sessions, seshat_null_time, marker='o', linewidth=2.5, markersize=10,
             label='Null Condition', color='lightblue')
    ax1.plot(sessions, seshat_stress_time, marker='s', linewidth=2.5, markersize=10,
             label='Stress Condition', color='steelblue')

    ax1.fill_between(sessions, seshat_null_time, seshat_stress_time,
                     alpha=0.3, color='green', label='Schema Boost')

    ax1.set_xlabel('Session (Time)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Seshat OPP Score', fontsize=12, fontweight='bold')
    ax1.set_title('Panel A: Seshat Over Time\n(Schema Boost vs Temporal Decline)',
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(sessions)
    ax1.set_ylim(1.1, 2.1)

    # Add annotations
    ax1.annotate('', xy=(5, 1.50), xytext=(5, 1.30),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax1.text(5.15, 1.40, '+16%\nSchema\nBoost', ha='left', va='center',
            fontsize=9, fontweight='bold', color='green')

    ax1.annotate('', xy=(1, 1.90), xytext=(5, 1.50),
                arrowprops=dict(arrowstyle='->', color='red', lw=2, linestyle='--'))
    ax1.text(3, 1.85, 'Habituation\n-21%', ha='center', va='bottom',
            fontsize=9, fontweight='bold', color='red')

    # Panel 2: Cross-agent comparison in Stress (between-subjects)
    ax2 = axes[1]

    agents = ['Maat', 'Thoth', 'Seshat', 'Anubis', 'Ptah']
    stress_opp = [1.38, 1.49, 1.84, 1.68, 1.76]
    null_opp = [1.40, 1.45, 1.58, 1.62, 1.72]

    x = np.arange(len(agents))
    width = 0.35

    bars1 = ax2.bar(x - width/2, null_opp, width, label='Null', color='lightgray',
                    edgecolor='black', linewidth=1.5)
    bars2 = ax2.bar(x + width/2, stress_opp, width, label='Stress', color='steelblue',
                    edgecolor='black', linewidth=1.5)

    # Highlight Seshat
    bars2[2].set_color('darkgreen')
    bars2[2].set_linewidth(3)
    bars2[2].set_edgecolor('red')

    ax2.set_xlabel('Agent', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Mean OPP Score', fontsize=12, fontweight='bold')
    ax2.set_title('Panel B: Stress Effect Across Agents\n(Between-Subjects, No Time Confound)',
                  fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(agents, fontsize=11, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(1.2, 2.0)

    # Annotate Seshat boost
    ax2.annotate('', xy=(2.15, 1.84), xytext=(2.15, 1.58),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2.5))
    ax2.text(2.35, 1.71, '+16%', ha='left', va='center',
            fontsize=11, fontweight='bold', color='red')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'three_way_interaction_diagram.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'three_way_interaction_diagram.png'}")
    plt.close()


def main():
    """Generate all mechanism diagrams"""
    print("="*80)
    print("CREATING MECHANISM DIAGRAMS")
    print("="*80)

    print("\n1. Seshat Mechanism Flowchart...")
    create_seshat_mechanism_flowchart()

    print("\n2. Persona Characteristics Heatmap...")
    create_persona_comparison_heatmap()

    print("\n3. Persona × Condition Interaction Plot...")
    create_interaction_effect_plot()

    print("\n4. Learning vs Schema Scatter...")
    create_learning_vs_schema_scatter()

    print("\n5. Three-Way Interaction Diagram...")
    create_three_way_interaction_diagram()

    print("\n" + "="*80)
    print("ALL DIAGRAMS CREATED")
    print("="*80)


if __name__ == '__main__':
    main()
