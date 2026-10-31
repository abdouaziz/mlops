from fastapi.testclient import TestClient

from app.main import app


def test_health():
    # Sans bloc "with", le lifespan ne tourne pas : les modèles ne sont pas chargés
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
