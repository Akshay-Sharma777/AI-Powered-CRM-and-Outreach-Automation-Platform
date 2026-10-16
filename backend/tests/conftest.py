"""
Test fixtures and configuration for backend pytest suite.
"""

import os
import sys
from pathlib import Path
import pytest

# Ensure repository root and backend directories are on sys.path
CWD = Path.cwd().resolve()
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = REPO_ROOT / "backend"

for p in (CWD, REPO_ROOT, BACKEND_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["ENVIRONMENT"] = "testing"
os.environ["SECRET_KEY"] = "test-secret-key-for-unit-testing-min-32-chars-long!"
os.environ["GEMINI_MOCK_MODE"] = "true"

try:
    from backend.app.main import app
except ModuleNotFoundError:
    from app.main import app


@pytest.fixture(scope="session")
def client():
    """Provides a TestClient instance for API tests."""
    with TestClient(app) as test_client:
        yield test_client
