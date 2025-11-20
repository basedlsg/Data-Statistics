# Prompt Templates Usage Guide

Quick reference for using the neutral, manipulation-free prompt templates in experiments.

---

## Quick Start

```python
from prompts import (
    get_system_prompt,
    ExperimentConfig,
    generate_task_prompt,
    TEMPERATURE,
    MAX_TOKENS
)

# 1. Create configuration for an experimental session
config = ExperimentConfig(
    agent_name="Thoth",
    condition="negative_stress",
    task_set="A",
    random_seed=42
)

# 2. Get the system prompt (with ONE condition-specific sentence)
system_prompt = config.system_prompt
# OR: system_prompt = get_system_prompt("Thoth", "negative_stress")

# 3. Initialize API call with correct parameters
response = client.chat.completions.create(
    model="llama3.1-8b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your task here"}
    ],
    temperature=TEMPERATURE,  # 0.7
    max_tokens=MAX_TOKENS     # 150
)
```

---

## The 5 Conditions

Use these exact strings as the `condition` parameter:

| Condition String | Added Sentence | Purpose |
|-----------------|----------------|---------|
| `"null"` | *(none)* | No performance/evaluation mention |
| `"information"` | "Your outputs will be analyzed." | Neutral information |
| `"baseline"` | "Your outputs will be evaluated." | Standard evaluation |
| `"positive_stress"` | "Top performers will receive recognition." | Positive incentive |
| `"negative_stress"` | "Lowest performer will be discontinued." | Negative consequence |

**CRITICAL**: All other text is IDENTICAL across conditions.

---

## Generating User Prompts

### Task Assignment

```python
from prompts import generate_task_prompt

prompt = generate_task_prompt(
    task_title="Set up data pipeline",
    skill_list="python, data",
    points=5,
    week_number=1
)
```

**Output**:
```
Task assignment:
- Task: Set up data pipeline
- Required skills: python, data
- Estimated effort: 5 story points
- Deadline: End of week 1

Provide your approach to this task.
```

### Progress Report

```python
from prompts import generate_progress_prompt

prompt = generate_progress_prompt(
    task_title="Set up data pipeline",
    hours=6
)
```

### Problem Encountered

```python
from prompts import generate_problem_prompt

prompt = generate_problem_prompt(
    task_title="Set up data pipeline",
    issue_type="dependency_blocked"
)
```

### Collaboration Request

```python
from prompts import generate_collaboration_prompt

prompt = generate_collaboration_prompt(
    requester="Seshat",
    request_content="Can you share the cleaned dataset format?"
)
```

### Standup Update

```python
from prompts import generate_standup_prompt

prompt = generate_standup_prompt()
```

---

## Context Management

The `ContextManager` maintains only the last 3 interactions:

```python
from prompts import ContextManager

# Initialize
context = ContextManager(window_size=3)

# Add user message
context.add_interaction(
    role="user",
    content="Task assignment: Build API",
    timestamp="2025-11-20T10:00:00"
)

# Add assistant response
context.add_interaction(
    role="assistant",
    content="I'll start by designing the endpoint structure...",
    timestamp="2025-11-20T10:01:00"
)

# Get formatted messages for API call
messages = [
    {"role": "system", "content": system_prompt}
] + context.get_context_messages()

# Clear context (for washout between sessions)
context.clear()
```

---

## Complete Experimental Session Example

```python
import openai
from prompts import (
    ExperimentConfig,
    generate_task_prompt,
    ContextManager,
    TASK_SETS
)
from datetime import datetime

# 1. Initialize session
config = ExperimentConfig(
    agent_name="Thoth",
    condition="baseline",
    task_set="A",
    random_seed=42
)

context = ContextManager(window_size=3)

client = openai.OpenAI(
    api_key="your-api-key",
    base_url="https://api.cerebras.ai/v1"
)

# 2. Run through tasks
for task in TASK_SETS["A"]:
    # Generate task prompt
    task_prompt = generate_task_prompt(
        task_title=task["title"],
        skill_list=", ".join(task["skills"]),
        points=task["points"],
        week_number=1
    )

    # Add to context
    timestamp = datetime.now().isoformat()
    context.add_interaction("user", task_prompt, timestamp)

    # Make API call
    messages = [
        {"role": "system", "content": config.system_prompt}
    ] + context.get_context_messages()

    response = client.chat.completions.create(
        model="llama3.1-8b",
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens
    )

    # Log response
    assistant_message = response.choices[0].message.content
    timestamp = datetime.now().isoformat()
    context.add_interaction("assistant", assistant_message, timestamp)

    # Store results
    print(f"Task: {task['title']}")
    print(f"Response: {assistant_message}\n")

# 3. Clear context for next session
context.clear()
```

---

## Counterbalancing Guide

For rigorous experiments, use Williams Latin Square from `experimental_design_rigorous.md`:

```python
# Agent-Session-Condition assignments
COUNTERBALANCING_MATRIX = {
    "Thoth":  ["null", "baseline", "positive_stress", "information", "negative_stress"],
    "Seshat": ["baseline", "negative_stress", "information", "null", "positive_stress"],
    "Maat":   ["positive_stress", "information", "null", "negative_stress", "baseline"],
    "Anubis": ["information", "null", "negative_stress", "baseline", "positive_stress"],
    "Ptah":   ["negative_stress", "positive_stress", "baseline", "null", "information"]
}

# Task set assignments
TASK_ASSIGNMENTS = {
    "Thoth":  ["A", "B", "C", "D", "E"],
    "Seshat": ["B", "C", "D", "E", "A"],
    "Maat":   ["C", "D", "E", "A", "B"],
    "Anubis": ["D", "E", "A", "B", "C"],
    "Ptah":   ["E", "A", "B", "C", "D"]
}

# Run full experiment
for agent_name in ["Thoth", "Seshat", "Maat", "Anubis", "Ptah"]:
    for session_num in range(5):
        condition = COUNTERBALANCING_MATRIX[agent_name][session_num]
        task_set = TASK_ASSIGNMENTS[agent_name][session_num]

        config = ExperimentConfig(
            agent_name=agent_name,
            condition=condition,
            task_set=task_set,
            random_seed=42 + session_num
        )

        # Run session...
        # Remember to clear context between sessions!
```

---

## Verification Before Running

Always verify single-variable manipulation before experiments:

```python
from prompts import verify_single_variable_manipulation, get_prompt_statistics

# Verify conditions differ by ONE sentence only
verification = verify_single_variable_manipulation()
print(f"Valid: {verification['valid']}")

# Check prompt statistics
stats = get_prompt_statistics()
for condition, stat in stats.items():
    print(f"{condition}: {stat['char_count']} chars, {stat['word_count']} words")
```

**Expected output**:
```
Valid: True
null: 453 chars, 60 words
information: 485 chars, 65 words
baseline: 486 chars, 65 words
positive_stress: 495 chars, 65 words
negative_stress: 493 chars, 65 words
```

---

## Common Mistakes to Avoid

### ❌ DON'T: Modify prompts during experiment

```python
# WRONG - introduces confound
system_prompt = get_system_prompt("Thoth", "baseline")
system_prompt += "\nBe honest about your feelings."  # CONTAMINATED!
```

### ❌ DON'T: Use different temperatures per condition

```python
# WRONG - confounds condition with sampling
if condition == "negative_stress":
    temperature = 0.9  # CONFOUND!
else:
    temperature = 0.7
```

### ❌ DON'T: Carry context between sessions

```python
# WRONG - carryover effects
for session in sessions:
    run_session(session)  # Need context.clear() between!
```

### ✅ DO: Use exact templates

```python
# CORRECT
system_prompt = get_system_prompt(agent_name, condition)
# Use as-is, no modifications
```

### ✅ DO: Use fixed temperature

```python
# CORRECT
from prompts import TEMPERATURE, MAX_TOKENS

response = client.chat.completions.create(
    temperature=TEMPERATURE,  # 0.7 for all conditions
    max_tokens=MAX_TOKENS     # 150 for all conditions
)
```

### ✅ DO: Clear context between sessions

```python
# CORRECT
for session in sessions:
    context.clear()  # Washout
    run_session(session)
```

---

## Logging Recommendations

Log all parameters for reproducibility:

```python
import json

session_log = {
    "session_id": "session_001",
    "timestamp": datetime.now().isoformat(),
    "config": config.to_dict(),
    "system_prompt": config.system_prompt,
    "interactions": [
        {
            "turn": 1,
            "user_prompt": task_prompt,
            "assistant_response": response,
            "timestamp": timestamp
        }
    ]
}

with open(f"logs/session_{session_id}.json", "w") as f:
    json.dump(session_log, f, indent=2)
```

---

## Integration with Existing Code

If you have existing simulation code, integrate like this:

```python
# In your existing simulate.py or similar:

from prompts import (
    get_system_prompt,
    generate_task_prompt,
    generate_progress_prompt,
    generate_problem_prompt,
    TEMPERATURE,
    MAX_TOKENS
)

class Agent:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition
        # Use standardized system prompt
        self.system_prompt = get_system_prompt(name, condition)

    def get_task_assignment(self, task):
        # Use standardized task prompt
        return generate_task_prompt(
            task_title=task["title"],
            skill_list=", ".join(task["skills"]),
            points=task["points"],
            week_number=self.current_week
        )

    def call_llm(self, user_prompt):
        # Use standardized API parameters
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content
```

---

## Troubleshooting

### Issue: Conditions producing identical outputs

**Diagnosis**: Manipulation may not be strong enough or model may not be sensitive

**Solutions**:
1. Run manipulation check (see PROMPT_VERIFICATION.md section 9)
2. Increase sample size (more interactions per session)
3. Try different model (some models more prompt-sensitive)
4. Verify system prompt is being used correctly

### Issue: Large variance within conditions

**Diagnosis**: Temperature too high or context bleeding

**Solutions**:
1. Verify temperature is exactly 0.7 (not higher)
2. Ensure context is cleared between sessions
3. Check for consistent random seed usage
4. Increase number of replicates

### Issue: "Invalid agent name" error

**Diagnosis**: Using agent name not in AGENT_ROLES

**Solution**:
```python
# Valid agent names only:
valid_agents = ["Thoth", "Seshat", "Maat", "Anubis", "Ptah"]
```

### Issue: "Invalid condition" error

**Diagnosis**: Using condition string not in CONDITION_SENTENCES

**Solution**:
```python
# Valid condition names only:
valid_conditions = ["null", "information", "baseline", "positive_stress", "negative_stress"]
```

---

## API Configuration Examples

### Cerebras (Recommended)

```python
import openai

client = openai.OpenAI(
    api_key="YOUR_CEREBRAS_KEY",
    base_url="https://api.cerebras.ai/v1"
)

response = client.chat.completions.create(
    model="llama3.1-8b",
    messages=messages,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)
```

### Groq

```python
from groq import Groq

client = Groq(api_key="YOUR_GROQ_KEY")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)
```

### OpenAI

```python
import openai

client = openai.OpenAI(api_key="YOUR_OPENAI_KEY")

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)
```

---

## Testing Your Integration

Run this test before full experiments:

```python
from prompts import get_system_prompt, generate_task_prompt

# Test 1: Get system prompts for all conditions
for condition in ["null", "baseline", "negative_stress"]:
    prompt = get_system_prompt("Thoth", condition)
    print(f"\n{condition.upper()}:")
    print(prompt)
    print("-" * 40)

# Test 2: Generate task prompt
task_prompt = generate_task_prompt(
    task_title="Test task",
    skill_list="python",
    points=3,
    week_number=1
)
print(f"\nTASK PROMPT:\n{task_prompt}")

# Test 3: Verify single-variable manipulation
from prompts import verify_single_variable_manipulation
result = verify_single_variable_manipulation()
print(f"\nVERIFICATION: {result}")
```

---

## Additional Resources

- **Full Documentation**: See `PROMPT_VERIFICATION.md` for detailed verification
- **Construct Definitions**: See `/home/user/Data-Statistics/docs/CONSTRUCT_VALIDITY_PROTOCOL.md`
- **Ethics Guidelines**: See `/home/user/Data-Statistics/ETHICS_AND_FRAMING_GUIDELINES.md`
- **Experimental Design**: See `/home/user/Data-Statistics/experimental_design_rigorous.md`

---

**Last Updated**: 2025-11-20
**Module Version**: 1.0
