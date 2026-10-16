# AI Engine Package (`ai`)

This package powers prompt generation, structured email drafting, safety checks, and error diagnostics for the outreach platform using Google Gemini Flash.

---

## The Three Cardinal Rules

1. **NO BACKEND IMPORTS**: Never import from `backend/`. This package must remain decoupled and testable in total isolation.
2. **NO DATABASE ACCESS**: Never connect to PostgreSQL or execute SQL queries. The caller passes dictionaries/Pydantic models, and the caller persists results.
3. **NO MESSAGE SENDING**: Never interact with email or messaging APIs. The AI only creates draft proposals. Human beings approve and send.

---

## Directory Overview

- `gemini_client.py`: Wrapper for Gemini API with retry, backoff, and offline mock mode.
- `prompts/`: Versioned prompt templates and tone guides.
- `schemas/`: Pydantic models for structured outputs (`draft_output.py`).
- `validators/`: Strict fact-checker (`fact_check.py`), safety filters, and prompt-injection guard.
- `extraction/`: Experience parser and category classifier.
- `explain/`: Explainer turning score reason codes into user-friendly text.
- `diagnosis/`: AI-assisted error root cause diagnosis.
- `fixtures/`: Offline test datasets and mock HTML snapshots.
- `evals/`: Automated evaluation benchmarks for CI.
