"""
Here we will use Abstract class for llm providers
easier for us to swap the model in future
"""

from abc import ABC, abstractmethod
from typing import Iterator

class BaseLLM(ABC):
    """Abstract interface for LLM providers."""
    # what does it mean by abstract interface for llm providers ??

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """generating a response from a single prompt"""
        pass

    @abstractmethod
    def generate_with_context(
        self,
        query: str,
        context: str,
        **kwargs
    ) -> str:
        """Generating a response using context (for RAG)."""
        pass

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """Stream response token by token"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """get the model name"""
        pass




    
