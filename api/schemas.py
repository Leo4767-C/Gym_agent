"""Pydantic schemas for API request/response validation."""

from typing import Any
from pydantic import BaseModel, Field


class MessageItem(BaseModel):
    """A single chat message."""
    role: str = "user"       # "user" or "assistant"
    content: str = ""


class ChatRequest(BaseModel):
    """Incoming chat message from the frontend."""
    message: str = Field(..., min_length=3, max_length=1000)
    history: list[MessageItem] = []   # Previous conversation turns


class ChatResponse(BaseModel):
    """Unified response — fields populated based on response_type."""
    response_type:        str
    thought_process:      str = ""
    motivational_message: str = ""
    latency_ms:           int = 0
    filters_used:         dict[str, Any] = {}
    # workout_plan
    workout_plan:         list[dict[str, Any]] = []
    # nutrition
    nutrition_advice:     dict[str, Any] = {}
    meal_plan:            list[dict[str, Any]] = []
    supplements:          list[str] = []
    # schedule
    goal:                 str = ""
    weekly_schedule:      list[dict[str, Any]] = []
    # exercise_guide
    exercise_guide:       dict[str, Any] = {}


class HealthResponse(BaseModel):
    """Health check response."""
    status:   str
    db_docs:  int
    model:    str
