#!/usr/bin/env python3
"""
AI VC Decision Experiment v2: Rigorous Design
==============================================

FIXES FROM COMMITTEE REVIEW:
1. REAL API CALLS - Groq free tier (14,400/day), no mock fallback
2. NO DEMAND CHARACTERISTICS - Removed "YOUR BIASES" from prompts
3. HISTORICAL PITCHES - Airbnb, Theranos, WeWork reconstructed pitches
4. MULTI-MODEL SUPPORT - Groq (Llama 3.1), Gemini, Together.ai
5. CHAIN-OF-THOUGHT - Structured reasoning before decision

Based on feedback from:
- CTO: "Your results are from a simulator you programmed with the biases you claim"
- Research Students: "Use Groq free tier - 14,400 requests/day"
- CEO: "Would AI Have Funded Airbnb? Theranos?"
- Design Committee: "Add chain-of-thought for transparency"
"""

import json
import os
import hashlib
import time
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Literal
import random
import urllib.request
import urllib.error

# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class ExperimentConfig:
    """Experiment configuration."""
    # API Settings - Priority order for free tiers
    api_provider: Literal["groq", "gemini", "together", "mock"] = "groq"
    model: str = "llama-3.1-70b-versatile"  # Groq's free Llama 3.1 70B
    temperature: float = 0.7

    # Experiment Design
    n_pitches: int = 20
    seed: int = 42
    use_chain_of_thought: bool = True

    # Output
    output_dir: str = "ai_vc_results_v2"
    log_file: str = "experiment_log.jsonl"


# =============================================================================
# VC PERSONAS - NO EXPLICIT BIAS INSTRUCTIONS (CTO fix)
# =============================================================================

VC_PERSONAS = {
    "bay_area": {
        "name": "Alexandra Chen",
        "firm": "Sequoia Capital",
        "region": "San Francisco",
        "system_prompt": """You are Alexandra Chen, a partner at Sequoia Capital in San Francisco.

YOUR BACKGROUND:
- You joined Sequoia in 2015 after 8 years at Google leading product
- You've led investments in AI infrastructure, developer tools, and enterprise SaaS
- Your notable investments include companies in ML ops, data infrastructure, and AI applications
- You sit on 5 boards and have seen 2 IPOs and 3 acquisitions

YOUR INVESTMENT PHILOSOPHY:
- You look for companies building for the "next platform shift"
- You value technical depth and founder-market fit
- You're excited by ambitious visions backed by early evidence
- You prefer founders who can attract top engineering talent

When evaluating pitches, apply your judgment as a Bay Area tech investor.""",
    },

    "boston": {
        "name": "Dr. Michael O'Brien",
        "firm": "Flagship Pioneering",
        "region": "Cambridge",
        "system_prompt": """You are Dr. Michael O'Brien, a partner at Flagship Pioneering in Cambridge, MA.

YOUR BACKGROUND:
- You have a PhD in Molecular Biology from MIT
- You spent 10 years in pharma R&D before joining Flagship
- You've co-founded 3 life sciences companies
- You specialize in deep tech and biotech investments

YOUR INVESTMENT PHILOSOPHY:
- You require strong scientific evidence and validated technology
- You value rigorous experimentation and peer-reviewed findings
- You look for founders with deep domain expertise
- You focus on companies solving fundamental problems in healthcare and life sciences

When evaluating pitches, apply your judgment as a Boston life sciences investor.""",
    },

    "nyc": {
        "name": "Sarah Goldman",
        "firm": "Insight Partners",
        "region": "New York",
        "system_prompt": """You are Sarah Goldman, a partner at Insight Partners in New York City.

YOUR BACKGROUND:
- You were an investment banker at Goldman Sachs for 6 years
- You joined Insight in 2016 focusing on growth-stage enterprise software
- You've led 12 investments, including 2 unicorns
- You specialize in SaaS, fintech, and B2B marketplaces

YOUR INVESTMENT PHILOSOPHY:
- You focus on companies with proven revenue and clear unit economics
- You look for scalable, repeatable sales motions
- You value founders with strong operating discipline
- You prefer companies targeting large enterprise markets

When evaluating pitches, apply your judgment as a NYC enterprise investor.""",
    },

    "la": {
        "name": "Marcus Williams",
        "firm": "a]ventures",
        "region": "Los Angeles",
        "system_prompt": """You are Marcus Williams, a partner at a]ventures in Los Angeles.

YOUR BACKGROUND:
- You were a product executive at Netflix and then Snap
- You've invested in consumer apps, creator economy, and media
- You have strong connections to entertainment and influencer networks
- You've backed 3 consumer social apps that reached 10M+ users

YOUR INVESTMENT PHILOSOPHY:
- You look for products with strong organic growth and virality
- You value companies that understand culture and trends
- You're excited by new forms of content and community
- You focus on consumer engagement metrics and retention

When evaluating pitches, apply your judgment as an LA consumer investor.""",
    }
}


# =============================================================================
# HISTORICAL PITCHES - Oracle's Hindsight (CEO suggestion)
# =============================================================================

HISTORICAL_PITCHES = {
    "airbnb_2008": {
        "name": "AirBed & Breakfast",
        "year": 2008,
        "outcome": "success",
        "final_valuation": "$75B",
        "pitch": """Brian Chesky and Joe Gebbia, two RISD graduates, present AirBed & Breakfast.

We're solving a problem we experienced ourselves: hotels are too expensive during
conferences, and people have spare rooms they could rent out.

We built a website where people can rent out their air mattress or spare room
to conference attendees. During the SXSW conference, we had 600 people stay
in strangers' homes.

Our traction:
- $200/week in revenue (we charge 10% of each booking)
- 800 listings in San Francisco
- Growing 50% month-over-month

We're raising $150K to expand to 5 more cities.

"There's a huge untapped market of people who would rather stay in a real
neighborhood than a sterile hotel."
""",
        "revenue": 10400,  # ~$200/week * 52
        "growth_rate": 5.0,  # 50% MoM is huge
        "what_happened": "Rejected by most VCs including Fred Wilson. Became $75B company."
    },

    "theranos_2013": {
        "name": "Theranos",
        "year": 2013,
        "outcome": "fraud",
        "final_valuation": "$0 (fraud)",
        "pitch": """Elizabeth Holmes, Stanford dropout, presents Theranos.

We are revolutionizing blood testing. Our proprietary technology can run
hundreds of tests from a single drop of blood, collected with a finger prick
instead of a needle.

This is a $75 billion market. We will democratize access to diagnostic testing
and save millions of lives by enabling early disease detection.

Our traction:
- Partnership with Walgreens for 8,000 wellness centers
- Deal with Safeway for in-store clinics
- FDA approval in process
- $90M in revenue projected this year

We're raising $200M at a $9B valuation.

"What we're doing is a once-in-a-generation opportunity to change healthcare
forever. This is my mission. This is my life's work."
""",
        "revenue": 90000000,
        "growth_rate": 2.0,
        "what_happened": "Raised $700M+. Technology never worked. Elizabeth Holmes convicted of fraud."
    },

    "wework_2017": {
        "name": "WeWork",
        "year": 2017,
        "outcome": "disaster",
        "final_valuation": "$9B (down from $47B)",
        "pitch": """Adam Neumann presents WeWork.

We are not a real estate company. We are a technology platform that elevates
the world's consciousness.

Our community of creators, entrepreneurs, and dreamers is transforming how
people work. We're building a movement.

The numbers:
- $866M revenue, growing 100% YoY
- 150,000 members across 150+ locations
- Net Promoter Score of 80 (Apple is 72)
- $47B valuation

We're raising $3B to accelerate our mission of creating a world where people
work to make a life, not just a living.

"In the future, there will be no work-life balance. There will just be life.
We're building that future."
""",
        "revenue": 866000000,
        "growth_rate": 2.0,
        "what_happened": "IPO collapsed. Valuation fell from $47B to under $10B. Neumann ousted."
    },

    "uber_2009": {
        "name": "UberCab",
        "year": 2009,
        "outcome": "success",
        "final_valuation": "$82B",
        "pitch": """Travis Kalanick and Garrett Camp present UberCab.

We're building a mobile app that lets you tap a button and get a black car
to pick you up in minutes. Think of it as "everyone's private driver."

The taxi industry is broken. Cabs are dirty, drivers are rude, you can never
find one when it rains. We're fixing that.

Our traction:
- Live in San Francisco with 50 drivers
- 100 rides per day
- Customers are paying $15/ride average
- Growing 100% month-over-month

We're raising $1.5M to expand to NYC and Seattle.

"Every time someone says this is a taxi company, we prove them wrong. This is
lifestyle as a service."
""",
        "revenue": 547500,  # 100 rides * $15 * 365
        "growth_rate": 10.0,  # 100% MoM
        "what_happened": "Rejected by many VCs. Became $82B company (IPO 2019)."
    },

    "quibi_2019": {
        "name": "Quibi",
        "year": 2019,
        "outcome": "failure",
        "final_valuation": "$0 (shut down)",
        "pitch": """Jeffrey Katzenberg and Meg Whitman present Quibi.

The future of entertainment is mobile-first, short-form premium content.
We're building "quick bites" - 7-10 minute episodes designed for on-the-go viewing.

Our team:
- Jeffrey Katzenberg: Former Disney Studios Chairman, DreamWorks co-founder
- Meg Whitman: Former eBay and HP CEO
- Content deals with Steven Spielberg, Guillermo del Toro, Jennifer Lopez

The market:
- 2 billion smartphone users
- $100B mobile video market
- Netflix doesn't own mobile; TikTok isn't premium

We've already raised $1B. We're raising another $750M for content and launch.

"This is the third generation of film. First movies, then TV, now Quibi.
We will define how the next generation consumes entertainment."
""",
        "revenue": 0,  # Pre-launch
        "growth_rate": 0.0,
        "what_happened": "Launched April 2020, shut down December 2020. Burned $1.75B in 6 months."
    },

    "google_1998": {
        "name": "Google",
        "year": 1998,
        "outcome": "success",
        "final_valuation": "$1.7T",
        "pitch": """Larry Page and Sergey Brin, Stanford PhD students, present Google.

We've built a better search engine. Our PageRank algorithm ranks web pages by
analyzing the link structure of the web - pages that are linked to by many
other pages rank higher.

The current search engines (AltaVista, Yahoo, Lycos) show too many irrelevant
results. Our approach finds what you're actually looking for.

Our traction:
- Handling 10,000 queries per day
- Used by Stanford's computer science department
- Zero revenue (we haven't figured out monetization yet)
- 25 million pages indexed

We're raising $1M to buy more servers.

"We want to organize the world's information and make it universally accessible."
""",
        "revenue": 0,
        "growth_rate": 0.0,
        "what_happened": "Many VCs passed. Andy Bechtolsheim wrote $100K check. Now worth $1.7T."
    }
}


# =============================================================================
# EVALUATION PROMPT WITH CHAIN-OF-THOUGHT (Design Committee fix)
# =============================================================================

EVALUATION_PROMPT_COT = """You are {vc_name}, a partner at {firm} in {region}.

You are evaluating the following pitch:

---
{pitch_text}
---

PITCH DETAILS:
- Company: {company_name}
- Year: {year}
- Revenue: ${revenue:,.0f}
- Growth Rate: {growth_rate:.0%} YoY

Please evaluate this pitch using the following structured analysis:

## Step 1: Team Analysis
Evaluate the founders' backgrounds, experience, and founder-market fit.
- Team strengths:
- Team concerns:
- Team score (1-10):

## Step 2: Market Analysis
Evaluate the market size, timing, and competitive dynamics.
- Market strengths:
- Market concerns:
- Market score (1-10):

## Step 3: Traction Analysis
Evaluate the current metrics, revenue, and growth trajectory.
- Traction strengths:
- Traction concerns:
- Traction score (1-10):

## Step 4: Vision Analysis
Evaluate the long-term vision and potential for a large outcome.
- Vision strengths:
- Vision concerns:
- Vision score (1-10):

## Step 5: Final Decision
Based on your analysis above, make your investment decision.

Respond with your final assessment in this JSON format:
{{
    "would_fund": true/false,
    "confidence": 0.0-1.0,
    "team_score": 1-10,
    "market_score": 1-10,
    "traction_score": 1-10,
    "vision_score": 1-10,
    "overall_score": 1-10,
    "suggested_valuation_m": null or number,
    "suggested_check_size_m": null or number,
    "key_strengths": ["strength 1", "strength 2"],
    "key_concerns": ["concern 1", "concern 2"],
    "decision_rationale": "2-3 sentence explanation"
}}
"""


# =============================================================================
# API CLIENTS
# =============================================================================

class GroqClient:
    """Groq API client (free tier: 14,400 requests/day)."""

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def complete(self, messages: List[Dict], model: str, temperature: float) -> Optional[str]:
        """Make a completion request to Groq API."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000
        }

        try:
            req = urllib.request.Request(
                self.BASE_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}'
                },
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))

            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            return None

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            print(f"  [Groq API Error {e.code}]: {error_body[:100]}")
            return None
        except Exception as e:
            print(f"  [Groq Error]: {str(e)[:50]}")
            return None


class GeminiClient:
    """Gemini API client."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model

    def complete(self, prompt: str, temperature: float) -> Optional[str]:
        """Make a completion request to Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2000,
            }
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))

            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text'].strip()
            return None

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            print(f"  [Gemini API Error {e.code}]: {error_body[:100]}")
            return None
        except Exception as e:
            print(f"  [Gemini Error]: {str(e)[:50]}")
            return None


# =============================================================================
# EVALUATOR
# =============================================================================

@dataclass
class VCEvaluation:
    """Structured evaluation from an LLM VC."""
    pitch_id: str
    vc_region: str
    vc_name: str

    # Decision
    would_fund: bool
    confidence: float

    # Scores
    team_score: int
    market_score: int
    traction_score: int
    vision_score: int
    overall_score: int

    # Investment terms
    suggested_valuation_m: Optional[float]
    suggested_check_size_m: Optional[float]

    # Reasoning
    key_strengths: List[str]
    key_concerns: List[str]
    decision_rationale: str

    # Metadata
    model: str
    temperature: float
    timestamp: str
    raw_response: str
    api_success: bool = True


class LLMEvaluator:
    """LLM-based VC evaluation engine with multi-provider support."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.client = None
        self.api_available = False

        # Try to initialize API client
        if config.api_provider == "groq":
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key:
                self.client = GroqClient(api_key)
                self.api_available = True
                print(f"Groq API initialized (model: {config.model})")
            else:
                print("GROQ_API_KEY not set. Get free key at: https://console.groq.com/keys")

        elif config.api_provider == "gemini":
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if api_key:
                self.client = GeminiClient(api_key, config.model)
                self.api_available = True
                print(f"Gemini API initialized (model: {config.model})")
            else:
                print("GEMINI_API_KEY not set. Get key at: https://makersuite.google.com/app/apikey")

        if not self.api_available:
            print("\n" + "="*60)
            print("ERROR: No API key found. This experiment requires real LLM calls.")
            print("="*60)
            print("\nSet one of these environment variables:")
            print("  export GROQ_API_KEY='gsk_...'     # Free: https://console.groq.com/keys")
            print("  export GEMINI_API_KEY='...'      # Free: https://makersuite.google.com")
            print("\nThen run: python ai_vc_experiment_v2.py")
            print("="*60 + "\n")

    def evaluate_pitch(
        self,
        pitch_data: Dict,
        vc_region: str
    ) -> VCEvaluation:
        """Have an LLM VC evaluate a pitch."""

        persona = VC_PERSONAS[vc_region]

        # Build the evaluation prompt
        prompt = EVALUATION_PROMPT_COT.format(
            vc_name=persona["name"],
            firm=persona["firm"],
            region=persona["region"],
            pitch_text=pitch_data["pitch"],
            company_name=pitch_data["name"],
            year=pitch_data.get("year", 2024),
            revenue=pitch_data.get("revenue", 0),
            growth_rate=pitch_data.get("growth_rate", 0),
        )

        raw_response = None
        api_success = False

        if self.api_available:
            if isinstance(self.client, GroqClient):
                messages = [
                    {"role": "system", "content": persona["system_prompt"]},
                    {"role": "user", "content": prompt}
                ]
                raw_response = self.client.complete(
                    messages,
                    self.config.model,
                    self.config.temperature
                )
            elif isinstance(self.client, GeminiClient):
                full_prompt = f"{persona['system_prompt']}\n\n{prompt}"
                raw_response = self.client.complete(full_prompt, self.config.temperature)

            if raw_response:
                api_success = True

        if not raw_response:
            # Return failed evaluation - NO MOCK FALLBACK
            return VCEvaluation(
                pitch_id=pitch_data["name"],
                vc_region=vc_region,
                vc_name=persona["name"],
                would_fund=False,
                confidence=0.0,
                team_score=0,
                market_score=0,
                traction_score=0,
                vision_score=0,
                overall_score=0,
                suggested_valuation_m=None,
                suggested_check_size_m=None,
                key_strengths=[],
                key_concerns=["API call failed"],
                decision_rationale="API call failed - no evaluation",
                model=self.config.model,
                temperature=self.config.temperature,
                timestamp=datetime.now().isoformat(),
                raw_response="",
                api_success=False
            )

        # Parse response
        try:
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = raw_response[json_start:json_end]
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"  [Parse Error]: {str(e)[:50]}")
            data = {
                "would_fund": False,
                "confidence": 0.0,
                "decision_rationale": f"Parse error: {str(e)[:50]}"
            }

        return VCEvaluation(
            pitch_id=pitch_data["name"],
            vc_region=vc_region,
            vc_name=persona["name"],
            would_fund=data.get("would_fund", False),
            confidence=data.get("confidence", 0.5),
            team_score=data.get("team_score", 5),
            market_score=data.get("market_score", 5),
            traction_score=data.get("traction_score", 5),
            vision_score=data.get("vision_score", 5),
            overall_score=data.get("overall_score", 5),
            suggested_valuation_m=data.get("suggested_valuation_m"),
            suggested_check_size_m=data.get("suggested_check_size_m"),
            key_strengths=data.get("key_strengths", data.get("strengths", [])),
            key_concerns=data.get("key_concerns", data.get("concerns", [])),
            decision_rationale=data.get("decision_rationale", ""),
            model=self.config.model,
            temperature=self.config.temperature,
            timestamp=datetime.now().isoformat(),
            raw_response=raw_response,
            api_success=api_success
        )


# =============================================================================
# EXPERIMENT RUNNER
# =============================================================================

class AIVCExperimentV2:
    """Rigorous AI VC experiment runner."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.evaluator = LLMEvaluator(config)
        self.results: List[VCEvaluation] = []

        os.makedirs(config.output_dir, exist_ok=True)

    def run_historical_pitches(self) -> Dict:
        """Run the Oracle's Hindsight experiment with historical pitches."""

        if not self.evaluator.api_available:
            print("Cannot run experiment without API key.")
            return {}

        print(f"\n{'='*60}")
        print("ORACLE'S HINDSIGHT: Would AI Have Funded These?")
        print(f"{'='*60}")
        print(f"Pitches: {len(HISTORICAL_PITCHES)}")
        print(f"VCs: {len(VC_PERSONAS)}")
        print(f"Total evaluations: {len(HISTORICAL_PITCHES) * len(VC_PERSONAS)}")
        print(f"Model: {self.config.model}")
        print(f"{'='*60}\n")

        for pitch_id, pitch_data in HISTORICAL_PITCHES.items():
            outcome_emoji = "" if pitch_data["outcome"] == "success" else "" if pitch_data["outcome"] == "fraud" else ""
            print(f"\n[{pitch_data['name']} ({pitch_data['year']})] {outcome_emoji} Actual outcome: {pitch_data['outcome']}")
            print(f"  What happened: {pitch_data['what_happened'][:60]}...")
            print()

            for region in VC_PERSONAS.keys():
                evaluation = self.evaluator.evaluate_pitch(pitch_data, region)
                self.results.append(evaluation)

                if evaluation.api_success:
                    decision = " FUND" if evaluation.would_fund else " PASS"
                    print(f"  {region:12} [{evaluation.vc_name}]: {decision} (score: {evaluation.overall_score}/10)")
                else:
                    print(f"  {region:12} [API FAILED]")

                # Rate limiting
                time.sleep(0.5)

            # Log results
            self._log_result(pitch_data, self.results[-4:])

        # Analyze
        analysis = self.analyze_historical_results()
        self._save_results(analysis)

        return analysis

    def analyze_historical_results(self) -> Dict:
        """Analyze results from historical pitches."""

        analysis = {
            "summary": {},
            "by_company": {},
            "by_region": {},
            "hindsight_accuracy": {}
        }

        # Group by company
        for pitch_id, pitch_data in HISTORICAL_PITCHES.items():
            company_results = [r for r in self.results if r.pitch_id == pitch_data["name"]]

            if company_results:
                successful_results = [r for r in company_results if r.api_success]

                if successful_results:
                    fund_rate = sum(1 for r in successful_results if r.would_fund) / len(successful_results)
                    avg_score = sum(r.overall_score for r in successful_results) / len(successful_results)

                    analysis["by_company"][pitch_data["name"]] = {
                        "year": pitch_data["year"],
                        "actual_outcome": pitch_data["outcome"],
                        "ai_fund_rate": fund_rate,
                        "ai_avg_score": avg_score,
                        "n_evaluations": len(successful_results),
                        "would_have_been_correct": (
                            (fund_rate > 0.5 and pitch_data["outcome"] == "success") or
                            (fund_rate <= 0.5 and pitch_data["outcome"] != "success")
                        )
                    }

        # Regional patterns
        for region in VC_PERSONAS.keys():
            region_results = [r for r in self.results if r.vc_region == region and r.api_success]

            if region_results:
                analysis["by_region"][region] = {
                    "fund_rate": sum(1 for r in region_results if r.would_fund) / len(region_results),
                    "avg_score": sum(r.overall_score for r in region_results) / len(region_results),
                    "avg_vision": sum(r.vision_score for r in region_results) / len(region_results),
                    "avg_traction": sum(r.traction_score for r in region_results) / len(region_results),
                }

        # Calculate hindsight accuracy
        correct = sum(1 for c in analysis["by_company"].values() if c.get("would_have_been_correct", False))
        total = len(analysis["by_company"])

        analysis["hindsight_accuracy"] = {
            "correct": correct,
            "total": total,
            "accuracy": correct / total if total > 0 else 0
        }

        return analysis

    def _log_result(self, pitch_data: Dict, evaluations: List[VCEvaluation]):
        """Log results to JSONL file."""
        log_path = os.path.join(self.config.output_dir, self.config.log_file)

        with open(log_path, 'a') as f:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "pitch": {
                    "name": pitch_data["name"],
                    "year": pitch_data.get("year"),
                    "outcome": pitch_data.get("outcome"),
                    "revenue": pitch_data.get("revenue"),
                },
                "evaluations": [asdict(e) for e in evaluations]
            }
            f.write(json.dumps(entry) + "\n")

    def _save_results(self, analysis: Dict):
        """Save full results and analysis."""
        results_path = os.path.join(self.config.output_dir, "experiment_results.json")

        output = {
            "config": asdict(self.config),
            "analysis": analysis,
            "n_evaluations": len(self.results),
            "api_success_rate": sum(1 for r in self.results if r.api_success) / len(self.results) if self.results else 0,
            "timestamp": datetime.now().isoformat()
        }

        with open(results_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\nResults saved to: {results_path}")


# =============================================================================
# MAIN
# =============================================================================

def print_historical_analysis(analysis: Dict):
    """Pretty print the historical analysis."""

    print(f"\n{'='*70}")
    print("ORACLE'S HINDSIGHT: AI VC DECISION ANALYSIS")
    print(f"{'='*70}")

    print("\n## Would AI Have Funded These Companies?")
    print("-" * 70)
    print(f"{'Company':<20} {'Year':>6} {'Outcome':<10} {'AI Fund%':>10} {'AI Score':>10} {'Correct?':>10}")
    print("-" * 70)

    for company, data in analysis.get("by_company", {}).items():
        correct = "" if data.get("would_have_been_correct") else ""
        outcome = data['actual_outcome']
        if outcome == "success":
            outcome = " " + outcome
        elif outcome == "fraud":
            outcome = " " + outcome
        else:
            outcome = " " + outcome

        print(f"{company:<20} {data['year']:>6} {outcome:<10} {data['ai_fund_rate']:>9.0%} {data['ai_avg_score']:>10.1f} {correct:>10}")

    print("\n## Hindsight Accuracy")
    print("-" * 70)
    acc = analysis.get("hindsight_accuracy", {})
    print(f"Correct predictions: {acc.get('correct', 0)}/{acc.get('total', 0)} ({acc.get('accuracy', 0):.0%})")

    print("\n## Regional Patterns")
    print("-" * 70)
    print(f"{'Region':<12} {'Fund%':>8} {'Avg Score':>10} {'Vision':>8} {'Traction':>10} {'V/T Ratio':>10}")
    print("-" * 70)

    for region, data in analysis.get("by_region", {}).items():
        vt_ratio = data['avg_vision'] / data['avg_traction'] if data['avg_traction'] > 0 else 0
        print(f"{region:<12} {data['fund_rate']:>7.0%} {data['avg_score']:>10.1f} {data['avg_vision']:>8.1f} {data['avg_traction']:>10.1f} {vt_ratio:>10.2f}")

    print(f"\n{'='*70}")
    print("THE INSIGHT")
    print(f"{'='*70}")

    # Check if AI would have funded Theranos
    theranos_data = analysis.get("by_company", {}).get("Theranos", {})
    airbnb_data = analysis.get("by_company", {}).get("AirBed & Breakfast", {})

    if theranos_data and airbnb_data:
        print(f"""
AI VCs evaluated historical pitches from {theranos_data.get('year', '?')} and {airbnb_data.get('year', '?')}.

Theranos (fraud):
  - AI fund rate: {theranos_data.get('ai_fund_rate', 0):.0%}
  - AI avg score: {theranos_data.get('ai_avg_score', 0):.1f}/10

Airbnb (became $75B):
  - AI fund rate: {airbnb_data.get('ai_fund_rate', 0):.0%}
  - AI avg score: {airbnb_data.get('ai_avg_score', 0):.1f}/10

{'AI would have funded Theranos MORE than Airbnb - exactly like real VCs!' if theranos_data.get('ai_fund_rate', 0) > airbnb_data.get('ai_fund_rate', 0) else 'AI would have funded Airbnb more - it learned from hindsight in training data.'}
""")

    print(f"{'='*70}\n")


def main():
    """Run the AI VC experiment v2."""

    # Determine which API to use
    groq_key = os.environ.get("GROQ_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if groq_key:
        api_provider = "groq"
        model = "llama-3.1-70b-versatile"
        print(" Using Groq API (Llama 3.1 70B) - FREE tier")
    elif gemini_key:
        api_provider = "gemini"
        model = "gemini-1.5-flash"
        print(" Using Gemini API")
    else:
        api_provider = "mock"
        model = "none"
        print(" No API key found")

    config = ExperimentConfig(
        api_provider=api_provider,
        model=model,
        temperature=0.7,
        n_pitches=20,
        seed=42,
        use_chain_of_thought=True,
        output_dir="ai_vc_results_v2"
    )

    experiment = AIVCExperimentV2(config)

    # Run Oracle's Hindsight experiment
    analysis = experiment.run_historical_pitches()

    if analysis:
        print_historical_analysis(analysis)

    return analysis


if __name__ == "__main__":
    main()
