from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_webhook_alert_creates_ticket():
    payload = {
        "name": "CPU high",
        "severity": "critical",
        "source": "grafana",
        "details": "CPU > 90%"
    }

    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ticket_created"
    assert data["alert"]["name"] == "CPU high"
    assert data["alert"]["metadata"]["processed_by"] == "automation_engine"
    assert data["itsm_result"]["status"] == "mocked"


def test_webhook_alert_ignored_when_low_severity():
    payload = {
        "name": "Disk info",
        "severity": "low",
        "source": "grafana",
        "details": "Disk usage at 40%"
    }

    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ignored"
    assert data["reason"] == "severity below threshold"
