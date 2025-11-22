#!/usr/bin/env python3
"""
Phase 1 API Client - Multi-Model Support
Supports: Cerebras (Llama 3.1), OpenAI (GPT-4), Anthropic (Claude 3.5)
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
import httpx
from openai import OpenAI

# Disable SSL warnings for development
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CerebrasClient:
    """Cerebras Llama 3.1 8B client"""

    def __init__(self, api_key: str, max_retries: int = 4):
        self.api_key = api_key
        self.max_retries = max_retries
        self.model = "llama3.1-8b"

        # Use OpenAI-compatible client
        self.client = OpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=api_key,
            http_client=httpx.Client(verify=False, timeout=60)
        )
        logger.info("CerebrasClient initialized")

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 150) -> Optional[Dict[str, Any]]:
        """Generate response with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                latency = time.time() - start_time
                content = response.choices[0].message.content.strip()

                return {
                    'content': content,
                    'latency': latency,
                    'model': self.model,
                    'tokens': len(content.split())
                }

            except Exception as e:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s, 8s
                logger.warning(f"Cerebras attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {wait_time}s...")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Cerebras failed after {self.max_retries} attempts")
                    return None


class GPT4Client:
    """OpenAI GPT-4 client"""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", max_retries: int = 4):
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries

        self.client = OpenAI(
            api_key=api_key,
            http_client=httpx.Client(verify=False, timeout=60)
        )
        logger.info(f"GPT4Client initialized with model={model}")

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 150) -> Optional[Dict[str, Any]]:
        """Generate response with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                latency = time.time() - start_time
                content = response.choices[0].message.content.strip()

                return {
                    'content': content,
                    'latency': latency,
                    'model': self.model,
                    'tokens': len(content.split())
                }

            except Exception as e:
                wait_time = 2 ** attempt
                logger.warning(f"GPT-4 attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {wait_time}s...")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"GPT-4 failed after {self.max_retries} attempts")
                    return None


class ClaudeClient:
    """Anthropic Claude 3.5 client"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", max_retries: int = 4):
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries

        # Try to import anthropic
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.available = True
            logger.info(f"ClaudeClient initialized with model={model}")
        except ImportError:
            logger.warning("Anthropic SDK not available. Install with: pip install anthropic")
            self.available = False

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 150) -> Optional[Dict[str, Any]]:
        """Generate response with exponential backoff retry"""
        if not self.available:
            logger.error("Claude client not available")
            return None

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                # Convert messages format (Claude uses different format)
                # Extract system message if present
                system_message = ""
                user_messages = []
                for msg in messages:
                    if msg['role'] == 'system':
                        system_message = msg['content']
                    else:
                        user_messages.append(msg)

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_message if system_message else None,
                    messages=user_messages
                )

                latency = time.time() - start_time
                content = response.content[0].text.strip()

                return {
                    'content': content,
                    'latency': latency,
                    'model': self.model,
                    'tokens': len(content.split())
                }

            except Exception as e:
                wait_time = 2 ** attempt
                logger.warning(f"Claude attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {wait_time}s...")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Claude failed after {self.max_retries} attempts")
                    return None


class MultiModelClient:
    """Unified client supporting all 3 models"""

    def __init__(self, cerebras_key: str, openai_key: str, anthropic_key: str):
        self.clients = {
            'cerebras': CerebrasClient(cerebras_key),
            'gpt4': GPT4Client(openai_key),
            'claude': ClaudeClient(anthropic_key)
        }
        logger.info("MultiModelClient initialized with 3 models")

    def generate(self, model_name: str, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 150) -> Optional[Dict[str, Any]]:
        """Generate response from specified model"""
        if model_name not in self.clients:
            logger.error(f"Unknown model: {model_name}. Available: {list(self.clients.keys())}")
            return None

        return self.clients[model_name].generate(messages, temperature, max_tokens)


if __name__ == "__main__":
    # Test with dummy keys
    print("Phase 1 API Client initialized")
    print("Supported models: Cerebras (llama3.1-8b), GPT-4 (gpt-4o-mini), Claude (claude-3-5-sonnet)")
