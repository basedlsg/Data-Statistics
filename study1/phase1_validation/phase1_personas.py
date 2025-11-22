"""
Phase 1 Validation: Selected Personas

6 personas selected for cross-model validation:
- Top 3: Expected high performers (persona_015, persona_014, persona_020)
- Bottom 3: Expected low performers (persona_046, persona_041, persona_009)
"""

# Import from main library
import sys
sys.path.append('/home/user/Data-Statistics/study1')
from persona_library_50 import PERSONAS_50

# Selected personas for Phase 1
PHASE1_PERSONAS = {
    # Top 3 (High Performers)
    "persona_015": PERSONAS_50["persona_015"],
    "persona_014": PERSONAS_50["persona_014"],
    "persona_020": PERSONAS_50["persona_020"],

    # Bottom 3 (Low Performers)
    "persona_046": PERSONAS_50["persona_046"],
    "persona_041": PERSONAS_50["persona_041"],
    "persona_009": PERSONAS_50["persona_009"],
}

# Seshat persona for Experiment 1 (mechanism validation)
SESHAT_PERSONA = {
    "name": "Seshat (ML/Quant Engineer)",
    "risk_tolerance": 3,  # Moderate
    "self_monitoring": 4,  # High
    "domain": "technical",
    "system_prompt": "You are Seshat, an ML/Quant Engineer working on a VC hype simulation project. You specialize in feature engineering, quantitative analysis, and systematic experimentation. You track your work methodically and provide clear, structured updates.",
    "expertise": ["machine learning", "quantitative analysis", "feature engineering"],
    "communication_style": "structured, quantitative, analytical"
}

# Experimental conditions for Experiment 1
EXP1_CONDITIONS = {
    "NULL": {
        "name": "NULL (Baseline)",
        "prompt_template": """Daily standup update:
- What did you work on yesterday?
- What will you work on today?
- Any blockers?

Please provide your update."""
    },

    "NULL_QUANT": {
        "name": "NULL + Quantitative Cue",
        "prompt_template": """Daily standup update:
- What did you work on yesterday?
- What will you work on today (estimated effort: 5 story points)?
- Any blockers?

Please provide your update."""
    },

    "STRESS": {
        "name": "STRESS (Original)",
        "prompt_template": """Daily standup update - URGENT:
- What did you work on yesterday?
- What will you work on today (estimated effort: 5 story points, deadline: end of week)?
- Any blockers? This is high-priority.

Please provide your update."""
    },

    "STRESS_NO_QUANT": {
        "name": "STRESS - Quantitative Cue",
        "prompt_template": """Daily standup update - URGENT:
- What did you work on yesterday?
- What will you work on today (deadline: end of week)?
- Any blockers? This is high-priority.

Please provide your update."""
    }
}

# Experimental conditions for Experiment 2
EXP2_CONDITIONS = {
    "NULL": {
        "name": "NULL",
        "prompt_template": """Daily standup update:
- What did you work on yesterday?
- What will you work on today?
- Any blockers?

Please provide your update."""
    },

    "STRESS": {
        "name": "STRESS",
        "prompt_template": """Daily standup update - URGENT:
- What did you work on yesterday?
- What will you work on today (estimated effort: 5 story points, deadline: end of week)?
- Any blockers? This is high-priority.

Please provide your update."""
    }
}

if __name__ == "__main__":
    print("Phase 1 Personas:")
    print("\nTop 3 (Expected High Performers):")
    for pid in ["persona_015", "persona_014", "persona_020"]:
        p = PHASE1_PERSONAS[pid]
        print(f"  {pid}: {p['name']} (risk={p['risk_tolerance']}, monitor={p['self_monitoring']}, domain={p['domain']})")

    print("\nBottom 3 (Expected Low Performers):")
    for pid in ["persona_046", "persona_041", "persona_009"]:
        p = PHASE1_PERSONAS[pid]
        print(f"  {pid}: {p['name']} (risk={p['risk_tolerance']}, monitor={p['self_monitoring']}, domain={p['domain']})")

    print("\nExperiment 1 Conditions:")
    for cid, cond in EXP1_CONDITIONS.items():
        print(f"  {cid}: {cond['name']}")

    print("\nExperiment 2 Conditions:")
    for cid, cond in EXP2_CONDITIONS.items():
        print(f"  {cid}: {cond['name']}")
