from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging


from pydantic_ai import Agent, AgentRunResult, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.litellm import LiteLLMProvider
from app.config import settings


logger = logging.getLogger(__name__)

class BaseLLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Returns a standardized dictionary: {'text': str, 'usage': dict, 'raw': any}"""
        pass

class OllamaClient(BaseLLMClient):
    def __init__(
        self, 
        model_name: str = "ollama/llama3", 
        base_url: Optional[str] = None,
        model: Optional[OpenAIChatModel] = None,  # For testing: inject a mock model 
        api_key: str = "sk-not-required"
    ):
        # If a model is provided (e.g. TestModel), use it. Otherwise, create the real one.
        if model:
            self.model = model
        else:
            self.provider = LiteLLMProvider(
                api_base=base_url or settings.ollama_url,
                api_key=api_key
            )
            self.model = OpenAIChatModel(
                model_name=model_name,
                provider=self.provider
            )

    async def generate(
        self, 
        prompt: str, 
        tools: Optional[List[Tool]] = None, 
        system_prompt: str = "You are a helpful financial assistant.",
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Standardized generation method. 
        Uses an Agent for both simple text and tool-calling for consistency.
        """
        try:
            agent = Agent(
                model=self.model,
                tools=tools or [],
                system_prompt=system_prompt
            )
            result: AgentRunResult = await agent.run(prompt)
            print(dir(result))
            return {
                "text": result.output, 
                "usage": result.usage(),
                "all_messages": result.all_messages(),
                "raw": result
            }
        except Exception as e:
            logger.error(f"LLM Generation Error ({self.model.model_name}): {e}")
            raise RuntimeError(f"Failed to generate response from {self.model.model_name}")


def get_llm_client(provider: Optional[str] = None) -> BaseLLMClient:
    """Factory to obtain an LLM client by provider name.

    provider: 'ollama'
    """
    _provider = (provider or settings.llm_provider or "ollama").lower()
    if _provider == "ollama":
        return OllamaClient()
    raise ValueError(f"Unknown LLM provider: {_provider}")
