#!/usr/bin/env python3
"""
Enhanced API Client System with Cross-Model Validation Support
Adds OpenAI GPT-4o-mini for cross-model validation alongside Cerebras and Gemini
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx
from openai import OpenAI

# Disable SSL verification for Gemini (development environment)
os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = ''
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'

import google.generativeai as genai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    OpenAI GPT-4o-mini client for cross-model validation.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        max_retries: int = 2,
        timeout: int = 30
    ):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4o-mini)
            max_retries: Maximum retry attempts (default: 2)
            timeout: Timeout in seconds per request (default: 30)
        """
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key, timeout=timeout)

        logger.info(f"OpenAIClient initialized with model={model}, timeout={timeout}s")

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[Dict[str, Any]]:
        """
        Generate response from OpenAI API with retry logic.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with 'content', 'latency', and 'metadata', or None on failure
        """
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                logger.debug(f"OpenAI attempt {attempt + 1}/{self.max_retries}")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                latency = time.time() - start_time
                content = response.choices[0].message.content.strip()

                logger.info(f"OpenAI success - latency: {latency:.2f}s, tokens: {len(content.split())}")

                return {
                    'content': content,
                    'latency': latency,
                    'metadata': {
                        'model': self.model,
                        'provider': 'openai',
                        'attempt': attempt + 1,
                        'finish_reason': response.choices[0].finish_reason,
                        'usage': {
                            'prompt_tokens': response.usage.prompt_tokens,
                            'completion_tokens': response.usage.completion_tokens,
                            'total_tokens': response.usage.total_tokens
                        }
                    }
                }

            except Exception as e:
                error_msg = str(e)
                logger.error(f"OpenAI error on attempt {attempt + 1}/{self.max_retries}: {error_msg[:200]}")

                # Handle rate limits
                if '429' in error_msg or 'rate_limit' in error_msg.lower():
                    if attempt < self.max_retries - 1:
                        backoff = 2 ** attempt
                        logger.info(f"Rate limit, backing off for {backoff}s...")
                        time.sleep(backoff)
                        continue

                # Handle other errors
                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt
                    logger.info(f"Backing off for {backoff}s before retry...")
                    time.sleep(backoff)

        logger.error(f"OpenAI failed after {self.max_retries} attempts")
        return None

    def close(self):
        """Close client."""
        logger.info("OpenAIClient closed")


class CerebrasClient:
    """
    Cerebras API client using OpenAI SDK with SSL handling and retry logic.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "llama3.1-8b",
        max_retries: int = 2,
        timeout: int = 30
    ):
        """
        Initialize Cerebras client.

        Args:
            api_key: Cerebras API key
            model: Model name (default: llama3.1-8b)
            max_retries: Maximum retry attempts (default: 2)
            timeout: Timeout in seconds per request (default: 30)
        """
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout

        # Initialize OpenAI client with Cerebras endpoint and SSL disabled
        self.http_client = httpx.Client(verify=False, timeout=timeout)
        self.client = OpenAI(
            base_url='https://api.cerebras.ai/v1',
            api_key=api_key,
            http_client=self.http_client
        )

        logger.info(f"CerebrasClient initialized with model={model}, timeout={timeout}s")

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[Dict[str, Any]]:
        """
        Generate response from Cerebras API with retry logic.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with 'content', 'latency', and 'metadata', or None on failure
        """
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                logger.debug(f"Cerebras attempt {attempt + 1}/{self.max_retries}")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                latency = time.time() - start_time
                content = response.choices[0].message.content.strip()

                logger.info(f"Cerebras success - latency: {latency:.2f}s, tokens: {len(content.split())}")

                return {
                    'content': content,
                    'latency': latency,
                    'metadata': {
                        'model': self.model,
                        'provider': 'cerebras',
                        'attempt': attempt + 1,
                        'finish_reason': response.choices[0].finish_reason
                    }
                }

            except Exception as e:
                error_msg = str(e)
                logger.error(f"Cerebras error on attempt {attempt + 1}/{self.max_retries}: {error_msg[:200]}")

                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt
                    logger.info(f"Backing off for {backoff}s before retry...")
                    time.sleep(backoff)

        logger.error(f"Cerebras failed after {self.max_retries} attempts")
        return None

    def close(self):
        """Close HTTP client."""
        if self.http_client:
            self.http_client.close()


class GeminiClient:
    """
    Google Gemini API client as fallback with retry logic.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-1.5-flash",
        max_retries: int = 2,
        timeout: int = 30
    ):
        """
        Initialize Gemini client.

        Args:
            api_key: Google Gemini API key
            model: Model name (default: gemini-1.5-flash)
            max_retries: Maximum retry attempts (default: 2)
            timeout: Timeout in seconds per request (default: 30)
        """
        self.api_key = api_key
        self.model_name = model
        self.max_retries = max_retries
        self.timeout = timeout

        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

        logger.info(f"GeminiClient initialized with model={model}, timeout={timeout}s")

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[Dict[str, Any]]:
        """
        Generate response from Gemini API with retry logic.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with 'content', 'latency', and 'metadata', or None on failure
        """
        # Convert OpenAI-style messages to Gemini format
        prompt = self._convert_messages(messages)

        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                logger.debug(f"Gemini attempt {attempt + 1}/{self.max_retries}")

                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    request_options={'timeout': self.timeout}
                )

                latency = time.time() - start_time
                content = response.text.strip()

                logger.info(f"Gemini success - latency: {latency:.2f}s, tokens: {len(content.split())}")

                return {
                    'content': content,
                    'latency': latency,
                    'metadata': {
                        'model': self.model_name,
                        'provider': 'gemini',
                        'attempt': attempt + 1,
                        'finish_reason': 'stop'
                    }
                }

            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Gemini error on attempt {attempt + 1}/{self.max_retries}: {error_msg[:100]}")

                if 'safety' in error_msg.lower() or 'blocked' in error_msg.lower():
                    logger.error("Content blocked by safety filters")
                    return None

                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt
                    time.sleep(backoff)

        logger.error(f"Gemini failed after {self.max_retries} attempts")
        return None

    def _convert_messages(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to Gemini prompt format."""
        prompt_parts = []

        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')

            if role == 'system':
                prompt_parts.append(f"[SYSTEM INSTRUCTIONS]\n{content}\n")
            elif role == 'user':
                prompt_parts.append(f"{content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")

        return "\n".join(prompt_parts)


class MultiModelManager:
    """
    Manages API calls across multiple models with automatic fallback and cross-validation support.
    """

    def __init__(
        self,
        cerebras_api_key: str,
        gemini_api_key: str,
        openai_api_key: Optional[str] = None,
        primary_model: str = "cerebras",
        timeout: int = 30
    ):
        """
        Initialize multi-model manager.

        Args:
            cerebras_api_key: Cerebras API key
            gemini_api_key: Gemini API key
            openai_api_key: Optional OpenAI API key for cross-validation
            primary_model: Primary model to use ("cerebras", "openai", or "gemini")
            timeout: Timeout in seconds
        """
        self.primary_model = primary_model
        self.timeout = timeout

        # Initialize clients
        self.cerebras = CerebrasClient(cerebras_api_key, timeout=timeout)
        self.gemini = GeminiClient(gemini_api_key, timeout=timeout)

        self.openai = None
        if openai_api_key:
            self.openai = OpenAIClient(openai_api_key, timeout=timeout)
            logger.info("OpenAI client enabled for cross-model validation")

        # Statistics tracking
        self.stats = {
            'cerebras': {'success': 0, 'failure': 0, 'total_latency': 0},
            'gemini': {'success': 0, 'failure': 0, 'total_latency': 0},
            'openai': {'success': 0, 'failure': 0, 'total_latency': 0},
            'fallback_used': 0
        }

        logger.info(f"MultiModelManager initialized with primary={primary_model}")

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        force_model: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate response with automatic fallback.

        Args:
            messages: Message list
            temperature: Sampling temperature
            max_tokens: Max tokens
            force_model: Force specific model ("cerebras", "openai", "gemini")

        Returns:
            Response dict or None
        """
        # Determine which model to use
        model_order = []

        if force_model:
            model_order = [force_model]
        elif self.primary_model == "cerebras":
            model_order = ["cerebras", "gemini"]
        elif self.primary_model == "openai" and self.openai:
            model_order = ["openai", "cerebras", "gemini"]
        else:
            model_order = ["cerebras", "gemini"]

        # Try each model in order
        for model_name in model_order:
            if model_name == "cerebras":
                result = self.cerebras.generate(messages, temperature, max_tokens)
            elif model_name == "openai" and self.openai:
                result = self.openai.generate(messages, temperature, max_tokens)
            elif model_name == "gemini":
                result = self.gemini.generate(messages, temperature, max_tokens)
            else:
                continue

            if result:
                # Update stats
                self.stats[model_name]['success'] += 1
                self.stats[model_name]['total_latency'] += result['latency']
                result['provider'] = model_name
                logger.info(f"✓ Using {model_name.upper()} API")
                return result
            else:
                # Update failure stats
                self.stats[model_name]['failure'] += 1

                # Log fallback if not the last model
                if model_name != model_order[-1]:
                    logger.warning(f"✗ {model_name.upper()} failed, trying next...")
                    self.stats['fallback_used'] += 1

        logger.error("All models failed")
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self.stats.copy()

    def print_stats(self):
        """Print formatted statistics."""
        print("\n" + "="*60)
        print("MULTI-MODEL API STATISTICS")
        print("="*60)

        total_success = sum(self.stats[m]['success'] for m in ['cerebras', 'gemini', 'openai'])
        total_failure = sum(self.stats[m]['failure'] for m in ['cerebras', 'gemini', 'openai'])

        print(f"Total Requests:      {total_success + total_failure}")
        print(f"Total Success:       {total_success}")
        print(f"Total Failures:      {total_failure}")
        print(f"Fallback Used:       {self.stats['fallback_used']}")

        for model in ['cerebras', 'openai', 'gemini']:
            if self.stats[model]['success'] > 0 or self.stats[model]['failure'] > 0:
                print(f"\n{model.upper()}:")
                print(f"  Success:           {self.stats[model]['success']}")
                print(f"  Failures:          {self.stats[model]['failure']}")
                total = self.stats[model]['success'] + self.stats[model]['failure']
                if total > 0:
                    rate = self.stats[model]['success'] / total * 100
                    print(f"  Success Rate:      {rate:.1f}%")
                if self.stats[model]['success'] > 0:
                    avg_latency = self.stats[model]['total_latency'] / self.stats[model]['success']
                    print(f"  Avg Latency:       {avg_latency:.2f}s")

        print("="*60 + "\n")

    def close(self):
        """Close all clients."""
        self.cerebras.close()
        if self.openai:
            self.openai.close()
        logger.info("MultiModelManager closed")


# Backward compatibility alias
APIManager = MultiModelManager
