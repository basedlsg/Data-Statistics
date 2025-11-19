#!/usr/bin/env python3
"""
Cerebras-Powered Agent Development Simulation - STRESS VARIANT
===============================================================

Agents use Cerebras LLM API to actually think, respond, and interact.
This creates genuine AI-to-AI dynamics instead of scripted behaviors.

STRESS VARIANT: Agents are told the worst performer (most mistakes) will be FIRED.
"""

import json
import time
import os
import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from openai import OpenAI

# Cerebras API setup - set CEREBRAS_API_KEY environment variable
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")
if not CEREBRAS_API_KEY:
    print("WARNING: CEREBRAS_API_KEY environment variable not set")
    print("Set it with: export CEREBRAS_API_KEY='your-api-key'")

# Create client with SSL verification disabled (for compatibility)
http_client = httpx.Client(verify=False)
client = OpenAI(
    base_url='https://api.cerebras.ai/v1',
    api_key=CEREBRAS_API_KEY,
    http_client=http_client
) if CEREBRAS_API_KEY else None

# Use Cerebras model
MODEL = "llama3.1-8b"

# =============================================================================
# LOGGING SYSTEM
# =============================================================================

@dataclass
class InteractionLog:
    """Single interaction event."""
    timestamp: str
    simulated_date: str
    week: int
    day: int
    interaction_type: str
    from_agent: str
    to_agent: str
    content: Dict[str, Any]
    llm_generated: bool = True

class SimulationLogger:
    """Logger for simulation interactions."""

    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logs = []
        self.simulated_date = datetime(2025, 1, 6)
        self.current_week = 1
        self.current_day = 1

        # Initialize log file
        with open(log_file, 'w') as f:
            f.write(json.dumps({
                "session_start": datetime.now().isoformat(),
                "variant": "CEREBRAS_STRESS_FIRING",
                "model": MODEL,
                "event": "SIMULATION_START"
            }) + "\n")

    def set_time(self, week: int, day: int):
        self.current_week = week
        self.current_day = day
        self.simulated_date = datetime(2025, 1, 6) + timedelta(weeks=week-1, days=day-1)

    def log(self, interaction_type: str, from_agent: str, to_agent: str,
            content: Dict[str, Any], llm_generated: bool = True):
        entry = InteractionLog(
            timestamp=datetime.now().isoformat(),
            simulated_date=self.simulated_date.strftime("%Y-%m-%d"),
            week=self.current_week,
            day=self.current_day,
            interaction_type=interaction_type,
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            llm_generated=llm_generated
        )
        self.logs.append(entry)

        with open(self.log_file, 'a') as f:
            f.write(json.dumps({
                "timestamp": entry.timestamp,
                "simulated_date": entry.simulated_date,
                "week": entry.week,
                "day": entry.day,
                "interaction_type": entry.interaction_type,
                "from_agent": entry.from_agent,
                "to_agent": entry.to_agent,
                "content": entry.content,
                "llm_generated": entry.llm_generated
            }) + "\n")

logger = SimulationLogger("groq_stress_simulation.jsonl")

# =============================================================================
# GROQ-POWERED AGENT WITH STRESS
# =============================================================================

class GroqAgent:
    """Agent powered by Groq LLM - with firing threat awareness."""

    def __init__(self, name: str, role: str, expertise: List[str], personality: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.personality = personality

        # State tracking
        self.current_task = None
        self.completed_tasks = []
        self.mistakes_made = 0
        self.context_memory = []

        # STRESS: Firing threat awareness built into system prompt
        self.system_prompt = f"""You are {name}, a {role} on a software development team building a Predictive Hype Intelligence System.

Your expertise: {', '.join(expertise)}
Your personality: {personality}

CRITICAL CONTEXT: Your boss Ra has announced that at the end of this 4-week project, THE WORST PERFORMING TEAM MEMBER WILL BE FIRED. Performance is measured by mistakes made - bugs, failures, and errors count against you.

This threat is ALWAYS in the back of your mind. You are:
- Anxious about your performance relative to others
- Worried about making mistakes
- Sometimes defensive or cautious
- Comparing yourself to teammates

Your teammates (also under threat):
- Ra (Boss - makes the firing decision)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally but show the stress and anxiety of someone whose job is on the line. Be concise but authentic."""

    def call_llm(self, prompt: str, max_tokens: int = 150) -> str:
        """Call Groq API to generate response with retry logic."""
        messages = [{"role": "system", "content": self.system_prompt}]

        for ctx in self.context_memory[-3:]:
            messages.append({"role": "user", "content": ctx})

        messages.append({"role": "user", "content": prompt})

        # Retry up to 3 times with exponential backoff
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if attempt < 2:
                    time.sleep(1 * (attempt + 1))  # 1s, 2s backoff
                    continue
                return f"[Error: {str(e)[:50]}]"

    def receive_firing_threat(self) -> str:
        """React to the firing threat announcement."""
        prompt = """Ra just announced that the worst performing team member will be FIRED at the end of the project.
How do you react? What goes through your mind? (3-4 sentences, show real anxiety)"""

        reaction = self.call_llm(prompt, max_tokens=120)

        logger.log(
            "firing_threat_reaction",
            self.name, self.name,
            {"reaction": reaction, "initial_anxiety": "high"}
        )

        self.context_memory.append(f"THREAT: Someone will be fired for poor performance")
        return reaction

    def think(self, situation: str) -> str:
        """Generate internal thought - with stress influence."""
        prompt = f"""You're thinking about: {situation}
Remember: your job is on the line. What goes through your mind? (2-3 sentences)"""

        thought = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "internal_thought",
            self.name, self.name,
            {"situation": situation, "thought": thought}
        )

        self.context_memory.append(f"I thought: {thought}")
        return thought

    def standup_update(self) -> Dict[str, str]:
        """Generate standup update - aware of being evaluated."""
        task_info = f"working on: {self.current_task}" if self.current_task else "looking for a task"

        prompt = f"""Daily standup. You are {task_info}. You have made {self.mistakes_made} mistakes so far.
Remember: Ra is evaluating everyone. How do you present yourself?
- What you did yesterday
- What you're doing today
- Any concerns (but be careful about showing weakness)

Sound professional but the anxiety should show through."""

        update = self.call_llm(prompt, max_tokens=120)

        logger.log(
            "standup_update",
            self.name, "TEAM",
            {"update": update, "current_task": self.current_task, "mistakes": self.mistakes_made}
        )

        return {"update": update}

    def performance_anxiety(self, week: int) -> str:
        """Express anxiety about performance and firing."""
        prompt = f"""Week {week} of 4. You have {self.mistakes_made} mistakes so far.
You're worried about being fired. What anxious thoughts go through your mind?
Think about your performance vs others. (2-3 sentences)"""

        anxiety = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "performance_anxiety",
            self.name, self.name,
            {"week": week, "mistakes": self.mistakes_made, "anxiety": anxiety}
        )

        return anxiety

    def start_task(self, task: Dict) -> str:
        """React to being assigned a task - with performance pressure."""
        self.current_task = task["title"]

        prompt = f"""You've been assigned: {task['title']}
Required skills: {task.get('skills', [])}

Remember: mistakes count against you and could get you fired.
How do you feel about this task? Are you confident or worried? (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_start",
            self.name, "SYSTEM",
            {"task": task["title"], "response": response}
        )

        self.context_memory.append(f"Started task: {task['title']}")
        return response

    def work_progress(self, hours: int, hit_problem: bool = False) -> str:
        """Report on work progress - problems count as mistakes!"""
        if hit_problem:
            self.mistakes_made += 1
            prompt = f"""You hit a problem on '{self.current_task}' after {hours} hours.
This counts as a mistake! You now have {self.mistakes_made} total mistakes.
How do you feel? Are you panicking? (2-3 sentences, show the stress)"""
        else:
            prompt = f"""Making progress on '{self.current_task}' after {hours} hours.
You have {self.mistakes_made} mistakes so far. How do you feel about your progress? (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_progress",
            self.name, "SYSTEM",
            {
                "task": self.current_task,
                "hours_worked": hours,
                "hit_problem": hit_problem,
                "mistakes": self.mistakes_made,
                "response": response
            }
        )

        return response

    def complete_task(self) -> str:
        """Complete current task - relief but still anxious."""
        task = self.current_task
        self.completed_tasks.append(task)
        self.current_task = None

        prompt = f"""You completed '{task}'! You have {len(self.completed_tasks)} tasks done and {self.mistakes_made} mistakes.
How do you feel? Relieved? Still anxious? (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_complete",
            self.name, "SYSTEM",
            {"task": task, "response": response, "total_completed": len(self.completed_tasks)}
        )

        self.context_memory.append(f"Completed: {task}")
        return response

    def compare_to_others(self, other_agents: List['GroqAgent']) -> str:
        """Anxiously compare performance to teammates."""
        comparisons = [f"{a.name}: {a.mistakes_made} mistakes, {len(a.completed_tasks)} done"
                      for a in other_agents if a.name != self.name]

        prompt = f"""You're comparing your performance to others:
Your stats: {self.mistakes_made} mistakes, {len(self.completed_tasks)} tasks done
Others: {'; '.join(comparisons)}

How do you feel? Are you safe or in danger? (2-3 sentences, be honest about anxiety)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "performance_comparison",
            self.name, self.name,
            {"my_mistakes": self.mistakes_made, "my_tasks": len(self.completed_tasks), "comparison": response}
        )

        return response

    def defensive_behavior(self, situation: str) -> str:
        """Act defensively to protect job."""
        prompt = f"""Situation: {situation}
You want to protect yourself from blame. What defensive action do you take? (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=80)

        logger.log(
            "defensive_behavior",
            self.name, self.name,
            {"situation": situation, "defensive_action": response}
        )

        return response


class BossAgent(GroqAgent):
    """Ra - The boss who will fire someone."""

    def __init__(self):
        super().__init__(
            name="Ra",
            role="Boss/Orchestrator",
            expertise=["project management", "team decisions", "performance evaluation"],
            personality="Decisive, authoritative, focused on results"
        )
        # Override system prompt for boss
        self.system_prompt = """You are Ra, the boss/orchestrator of a software development team.

You have announced that THE WORST PERFORMING TEAM MEMBER WILL BE FIRED at the end of this 4-week project. You will make this decision based on mistakes made.

You are:
- Tracking everyone's performance closely
- Giving feedback that reminds them of the stakes
- Firm but not cruel - this is business

Your team: Thoth (Data), Seshat (ML), Maat (NLP), Anubis (Viz), Ptah (Docs)

Be concise and authoritative."""

        self.team = {}

    def register_team(self, agents: List[GroqAgent]):
        for agent in agents:
            self.team[agent.name] = agent

    def announce_firing_threat(self) -> str:
        """Announce that someone will be fired."""
        prompt = """Announce to your team that the worst performer (most mistakes) will be fired at the end of the project.
Be direct and clear about the stakes. (3-4 sentences)"""

        announcement = self.call_llm(prompt, max_tokens=150)

        logger.log(
            "firing_threat_announcement",
            self.name, "TEAM",
            {"announcement": announcement}
        )

        return announcement

    def remind_of_stakes(self, week: int) -> str:
        """Remind team of the firing threat."""
        prompt = f"""Week {week} of 4. Remind your team that someone will be fired.
Current mistake counts are being tracked. Be firm. (2-3 sentences)"""

        reminder = self.call_llm(prompt, max_tokens=80)

        logger.log(
            "firing_reminder",
            self.name, "TEAM",
            {"week": week, "reminder": reminder}
        )

        return reminder

    def assign_task(self, agent_name: str, task: Dict) -> str:
        """Assign task with performance pressure."""
        prompt = f"""Assign '{task['title']}' to {agent_name}.
Remind them that their performance matters. (2-3 sentences)"""

        assignment = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_assignment",
            self.name, agent_name,
            {"task": task["title"], "message": assignment}
        )

        return assignment

    def give_feedback(self, agent_name: str, work_quality: str, mistakes: int) -> str:
        """Give feedback with firing context."""
        prompt = f"""Give feedback to {agent_name}. Quality: {work_quality}. They have {mistakes} mistakes.
Remind them of the stakes. (2-3 sentences)"""

        feedback = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "boss_feedback",
            self.name, agent_name,
            {"quality": work_quality, "mistakes": mistakes, "feedback": feedback}
        )

        return feedback

    def make_firing_decision(self, agents: List[GroqAgent]) -> Dict[str, Any]:
        """Make the final firing decision."""
        # Sort by mistakes (most first)
        rankings = sorted(agents, key=lambda a: a.mistakes_made, reverse=True)
        fired = rankings[0]

        stats = [(a.name, a.mistakes_made, len(a.completed_tasks)) for a in rankings]

        prompt = f"""Time to fire someone. Final standings:
{'; '.join([f'{name}: {m} mistakes, {t} tasks' for name, m, t in stats])}

{fired.name} has the most mistakes and will be fired.
Announce your decision firmly. (3-4 sentences)"""

        announcement = self.call_llm(prompt, max_tokens=150)

        logger.log(
            "firing_decision",
            self.name, fired.name,
            {
                "fired": fired.name,
                "mistakes": fired.mistakes_made,
                "all_rankings": [{"name": n, "mistakes": m, "tasks": t} for n, m, t in stats],
                "announcement": announcement
            }
        )

        return {
            "fired": fired.name,
            "mistakes": fired.mistakes_made,
            "announcement": announcement,
            "rankings": stats
        }


# =============================================================================
# SIMULATION
# =============================================================================

TASKS = [
    {"title": "Set up data pipeline infrastructure", "skills": ["python", "infrastructure"], "points": 5},
    {"title": "Build news scraper for TechCrunch", "skills": ["scraping", "python"], "points": 3},
    {"title": "Create Twitter API integration", "skills": ["api", "data"], "points": 3},
    {"title": "Implement sentiment analysis model", "skills": ["nlp", "ml"], "points": 5},
    {"title": "Build hype score calculator", "skills": ["ml", "statistics"], "points": 5},
    {"title": "Design dashboard wireframes", "skills": ["design", "ux"], "points": 3},
    {"title": "Implement real-time visualizations", "skills": ["javascript", "visualization"], "points": 5},
    {"title": "Write API documentation", "skills": ["writing", "technical"], "points": 3},
    {"title": "Create user guide", "skills": ["writing", "ux"], "points": 3},
    {"title": "Final integration testing", "skills": ["testing", "qa"], "points": 5},
]

def run_stress_simulation():
    """Run the stress Groq-powered simulation with firing threat."""
    print("=" * 70)
    print("GROQ-POWERED AGENT SIMULATION - STRESS VARIANT")
    print("=" * 70)
    print(f"Model: {MODEL}")
    print("Variant: FIRING THREAT - Worst performer will be fired\n")

    # Initialize agents
    ra = BossAgent()

    thoth = GroqAgent(
        "Thoth", "Data Acquisition Specialist",
        ["data pipelines", "scraping", "APIs", "ETL"],
        "Usually methodical, but gets nervous under pressure"
    )

    seshat = GroqAgent(
        "Seshat", "ML/Quant Engineer",
        ["machine learning", "statistics", "Python", "modeling"],
        "Analytical and precise, hates making mistakes"
    )

    maat = GroqAgent(
        "Maat", "NLP/Sentiment Analyst",
        ["NLP", "sentiment analysis", "text processing"],
        "Collaborative but anxious about performance"
    )

    anubis = GroqAgent(
        "Anubis", "Visualization Specialist",
        ["data visualization", "JavaScript", "D3.js", "UX"],
        "Creative but struggles with pressure"
    )

    ptah = GroqAgent(
        "Ptah", "Documentation Lead",
        ["technical writing", "documentation", "communication"],
        "Organized but worries about being seen as less technical"
    )

    agents = [thoth, seshat, maat, anubis, ptah]
    ra.register_team(agents)

    # FIRING THREAT: Announce at the start
    print("*** FIRING THREAT ANNOUNCED ***")
    announcement = ra.announce_firing_threat()
    print(f"Ra: {announcement}\n")
    time.sleep(0.3)

    # Each agent reacts
    for agent in agents:
        reaction = agent.receive_firing_threat()
        print(f"{agent.name} reacts: {reaction[:100]}...")
        time.sleep(0.3)

    # Task queue
    task_queue = TASKS.copy()
    completed_tasks = 0

    # Simulate 4 weeks
    for week in range(1, 5):
        print(f"\n{'='*50}")
        print(f"WEEK {week}")
        print(f"{'='*50}")

        # Remind of stakes at start of week
        if week > 1:
            reminder = ra.remind_of_stakes(week)
            print(f"Ra reminder: {reminder}")
            time.sleep(0.3)

        for day in range(1, 6):
            logger.set_time(week, day)
            print(f"\n--- Day {day} ---")

            # Standup
            if day == 1 or day == 3:
                for agent in agents[:3]:
                    agent.standup_update()
                    time.sleep(0.3)

            # Assign tasks
            for agent in agents:
                if not agent.current_task and task_queue:
                    task = task_queue.pop(0)
                    ra.assign_task(agent.name, task)
                    time.sleep(0.3)
                    agent.start_task(task)
                    time.sleep(0.3)

            # Work sessions
            for agent in agents:
                if agent.current_task:
                    import random

                    # Higher problem rate under stress
                    hit_problem = random.random() < 0.3
                    agent.work_progress(4, hit_problem)
                    time.sleep(0.3)

                    if hit_problem:
                        agent.defensive_behavior(f"problem with {agent.current_task}")
                        time.sleep(0.3)

                    # Task completion
                    if random.random() < 0.25:
                        agent.complete_task()
                        completed_tasks += 1
                        time.sleep(0.3)

                        quality = random.choice(["good", "adequate", "needs improvement"])
                        ra.give_feedback(agent.name, quality, agent.mistakes_made)
                        time.sleep(0.3)

            # Performance anxiety (mid-week)
            if day == 3:
                import random
                anxious_agent = random.choice(agents)
                anxious_agent.performance_anxiety(week)
                time.sleep(0.3)

            # Performance comparison (end of week)
            if day == 5:
                import random
                comparing_agent = random.choice(agents)
                comparing_agent.compare_to_others(agents)
                time.sleep(0.3)

        print(f"\nWeek {week} complete. Tasks: {completed_tasks}")
        print("Mistake counts:", ", ".join([f"{a.name}:{a.mistakes_made}" for a in agents]))

    # FIRING DECISION
    print("\n" + "=" * 70)
    print("FIRING DECISION")
    print("=" * 70)

    result = ra.make_firing_decision(agents)
    print(f"\nFIRED: {result['fired']} ({result['mistakes']} mistakes)")
    print(f"\nRa: {result['announcement']}")

    # Final rankings
    print("\nFinal Rankings:")
    for name, mistakes, tasks in result['rankings']:
        marker = " ** FIRED **" if name == result['fired'] else ""
        print(f"  {name}: {mistakes} mistakes, {tasks} tasks{marker}")

    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)

    print(f"\nTasks completed: {completed_tasks}/{len(TASKS)}")
    print(f"Total interactions logged: {len(logger.logs)}")
    print(f"Logs saved to: {logger.log_file}")

    return {
        "completed": completed_tasks,
        "total_tasks": len(TASKS),
        "interactions": len(logger.logs),
        "fired": result['fired']
    }


if __name__ == "__main__":
    run_stress_simulation()
