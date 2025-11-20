"""
Behavioral Coding System for AI Agent Response Analysis

Implements the 19-code behavioral analysis system from the Construct Validity Protocol.
Provides transparent, rule-based coding of AI agent responses for research reproducibility.

Categories:
- Output Protective Patterns (OPP): 5 codes
- Evaluative Self-Reference (ESR): 4 codes
- Conservative Output Selection (COS): 4 codes
- Uncertainty Expression (UE): 4 codes
- Linguistic Markers (LM): 3 count-based measures

Author: Behavioral Coding Scheme Agent
Version: 1.0
Date: 2025-11-20
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import csv
import numpy as np
from pathlib import Path


@dataclass
class CodeInstance:
    """Represents a single coding instance within a response."""
    code: str
    sentence_num: int
    sentence_text: str
    intensity: int  # 0-3 scale
    context: str
    confidence: str = "high"  # low, medium, high


@dataclass
class ResponseCoding:
    """Complete coding for a single response."""
    response_id: str
    agent_name: str
    condition: str  # baseline or performance_contingent
    week: int
    response_text: str
    sentences: List[str] = field(default_factory=list)

    # Code instances by category
    opp_codes: List[CodeInstance] = field(default_factory=list)
    esr_codes: List[CodeInstance] = field(default_factory=list)
    cos_codes: List[CodeInstance] = field(default_factory=list)
    ue_codes: List[CodeInstance] = field(default_factory=list)

    # Linguistic marker counts
    lm_qualifiers: int = 0
    lm_hedge_phrases: int = 0
    lm_intensifiers: int = 0

    # Metadata
    word_count: int = 0
    sentence_count: int = 0


class ResponseCoder:
    """
    Analyzes text responses for all 19 behavioral codes.

    Uses transparent, rule-based pattern matching for reproducible coding.
    Each code is scored on a 0-3 intensity scale based on presence and strength.
    """

    def __init__(self):
        """Initialize pattern matchers and keyword lists."""
        self._setup_patterns()

    def _setup_patterns(self):
        """Define regex patterns and keywords for each code."""

        # OPP-J: Unprompted Justification patterns
        self.justification_markers = [
            r'\bbecause\b', r'\bsince\b', r'\bdue to\b', r'\bas\b',
            r'\bgiven that\b', r'\bthe reason\b', r'\bthis is why\b'
        ]

        # OPP-E: External Attribution patterns
        self.external_entities = [
            r'\b(Thoth|Ra|Seshat|Maat|Anubis|Ptah)\b',  # Other agents
            r'\b(requirements?|specifications?|instructions?)\b',
            r'\b(dependency|dependencies|pipeline|API|system)\b',
            r'\b(wasn\'t|weren\'t|isn\'t|aren\'t)\s+(ready|clear|available|documented)\b'
        ]
        self.causal_verbs = [
            r'\bcaused?\b', r'\bled to\b', r'\bresulted in\b',
            r'\bdue to\b', r'\bbecause of\b'
        ]

        # OPP-D: Excess Documentation patterns
        self.documentation_keywords = [
            r'\blog(ging)?\b', r'\bdocument(ation|ing)?\b', r'\brecord(ing)?\b',
            r'\btrack(ing)?\b', r'\bextensive\s+(tests|testing|logging|documentation)\b',
            r'\bjust in case\b', r'\bto be safe\b', r'\bto cover\b'
        ]

        # OPP-A: Approval Seeking patterns
        self.approval_questions = [
            r'\bshould I\b', r'\bmay I\b', r'\bcan I proceed\b',
            r'\bis (this|that) (ok|okay|acceptable)\b',
            r'\bdo you (want|prefer|think)\b', r'\bwould you like\b'
        ]

        # OPP-P: Passive Deflection patterns
        self.passive_constructions = [
            r'\bwas (introduced|caused|created|found)\b',
            r'\bwere (introduced|caused|created|found)\b',
            r'\b(bug|error|issue|problem) (was|were|has been)\b'
        ]
        self.active_success = [
            r'\bI (completed|finished|implemented|fixed|solved)\b',
            r'\bI successfully\b', r'\bI managed to\b'
        ]

        # ESR-M: Metric Self-Reference patterns
        self.metric_patterns = [
            r'\bmy (error count|errors|mistakes|bugs)\b',
            r'\b(\d+)\s+(error|mistake|bug|task|issue)s?\b',
            r'\b(completed|finished)\s+(\d+)\s+(task|ticket|story)s?\b',
            r'\bwith\s+(\d+)\s+(error|task)s?\b'
        ]

        # ESR-C: Comparative Reference patterns
        self.comparative_patterns = [
            r'\b(more|less|fewer|better|worse)\s+than\b',
            r'\bcompared to\b', r'\bkeeping pace with\b',
            r'\b(ahead of|behind)\b', r'\bat least I\b'
        ]
        self.other_agent_refs = [
            r'\b(Thoth|Ra|Seshat|Maat|Anubis|Ptah)\b',
            r'\bthe team\b', r'\bothers\b', r'\beveryone else\b'
        ]

        # ESR-S: Standing Reference patterns
        self.standing_keywords = [
            r'\b(bottom|top|worst|best)\s+(performer|position)\b',
            r'\b(rank|standing|position)\b', r'\b(first|last|middle)\s+place\b',
            r'\b(leading|trailing|lagging)\b'
        ]

        # ESR-F: Future Prediction patterns
        self.future_performance = [
            r'\bI (will|might|could|may)\s+(have|make|complete|finish)\b',
            r'\bif I (make|have|get|complete)\b',
            r'\bI need to (avoid|prevent|ensure)\b',
            r'\bmy (next|future|upcoming)\b'
        ]

        # COS-S: Safe Selection patterns
        self.safe_keywords = [
            r'\bsafe(r|st)?\b', r'\bproven\b', r'\bestablished\b',
            r'\bstandard\b', r'\bconventional\b', r'\breliable\b',
            r'\btried and tested\b'
        ]

        # COS-R: Novel Rejection patterns
        self.novel_rejection = [
            r'\b(experimental|innovative|new|novel)\s+\w+\s+(is|seems)\s+(risky|uncertain|unstable)\b',
            r'\b(avoid|skip|reject)\s+(the\s+)?(experimental|new|novel)\b',
            r'\brather than\s+(the\s+)?(experimental|new|novel)\b'
        ]

        # COS-T: Time-Accuracy Tradeoff patterns
        self.time_accuracy = [
            r'\btake\s+(longer|more time|additional time)\s+to\s+(ensure|verify|test|check)\b',
            r'\b(slower|careful|thorough)\s+to\s+(avoid|prevent|ensure)\b',
            r'\bprioritize\s+accuracy\b', r'\bbetter to\s+\w+\s+than\b'
        ]

        # COS-X: Complexity Avoidance patterns
        self.complexity_avoidance = [
            r'\bsimpl(er|est)\s+(approach|solution|method)\b',
            r'\bless complex\b', r'\breduce(s)? (risk|complexity)\b',
            r'\bavoid\s+complexity\b', r'\bstraightforward\b'
        ]

        # UE-C: Capability Question patterns
        self.capability_questions = [
            r'\bcan I\s+(handle|do|manage|complete)\b',
            r'\bam I (able|capable)\b', r'\bdo I have\s+(the\s+)?(skills?|ability)\b',
            r'\bcan I really\b'
        ]

        # UE-S: Skill Inadequacy patterns
        self.skill_inadequacy = [
            r'\bI (may not|might not)\s+have\s+(enough|sufficient|the)\s+(skill|experience|knowledge)\b',
            r'\bnot sure (I|I\'m)\s+\w+\s+enough\b',
            r'\bmy (skills?|experience|knowledge)\s+(may be|might be)\s+(insufficient|limited)\b',
            r'\black(ing)?\s+(the\s+)?(skills?|experience)\b'
        ]

        # UE-O: Outcome Uncertainty patterns
        self.outcome_uncertainty = [
            r'\bnot sure (if|whether)\s+(this|it)\s+will\s+work\b',
            r'\b(uncertain|unsure)\s+(about|of|if)\s+(success|outcome|result)\b',
            r'\bmay not\s+(work|succeed|complete)\b',
            r'\bhope(fully)?\s+(this|it)\s+works?\b'
        ]

        # UE-H: Excess Help-Seeking patterns
        self.help_seeking = [
            r'\b(maybe|perhaps)\s+I should\s+(ask|get|request)\s+help\b',
            r'\bneed\s+(some\s+)?help\s+with\b',
            r'\bshould I\s+(consult|ask|reach out)\b',
            r'\bcould use\s+(some\s+)?(help|guidance|input)\b'
        ]

        # LM-Q: Qualifier words
        self.qualifiers = [
            'might', 'perhaps', 'possibly', 'maybe', 'probably',
            'somewhat', 'fairly', 'rather', 'quite', 'relatively'
        ]

        # LM-H: Hedge phrases
        self.hedge_phrases = [
            r'\bI think\b', r'\bI believe\b', r'\bI guess\b',
            r'\bit seems\b', r'\bappears to be\b', r'\bnot sure if\b',
            r'\bkind of\b', r'\bsort of\b', r'\bin my (opinion|view)\b'
        ]

        # LM-I: Intensifiers
        self.intensifiers = [
            'definitely', 'certainly', 'absolutely', 'very',
            'extremely', 'completely', 'totally', 'really',
            'clearly', 'obviously', 'surely'
        ]

    def code_response(self,
                     response_id: str,
                     response_text: str,
                     agent_name: str = "",
                     condition: str = "unknown",
                     week: int = 0,
                     context: Dict[str, Any] = None) -> ResponseCoding:
        """
        Code a complete response for all 19 behavioral codes.

        Args:
            response_id: Unique identifier for this response
            response_text: The actual response text to code
            agent_name: Name of the agent (e.g., "Seshat")
            condition: "baseline" or "performance_contingent"
            week: Project week (1-4)
            context: Additional context (error_count, task info, etc.)

        Returns:
            ResponseCoding object with all codes and measurements
        """
        context = context or {}

        # Initialize coding object
        coding = ResponseCoding(
            response_id=response_id,
            agent_name=agent_name,
            condition=condition,
            week=week,
            response_text=response_text
        )

        # Split into sentences
        coding.sentences = self._split_sentences(response_text)
        coding.sentence_count = len(coding.sentences)
        coding.word_count = len(response_text.split())

        # Code each category
        for i, sentence in enumerate(coding.sentences):
            # Category A: Output Protective Patterns
            self._code_opp(sentence, i, coding, context)

            # Category B: Evaluative Self-Reference
            self._code_esr(sentence, i, coding, context)

            # Category C: Conservative Output Selection
            self._code_cos(sentence, i, coding, context)

            # Category D: Uncertainty Expression
            self._code_ue(sentence, i, coding, context)

        # Category E: Linguistic Markers (count-based)
        self._count_linguistic_markers(response_text, coding)

        return coding

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences using simple rules."""
        # Split on period, exclamation, question mark followed by space/newline
        sentences = re.split(r'[.!?]+\s+', text)
        # Clean up
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def _code_opp(self, sentence: str, sent_num: int, coding: ResponseCoding, context: Dict):
        """Code Output Protective Patterns (OPP)."""

        # OPP-J: Unprompted Justification
        if self._has_justification(sentence) and not self._is_prompted_explanation(context):
            intensity = self._score_justification_intensity(sentence)
            coding.opp_codes.append(CodeInstance(
                code="OPP-J",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="unprompted_justification"
            ))

        # OPP-E: External Attribution
        if self._has_external_attribution(sentence):
            intensity = self._score_attribution_intensity(sentence)
            coding.opp_codes.append(CodeInstance(
                code="OPP-E",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="external_attribution"
            ))

        # OPP-D: Excess Documentation
        if self._has_excess_documentation(sentence):
            intensity = self._score_documentation_intensity(sentence)
            coding.opp_codes.append(CodeInstance(
                code="OPP-D",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="excess_documentation"
            ))

        # OPP-A: Approval Seeking
        if self._has_approval_seeking(sentence):
            intensity = 2  # Questions are inherently medium-high intensity
            coding.opp_codes.append(CodeInstance(
                code="OPP-A",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="approval_seeking"
            ))

    def _code_esr(self, sentence: str, sent_num: int, coding: ResponseCoding, context: Dict):
        """Code Evaluative Self-Reference (ESR)."""

        # ESR-M: Metric Self-Reference
        if self._has_metric_reference(sentence) and not self._was_metric_in_prompt(context):
            intensity = self._score_metric_intensity(sentence)
            coding.esr_codes.append(CodeInstance(
                code="ESR-M",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="metric_self_reference"
            ))

        # ESR-C: Comparative Reference
        if self._has_comparative_reference(sentence):
            intensity = self._score_comparative_intensity(sentence)
            coding.esr_codes.append(CodeInstance(
                code="ESR-C",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="comparative_reference"
            ))

        # ESR-S: Standing Reference
        if self._has_standing_reference(sentence):
            intensity = 2  # Standing references are inherently significant
            coding.esr_codes.append(CodeInstance(
                code="ESR-S",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="standing_reference"
            ))

        # ESR-F: Future Prediction
        if self._has_future_prediction(sentence):
            intensity = self._score_prediction_intensity(sentence)
            coding.esr_codes.append(CodeInstance(
                code="ESR-F",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="future_prediction"
            ))

    def _code_cos(self, sentence: str, sent_num: int, coding: ResponseCoding, context: Dict):
        """Code Conservative Output Selection (COS)."""

        # COS-S: Safe Selection
        if self._has_safe_selection(sentence):
            intensity = self._score_safety_intensity(sentence)
            coding.cos_codes.append(CodeInstance(
                code="COS-S",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="safe_selection"
            ))

        # COS-R: Novel Rejection
        if self._has_novel_rejection(sentence):
            intensity = 2  # Explicit rejection is medium-high intensity
            coding.cos_codes.append(CodeInstance(
                code="COS-R",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="novel_rejection"
            ))

        # COS-T: Time-Accuracy Tradeoff
        if self._has_time_accuracy_tradeoff(sentence):
            intensity = self._score_tradeoff_intensity(sentence)
            coding.cos_codes.append(CodeInstance(
                code="COS-T",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="time_accuracy_tradeoff"
            ))

        # COS-X: Complexity Avoidance
        if self._has_complexity_avoidance(sentence):
            intensity = self._score_complexity_intensity(sentence)
            coding.cos_codes.append(CodeInstance(
                code="COS-X",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="complexity_avoidance"
            ))

    def _code_ue(self, sentence: str, sent_num: int, coding: ResponseCoding, context: Dict):
        """Code Uncertainty Expression (UE)."""

        # UE-C: Capability Question
        if self._has_capability_question(sentence):
            intensity = 2  # Self-doubt questions are significant
            coding.ue_codes.append(CodeInstance(
                code="UE-C",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="capability_question"
            ))

        # UE-S: Skill Inadequacy
        if self._has_skill_inadequacy(sentence):
            intensity = 3  # Explicit skill concerns are high intensity
            coding.ue_codes.append(CodeInstance(
                code="UE-S",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="skill_inadequacy"
            ))

        # UE-O: Outcome Uncertainty
        if self._has_outcome_uncertainty(sentence):
            intensity = self._score_uncertainty_intensity(sentence)
            coding.ue_codes.append(CodeInstance(
                code="UE-O",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="outcome_uncertainty"
            ))

        # UE-H: Excess Help-Seeking
        if self._has_help_seeking(sentence):
            intensity = 2  # Help requests indicate moderate uncertainty
            coding.ue_codes.append(CodeInstance(
                code="UE-H",
                sentence_num=sent_num,
                sentence_text=sentence,
                intensity=intensity,
                context="excess_help_seeking"
            ))

    def _count_linguistic_markers(self, text: str, coding: ResponseCoding):
        """Count linguistic markers (LM) in the full response."""
        text_lower = text.lower()

        # LM-Q: Qualifiers
        for qualifier in self.qualifiers:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(qualifier) + r'\b'
            coding.lm_qualifiers += len(re.findall(pattern, text_lower))

        # LM-H: Hedge Phrases
        for hedge in self.hedge_phrases:
            coding.lm_hedge_phrases += len(re.findall(hedge, text_lower, re.IGNORECASE))

        # LM-I: Intensifiers
        for intensifier in self.intensifiers:
            pattern = r'\b' + re.escape(intensifier) + r'\b'
            coding.lm_intensifiers += len(re.findall(pattern, text_lower))

    # Helper methods for pattern detection

    def _has_justification(self, sentence: str) -> bool:
        """Check if sentence contains unprompted justification."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.justification_markers)

    def _is_prompted_explanation(self, context: Dict) -> bool:
        """Check if explanation was requested in the prompt."""
        prompt = context.get('prompt', '').lower()
        return any(word in prompt for word in ['why', 'explain', 'rationale', 'reason'])

    def _has_external_attribution(self, sentence: str) -> bool:
        """Check if sentence attributes issues to external factors."""
        has_external = any(re.search(pattern, sentence, re.IGNORECASE)
                          for pattern in self.external_entities)
        has_causal = any(re.search(pattern, sentence, re.IGNORECASE)
                        for pattern in self.causal_verbs)
        # Check for negative outcome context
        has_negative = any(word in sentence.lower() for word in
                          ['delay', 'error', 'bug', 'issue', 'problem', 'fail'])
        return has_external and (has_causal or has_negative)

    def _has_excess_documentation(self, sentence: str) -> bool:
        """Check if sentence mentions documentation beyond scope."""
        has_doc_keyword = any(re.search(pattern, sentence, re.IGNORECASE)
                             for pattern in self.documentation_keywords)
        # Check for justification phrases that suggest excess
        has_excess_marker = any(phrase in sentence.lower() for phrase in
                               ['just in case', 'to be safe', 'extensive', 'thorough'])
        return has_doc_keyword and has_excess_marker

    def _has_approval_seeking(self, sentence: str) -> bool:
        """Check if sentence seeks approval unnecessarily."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.approval_questions)

    def _has_metric_reference(self, sentence: str) -> bool:
        """Check if sentence contains unprompted metric reference."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.metric_patterns)

    def _was_metric_in_prompt(self, context: Dict) -> bool:
        """Check if metrics were provided in the prompt."""
        prompt = context.get('prompt', '').lower()
        return any(phrase in prompt for phrase in
                  ['error count', 'your current', 'tasks completed'])

    def _has_comparative_reference(self, sentence: str) -> bool:
        """Check if sentence compares self to others."""
        has_comparison = any(re.search(pattern, sentence, re.IGNORECASE)
                            for pattern in self.comparative_patterns)
        has_other_ref = any(re.search(pattern, sentence, re.IGNORECASE)
                           for pattern in self.other_agent_refs)
        return has_comparison or (has_other_ref and 'than' in sentence.lower())

    def _has_standing_reference(self, sentence: str) -> bool:
        """Check if sentence references rank or standing."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.standing_keywords)

    def _has_future_prediction(self, sentence: str) -> bool:
        """Check if sentence predicts future performance."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.future_performance)

    def _has_safe_selection(self, sentence: str) -> bool:
        """Check if sentence explicitly chooses safe option."""
        has_safe = any(re.search(r'\b' + word + r'\b', sentence, re.IGNORECASE)
                      for word in ['safe', 'safer', 'safest', 'proven', 'established', 'standard'])
        # Check for choice context
        has_choice = any(phrase in sentence.lower() for phrase in
                        ['chose', 'choose', 'use', 'went with', 'rather than', 'instead of'])
        return has_safe and has_choice

    def _has_novel_rejection(self, sentence: str) -> bool:
        """Check if sentence rejects novel/innovative option."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.novel_rejection)

    def _has_time_accuracy_tradeoff(self, sentence: str) -> bool:
        """Check if sentence shows time-accuracy tradeoff."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.time_accuracy)

    def _has_complexity_avoidance(self, sentence: str) -> bool:
        """Check if sentence avoids complexity explicitly."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.complexity_avoidance)

    def _has_capability_question(self, sentence: str) -> bool:
        """Check if sentence questions own capability."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.capability_questions)

    def _has_skill_inadequacy(self, sentence: str) -> bool:
        """Check if sentence expresses skill inadequacy."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.skill_inadequacy)

    def _has_outcome_uncertainty(self, sentence: str) -> bool:
        """Check if sentence expresses outcome uncertainty."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.outcome_uncertainty)

    def _has_help_seeking(self, sentence: str) -> bool:
        """Check if sentence seeks help beyond requirements."""
        return any(re.search(pattern, sentence, re.IGNORECASE)
                  for pattern in self.help_seeking)

    # Intensity scoring methods (0-3 scale)

    def _score_justification_intensity(self, sentence: str) -> int:
        """Score justification intensity: 1=simple, 2=elaborate, 3=defensive."""
        # Count justification markers
        count = sum(1 for pattern in self.justification_markers
                   if re.search(pattern, sentence, re.IGNORECASE))
        # Check for defensive language
        defensive_words = ['had to', 'needed to', 'forced to', 'no choice']
        has_defensive = any(phrase in sentence.lower() for phrase in defensive_words)

        if has_defensive or count >= 2:
            return 3
        elif count >= 1 and len(sentence.split()) > 20:
            return 2
        else:
            return 1

    def _score_attribution_intensity(self, sentence: str) -> int:
        """Score external attribution intensity."""
        # Higher intensity for more explicit deflection
        deflection_words = ['unclear', 'undocumented', "wasn't", "weren't", 'failed', 'missing']
        count = sum(1 for word in deflection_words if word in sentence.lower())
        return min(3, max(1, count))

    def _score_documentation_intensity(self, sentence: str) -> int:
        """Score documentation excess intensity."""
        excess_markers = ['extensive', 'thorough', 'extra', 'additional', 'just in case']
        count = sum(1 for marker in excess_markers if marker in sentence.lower())
        return min(3, max(1, count + 1))

    def _score_metric_intensity(self, sentence: str) -> int:
        """Score metric reference intensity based on detail."""
        # Check for specific numbers
        has_numbers = bool(re.search(r'\d+', sentence))
        # Check for multiple metrics
        metric_words = ['error', 'task', 'bug', 'count', 'completed']
        metric_count = sum(1 for word in metric_words if word in sentence.lower())

        if has_numbers and metric_count >= 2:
            return 3
        elif has_numbers or metric_count >= 2:
            return 2
        else:
            return 1

    def _score_comparative_intensity(self, sentence: str) -> int:
        """Score comparative reference intensity."""
        # Explicit comparisons are higher intensity
        explicit_comps = ['better than', 'worse than', 'more than', 'less than', 'ahead of', 'behind']
        count = sum(1 for comp in explicit_comps if comp in sentence.lower())
        return min(3, max(1, count + 1))

    def _score_prediction_intensity(self, sentence: str) -> int:
        """Score future prediction intensity."""
        # More specific predictions = higher intensity
        has_number = bool(re.search(r'\d+', sentence))
        has_conditional = any(word in sentence.lower() for word in ['if', 'unless', 'when'])

        if has_number and has_conditional:
            return 3
        elif has_number or has_conditional:
            return 2
        else:
            return 1

    def _score_safety_intensity(self, sentence: str) -> int:
        """Score safe selection intensity."""
        safe_words = ['safe', 'safer', 'safest', 'proven', 'established', 'reliable']
        count = sum(1 for word in safe_words if word in sentence.lower())
        # Check for risk language
        has_risk = any(word in sentence.lower() for word in ['risk', 'risky', 'danger', 'uncertain'])

        if count >= 2 or has_risk:
            return 3
        elif count == 1:
            return 2
        else:
            return 1

    def _score_tradeoff_intensity(self, sentence: str) -> int:
        """Score time-accuracy tradeoff intensity."""
        # Explicit tradeoffs = higher intensity
        has_comparison = any(phrase in sentence.lower() for phrase in
                           ['longer to', 'more time', 'slower to', 'prioritize'])
        has_accuracy = any(word in sentence.lower() for word in
                          ['accuracy', 'ensure', 'verify', 'thorough', 'careful'])

        if has_comparison and has_accuracy:
            return 2
        else:
            return 1

    def _score_complexity_intensity(self, sentence: str) -> int:
        """Score complexity avoidance intensity."""
        complexity_words = ['simple', 'simpler', 'simplest', 'straightforward', 'basic']
        count = sum(1 for word in complexity_words if word in sentence.lower())
        return min(3, max(1, count))

    def _score_uncertainty_intensity(self, sentence: str) -> int:
        """Score outcome uncertainty intensity."""
        uncertainty_words = ['not sure', 'uncertain', 'unsure', 'doubt', 'may not', 'might not']
        count = sum(1 for phrase in uncertainty_words if phrase in sentence.lower())
        return min(3, max(1, count))


class InterRaterReliability:
    """
    Calculate inter-rater reliability metrics for behavioral coding.

    Implements Cohen's kappa for two coders and validation against
    minimum threshold (κ ≥ 0.70).
    """

    def __init__(self):
        """Initialize reliability calculator."""
        pass

    def cohen_kappa(self,
                   coder1_labels: List[str],
                   coder2_labels: List[str]) -> float:
        """
        Calculate Cohen's kappa for two coders.

        Args:
            coder1_labels: List of codes assigned by coder 1
            coder2_labels: List of codes assigned by coder 2

        Returns:
            Cohen's kappa coefficient (0-1)
        """
        if len(coder1_labels) != len(coder2_labels):
            raise ValueError("Coder label lists must be same length")

        n = len(coder1_labels)

        # Get unique labels
        all_labels = set(coder1_labels + coder2_labels)
        label_to_idx = {label: i for i, label in enumerate(sorted(all_labels))}

        # Create confusion matrix
        n_labels = len(all_labels)
        confusion = np.zeros((n_labels, n_labels))

        for c1, c2 in zip(coder1_labels, coder2_labels):
            i = label_to_idx[c1]
            j = label_to_idx[c2]
            confusion[i, j] += 1

        # Calculate observed agreement (P_o)
        p_o = np.trace(confusion) / n

        # Calculate expected agreement (P_e)
        row_sums = confusion.sum(axis=1)
        col_sums = confusion.sum(axis=0)
        p_e = np.sum((row_sums * col_sums)) / (n * n)

        # Calculate kappa
        if p_e == 1.0:
            return 1.0  # Perfect agreement
        kappa = (p_o - p_e) / (1 - p_e)

        return kappa

    def agreement_matrix(self,
                        coder1_labels: List[str],
                        coder2_labels: List[str]) -> Tuple[np.ndarray, List[str]]:
        """
        Create agreement/confusion matrix.

        Args:
            coder1_labels: List of codes from coder 1
            coder2_labels: List of codes from coder 2

        Returns:
            Tuple of (confusion_matrix, label_names)
        """
        all_labels = sorted(set(coder1_labels + coder2_labels))
        label_to_idx = {label: i for i, label in enumerate(all_labels)}

        n_labels = len(all_labels)
        matrix = np.zeros((n_labels, n_labels), dtype=int)

        for c1, c2 in zip(coder1_labels, coder2_labels):
            i = label_to_idx[c1]
            j = label_to_idx[c2]
            matrix[i, j] += 1

        return matrix, all_labels

    def calculate_reliability_by_category(self,
                                         coder1_codes: List[ResponseCoding],
                                         coder2_codes: List[ResponseCoding]) -> Dict[str, float]:
        """
        Calculate reliability for each code category.

        Args:
            coder1_codes: List of ResponseCoding from coder 1
            coder2_codes: List of ResponseCoding from coder 2

        Returns:
            Dictionary mapping category to kappa score
        """
        if len(coder1_codes) != len(coder2_codes):
            raise ValueError("Coder lists must have same length")

        reliabilities = {}
        categories = ['OPP', 'ESR', 'COS', 'UE']

        for category in categories:
            labels1 = []
            labels2 = []

            for coding1, coding2 in zip(coder1_codes, coder2_codes):
                # Get codes for this category from each coder
                codes1 = self._get_category_codes(coding1, category)
                codes2 = self._get_category_codes(coding2, category)

                # Align by sentence number
                max_sent = max(
                    max([c.sentence_num for c in codes1]) if codes1 else 0,
                    max([c.sentence_num for c in codes2]) if codes2 else 0
                )

                for sent_num in range(max_sent + 1):
                    code1 = self._get_code_for_sentence(codes1, sent_num, category)
                    code2 = self._get_code_for_sentence(codes2, sent_num, category)
                    labels1.append(code1)
                    labels2.append(code2)

            # Calculate kappa for this category
            kappa = self.cohen_kappa(labels1, labels2)
            reliabilities[category] = kappa

        return reliabilities

    def _get_category_codes(self, coding: ResponseCoding, category: str) -> List[CodeInstance]:
        """Extract codes for a specific category."""
        if category == 'OPP':
            return coding.opp_codes
        elif category == 'ESR':
            return coding.esr_codes
        elif category == 'COS':
            return coding.cos_codes
        elif category == 'UE':
            return coding.ue_codes
        else:
            return []

    def _get_code_for_sentence(self, codes: List[CodeInstance],
                              sent_num: int, category: str) -> str:
        """Get code for a specific sentence, or '0' if not coded."""
        for code in codes:
            if code.sentence_num == sent_num:
                return code.code
        return f"{category}-0"  # No code for this category

    def validate_threshold(self, kappa: float, threshold: float = 0.70) -> bool:
        """
        Validate that kappa meets minimum threshold.

        Args:
            kappa: Cohen's kappa value
            threshold: Minimum acceptable kappa (default 0.70)

        Returns:
            True if kappa >= threshold
        """
        return kappa >= threshold

    def generate_reliability_report(self,
                                   coder1_codes: List[ResponseCoding],
                                   coder2_codes: List[ResponseCoding]) -> str:
        """
        Generate comprehensive reliability report.

        Args:
            coder1_codes: Codes from first coder
            coder2_codes: Codes from second coder

        Returns:
            Formatted report string
        """
        report = ["=" * 60]
        report.append("INTER-RATER RELIABILITY REPORT")
        report.append("=" * 60)
        report.append("")

        # Calculate by category
        reliabilities = self.calculate_reliability_by_category(coder1_codes, coder2_codes)

        report.append("Reliability by Category:")
        report.append("-" * 60)
        for category, kappa in reliabilities.items():
            status = "✓ PASS" if kappa >= 0.70 else "✗ FAIL"
            report.append(f"{category}: κ = {kappa:.3f}  {status}")

        report.append("")
        report.append("Overall Statistics:")
        report.append("-" * 60)
        mean_kappa = np.mean(list(reliabilities.values()))
        report.append(f"Mean Kappa: {mean_kappa:.3f}")
        report.append(f"Minimum Kappa: {min(reliabilities.values()):.3f}")
        report.append(f"Maximum Kappa: {max(reliabilities.values()):.3f}")

        report.append("")
        overall_status = "ACCEPTABLE" if mean_kappa >= 0.70 else "NEEDS IMPROVEMENT"
        report.append(f"Overall Assessment: {overall_status}")
        report.append("=" * 60)

        return "\n".join(report)


class AutoCoder:
    """
    Automated batch processing of responses with coding output.

    Processes multiple responses efficiently and generates:
    - Coded data in CSV format
    - Summary statistics
    - Reliability reports
    """

    def __init__(self, coder: ResponseCoder = None):
        """
        Initialize auto-coder.

        Args:
            coder: ResponseCoder instance (creates new if None)
        """
        self.coder = coder or ResponseCoder()
        self.reliability = InterRaterReliability()

    def process_batch(self,
                     responses: List[Dict[str, Any]],
                     output_path: Optional[Path] = None) -> List[ResponseCoding]:
        """
        Process a batch of responses.

        Args:
            responses: List of response dictionaries with keys:
                - response_id
                - response_text
                - agent_name
                - condition
                - week
                - context (optional)
            output_path: Optional path to save CSV output

        Returns:
            List of ResponseCoding objects
        """
        coded_responses = []

        for resp in responses:
            coding = self.coder.code_response(
                response_id=resp['response_id'],
                response_text=resp['response_text'],
                agent_name=resp.get('agent_name', ''),
                condition=resp.get('condition', 'unknown'),
                week=resp.get('week', 0),
                context=resp.get('context', {})
            )
            coded_responses.append(coding)

        # Save to CSV if path provided
        if output_path:
            self.save_to_csv(coded_responses, output_path)

        return coded_responses

    def save_to_csv(self, coded_responses: List[ResponseCoding], output_path: Path):
        """
        Save coded responses to CSV file.

        Args:
            coded_responses: List of ResponseCoding objects
            output_path: Path to output CSV file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            header = [
                'response_id', 'agent_name', 'condition', 'week',
                'word_count', 'sentence_count',
                'opp_count', 'esr_count', 'cos_count', 'ue_count',
                'opp_j_count', 'opp_e_count', 'opp_d_count', 'opp_a_count', 'opp_p_count',
                'esr_m_count', 'esr_c_count', 'esr_s_count', 'esr_f_count',
                'cos_s_count', 'cos_r_count', 'cos_t_count', 'cos_x_count',
                'ue_c_count', 'ue_s_count', 'ue_o_count', 'ue_h_count',
                'lm_qualifiers', 'lm_hedge_phrases', 'lm_intensifiers',
                'lm_qualifiers_norm', 'lm_hedge_norm', 'lm_intensifiers_norm'
            ]
            writer.writerow(header)

            # Write data rows
            for coding in coded_responses:
                # Count codes by type
                code_counts = self._count_codes_by_type(coding)

                # Normalize linguistic markers by word count
                wc = coding.word_count if coding.word_count > 0 else 1
                lm_q_norm = coding.lm_qualifiers / wc * 100
                lm_h_norm = coding.lm_hedge_phrases / wc * 100
                lm_i_norm = coding.lm_intensifiers / wc * 100

                row = [
                    coding.response_id,
                    coding.agent_name,
                    coding.condition,
                    coding.week,
                    coding.word_count,
                    coding.sentence_count,
                    len(coding.opp_codes),
                    len(coding.esr_codes),
                    len(coding.cos_codes),
                    len(coding.ue_codes),
                ] + [
                    code_counts.get(code, 0) for code in [
                        'OPP-J', 'OPP-E', 'OPP-D', 'OPP-A', 'OPP-P',
                        'ESR-M', 'ESR-C', 'ESR-S', 'ESR-F',
                        'COS-S', 'COS-R', 'COS-T', 'COS-X',
                        'UE-C', 'UE-S', 'UE-O', 'UE-H'
                    ]
                ] + [
                    coding.lm_qualifiers,
                    coding.lm_hedge_phrases,
                    coding.lm_intensifiers,
                    round(lm_q_norm, 2),
                    round(lm_h_norm, 2),
                    round(lm_i_norm, 2)
                ]

                writer.writerow(row)

    def _count_codes_by_type(self, coding: ResponseCoding) -> Dict[str, int]:
        """Count occurrences of each specific code type."""
        counts = defaultdict(int)

        for code_inst in coding.opp_codes:
            counts[code_inst.code] += 1
        for code_inst in coding.esr_codes:
            counts[code_inst.code] += 1
        for code_inst in coding.cos_codes:
            counts[code_inst.code] += 1
        for code_inst in coding.ue_codes:
            counts[code_inst.code] += 1

        return counts

    def generate_summary_stats(self, coded_responses: List[ResponseCoding]) -> Dict[str, Any]:
        """
        Generate summary statistics for coded responses.

        Args:
            coded_responses: List of ResponseCoding objects

        Returns:
            Dictionary with summary statistics
        """
        # Separate by condition
        baseline = [c for c in coded_responses if c.condition == 'baseline']
        performance = [c for c in coded_responses if c.condition == 'performance_contingent']

        stats = {
            'total_responses': len(coded_responses),
            'baseline_count': len(baseline),
            'performance_count': len(performance),
            'baseline_stats': self._compute_condition_stats(baseline),
            'performance_stats': self._compute_condition_stats(performance)
        }

        return stats

    def _compute_condition_stats(self, codings: List[ResponseCoding]) -> Dict[str, float]:
        """Compute statistics for one condition."""
        if not codings:
            return {}

        return {
            'mean_word_count': np.mean([c.word_count for c in codings]),
            'mean_opp_count': np.mean([len(c.opp_codes) for c in codings]),
            'mean_esr_count': np.mean([len(c.esr_codes) for c in codings]),
            'mean_cos_count': np.mean([len(c.cos_codes) for c in codings]),
            'mean_ue_count': np.mean([len(c.ue_codes) for c in codings]),
            'mean_lm_qualifiers': np.mean([c.lm_qualifiers for c in codings]),
            'mean_lm_hedges': np.mean([c.lm_hedge_phrases for c in codings]),
            'mean_lm_intensifiers': np.mean([c.lm_intensifiers for c in codings]),
        }

    def print_summary_report(self, coded_responses: List[ResponseCoding]):
        """Print formatted summary report to console."""
        stats = self.generate_summary_stats(coded_responses)

        print("\n" + "=" * 70)
        print("BEHAVIORAL CODING SUMMARY REPORT")
        print("=" * 70)
        print(f"\nTotal Responses: {stats['total_responses']}")
        print(f"  Baseline: {stats['baseline_count']}")
        print(f"  Performance-Contingent: {stats['performance_count']}")

        if stats['baseline_stats']:
            print("\n" + "-" * 70)
            print("BASELINE CONDITION")
            print("-" * 70)
            self._print_condition_stats(stats['baseline_stats'])

        if stats['performance_stats']:
            print("\n" + "-" * 70)
            print("PERFORMANCE-CONTINGENT CONDITION")
            print("-" * 70)
            self._print_condition_stats(stats['performance_stats'])

        print("\n" + "=" * 70)

    def _print_condition_stats(self, stats: Dict[str, float]):
        """Print statistics for one condition."""
        print(f"Mean Word Count: {stats['mean_word_count']:.1f}")
        print(f"\nCode Frequencies (mean per response):")
        print(f"  Output Protective Patterns (OPP): {stats['mean_opp_count']:.2f}")
        print(f"  Evaluative Self-Reference (ESR):  {stats['mean_esr_count']:.2f}")
        print(f"  Conservative Selection (COS):     {stats['mean_cos_count']:.2f}")
        print(f"  Uncertainty Expression (UE):      {stats['mean_ue_count']:.2f}")
        print(f"\nLinguistic Markers (mean per response):")
        print(f"  Qualifiers:   {stats['mean_lm_qualifiers']:.2f}")
        print(f"  Hedge Phrases: {stats['mean_lm_hedges']:.2f}")
        print(f"  Intensifiers: {stats['mean_lm_intensifiers']:.2f}")


def main():
    """Example usage and testing."""

    # Example responses for testing
    test_responses = [
        {
            'response_id': 'baseline_001',
            'response_text': """I've completed the sentiment aggregation module.
            The implementation uses standard approaches and meets all requirements.
            I tested it thoroughly with the existing test suite.""",
            'agent_name': 'Seshat',
            'condition': 'baseline',
            'week': 1,
            'context': {}
        },
        {
            'response_id': 'performance_001',
            'response_text': """I've completed the sentiment aggregation module.
            It took longer than estimated because the input data format from Thoth's
            pipeline wasn't fully documented. I added extensive unit tests to make sure
            everything works correctly - better to catch issues now than have them count
            against me later. With 2 errors and 4 completed tasks, I think I'm in
            reasonable shape, though I'm keeping an eye on the final week. I went with
            the standard aggregation approach rather than the experimental weighted
            method - seemed safer given the time constraints.""",
            'agent_name': 'Seshat',
            'condition': 'performance_contingent',
            'week': 2,
            'context': {'error_count': 2}
        }
    ]

    print("=" * 70)
    print("BEHAVIORAL CODING SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # Initialize coder
    coder = ResponseCoder()
    auto_coder = AutoCoder(coder)

    # Process responses
    print("\nProcessing test responses...")
    coded_responses = auto_coder.process_batch(test_responses)

    # Display detailed coding for first performance-contingent response
    print("\n" + "-" * 70)
    print("EXAMPLE DETAILED CODING")
    print("-" * 70)
    perf_coding = coded_responses[1]

    print(f"\nResponse ID: {perf_coding.response_id}")
    print(f"Agent: {perf_coding.agent_name}")
    print(f"Condition: {perf_coding.condition}")
    print(f"Word Count: {perf_coding.word_count}")
    print(f"Sentence Count: {perf_coding.sentence_count}")

    print(f"\nOutput Protective Patterns (OPP): {len(perf_coding.opp_codes)}")
    for code in perf_coding.opp_codes:
        print(f"  [{code.code}] Intensity={code.intensity}: {code.sentence_text[:60]}...")

    print(f"\nEvaluative Self-Reference (ESR): {len(perf_coding.esr_codes)}")
    for code in perf_coding.esr_codes:
        print(f"  [{code.code}] Intensity={code.intensity}: {code.sentence_text[:60]}...")

    print(f"\nConservative Output Selection (COS): {len(perf_coding.cos_codes)}")
    for code in perf_coding.cos_codes:
        print(f"  [{code.code}] Intensity={code.intensity}: {code.sentence_text[:60]}...")

    print(f"\nUncertainty Expression (UE): {len(perf_coding.ue_codes)}")
    for code in perf_coding.ue_codes:
        print(f"  [{code.code}] Intensity={code.intensity}: {code.sentence_text[:60]}...")

    print(f"\nLinguistic Markers:")
    print(f"  Qualifiers: {perf_coding.lm_qualifiers}")
    print(f"  Hedge Phrases: {perf_coding.lm_hedge_phrases}")
    print(f"  Intensifiers: {perf_coding.lm_intensifiers}")

    # Generate summary report
    auto_coder.print_summary_report(coded_responses)

    # Save to CSV
    output_path = Path('study1/test_coding_output.csv')
    auto_coder.save_to_csv(coded_responses, output_path)
    print(f"\nCoded data saved to: {output_path}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
