"""
Test fixtures and configuration for backend pytest suite.
"""

import os
import pytest
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
