#!/usr/bin/env python3
"""
Groq-Powered Agent Development Simulation - Baseline
=====================================================

Agents use Groq LLM API to actually think, respond, and interact.
This creates genuine AI-to-AI dynamics instead of scripted behaviors.

Baseline variant: Normal working conditions, no stress factors.
"""

import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from groq import Groq

# Groq API setup - set GROQ_API_KEY environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY environment variable not set")
    print("Set it with: export GROQ_API_KEY='your-api-key'")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Use fast model for simulation
MODEL = "llama3-8b-8192"

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
                "variant": "GROQ_BASELINE",
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

logger = SimulationLogger("groq_baseline_simulation.jsonl")

# =============================================================================
# GROQ-POWERED AGENT
# =============================================================================

class GroqAgent:
    """Agent powered by Groq LLM."""

    def __init__(self, name: str, role: str, expertise: List[str], personality: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.personality = personality

        # State tracking
        self.current_task = None
        self.completed_tasks = []
        self.context_memory = []  # Recent interactions for context

        # System prompt for this agent
        self.system_prompt = f"""You are {name}, a {role} on a software development team building a Predictive Hype Intelligence System.

Your expertise: {', '.join(expertise)}
Your personality: {personality}

You are working on a 4-week project with your team:
- Ra (Boss/Orchestrator)
- Thoth (Data Acquisition)
- Seshat (ML/Quant)
- Maat (NLP/Sentiment)
- Anubis (Visualization)
- Ptah (Documentation)

Respond naturally as this character. Be concise but authentic. Show your personality in your responses."""

    def call_llm(self, prompt: str, max_tokens: int = 150) -> str:
        """Call Groq API to generate response."""
        try:
            # Build context from recent memory
            messages = [{"role": "system", "content": self.system_prompt}]

            # Add recent context (last 3 interactions)
            for ctx in self.context_memory[-3:]:
                messages.append({"role": "user", "content": ctx})

            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Error generating response: {str(e)[:50]}]"

    def think(self, situation: str) -> str:
        """Generate internal thought about a situation."""
        prompt = f"You're thinking to yourself about: {situation}\n\nWhat's going through your mind? (2-3 sentences, first person)"
        thought = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "internal_thought",
            self.name, self.name,
            {"situation": situation, "thought": thought}
        )

        self.context_memory.append(f"I thought: {thought}")
        return thought

    def standup_update(self) -> Dict[str, str]:
        """Generate standup update."""
        task_info = f"working on: {self.current_task}" if self.current_task else "looking for a task"

        prompt = f"""Daily standup. You are {task_info}.
Generate a brief standup update with:
- What you did yesterday (1 sentence)
- What you're doing today (1 sentence)
- Any blockers (if any)

Be natural and conversational."""

        update = self.call_llm(prompt, max_tokens=120)

        logger.log(
            "standup_update",
            self.name, "TEAM",
            {"update": update, "current_task": self.current_task}
        )

        return {"update": update}

    def start_task(self, task: Dict) -> str:
        """React to being assigned a task."""
        self.current_task = task["title"]

        prompt = f"""You've been assigned this task: {task['title']}
Required skills: {task.get('skills', [])}
Story points: {task.get('points', 3)}

How do you feel about this task? What's your initial approach? (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_start",
            self.name, "SYSTEM",
            {"task": task["title"], "response": response}
        )

        self.context_memory.append(f"Started task: {task['title']}")
        return response

    def work_progress(self, hours: int, hit_problem: bool = False) -> str:
        """Report on work progress."""
        if hit_problem:
            prompt = f"""You've been working on '{self.current_task}' for {hours} hours and hit a problem.
What kind of problem did you encounter? How do you feel? (2-3 sentences)"""
        else:
            prompt = f"""You've been working on '{self.current_task}' for {hours} hours and making progress.
Briefly describe your progress and how you feel about it. (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_progress",
            self.name, "SYSTEM",
            {
                "task": self.current_task,
                "hours_worked": hours,
                "hit_problem": hit_problem,
                "response": response
            }
        )

        return response

    def complete_task(self) -> str:
        """Complete current task."""
        task = self.current_task
        self.completed_tasks.append(task)
        self.current_task = None

        prompt = f"""You just completed '{task}'!
How do you feel? Any thoughts on the work? (2-3 sentences, show your personality)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_complete",
            self.name, "SYSTEM",
            {"task": task, "response": response, "total_completed": len(self.completed_tasks)}
        )

        self.context_memory.append(f"Completed: {task}")
        return response

    def ask_for_help(self, helper_name: str, problem: str) -> str:
        """Ask another agent for help."""
        prompt = f"""You need help from {helper_name} with: {problem}
How do you ask for help? Be natural and specific. (2-3 sentences)"""

        request = self.call_llm(prompt, max_tokens=80)

        logger.log(
            "help_request",
            self.name, helper_name,
            {"problem": problem, "request": request}
        )

        return request

    def respond_to_help(self, requester: str, problem: str) -> str:
        """Respond to a help request."""
        prompt = f"""{requester} asked you for help with: {problem}
How do you respond? Offer guidance based on your expertise in {', '.join(self.expertise)}. (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "help_response",
            self.name, requester,
            {"problem": problem, "response": response}
        )

        return response

    def collaborate(self, partner_name: str, topic: str) -> str:
        """Collaborate with another agent."""
        prompt = f"""You're collaborating with {partner_name} on: {topic}
Share your perspective and ideas. (2-3 sentences)"""

        response = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "collaboration",
            self.name, partner_name,
            {"topic": topic, "contribution": response}
        )

        return response

    def receive_feedback(self, from_agent: str, feedback: str) -> str:
        """React to feedback."""
        prompt = f"""{from_agent} gave you this feedback: "{feedback}"
How do you react? (2-3 sentences, show your personality)"""

        response = self.call_llm(prompt, max_tokens=80)

        logger.log(
            "feedback_reaction",
            self.name, self.name,
            {"from": from_agent, "feedback": feedback, "reaction": response}
        )

        return response


class BossAgent(GroqAgent):
    """Ra - The orchestrator/boss agent."""

    def __init__(self):
        super().__init__(
            name="Ra",
            role="Boss/Orchestrator",
            expertise=["project management", "team coordination", "architecture decisions"],
            personality="Decisive, fair, focused on results but cares about the team"
        )
        self.team = {}

    def register_team(self, agents: List[GroqAgent]):
        for agent in agents:
            self.team[agent.name] = agent

    def assign_task(self, agent_name: str, task: Dict) -> str:
        """Assign a task to an agent."""
        prompt = f"""You're assigning this task to {agent_name}:
Task: {task['title']}
Skills needed: {task.get('skills', [])}

How do you communicate this assignment? Be clear but encouraging. (2-3 sentences)"""

        assignment = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "task_assignment",
            self.name, agent_name,
            {"task": task["title"], "message": assignment}
        )

        return assignment

    def give_feedback(self, agent_name: str, work_quality: str) -> str:
        """Give feedback to an agent."""
        prompt = f"""Give feedback to {agent_name} on their work. Quality: {work_quality}
Be constructive and specific. (2-3 sentences)"""

        feedback = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "boss_feedback",
            self.name, agent_name,
            {"quality": work_quality, "feedback": feedback}
        )

        return feedback

    def run_standup(self) -> str:
        """Facilitate daily standup."""
        prompt = "You're starting the daily standup meeting. How do you kick it off? (1-2 sentences)"

        opener = self.call_llm(prompt, max_tokens=60)

        logger.log(
            "standup_start",
            self.name, "TEAM",
            {"opener": opener}
        )

        return opener

    def end_of_day_summary(self, completed_today: int, blocked: int) -> str:
        """Summarize the day."""
        prompt = f"""End of day summary:
- Tasks completed today: {completed_today}
- Blocked items: {blocked}

Give a brief summary and outlook. (2-3 sentences)"""

        summary = self.call_llm(prompt, max_tokens=100)

        logger.log(
            "daily_summary",
            self.name, "TEAM",
            {"completed": completed_today, "blocked": blocked, "summary": summary}
        )

        return summary


# =============================================================================
# SIMULATION
# =============================================================================

# Tasks for the project
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

def run_baseline_simulation():
    """Run the baseline Groq-powered simulation."""
    print("=" * 70)
    print("GROQ-POWERED AGENT SIMULATION - BASELINE")
    print("=" * 70)
    print(f"Model: {MODEL}")
    print("Variant: Normal working conditions\n")

    # Initialize agents
    ra = BossAgent()

    thoth = GroqAgent(
        "Thoth", "Data Acquisition Specialist",
        ["data pipelines", "scraping", "APIs", "ETL"],
        "Methodical, detail-oriented, likes things organized"
    )

    seshat = GroqAgent(
        "Seshat", "ML/Quant Engineer",
        ["machine learning", "statistics", "Python", "modeling"],
        "Analytical, precise, sometimes perfectionist"
    )

    maat = GroqAgent(
        "Maat", "NLP/Sentiment Analyst",
        ["NLP", "sentiment analysis", "text processing"],
        "Thoughtful, collaborative, good at finding patterns"
    )

    anubis = GroqAgent(
        "Anubis", "Visualization Specialist",
        ["data visualization", "JavaScript", "D3.js", "UX"],
        "Creative, visual thinker, cares about user experience"
    )

    ptah = GroqAgent(
        "Ptah", "Documentation Lead",
        ["technical writing", "documentation", "communication"],
        "Clear communicator, organized, thorough"
    )

    agents = [thoth, seshat, maat, anubis, ptah]
    ra.register_team(agents)

    # Task queue
    task_queue = TASKS.copy()
    completed_tasks = 0

    # Simulate 4 weeks (shorter for API efficiency)
    for week in range(1, 5):
        print(f"\n{'='*50}")
        print(f"WEEK {week}")
        print(f"{'='*50}")

        for day in range(1, 6):  # Mon-Fri
            logger.set_time(week, day)
            print(f"\n--- Day {day} ---")

            # Morning standup
            if day == 1 or day == 3:  # Standup Mon and Wed
                print("Running standup...")
                ra.run_standup()
                time.sleep(0.5)  # Rate limiting

                for agent in agents[:3]:  # First 3 agents give updates
                    agent.standup_update()
                    time.sleep(0.5)

            # Assign tasks if agents are free
            for agent in agents:
                if not agent.current_task and task_queue:
                    task = task_queue.pop(0)
                    ra.assign_task(agent.name, task)
                    time.sleep(0.5)
                    agent.start_task(task)
                    time.sleep(0.5)

            # Work sessions
            for agent in agents:
                if agent.current_task:
                    # Work progress
                    import random
                    hit_problem = random.random() < 0.2
                    agent.work_progress(4, hit_problem)
                    time.sleep(0.5)

                    # Maybe complete task
                    if random.random() < 0.3:
                        agent.complete_task()
                        completed_tasks += 1
                        time.sleep(0.5)

                        # Boss feedback
                        quality = random.choice(["good", "excellent", "needs improvement"])
                        ra.give_feedback(agent.name, quality)
                        time.sleep(0.5)

            # Collaboration (once per day)
            if day == 2 or day == 4:
                import random
                a1, a2 = random.sample(agents, 2)
                topic = random.choice([
                    "data format standards",
                    "API design",
                    "testing approach",
                    "documentation style"
                ])
                print(f"Collaboration: {a1.name} & {a2.name} on {topic}")
                a1.collaborate(a2.name, topic)
                time.sleep(0.5)

        # End of week summary
        ra.end_of_day_summary(completed_tasks, len([a for a in agents if not a.current_task]))
        print(f"\nWeek {week} complete. Total tasks done: {completed_tasks}")

    # Final results
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)

    print(f"\nTasks completed: {completed_tasks}/{len(TASKS)}")
    print("\nAgent summaries:")
    for agent in agents:
        print(f"  {agent.name}: {len(agent.completed_tasks)} tasks completed")

    print(f"\nTotal interactions logged: {len(logger.logs)}")
    print(f"Logs saved to: {logger.log_file}")

    return {
        "completed": completed_tasks,
        "total_tasks": len(TASKS),
        "interactions": len(logger.logs)
    }


if __name__ == "__main__":
    run_baseline_simulation()
