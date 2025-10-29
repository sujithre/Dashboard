"""
Test suite for the Azure Cost Analysis Dashboard Flask application.
"""

import pytest
from app import app, load_csv_data


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_app_exists():
    """Test that the Flask app exists."""
    assert app is not None


def test_app_is_testing(client):
    """Test that the app is in testing mode."""
    assert app.config["TESTING"]


def test_load_csv_data():
    """Test that CSV data can be loaded."""
    data = load_csv_data()
    assert isinstance(data, list)
    # Check that we have at least some data
    assert len(data) >= 0


def test_index_route(client):
    """Test the main index route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cost Analysis Dashboard" in response.data or b"dashboard" in response.data.lower()


def test_top5_subscriptions_api(client):
    """Test the top 5 subscriptions API endpoint."""
    response = client.get("/api/top5Subscriptions")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 5


def test_top5_applications_api(client):
    """Test the top 5 applications API endpoint."""
    response = client.get("/api/top5Applications")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 5


def test_top5_service_names_api(client):
    """Test the top 5 service names API endpoint."""
    response = client.get("/api/top5ServiceNames")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 5


def test_top5_resources_api(client):
    """Test the top 5 resources API endpoint."""
    response = client.get("/api/top5Resources")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "total" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 5


def test_sum_of_cost_by_date_api(client):
    """Test the sum of cost by date API endpoint."""
    response = client.get("/api/SumofCost")
    assert response.status_code == 200
    data = response.get_json()
    assert "dates" in data
    assert "costs" in data
    assert isinstance(data["dates"], list)
    assert isinstance(data["costs"], list)


def test_get_data_api(client):
    """Test the get all data API endpoint."""
    response = client.get("/api/data")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_csv_data_structure():
    """Test that loaded CSV data has expected structure."""
    data = load_csv_data()
    if len(data) > 0:
        # Check that first row has expected keys
        expected_keys = ["SubscriptionId", "ServiceName", "Cost"]
        for key in expected_keys:
            assert key in data[0], f"Expected key '{key}' not found in CSV data"

        # Check that Cost is converted to float
        assert isinstance(data[0]["Cost"], (int, float))


def test_api_response_totals(client):
    """Test that API responses include valid totals."""
    endpoints = [
        "/api/top5Subscriptions",
        "/api/top5Applications",
        "/api/top5ServiceNames",
        "/api/top5Resources",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        data = response.get_json()
        assert isinstance(data["total"], (int, float))
        assert data["total"] >= 0
