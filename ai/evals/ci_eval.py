"""
CI Prompt and Fact Check Evaluation Script (AI-22).
Verifies that generated drafts strictly comply with schema and fact checking.
Runs in offline mode so CI never makes external API requests.
"""

import sys
from ai.gemini_client import GeminiClient
from ai.schemas.draft_output import AIDraftOutput
from ai.validators.fact_check import fact_check_draft


def run_ci_eval():
    print("Running AI CI Evaluation Suite...")
    client = GeminiClient()

    # Sample verified facts for the test run
    verified_facts = {
        "fact_01": "Junior Python Developer",
        "fact_02": "FastAPI and Docker",
        "salary_text": "₹6,00,000 PA"
    }

    prompt = "Generate outreach draft for Junior Python Developer at Acme AI"
    output, usage = client.generate(prompt=prompt)

    # 1. Validate Schema
    try:
        validated = AIDraftOutput(**output)
        print(" [PASS] Schema validation passed.")
    except Exception as e:
        print(f" [FAIL] Schema validation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Validate Fact Checking
    is_valid, issues = fact_check_draft(output, verified_facts)
    if not is_valid:
        print(f" [FAIL] Fact checking failed: {issues}", file=sys.stderr)
        sys.exit(1)

    print(" [PASS] Anti-hallucination fact checking passed.")
    print(f"Evaluation succeeded. Token usage: {usage}")
    return 0


if __name__ == "__main__":
    sys.exit(run_ci_eval())
