from fastapi.testclient import TestClient


def test_liveness_endpoint(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200


def test_readiness_endpoint(client: TestClient) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/health/metrics")

    assert response.status_code == 200
