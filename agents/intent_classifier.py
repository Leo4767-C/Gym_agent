"""Intent classification — routes user query to the correct agent."""

import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed

from config import VALID_INTENTS
from agents.llm import get_llm, extract_json

logger = logging.getLogger(__name__)

INTENT_PROMPT = PromptTemplate.from_template(
    """You are a fitness assistant intent classifier. Classify the user's query into exactly ONE category:

- "workout_plan": User wants exercises or a workout plan for specific muscles/equipment.
- "nutrition": User asks about food, diet, macros, calories, meal plans, supplements, what to eat.
- "schedule": User wants a weekly/daily workout schedule or training program for weight gain or weight loss.
- "exercise_guide": User asks how to perform a specific exercise, correct form, or common mistakes.

User query: "{query}"

Output ONLY a JSON object:
{{"intent": "<one of: workout_plan, nutrition, schedule, exercise_guide>"}}"""
)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(2))
def classify_intent(query: str) -> str:
    """Classifies the user query into one of the 4 supported intents."""
    chain = INTENT_PROMPT | get_llm() | StrOutputParser()
    raw = chain.invoke({"query": query})
    parsed = extract_json(raw)
    intent = parsed.get("intent", "workout_plan")
    if intent not in VALID_INTENTS:
        intent = "workout_plan"
    logger.info("Intent classified: %s", intent)
    return intent
