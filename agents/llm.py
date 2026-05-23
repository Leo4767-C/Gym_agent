"""LLM singleton and JSON extraction utility."""

import json
import logging
import re
from typing import Any

from langchain_community.llms import Ollama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, LLM_TEMPERATURE, LLM_TIMEOUT

logger = logging.getLogger(__name__)

_llm: Ollama | None = None


def get_llm() -> Ollama:
    """Returns a cached Ollama LLM instance."""
    global _llm
    if _llm is None:
        logger.info("Initialising Ollama LLM (%s) …", OLLAMA_MODEL)
        _llm = Ollama(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL,
            temperature=LLM_TEMPERATURE,
            timeout=LLM_TIMEOUT,
        )
    return _llm


def extract_json(text: str) -> dict[str, Any]:
    """
    Extracts the first valid JSON object from LLM output.

    Tries: direct parse → markdown fence → first brace block.
    Returns empty dict on failure.
    """
    text = text.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: markdown code fence
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass

    # Strategy 3: first brace-delimited object
    brace = re.search(r"\{.*\}", text, re.DOTALL)
    if brace:
        try:
            return json.loads(brace.group(0))
        except json.JSONDecodeError:
            pass

    logger.warning("Could not extract JSON: %s", text[:200])
    return {}
