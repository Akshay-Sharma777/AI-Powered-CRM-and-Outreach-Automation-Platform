"""
Unit tests covering Health check and middleware functionality (BE-01).
"""


def test_health_endpoint(client):
    """Tests GET /api/v1/health returns healthy status and version."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
    # Test X-Correlation-ID is set by middleware
    assert "x-correlation-id" in response.headers


def test_system_health_endpoint(client):
    """Tests GET /api/v1/system/health returns system operational metrics."""
    response = client.get("/api/v1/system/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "daily_credit_budget" in data
    assert "monthly_credit_budget" in data


def test_root_endpoint(client):
    """Tests GET / returns API metadata and links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "docs" in data
    assert "health" in data
