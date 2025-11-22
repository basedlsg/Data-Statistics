#!/usr/bin/env python3
"""
Phase 1 API Client - Multi-Model Support
Supports: Cerebras (Llama 3.1), Groq (Llama 3.1), Gemini (Flash 1.5)
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
import httpx
from openai import OpenAI
import google.generativeai as genai
from groq import Groq

# Disable SSL warnings for development
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'

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


class GroqClient:
    """Groq Llama 3.1 client"""

    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant", max_retries: int = 4):
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries

        self.client = Groq(api_key=api_key)
        logger.info(f"GroqClient initialized with model={model}")

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
                logger.warning(f"Groq attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {wait_time}s...")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Groq failed after {self.max_retries} attempts")
                    return None


class GeminiClient:
    """Google Gemini Flash 1.5 client"""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", max_retries: int = 4):
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries

        # Configure Gemini with REST transport (SSL-safe)
        genai.configure(api_key=api_key, transport='rest')
        self.client = genai.GenerativeModel(model)
        logger.info(f"GeminiClient initialized with model={model}")

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 150) -> Optional[Dict[str, Any]]:
        """Generate response with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()

                # Combine system and user messages for Gemini
                combined_prompt = ""
                for msg in messages:
                    if msg['role'] == 'system':
                        combined_prompt += f"[SYSTEM CONTEXT]\n{msg['content']}\n\n"
                    elif msg['role'] == 'user':
                        combined_prompt += f"[USER REQUEST]\n{msg['content']}"

                response = self.client.generate_content(
                    combined_prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                )

                latency = time.time() - start_time
                content = response.text.strip()

                return {
                    'content': content,
                    'latency': latency,
                    'model': self.model,
                    'tokens': len(content.split())
                }

            except Exception as e:
                wait_time = 2 ** attempt
                logger.warning(f"Gemini attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {wait_time}s...")
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Gemini failed after {self.max_retries} attempts")
                    return None


class MultiModelClient:
    """Unified client supporting all 3 models"""

    def __init__(self, cerebras_key: str, groq_key: str = "", gemini_key: str = ""):
        self.clients = {
            'cerebras': CerebrasClient(cerebras_key)
        }

        if groq_key:
            self.clients['groq'] = GroqClient(groq_key)

        if gemini_key:
            self.clients['gemini'] = GeminiClient(gemini_key)

        logger.info(f"MultiModelClient initialized with {len(self.clients)} models: {list(self.clients.keys())}")

    def generate(self, model_name: str, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 150) -> Optional[Dict[str, Any]]:
        """Generate response from specified model"""
        if model_name not in self.clients:
            logger.error(f"Unknown model: {model_name}. Available: {list(self.clients.keys())}")
            return None

        return self.clients[model_name].generate(messages, temperature, max_tokens)


if __name__ == "__main__":
    # Test with actual keys
    print("Phase 1 API Client initialized")
    print("Supported models: Cerebras (llama3.1-8b), Groq (llama-3.1-8b-instant), Gemini (flash-1.5)")
