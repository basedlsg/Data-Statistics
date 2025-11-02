#!/usr/bin/env python3
"""
VC Hype Scoring System - Rule-Based v0
Ma'at (Narrative & Sentiment) - 2025-11-02

Transparent, deterministic hype scorer based on:
1. Keyword/phrase detection (category-defining, paradigm-shift, etc.)
2. Elite VC co-mention analysis (Sequoia, Benchmark, Tiger, etc.)
3. Media cadence (press releases, articles per week)
4. Narrative intensity metrics

This is a v0 implementation using simple rule-based NLP.
Future versions may use FinBERT, GPT-based sentiment, or trained models.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Set
from collections import Counter


# High-hype keywords and phrases
HIGH_HYPE_KEYWORDS = {
    # Transformative language
    "category-defining",
    "paradigm-shift",
    "revolutionary",
    "transformative",
    "disruptive",
    "game-changing",
    "breakthrough",
    "unprecedented",

    # Market dominance
    "market leader",
    "dominant player",
    "winner-take-all",
    "network effects",
    "moat",
    "land grab",

    # Vision/narrative
    "vision",
    "moonshot",
    "ambitious",
    "audacious",
    "bold",
    "reimagining",
    "reinventing",
    "redefining",

    # Scale language
    "unicorn",
    "decacorn",
    "hypergrowth",
    "exponential",
    "viral",
    "explosive growth",

    # Quality signals (can be hype in excess)
    "oversubscribed",
    "competitive round",
    "pre-emptive",
    "insider",
    "proprietary",
}

# Elite VC firms (co-mentions increase hype)
ELITE_VC_FIRMS = {
    "sequoia",
    "andreessen horowitz",
    "a16z",
    "benchmark",
    "kleiner perkins",
    "accel",
    "greylock",
    "lightspeed",
    "tiger global",
    "coatue",
    "insight partners",
    "general catalyst",
    "founders fund",
    "thrive capital",
    "first round",
}

# Anti-hype keywords (fundamental/conservative language)
CONSERVATIVE_KEYWORDS = {
    "profitable",
    "cash-flow positive",
    "sustainable",
    "disciplined",
    "capital-efficient",
    "bootstrapped",
    "organic growth",
    "unit economics",
    "margin",
    "profitability",
}


@dataclass
class HypeSignals:
    """Container for detected hype signals in text."""

    high_hype_count: int
    elite_vc_mentions: int
    conservative_count: int
    text_length: int  # Number of words

    def get_keyword_density(self) -> float:
        """High-hype keyword density (per 100 words)."""
        if self.text_length == 0:
            return 0.0
        return (self.high_hype_count / self.text_length) * 100

    def get_elite_density(self) -> float:
        """Elite VC mention density (per 100 words)."""
        if self.text_length == 0:
            return 0.0
        return (self.elite_vc_mentions / self.text_length) * 100

    def get_conservative_density(self) -> float:
        """Conservative keyword density (dampens hype)."""
        if self.text_length == 0:
            return 0.0
        return (self.conservative_count / self.text_length) * 100


class HypeScorer:
    """Rule-based hype scorer for text documents."""

    def __init__(
        self,
        high_hype_keywords: Set[str] = HIGH_HYPE_KEYWORDS,
        elite_firms: Set[str] = ELITE_VC_FIRMS,
        conservative_keywords: Set[str] = CONSERVATIVE_KEYWORDS
    ):
        """
        Initialize hype scorer.

        Args:
            high_hype_keywords: Set of high-hype keywords/phrases
            elite_firms: Set of elite VC firm names
            conservative_keywords: Set of conservative/fundamental keywords
        """
        self.high_hype_keywords = high_hype_keywords
        self.elite_firms = elite_firms
        self.conservative_keywords = conservative_keywords

    def extract_signals(self, text: str) -> HypeSignals:
        """
        Extract hype signals from text.

        Args:
            text: Input text (press release, article, pitch deck excerpt)

        Returns:
            HypeSignals object with detected signals
        """
        # Normalize text
        text_lower = text.lower()

        # Count words
        words = re.findall(r'\w+', text_lower)
        text_length = len(words)

        # Count high-hype keywords
        high_hype_count = sum(
            text_lower.count(keyword)
            for keyword in self.high_hype_keywords
        )

        # Count elite VC mentions
        elite_vc_count = sum(
            text_lower.count(firm)
            for firm in self.elite_firms
        )

        # Count conservative keywords
        conservative_count = sum(
            text_lower.count(keyword)
            for keyword in self.conservative_keywords
        )

        return HypeSignals(
            high_hype_count=high_hype_count,
            elite_vc_mentions=elite_vc_count,
            conservative_count=conservative_count,
            text_length=text_length
        )

    def score(self, text: str, normalize: bool = True) -> float:
        """
        Compute hype score for text.

        Score components:
        1. High-hype keyword density (positive)
        2. Elite VC mention density (positive)
        3. Conservative keyword density (negative)

        Args:
            text: Input text
            normalize: If True, return score in [0, 1]; else raw score

        Returns:
            Hype score (higher = more hype)
        """
        signals = self.extract_signals(text)

        # Weighted combination
        hype_component = signals.get_keyword_density() * 1.0
        elite_component = signals.get_elite_density() * 2.0  # Elite VCs weight more
        conservative_penalty = signals.get_conservative_density() * 0.5

        raw_score = hype_component + elite_component - conservative_penalty

        if normalize:
            # Normalize to [0, 1] using sigmoid-like function
            # Typical scores range 0-20; normalize to [0, 1]
            return self._sigmoid_normalize(raw_score, midpoint=10.0, steepness=0.2)
        else:
            return raw_score

    @staticmethod
    def _sigmoid_normalize(x: float, midpoint: float = 10.0, steepness: float = 0.2) -> float:
        """
        Normalize score to [0, 1] using sigmoid.

        Args:
            x: Raw score
            midpoint: Score value that maps to 0.5
            steepness: How steep the sigmoid is

        Returns:
            Normalized score in [0, 1]
        """
        import math
        return 1 / (1 + math.exp(-steepness * (x - midpoint)))

    def score_batch(self, texts: List[str], normalize: bool = True) -> List[float]:
        """
        Score multiple texts.

        Args:
            texts: List of input texts
            normalize: If True, return normalized scores

        Returns:
            List of hype scores
        """
        return [self.score(text, normalize=normalize) for text in texts]

    def get_top_keywords(self, text: str, top_k: int = 10) -> List[tuple]:
        """
        Get top-k most frequent high-hype keywords in text.

        Args:
            text: Input text
            top_k: Number of top keywords to return

        Returns:
            List of (keyword, count) tuples
        """
        text_lower = text.lower()
        keyword_counts = Counter()

        for keyword in self.high_hype_keywords:
            count = text_lower.count(keyword)
            if count > 0:
                keyword_counts[keyword] = count

        return keyword_counts.most_common(top_k)


class MediaCadenceAnalyzer:
    """Analyzes media mention frequency as hype signal."""

    @staticmethod
    def compute_weekly_cadence(article_dates: List[str]) -> float:
        """
        Compute articles per week from list of dates.

        Args:
            article_dates: List of ISO date strings (YYYY-MM-DD)

        Returns:
            Average articles per week
        """
        if len(article_dates) < 2:
            return 0.0

        from datetime import datetime

        dates = sorted([datetime.fromisoformat(d) for d in article_dates])
        days_span = (dates[-1] - dates[0]).days

        if days_span == 0:
            return len(article_dates)  # All on same day

        weeks_span = days_span / 7.0
        return len(article_dates) / weeks_span

    @staticmethod
    def detect_press_spike(article_dates: List[str], window_days: int = 7) -> bool:
        """
        Detect if there's a spike in press mentions.

        Spike defined as: ≥3 articles in a rolling 7-day window

        Args:
            article_dates: List of ISO date strings
            window_days: Rolling window size in days

        Returns:
            True if spike detected
        """
        if len(article_dates) < 3:
            return False

        from datetime import datetime, timedelta

        dates = sorted([datetime.fromisoformat(d) for d in article_dates])

        for i, start_date in enumerate(dates):
            end_date = start_date + timedelta(days=window_days)
            articles_in_window = sum(
                1 for d in dates[i:] if d <= end_date
            )
            if articles_in_window >= 3:
                return True

        return False


def example_usage():
    """Example usage of HypeScorer."""

    # Example press release texts
    high_hype_text = """
    We're thrilled to announce our revolutionary $100M Series B, led by Sequoia Capital
    and Andreessen Horowitz. This category-defining round was heavily oversubscribed,
    with participation from Tiger Global and other elite investors. Our paradigm-shift
    approach to AI is transforming the industry, and we're on track for hypergrowth
    with strong network effects creating a powerful moat.
    """

    low_hype_text = """
    We've raised a $5M Series A to continue building our profitable, sustainable business.
    The company has been capital-efficient from day one, with strong unit economics and
    positive cash flow. We're focused on organic growth and maintaining disciplined
    operations while serving our customers.
    """

    # Score texts
    scorer = HypeScorer()

    high_score = scorer.score(high_hype_text, normalize=True)
    low_score = scorer.score(low_hype_text, normalize=True)

    print("High-hype text score:", f"{high_score:.3f}")
    print("Low-hype text score:", f"{low_score:.3f}")

    # Extract signals
    high_signals = scorer.extract_signals(high_hype_text)
    print("\nHigh-hype signals:")
    print(f"  Hype keywords: {high_signals.high_hype_count}")
    print(f"  Elite VC mentions: {high_signals.elite_vc_mentions}")
    print(f"  Conservative keywords: {high_signals.conservative_count}")

    # Get top keywords
    top_keywords = scorer.get_top_keywords(high_hype_text)
    print("\nTop hype keywords:")
    for keyword, count in top_keywords:
        print(f"  - {keyword}: {count}")

    # Media cadence example
    article_dates = [
        "2024-01-15",
        "2024-01-16",
        "2024-01-17",
        "2024-01-22",
        "2024-02-10",
    ]

    analyzer = MediaCadenceAnalyzer()
    cadence = analyzer.compute_weekly_cadence(article_dates)
    spike = analyzer.detect_press_spike(article_dates)

    print(f"\nMedia cadence: {cadence:.2f} articles/week")
    print(f"Press spike detected: {spike}")


if __name__ == "__main__":
    example_usage()
