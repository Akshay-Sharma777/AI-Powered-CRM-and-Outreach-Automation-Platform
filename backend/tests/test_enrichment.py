
import pytest
from types import SimpleNamespace
from backend.app.services.enrichment_service import save_enrichment_request

from backend.app.main import app
from backend.app.core.security import get_current_user
from backend.app.services.enrichment_service import validate_credit_confirmation
from backend.app.services.enrichment_service import save_enriched_contact


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


def test_enrichment_missing_confirmed_credits_returns_422(
    client, monkeypatch
):
    def fail_if_called(*args, **kwargs):
        pytest.fail("Database operation should not be called")

    monkeypatch.setattr(
        "backend.app.api.v1.enrichment.enrich_lead",
        fail_if_called
    )

    monkeypatch.setattr(
        "backend.app.services.enrichment_service.get_conn",
        fail_if_called
    )

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

def test_enriched_contact_is_saved():
    class FakeCursor:
        def execute(self, query, params):
            self.query = query
            self.params = params

        def fetchone(self):
            return (201,)

    cursor = FakeCursor()

    contact_id = save_enriched_contact(
        cur=cursor,
        lead_id=1,
        contact={
            "email": "jane@example.com",
            "phone": "9876543210"
        },
        provider="contactout"
    )

    assert contact_id == 201
    assert "INSERT INTO contacts" in cursor.query
    assert cursor.params == (
        1,
        "jane@example.com",
        "9876543210",
        "contactout"
    )