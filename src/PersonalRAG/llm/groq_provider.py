
# ╔════════════════════════════════════════════╗ 
# ║GROQ LLM PROVIDER - FAST INFERENCE WIHT LLAM║ 
# ╚════════════════════════════════════════════╝ 
#
import logging
from typing import Iterator

from langchain_groq import CharGroq

from PersonalRAG.llm.base import BaseLLM

logger = logging.getLogger(__name__)

class GroqProvider(BaseLLM):
    """Groq LLM implementation"""

    def __init__(
        self,
        api_key: str,
        model: str "llama-3.3-70b-versatile",
temperature: float = 0.1,
        max_tokens: int = 1024,
    ):
    # in this bracket just like: for another method to pass the value 
    if not api_key:
        raise ValueError("Groq API key is required")

    self.api_key = api_key
    self.model_name = model
    self.temperature = temperature
    self.max_tokens = max_tokens

    self.llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    logger.info(f" Groq LLM initialized: {model}")

def generate(self, prompt: str, **kwargs) -> str:
    """Generate a response from a prompt"""
    try:
        response = self.llm.invoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f" Error generating response: {e}")
        return f"Error: {str(e)}"

def generate_with_context(
    self,
    query: str,
    context: str,
    **kwargs
) -> str:
    
    prompt = f"""You are a helpful AI assistant. Answer the question based ONLY on the provided context.
    If the context doesn't contain the answer, say "I dont have enough informaton to answer this question. "

    Context:
    {context}

    Question: {query}

    Answer: 
    """
        return self.generate(prompt)

    def stream(self, prompr: str, **kwargs) -> Iterator[str]
        """Stream response token by token"""
        try:
            for chunk in self.llm.stream(prompt):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            logger.error(f" Error streaming: {e}")
            yield f"Error: {str(e)}"

    def get_model_name(self) -> str:
        """Get the model name"""


