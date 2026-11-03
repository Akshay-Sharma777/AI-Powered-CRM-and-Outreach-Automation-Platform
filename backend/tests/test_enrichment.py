
import pytest
from types import SimpleNamespace
from backend.app.services.enrichment_service import save_enrichment_request

from backend.app.main import app
from backend.app.core.security import get_current_user
from backend.app.services.enrichment_service import validate_credit_confirmation


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {
        "id": "test-user",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "researcher",
    }

    yield

    app.dependency_overrides.pop(get_current_user, None)


def test_enrichment_missing_confirmed_credits_returns_422(client):
    response = client.post(
        "/api/v1/leads/1/enrich",
        json={"provider": "contactout"}
    )

    assert response.status_code == 422


def test_monthly_credit_budget_exceeded(monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.enrichment_service.get_settings",
        lambda: SimpleNamespace(MONTHLY_CREDIT_BUDGET=5)
    )

    with pytest.raises(
        ValueError,
        match="Monthly credit budget exceeded"
    ):
        validate_credit_confirmation(
            estimated_credits=1,
            confirmed_credits=1,
            monthly_used=5
        )

def test_enrichment_request_saves_provider_and_timestamp():
    class FakeCursor:
        def execute(self, query, params):
            self.query = query
            self.params = params

        def fetchone(self):
            return (101,)

    cursor = FakeCursor()

    request_id = save_enrichment_request(
        cur=cursor,
        lead_id=1,
        provider="contactout",
        credits_used=1
    )

    assert request_id == 101
    assert "provider" in cursor.query
    assert "created_at" in cursor.query
    assert "NOW()" in cursor.query
    assert cursor.params == (1, "contactout", 1, "completed")
