import pytest
from fastapi.testclient import TestClient

from app.main import app


VALID_PAYLOAD = {
    "type_machine": "compresseur",
    "age_machine_jours": 1500,
    "derniere_maintenance_jours": 45,
    "temperature_moyenne": 68.5,
    "vibration_moyenne": 3.2,
    "pression_moyenne": 7.8,
    "nb_incidents_3_mois": 2,
}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_predict_valid_payload(client: TestClient) -> None:
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200

    body = response.json()

    assert body["criticite"] in {"basse", "moyenne", "haute"}

    probabilites = body["probabilites"]

    assert set(probabilites.keys()) == {"basse", "moyenne", "haute"}
    assert sum(probabilites.values()) == pytest.approx(1.0, abs=1e-6)

    for probabilite in probabilites.values():
        assert 0.0 <= probabilite <= 1.0


def test_predict_invalid_machine_type(client: TestClient) -> None:
    payload = {
        **VALID_PAYLOAD,
        "type_machine": "voiture",
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "machine_type",
    [
        "pompe",
        "compresseur",
        "convoyeur",
        "presse",
        "four",
    ],
)
def test_predict_accepts_all_machine_types(
    client: TestClient,
    machine_type: str,
) -> None:
    payload = {
        **VALID_PAYLOAD,
        "type_machine": machine_type,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["criticite"] in {
        "basse",
        "moyenne",
        "haute",
    }