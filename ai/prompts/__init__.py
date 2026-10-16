"""
Prompt Versioning and Loading Module.
"""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent
CURRENT_PROMPT_VERSION = "1.0.0"


def load_prompt(name: str, version: str = "v1") -> str:
    """Loads prompt template by name and version."""
    filename = f"{name}_{version}.md"
    target_path = PROMPTS_DIR / filename
    if not target_path.exists():
        raise FileNotFoundError(f"Prompt '{filename}' not found in {PROMPTS_DIR}")
    return target_path.read_text(encoding="utf-8")
