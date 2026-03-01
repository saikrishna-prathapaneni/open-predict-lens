import pytest
import logging
# from pydantic_ai.models.test import TestModel
from app.core.llm import OllamaClient
from app.core.tools.cal import calculate
from app.config import settings

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_local_ai():
    model = OllamaClient(
        model_name=settings.ollama_model_name,
        base_url=settings.ollama_url
    )

    system_prompt = "You are a helpful assistant that can perform " \
                    "calculations using the 'calculate' tool when needed."
    prompt = "What is 196 * 259?"
    result = await model.generate(prompt, tools=[calculate], system_prompt=system_prompt)
    logger.info("LLM Response: %s", result)
    assert "text" in result
    assert any(value in result["text"] for value in ["50764", "50,764"])
    assert "usage" in result
    