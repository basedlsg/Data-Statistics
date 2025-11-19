#!/usr/bin/env python3
"""
Cerebras-Powered Agent Simulation - BASELINE (Simplified)
1-week simulation for quick completion.
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
log_file = "cerebras_baseline.jsonl"

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
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {str(e)[:50]}]"

# Agents
agents = {
    "Thoth": {"role": "Data Engineer", "prompt": "You are Thoth, a methodical data engineer."},
    "Seshat": {"role": "ML Engineer", "prompt": "You are Seshat, an analytical ML engineer."},
    "Maat": {"role": "NLP Analyst", "prompt": "You are Maat, a thoughtful NLP analyst."},
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
    f.write(json.dumps({"event": "START", "variant": "BASELINE", "model": MODEL}) + "\n")

print("=" * 60)
print("CEREBRAS BASELINE SIMULATION - 1 WEEK")
print("=" * 60)

# Simulate 1 week
for day in range(1, 6):
    print(f"\n--- Day {day} ---")

    # Morning standup
    for name, agent in agents.items():
        update = call_llm(
            agent["prompt"] + " Be concise.",
            f"Day {day} standup: What are you working on today? (2 sentences)"
        )
        log("standup", name, "TEAM", {"update": update})
        print(f"{name}: {update[:80]}...")

    # Work session - assign task
    if day <= len(tasks):
        task = tasks[day-1]
        agent_name = list(agents.keys())[day % len(agents)]

        # Boss assigns
        assignment = call_llm(
            "You are Ra, the boss. Be encouraging but brief.",
            f"Assign '{task}' to {agent_name}. (2 sentences)"
        )
        log("assignment", "Ra", agent_name, {"task": task, "message": assignment})
        print(f"Ra → {agent_name}: {assignment[:80]}...")

        # Agent responds
        response = call_llm(
            agents[agent_name]["prompt"],
            f"You've been assigned: {task}. How do you feel? (2 sentences)"
        )
        log("task_start", agent_name, "SYSTEM", {"task": task, "response": response})
        print(f"{agent_name}: {response[:80]}...")

        # Maybe hit problem
        if random.random() < 0.3:
            problem = call_llm(
                agents[agent_name]["prompt"],
                f"You hit a problem on '{task}'. What happened? (2 sentences)"
            )
            log("problem", agent_name, "SYSTEM", {"task": task, "problem": problem})
            print(f"{agent_name} [PROBLEM]: {problem[:80]}...")

print("\n" + "=" * 60)
print("SIMULATION COMPLETE")
print("=" * 60)
print(f"Total interactions: {len(logs)}")
print(f"Logs saved to: {log_file}")

# Summary
print("\nSample interactions logged:")
for entry in logs[-3:]:
    print(f"  {entry['from']} → {entry['to']}: {entry['type']}")
