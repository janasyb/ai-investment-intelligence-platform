from app.main import app


def test_application_exposes_expected_routes() -> None:
    paths = set(app.openapi()["paths"])

    assert "/" in paths
    assert "/health/live" in paths
    assert "/health/ready" in paths
    assert "/health/metrics" in paths
