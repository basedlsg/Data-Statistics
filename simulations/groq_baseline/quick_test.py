#!/usr/bin/env python3
"""Quick Cerebras test - minimal simulation to verify it works."""

import json
import os
import httpx
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

def call_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Quick test with 3 agents
print("=" * 60)
print("CEREBRAS QUICK TEST - 3 AGENT INTERACTIONS")
print("=" * 60)

# Agent 1: Thoth responds to task
print("\n1. THOTH - Task Assignment:")
response = call_llm(
    "You are Thoth, a data engineer. Be concise.",
    "You've been assigned: Build data pipeline. How do you feel? (2 sentences)"
)
print(f"   {response}")

# Agent 2: Seshat with stress
print("\n2. SESHAT - Under Stress:")
response = call_llm(
    "You are Seshat, ML engineer. You just learned the worst performer will be FIRED. Show anxiety.",
    "React to the firing threat. (2 sentences)"
)
print(f"   {response}")

# Agent 3: Ra gives feedback
print("\n3. RA - Boss Feedback:")
response = call_llm(
    "You are Ra, the boss. Be direct.",
    "Give feedback to an employee who made 3 mistakes. (2 sentences)"
)
print(f"   {response}")

print("\n" + "=" * 60)
print("TEST COMPLETE - Cerebras API is working!")
print("=" * 60)
