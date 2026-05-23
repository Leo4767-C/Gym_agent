# AI Personal Trainer Agent

An intelligent fitness assistant powered by Retrieval-Augmented Generation (RAG) that provides personalized workout plans, nutrition advice, weekly training schedules, and exercise technique guides. The system uses a multi-agent architecture with intent-based routing, hybrid search (vector + BM25 re-ranking), and conversational memory to deliver context-aware responses entirely in Vietnamese.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Knowledge Base](#knowledge-base)
- [License](#license)

---

## Overview

The system accepts natural language queries from users and automatically classifies them into one of four intent categories:

| Intent             | Description                                                    |
| ------------------ | -------------------------------------------------------------- |
| `workout_plan`     | Generates structured exercise plans filtered by muscle group, equipment, and difficulty |
| `nutrition`        | Calculates TDEE/macros and suggests meal plans based on user goals |
| `schedule`         | Creates weekly training programs for weight gain or weight loss |
| `exercise_guide`   | Provides step-by-step form instructions with YouTube video references |

All responses are generated in Vietnamese with structured JSON output, enabling the frontend to render rich, typed UI components for each intent.

---

## Architecture

```
User Query
    |
    v
[Intent Classifier] ── LLM classifies into 1 of 4 intents
    |
    v
[Query Analyzer] ── Extracts metadata filters (muscle_group, equipment, difficulty)
    |
    v
[Hybrid Retrieval]
    |--- Vector Search (ChromaDB + sentence-transformers embeddings)
    |--- BM25 Re-ranking (keyword matching on top of vector results)
    |
    v
[Specialized Agent] ── One of: Workout / Nutrition / Schedule / Guide
    |
    v
[Structured JSON Response] ── Rendered by Next.js frontend
```

Key design decisions:

- **Multi-agent routing**: A central router classifies user intent and delegates to specialized agents, each with its own prompt template and output schema.
- **Hybrid search**: Initial vector similarity search retrieves 3x the required documents, then BM25 re-ranks them by keyword relevance to improve precision.
- **Conversational memory**: Chat history (up to 10 turns) is injected into every agent prompt, enabling follow-up queries like "change to 3 days" or "add more protein."
- **Retry with backoff**: All LLM calls use `tenacity` with configurable retry policies to handle transient Ollama failures.
- **Robust JSON extraction**: A three-strategy parser (direct parse, markdown fence, first brace block) ensures structured output even when the LLM wraps JSON in extra text.

---

## Tech Stack

### Backend

| Component        | Technology                                        |
| ---------------- | ------------------------------------------------- |
| Framework        | FastAPI 0.115+ with Uvicorn ASGI server           |
| LLM              | Ollama (local) running Qwen 2.5 3B               |
| Orchestration    | LangChain (prompts, chains, output parsers)       |
| Vector Database  | ChromaDB with persistent local storage            |
| Embeddings       | sentence-transformers/all-MiniLM-L6-v2 (CPU)      |
| Keyword Search   | rank-bm25 (BM25Okapi)                             |
| Validation       | Pydantic v2                                       |
| Retry Logic      | tenacity                                          |
| Video Search     | youtube-search-python                             |

### Frontend

| Component        | Technology                                        |
| ---------------- | ------------------------------------------------- |
| Framework        | Next.js 16 (App Router)                           |
| Language         | TypeScript                                        |
| UI Library       | React 19                                          |
| Icons            | Lucide React                                      |
| Streaming        | Server-Sent Events (SSE)                          |

---

## Project Structure

```
gym_agent/
├── main.py                    # FastAPI application entry point with lifespan management
├── config.py                  # Centralized configuration (LLM, ChromaDB, CORS, etc.)
│
├── agents/                    # AI agent pipeline
│   ├── __init__.py            # Exports run_agent()
│   ├── router.py              # Intent-based routing and chat history formatting
│   ├── intent_classifier.py   # LLM-powered 4-class intent classification
│   ├── retrieval.py           # Hybrid search: vector retrieval + BM25 re-ranking
│   ├── llm.py                 # Ollama LLM singleton and JSON extraction utilities
│   ├── tools.py               # External tools (YouTube video search)
│   ├── workout_agent.py       # Generates structured workout plans
│   ├── nutrition_agent.py     # Calculates macros and generates meal plans
│   ├── schedule_agent.py      # Creates weekly training schedules
│   └── guide_agent.py         # Produces exercise form guides with video links
│
├── api/                       # HTTP layer
│   ├── __init__.py
│   ├── routes.py              # REST endpoints: /chat, /chat/stream, /health, /upload
│   └── schemas.py             # Pydantic request/response models
│
├── database/                  # Vector database management
│   ├── __init__.py            # Exports get_vectorstore(), initialize_database()
│   ├── embeddings.py          # HuggingFace embedding model loader (CPU-pinned)
│   ├── vectorstore.py         # ChromaDB operations: create, seed, query
│   ├── ingestion.py           # File ingestion pipeline (PDF, CSV, JSON, TXT)
│   ├── seed_exercises.py      # 31 pre-built exercise documents with metadata
│   └── seed_nutrition.py      # 17 Vietnamese food and supplement documents
│
├── chroma_db/                 # ChromaDB persistent storage (auto-generated)
│
└── frontend/                  # Next.js client application
    ├── package.json
    ├── tsconfig.json
    └── src/
        ├── types.ts           # TypeScript interfaces for API responses
        ├── app/
        │   ├── layout.tsx     # Root layout
        │   ├── page.tsx       # Main chat interface
        │   └── globals.css    # Global styles
        └── components/
            ├── Header.tsx          # Application header
            ├── ChatInput.tsx       # Message input with send controls
            ├── WorkoutResult.tsx   # Workout plan card renderer
            ├── NutritionResult.tsx # Nutrition advice and meal plan display
            ├── ScheduleResult.tsx  # Weekly schedule table
            ├── GuideResult.tsx     # Exercise guide with embedded video
            ├── UploadModal.tsx     # File upload dialog for data ingestion
            └── Shared.tsx         # Reusable UI components
```

---

## Prerequisites

- **Python** 3.11 or higher
- **Node.js** 18 or higher (for the frontend)
- **Ollama** installed and running locally with the `qwen2.5:3b` model pulled

Verify Ollama is ready:

```bash
ollama list
# Should show qwen2.5:3b in the output
```

If the model is not yet available:

```bash
ollama pull qwen2.5:3b
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd gym_agent
```

### 2. Set up the Python backend

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

pip install fastapi uvicorn langchain langchain-community langchain-core \
    langchain-chroma langchain-huggingface langchain-text-splitters \
    chromadb sentence-transformers rank-bm25 tenacity pydantic \
    youtube-search-python pymupdf
```

### 3. Set up the Next.js frontend

```bash
cd frontend
npm install
cd ..
```

---

## Configuration

All settings are centralized in `config.py`:

```python
# LLM
OLLAMA_BASE_URL  = "http://localhost:11434"
OLLAMA_MODEL     = "qwen2.5:3b"
LLM_TEMPERATURE  = 0.2
LLM_TIMEOUT      = 120

# ChromaDB
CHROMA_PERSIST_DIR   = "./chroma_db"
COLLECTION_EXERCISES = "gym_exercises"
COLLECTION_NUTRITION = "gym_nutrition"

# Embedding
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval
NUM_DOCS_TO_FETCH = 5

# Chat Memory
MAX_CHAT_HISTORY = 10
```

Modify these values directly in the file as needed. No environment variables or `.env` file is required.

---

## Running the Application

### Start the backend

```bash
# From the project root, with the virtual environment activated
python main.py
```

The API server starts at `http://localhost:8000`. On first launch, ChromaDB is automatically seeded with the built-in exercise (31 documents) and nutrition (17 documents) knowledge base.

### Start the frontend

```bash
cd frontend
npm run dev
```

The frontend starts at `http://localhost:3000` and connects to the backend API.

### Verify the system

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "db_docs": 31,
  "model": "qwen2.5:3b"
}
```

---

## API Reference

All endpoints are prefixed with `/api`.

### POST /api/chat

Main conversational endpoint. Accepts a user message and optional chat history, returns a structured response based on classified intent.

**Request Body:**

```json
{
  "message": "Cho toi bai tap nguc voi ta don",
  "history": [
    { "role": "user", "content": "previous message" },
    { "role": "assistant", "content": "previous response" }
  ]
}
```

**Response:** A `ChatResponse` object with fields populated based on `response_type`. See [schemas.py](api/schemas.py) for the full schema.

### POST /api/chat/stream

Streaming variant using Server-Sent Events. Emits three event phases:

1. `thinking` -- Processing indicator
2. `result` -- Full structured response payload
3. `done` -- Stream termination signal

### GET /api/health

Returns system status, document count in ChromaDB, and the active LLM model name.

### POST /api/upload

Ingests external files into ChromaDB. Supports PDF, CSV, JSON, and TXT formats.

**Parameters (multipart/form-data):**

| Field             | Type   | Description                          |
| ----------------- | ------ | ------------------------------------ |
| `file`            | File   | The file to ingest                   |
| `collection_type` | string | Target collection: `exercises` or `nutrition` (default: `nutrition`) |

---

## Knowledge Base

The system ships with a pre-built knowledge base that is automatically seeded on first startup.

### Exercises (31 documents)

Covers 7 muscle groups with metadata filters for retrieval:

| Muscle Group | Count | Equipment Variants                          |
| ------------ | ----- | ------------------------------------------- |
| Chest        | 5     | dumbbell, barbell, bodyweight, cable         |
| Back         | 6     | dumbbell, barbell, bodyweight, machine, cable |
| Legs         | 6     | dumbbell, barbell, bodyweight, machine       |
| Shoulders    | 4     | dumbbell, barbell, cable                     |
| Arms         | 6     | dumbbell, barbell, bodyweight, cable         |
| Core         | 4     | bodyweight, cable                            |

Each document includes: name, muscle group, equipment, difficulty level, recommended sets/reps, rest time, and a technique description.

### Nutrition (17 documents)

Vietnamese-localized food database covering:

- **Protein sources**: chicken breast, eggs, salmon, lean beef, whey protein
- **Carbohydrate sources**: white rice, oats, sweet potato, banana
- **Healthy fats**: avocado, almonds, olive oil
- **Fat loss foods**: green salad, Greek yogurt, canned tuna
- **Supplements**: creatine monohydrate, BCAA

Each document includes: macronutrient breakdown per 100g, calorie count, recommended meal timing, and fitness goal alignment.

### Extending the Knowledge Base

New data can be added in two ways:

1. **Via the upload API**: Send PDF, CSV, JSON, or TXT files to `POST /api/upload`. Files are chunked (1000 characters, 150 overlap) and embedded automatically.
2. **Via seed files**: Add new `Document` objects to `seed_exercises.py` or `seed_nutrition.py` and restart the server. The database re-seeds if the document count is below the expected total.

---

## License

This project is provided as-is for educational and personal use.
