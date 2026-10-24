# AI Engineering Guide (Gemini Flash & Evaluation)

Welcome to the AI engineering team!
The `ai/` module is an isolated Python package imported by the backend. It handles LLM prompt compilation, structured drafting, output validation, prompt-injection defense, and automated error diagnostics.

---

## 1. The Three Cardinal Rules of the AI Module

1. **NEVER import from `backend/`**: The AI package must remain decoupled and testable in total isolation.
2. **NEVER touch the database**: The backend supplies input data as dictionaries/Pydantic models, and the backend stores the outputs.
3. **NEVER send emails or messages**: The AI package only produces draft content. Humans approve and dispatch.

---

## 2. Directory Structure

```
ai/
├── README.md
├── __init__.py
├── config.py              # Reads GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MOCK_MODE
├── gemini_client.py       # Wrapper with timeout, backoff, retry, and mock mode
├── prompts/
│   ├── __init__.py        # Version registry (load_prompt)
│   ├── CHANGELOG.md       # Version history
│   ├── email_draft_v1.md  # Core verified-facts prompt template
│   ├── tone_hr.md         # Recruiter tone guidelines
│   ├── tone_tpo.md        # College placement officer tone guidelines
│   └── tone_founder.md    # Startup founder tone guidelines
├── schemas/
│   └── draft_output.py    # Pydantic model mirroring contracts/ai-schemas/draft_output.json
├── validators/
│   ├── fact_check.py      # Validates every claim maps to an input fact_id
│   ├── safety_checks.py   # Length, spammy words, opt-out check
│   ├── injection_guard.py # Detects prompt injection in scraped text
│   └── output_guard.py    # Retries once on invalid schema, else flags needs_review
├── extraction/
│   ├── experience_parser.py # Regex + fallback extractor for years of experience
│   ├── category_classifier.py
│   └── company_matcher.py # Fuzzy duplicate proposer (never auto-merges)
├── diagnosis/
│   ├── error_diagnoser.py # Analyzes stack trace & payload to find root cause
│   ├── selector_suggester.py
│   └── payload_fixer.py
├── fixtures/              # Sample job and company data for offline development
└── evals/                 # Prompt evaluation scripts and CI benchmark suite
```

---

## 3. Strict Anti-Hallucination & Fact-Checking

When generating drafts with Gemini Flash:
- Every factual claim made in `body` must cite a valid `fact_id` present in the input.
- The `ai/validators/fact_check.py` scans the output text for numbers, salary values, and names. If any entity appears that was not present in the input facts, the draft fails validation.
- Missing data must result in a notice in `missing_information_warnings`, **never** an invented assumption.

---

## 4. Offline Mock Mode for Testing & CI

To ensure CI pipelines and unit tests run fast and cost nothing:
- Set `GEMINI_MOCK_MODE=true` in `.env`.
- `ai/gemini_client.py` will return canned, compliant JSON payloads without hitting Google's API endpoints.
- Real API calls are only made when `GEMINI_MOCK_MODE=false` and a valid `GEMINI_API_KEY` is present.

---

## 5. Running AI Unit Tests & Evals

```bash
# Run all unit tests
pytest ai/

# Run the prompt quality evaluation harness
python ai/evals/run_eval.py
```

---

## 6. Experience Range Parser (AI-05)

File: `ai/extraction/experience_parser.py`

`parse_experience(text)` extracts years of experience from messy job text and returns `ExperienceResult(min_experience, max_experience, opportunity_type, confidence, source)`.

- **Rules first:** Regex rules handle ranges (`2-4 years`), minimum (`3+ years`), maximum (`up to 2 years`), months (`6 months` = 0.5 years), and number words (`two to four years`).
- **Hard cases:** Numbers that are not experience requirements are ignored (`6 months internship`, `10 year old company`, `5 years ago`, `bond of 2 years`).
- **`opportunity_type`:** one of `fresher`, `internship`, `experienced`, `unknown`.
- **`max_experience = None`** means there is no upper limit (e.g. `5+ years`).
- **AI fallback is OFF by default.** It runs only when `use_ai=True`, a client (such as `GeminiClient`) is passed, and the rule confidence is below 0.6. If the AI reply is invalid, the rule result is returned.

```python
from ai.extraction.experience_parser import parse_experience

parse_experience("2-4 years of experience")
# ExperienceResult(min_experience=2.0, max_experience=4.0,
#                  opportunity_type='experienced', confidence=0.9, source='rules')
```

Tests: `pytest ai/evals/test_experience_parser.py` (40 rules-only phrases plus mock-client AI tests).