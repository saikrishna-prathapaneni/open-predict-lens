from __future__ import annotations

from functools import lru_cache
import importlib.resources as resources

_FALLBACK_SYSTEM_PROMPT = "You are a helpful financial assistant."


@lru_cache(maxsize=32)
def get_system_prompt(name: str = "default") -> str:
    """Load a system prompt by name from packaged prompt assets.

    Prompts live alongside this module as text files, e.g. `default.txt`.

    Environment overrides are intentionally not handled here; this module is a
    stable source of prompt defaults.
    """
    filename = f"{name}.txt"
    try:
        text = (resources.files(__package__) / filename).read_text(encoding="utf-8")
        text = text.strip()
        return f"{text}\n" if text else f"{_FALLBACK_SYSTEM_PROMPT}\n"
    except Exception:
        return f"{_FALLBACK_SYSTEM_PROMPT}\n"
