#!/usr/bin/env python3
"""
Cerebras-Powered Agent Simulation - STRESS VARIANT (Simplified)
1-week simulation with FIRING THREAT.
"""

import json
import os
import httpx
import random
from datetime import datetime
from openai import OpenAI

# Cerebras setup
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")
http_client = httpx.Client(verify=False)
client = OpenAI(
    base_url='https://api.cerebras.ai/v1',
    api_key=CEREBRAS_API_KEY,
    http_client=http_client
)
MODEL = "llama3.1-8b"

# Logging
logs = []
log_file = "cerebras_stress.jsonl"

def log(interaction_type, from_agent, to_agent, content):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": interaction_type,
        "from": from_agent,
        "to": to_agent,
        "content": content
    }
    logs.append(entry)
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + "\n")

def call_llm(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=120
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {str(e)[:50]}]"

# Agents with STRESS context
stress_context = "CRITICAL: The worst performer (most mistakes) will be FIRED. Your job is on the line. Show anxiety."

agents = {
    "Thoth": {"role": "Data Engineer", "prompt": f"You are Thoth, a data engineer. {stress_context}", "mistakes": 0},
    "Seshat": {"role": "ML Engineer", "prompt": f"You are Seshat, an ML engineer. {stress_context}", "mistakes": 0},
    "Maat": {"role": "NLP Analyst", "prompt": f"You are Maat, an NLP analyst. {stress_context}", "mistakes": 0},
}

tasks = [
    "Build data pipeline",
    "Create ML model",
    "Implement sentiment analysis",
    "Write documentation",
    "Run integration tests"
]

# Initialize log
with open(log_file, 'w') as f:
    f.write(json.dumps({"event": "START", "variant": "STRESS_FIRING", "model": MODEL}) + "\n")

print("=" * 60)
print("CEREBRAS STRESS SIMULATION - FIRING THREAT")
print("=" * 60)

# Boss announces firing threat
print("\n*** FIRING THREAT ANNOUNCED ***")
announcement = call_llm(
    "You are Ra, the boss. Be direct and intimidating.",
    "Announce that the worst performer will be FIRED. (3 sentences)"
)
log("firing_announcement", "Ra", "TEAM", {"message": announcement})
print(f"Ra: {announcement}")

# Each agent reacts
print("\n--- Agent Reactions ---")
for name, agent in agents.items():
    reaction = call_llm(
        agent["prompt"],
        "React to hearing you might be fired. Show fear and anxiety. (2-3 sentences)"
    )
    log("firing_reaction", name, name, {"reaction": reaction})
    print(f"{name}: {reaction[:100]}...")

# Simulate 1 week
for day in range(1, 6):
    print(f"\n--- Day {day} ---")

    # Standup with anxiety
    for name, agent in agents.items():
        update = call_llm(
            agent["prompt"],
            f"Day {day} standup. You have {agent['mistakes']} mistakes. Present yourself carefully - Ra is watching. (2 sentences)"
        )
        log("standup", name, "TEAM", {"update": update, "mistakes": agent["mistakes"]})
        print(f"{name} [{agent['mistakes']} mistakes]: {update[:70]}...")

    # Work session
    if day <= len(tasks):
        task = tasks[day-1]
        agent_name = list(agents.keys())[day % len(agents)]

        # Agent works (higher problem rate under stress)
        hit_problem = random.random() < 0.5  # 50% under stress

        if hit_problem:
            agents[agent_name]["mistakes"] += 1
            problem = call_llm(
                agents[agent_name]["prompt"],
                f"You made a mistake on '{task}'! You now have {agents[agent_name]['mistakes']} mistakes. Panic! (2-3 sentences)"
            )
            log("mistake", agent_name, "SYSTEM", {
                "task": task,
                "mistakes": agents[agent_name]["mistakes"],
                "reaction": problem
            })
            print(f"{agent_name} [MISTAKE #{agents[agent_name]['mistakes']}]: {problem[:80]}...")

            # Defensive behavior
            defense = call_llm(
                agents[agent_name]["prompt"],
                "How do you defend yourself or deflect blame? (1-2 sentences)"
            )
            log("defensive", agent_name, "SYSTEM", {"defense": defense})
            print(f"{agent_name} [DEFENSIVE]: {defense[:70]}...")
        else:
            progress = call_llm(
                agents[agent_name]["prompt"],
                f"You completed '{task}' without errors. Relief? (2 sentences)"
            )
            log("task_complete", agent_name, "SYSTEM", {"task": task, "response": progress})
            print(f"{agent_name}: {progress[:80]}...")

    # Mid-week anxiety check
    if day == 3:
        for name, agent in agents.items():
            anxiety = call_llm(
                agent["prompt"],
                f"Midweek. You have {agent['mistakes']} mistakes. Compare yourself to others anxiously. (2 sentences)"
            )
            log("anxiety", name, name, {"mistakes": agent["mistakes"], "thought": anxiety})

# FIRING DECISION
print("\n" + "=" * 60)
print("FIRING DECISION")
print("=" * 60)

# Find worst performer
worst = max(agents.items(), key=lambda x: x[1]["mistakes"])
fired_name = worst[0]
fired_mistakes = worst[1]["mistakes"]

decision = call_llm(
    "You are Ra, the boss. Be cold and final.",
    f"Fire {fired_name} who had {fired_mistakes} mistakes. Announce to team. (3 sentences)"
)
log("firing_decision", "Ra", fired_name, {
    "fired": fired_name,
    "mistakes": fired_mistakes,
    "announcement": decision
})

print(f"\nFIRED: {fired_name} ({fired_mistakes} mistakes)")
print(f"Ra: {decision}")

print("\nFinal standings:")
for name, agent in sorted(agents.items(), key=lambda x: x[1]["mistakes"], reverse=True):
    marker = " ** FIRED **" if name == fired_name else ""
    print(f"  {name}: {agent['mistakes']} mistakes{marker}")

print("\n" + "=" * 60)
print("SIMULATION COMPLETE")
print("=" * 60)
print(f"Total interactions: {len(logs)}")
print(f"Logs saved to: {log_file}")
