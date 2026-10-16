"""
Test fixtures and configuration for backend pytest suite.
"""

import os
import sys
from pathlib import Path
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["ENVIRONMENT"] = "testing"
os.environ["SECRET_KEY"] = "test-secret-key-for-unit-testing-min-32-chars-long!"
os.environ["GEMINI_MOCK_MODE"] = "true"

from backend.app.main import app


@pytest.fixture(scope="session")
def client():
    """Provides a TestClient instance for API tests."""
    with TestClient(app) as test_client:
        yield test_client
