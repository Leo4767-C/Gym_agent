"""FastAPI route definitions — with Chat History + Streaming support."""

import json
import logging
import time
import os
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from agents import run_agent
from config import OLLAMA_MODEL, COLLECTION_EXERCISES
from database import get_vectorstore
from database.ingestion import ingest_file
from api.schemas import ChatRequest, ChatResponse, HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


@router.post("/chat", response_model=ChatResponse, tags=["Agent"])
async def chat(request: ChatRequest) -> ChatResponse:
    """Main RAG pipeline — auto-classifies intent and generates response.
    Now accepts chat history for conversational memory.
    """
    t0 = time.perf_counter()
    logger.info("POST /api/chat — %s", request.message[:80])

    # Convert Pydantic models to dicts for the agent
    history_dicts = [{"role": m.role, "content": m.content} for m in request.history]

    try:
        result = run_agent(request.message, history=history_dicts)
    except Exception as exc:
        logger.exception("Agent error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))

    latency_ms = int((time.perf_counter() - t0) * 1000)
    logger.info("POST /api/chat — %d ms", latency_ms)

    return ChatResponse(
        response_type        = result.get("response_type", "workout_plan"),
        thought_process      = result.get("thought_process", ""),
        motivational_message = result.get("motivational_message", ""),
        latency_ms           = latency_ms,
        filters_used         = result.get("_filters_used", {}),
        workout_plan         = result.get("workout_plan", []),
        nutrition_advice     = result.get("nutrition_advice", {}),
        meal_plan            = result.get("meal_plan", []),
        supplements          = result.get("supplements", []),
        goal                 = result.get("goal", ""),
        weekly_schedule      = result.get("weekly_schedule", []),
        exercise_guide       = result.get("exercise_guide", {}),
    )


@router.post("/chat/stream", tags=["Agent"])
async def chat_stream(request: ChatRequest):
    """Streaming endpoint — sends partial results via Server-Sent Events (SSE).
    Emits events: 'thinking', 'result', 'done'.
    """
    async def event_generator():
        t0 = time.perf_counter()
        history_dicts = [{"role": m.role, "content": m.content} for m in request.history]

        # Phase 1: Thinking
        yield f"data: {json.dumps({'event': 'thinking', 'message': 'Đang phân tích câu hỏi...'})}\n\n"

        try:
            result = run_agent(request.message, history=history_dicts)
        except Exception as exc:
            yield f"data: {json.dumps({'event': 'error', 'message': str(exc)})}\n\n"
            return

        latency_ms = int((time.perf_counter() - t0) * 1000)

        # Phase 2: Send structured result
        result_payload = {
            "event": "result",
            "data": {
                "response_type":        result.get("response_type", "workout_plan"),
                "thought_process":      result.get("thought_process", ""),
                "motivational_message": result.get("motivational_message", ""),
                "latency_ms":           latency_ms,
                "filters_used":         result.get("_filters_used", {}),
                "workout_plan":         result.get("workout_plan", []),
                "nutrition_advice":     result.get("nutrition_advice", {}),
                "meal_plan":            result.get("meal_plan", []),
                "supplements":          result.get("supplements", []),
                "goal":                 result.get("goal", ""),
                "weekly_schedule":      result.get("weekly_schedule", []),
                "exercise_guide":       result.get("exercise_guide", {}),
            }
        }
        yield f"data: {json.dumps(result_payload, ensure_ascii=False)}\n\n"

        # Phase 3: Done
        yield f"data: {json.dumps({'event': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/health", response_model=HealthResponse, tags=["Infrastructure"])
async def health() -> HealthResponse:
    """Liveness / readiness probe."""
    try:
        vs = get_vectorstore(collection_name=COLLECTION_EXERCISES)
        db_docs = vs._collection.count()
        status = "ok" if db_docs > 0 else "degraded"
    except Exception:
        db_docs, status = -1, "degraded"
    return HealthResponse(status=status, db_docs=db_docs, model=OLLAMA_MODEL)


@router.post("/upload", tags=["Ingestion"])
async def upload_file(
    file: UploadFile = File(...),
    collection_type: str = Form("nutrition")
):
    """Uploads a raw file (PDF, CSV, JSON, TXT) and ingests it into ChromaDB."""
    allowed_extensions = ["pdf", "csv", "json", "txt"]
    ext = file.filename.split(".")[-1].lower() if file.filename else ""

    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    temp_dir = "/tmp/gym_agent_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        num_chunks = ingest_file(temp_path, collection_type=collection_type)
        return {"status": "success", "chunks_added": num_chunks, "filename": file.filename}
    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
