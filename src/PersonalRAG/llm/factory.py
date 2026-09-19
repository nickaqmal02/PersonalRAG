"""
LLM Factory - Created LLM providers based on config
"""

import logging
from typing import Optional

from PersonalRAG.llm.base import BaseLLM
from PersonalRAG.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)

# declaring the main class
class LLMFactory:
    """Factory for creating LLM providers"""
    @staticmethod
    def create(
        provider: str = "groq",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> BaseLLM:

        provider = provider.lower()
        # this ensure the consistency of our provider name

        if provider == "groq":
            if not api_key:
                raise ValueError("Groq requires an API key")
            return GroqProvider(
                api_key= api_key,
                model=model or "llama-3.3-70b-versatile",
                temperature=temperature,
                max_tokens=max_tokens,
            )

        raise ValueError(f"Unsupported provider: {provider}")


