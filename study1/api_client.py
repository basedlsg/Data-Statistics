#!/usr/bin/env python3
"""
API Client System with Cerebras Primary and Gemini Fallback
Provides robust API access with automatic fallback and comprehensive error handling.
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

            except httpx.TimeoutException as e:
                logger.warning(f"Cerebras timeout on attempt {attempt + 1}/{self.max_retries}: {str(e)[:100]}")
                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt  # Exponential backoff: 1s, 2s
                    logger.info(f"Backing off for {backoff}s before retry...")
                    time.sleep(backoff)

            except httpx.ConnectError as e:
                logger.error(f"Cerebras SSL/connection error on attempt {attempt + 1}: {str(e)[:100]}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

            except Exception as e:
                error_msg = str(e)
                logger.error(f"Cerebras error on attempt {attempt + 1}: {error_msg[:200]}")

                # Check for rate limit
                if 'rate_limit' in error_msg.lower() or '429' in error_msg:
                    logger.warning("Rate limit detected, backing off...")
                    time.sleep(5 * (attempt + 1))
                elif attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

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

            except TimeoutError as e:
                logger.warning(f"Gemini timeout on attempt {attempt + 1}/{self.max_retries}: {str(e)[:100]}")
                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt
                    logger.info(f"Backing off for {backoff}s before retry...")
                    time.sleep(backoff)

            except Exception as e:
                error_msg = str(e)
                logger.error(f"Gemini error on attempt {attempt + 1}: {error_msg[:200]}")

                # Check for rate limit or quota errors
                if 'quota' in error_msg.lower() or 'rate' in error_msg.lower() or '429' in error_msg:
                    logger.warning("Rate limit/quota detected, backing off...")
                    time.sleep(5 * (attempt + 1))
                elif 'blocked' in error_msg.lower() or 'safety' in error_msg.lower():
                    logger.error("Content blocked by safety filters")
                    return None  # Don't retry on safety blocks
                elif attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

        logger.error(f"Gemini failed after {self.max_retries} attempts")
        return None

    def _convert_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert OpenAI-style messages to Gemini prompt format.

        Args:
            messages: List of message dicts

        Returns:
            Combined prompt string
        """
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


class APIManager:
    """
    Manages API calls with automatic fallback from Cerebras to Gemini.
    Tracks usage statistics and provides comprehensive logging.
    """

    def __init__(
        self,
        cerebras_api_key: str,
        gemini_api_key: str,
        timeout: int = 30
    ):
        """
        Initialize API manager with both clients.

        Args:
            cerebras_api_key: Cerebras API key
            gemini_api_key: Google Gemini API key
            timeout: Default timeout in seconds
        """
        self.cerebras = CerebrasClient(
            api_key=cerebras_api_key,
            timeout=timeout
        )
        self.gemini = GeminiClient(
            api_key=gemini_api_key,
            timeout=timeout
        )

        # Usage statistics
        self.stats = {
            'cerebras_success': 0,
            'cerebras_failure': 0,
            'gemini_success': 0,
            'gemini_fallback': 0,
            'total_requests': 0,
            'total_latency': 0.0,
            'errors': []
        }

        logger.info("APIManager initialized with Cerebras primary, Gemini fallback")

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        force_provider: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate response with automatic fallback.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            force_provider: Force specific provider ('cerebras' or 'gemini')

        Returns:
            Dict with 'content', 'latency', 'provider', and 'metadata', or None on total failure
        """
        self.stats['total_requests'] += 1
        request_start = time.time()

        # Try Cerebras first (unless forcing Gemini)
        if force_provider != 'gemini':
            logger.info("Attempting Cerebras API...")
            result = self.cerebras.generate(messages, temperature, max_tokens)

            if result:
                self.stats['cerebras_success'] += 1
                self.stats['total_latency'] += result['latency']
                result['provider'] = 'cerebras'
                logger.info("✓ Using Cerebras API")
                return result
            else:
                self.stats['cerebras_failure'] += 1
                logger.warning("✗ Cerebras failed, falling back to Gemini...")

        # Fallback to Gemini (or if forced)
        if force_provider != 'cerebras':
            logger.info("Attempting Gemini API...")
            result = self.gemini.generate(messages, temperature, max_tokens)

            if result:
                self.stats['gemini_success'] += 1
                if force_provider != 'gemini':
                    self.stats['gemini_fallback'] += 1
                self.stats['total_latency'] += result['latency']
                result['provider'] = 'gemini'
                logger.info("✓ Using Gemini API")
                return result
            else:
                logger.error("✗ Gemini also failed")

        # Both failed
        total_latency = time.time() - request_start
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'latency': total_latency,
            'message': 'Both Cerebras and Gemini failed'
        }
        self.stats['errors'].append(error_record)
        logger.error(f"TOTAL FAILURE - Both APIs failed after {total_latency:.2f}s")

        return None

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics.

        Returns:
            Dict with comprehensive usage statistics
        """
        total_success = self.stats['cerebras_success'] + self.stats['gemini_success']
        avg_latency = (
            self.stats['total_latency'] / total_success
            if total_success > 0 else 0
        )

        return {
            'total_requests': self.stats['total_requests'],
            'total_success': total_success,
            'total_failures': len(self.stats['errors']),
            'cerebras': {
                'success': self.stats['cerebras_success'],
                'failure': self.stats['cerebras_failure'],
                'success_rate': (
                    self.stats['cerebras_success'] /
                    (self.stats['cerebras_success'] + self.stats['cerebras_failure'])
                    if (self.stats['cerebras_success'] + self.stats['cerebras_failure']) > 0
                    else 0
                )
            },
            'gemini': {
                'success': self.stats['gemini_success'],
                'fallback_activations': self.stats['gemini_fallback']
            },
            'performance': {
                'average_latency': avg_latency,
                'total_latency': self.stats['total_latency']
            },
            'errors': self.stats['errors'][-10:]  # Last 10 errors
        }

    def print_stats(self):
        """Print formatted statistics."""
        stats = self.get_stats()

        print("\n" + "=" * 60)
        print("API MANAGER STATISTICS")
        print("=" * 60)
        print(f"Total Requests:      {stats['total_requests']}")
        print(f"Total Success:       {stats['total_success']}")
        print(f"Total Failures:      {stats['total_failures']}")
        print()
        print("CEREBRAS:")
        print(f"  Success:           {stats['cerebras']['success']}")
        print(f"  Failures:          {stats['cerebras']['failure']}")
        print(f"  Success Rate:      {stats['cerebras']['success_rate']:.1%}")
        print()
        print("GEMINI:")
        print(f"  Success:           {stats['gemini']['success']}")
        print(f"  Fallback Used:     {stats['gemini']['fallback_activations']}")
        print()
        print("PERFORMANCE:")
        print(f"  Average Latency:   {stats['performance']['average_latency']:.2f}s")
        print(f"  Total Latency:     {stats['performance']['total_latency']:.2f}s")
        print("=" * 60 + "\n")

    def close(self):
        """Close all API clients."""
        self.cerebras.close()
        logger.info("APIManager closed")


def test_api_clients():
    """
    Quick test of both API clients.
    """
    print("\n" + "=" * 60)
    print("TESTING API CLIENTS")
    print("=" * 60)

    # Hardcoded API keys (as requested - don't worry about security for now)
    CEREBRAS_KEY = "csk-ywwnmnr4k4tnwrr2xfwdj855f3yxfv2t9n2m5dk8r48jv9w2"
    GEMINI_KEY = "AIzaSyD7JLZ7gt4bE5i87zcycGJS2_Nvfv1VNwI"

    # Initialize manager
    manager = APIManager(
        cerebras_api_key=CEREBRAS_KEY,
        gemini_api_key=GEMINI_KEY
    )

    # Test messages
    test_messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Be concise."
        },
        {
            "role": "user",
            "content": "What is 2+2? Answer in one sentence."
        }
    ]

    print("\nTest 1: Default behavior (Cerebras primary)")
    print("-" * 60)
    result = manager.generate(test_messages, temperature=0.0, max_tokens=100)
    if result:
        print(f"Provider: {result['provider']}")
        print(f"Latency: {result['latency']:.2f}s")
        print(f"Response: {result['content'][:200]}")
    else:
        print("FAILED")

    print("\nTest 2: Force Gemini")
    print("-" * 60)
    result = manager.generate(
        test_messages,
        temperature=0.0,
        max_tokens=100,
        force_provider='gemini'
    )
    if result:
        print(f"Provider: {result['provider']}")
        print(f"Latency: {result['latency']:.2f}s")
        print(f"Response: {result['content'][:200]}")
    else:
        print("FAILED")

    # Print statistics
    manager.print_stats()

    # Cleanup
    manager.close()

    print("\n✓ Testing complete")


if __name__ == "__main__":
    # Run tests when script is executed directly
    test_api_clients()
