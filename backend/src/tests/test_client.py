import pytest
from pydantic_ai.models.test import TestModel
from app.core import llm

@pytest.mark.asyncio
async def test_ollama_client():
    mock_model = TestModel(
        custom_output_text="fake-text",
        model_name="test-model"
    )
    client = llm.OllamaClient(model=mock_model)
    out = await client.generate("Hello world")
    assert out["text"] == "fake-text"
    assert out["usage"].total_tokens > 0  # TestModel auto-estimates usage!
    assert out["all_messages"][0].kind == 'request' # Verifies history structure