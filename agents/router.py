"""Agent router — classifies intent and delegates to the correct agent."""

import logging
from typing import Any

from config import MAX_CHAT_HISTORY
from agents.intent_classifier import classify_intent
from agents.retrieval import (
    run_query_analyzer, retrieve_exercises, retrieve_nutrition,
    format_exercises, format_nutrition,
)
from agents.workout_agent import generate_workout
from agents.nutrition_agent import generate_nutrition
from agents.schedule_agent import generate_schedule
from agents.guide_agent import generate_guide

logger = logging.getLogger(__name__)


def _format_history(history: list[dict]) -> str:
    """Converts history list to a readable string for LLM context."""
    if not history:
        return "(Chưa có lịch sử hội thoại)"
    # Keep only the last N turns
    recent = history[-(MAX_CHAT_HISTORY * 2):]
    lines = []
    for msg in recent:
        role = "User" if msg.get("role") == "user" else "AI"
        content = msg.get("content", "")[:300]  # Truncate long messages
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def run_agent(user_query: str, history: list[dict] | None = None) -> dict[str, Any]:
    """
    Main entry point — routes to the correct agent based on intent.
    Now accepts chat history for conversational memory.

    Returns a dict with 'response_type' and intent-specific data.
    """
    logger.info("Agent invoked: %s", user_query[:120])
    chat_history_str = _format_history(history or [])

    # Use the full context (current query + recent history) for better intent classification
    intent = classify_intent(user_query)

    if intent == "workout_plan":
        result = _handle_workout(user_query, chat_history_str)
    elif intent == "nutrition":
        result = _handle_nutrition(user_query, chat_history_str)
    elif intent == "schedule":
        result = _handle_schedule(user_query, chat_history_str)
    elif intent == "exercise_guide":
        result = _handle_guide(user_query, chat_history_str)
    else:
        result = _empty_response("workout_plan", {})

    result["response_type"] = intent
    logger.info("Agent completed (intent=%s)", intent)
    return result


def _handle_workout(query: str, chat_history: str) -> dict:
    filters = run_query_analyzer(query)
    exercises = retrieve_exercises(query, filters)
    if not exercises:
        return _empty_response("workout_plan", filters)
    result = generate_workout(query, format_exercises(exercises), chat_history)
    result["_filters_used"] = filters
    return result


def _handle_nutrition(query: str, chat_history: str) -> dict:
    docs = retrieve_nutrition(query)
    result = generate_nutrition(query, format_nutrition(docs), chat_history)
    result["_filters_used"] = {}
    return result


def _handle_schedule(query: str, chat_history: str) -> dict:
    filters = run_query_analyzer(query)
    exercises = retrieve_exercises(query, filters)
    if not exercises:
        return _empty_response("schedule", filters)
    result = generate_schedule(query, format_exercises(exercises), chat_history)
    result["_filters_used"] = filters
    return result


def _handle_guide(query: str, chat_history: str) -> dict:
    no_filter = {"muscle_group": None, "equipment": None, "difficulty": None}
    exercises = retrieve_exercises(query, no_filter)
    result = generate_guide(query, format_exercises(exercises), chat_history)
    result["_filters_used"] = {}
    return result


def _empty_response(intent: str, filters: dict) -> dict:
    return {
        "response_type": intent,
        "thought_process": "Không tìm thấy dữ liệu phù hợp trong cơ sở kiến thức.",
        "motivational_message": "Hãy thử lại với câu hỏi khác nhé!",
        "workout_plan": [],
        "_filters_used": filters,
    }
