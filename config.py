"""
config.py — Centralized configuration for the AI Personal Trainer.
"""

# ── Ollama LLM ──
OLLAMA_BASE_URL  = "http://localhost:11434"
OLLAMA_MODEL     = "qwen2.5:3b"
LLM_TEMPERATURE  = 0.2
LLM_TIMEOUT      = 120

# ── ChromaDB ──
CHROMA_PERSIST_DIR   = "./chroma_db"
COLLECTION_EXERCISES = "gym_exercises"
COLLECTION_NUTRITION = "gym_nutrition"

# ── Embedding ──
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ── Retrieval ──
NUM_DOCS_TO_FETCH = 5

# ── Chat Memory ──
MAX_CHAT_HISTORY = 10  # Number of recent turns (user+AI pairs) to keep

# ── Controlled vocabulary ──
VALID_MUSCLE_GROUPS = {"chest", "back", "legs", "shoulders", "arms", "core", "full_body"}
VALID_EQUIPMENT     = {"barbell", "dumbbell", "machine", "bodyweight", "cable", "kettlebell"}
VALID_DIFFICULTIES  = {"beginner", "intermediate", "advanced"}
VALID_INTENTS       = {"workout_plan", "nutrition", "schedule", "exercise_guide"}

# ── CORS ──
CORS_ORIGINS = [
    "http://localhost:3000", "http://127.0.0.1:3000",
    "http://localhost:3001", "http://127.0.0.1:3001",
    "http://localhost:5500", "http://127.0.0.1:5500",
]
