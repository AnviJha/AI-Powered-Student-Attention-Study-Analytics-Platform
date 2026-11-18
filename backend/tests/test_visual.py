from datetime import timedelta

from app.services.visual import summarize_visual_window
from test_api import client, register


def test_visual_scoring_and_missing_quality():
    assert summarize_visual_window(20, 20, 20, 20)["visual_signal_index"] == 100
    assert summarize_visual_window(20, 20, 0, 0)["visual_signal_index"] == 0
    assert summarize_visual_window(20, 8, 8, 8)["visual_signal_index"] is None
    assert summarize_visual_window(20, 10, 10, 5)["visual_signal_index"] == 70


def test_visual_consent_validation_ownership_expiry_and_deletion(client):
    a = register(client, "visual-a@example.com")
    b = register(client, "visual-b@example.com")
    sid = client.post("/api/sessions", headers=a, json={"subject": "Calculus"}).json()["id"]
    url = f"/api/sessions/{sid}"
    payload = {"algorithm_version": "face-presence-head-orientation-v1", "total_samples": 20,
               "valid_samples": 20, "face_samples": 18, "forward_samples": 12}
    assert client.post(f"{url}/visual-records", headers=a, json=payload).status_code == 409
    assert client.post(f"{url}/visual-consent", headers=b).status_code == 404
    assert client.post(f"{url}/visual-consent", headers=a).status_code == 200
    assert client.post(f"{url}/visual-records", headers=b, json=payload).status_code == 404
    assert client.post(f"{url}/visual-records", headers=a, json={**payload, "visual_attention_score": 100}).status_code == 422
    assert client.post(f"{url}/visual-records", headers=a, json={**payload, "forward_samples": 19}).status_code == 422
    result = client.post(f"{url}/visual-records", headers=a, json=payload)
    assert result.status_code == 201, result.text
    assert result.json()["visual_signal_index"] == 72
    assert result.json()["visual_attention_score"] is None
    assert client.post(f"{url}/visual-records", headers=a, json=payload).status_code == 429
    assert len(client.get(f"{url}/visual-records", headers=a).json()) == 1
    assert client.get(f"{url}/visual-records", headers=b).status_code == 404
    from app.main import get_db
    db = client.app.dependency_overrides[get_db]()
    doc = db.visual_records.find_one({"session_id": sid})
    assert timedelta(days=89) < doc["expires_at"] - doc["captured_at"] <= timedelta(days=90)
    assert client.delete(f"{url}/visual-records", headers=b).status_code == 404
    assert client.delete(f"{url}/visual-records", headers=a).json()["deleted_count"] == 1
    assert client.delete(f"{url}/visual-consent", headers=a).json()["active"] is False
    assert client.post(f"{url}/visual-records", headers=a, json=payload).status_code == 409
    assert client.post(f"{url}/visual-consent", headers=a).status_code == 200
    assert client.post(f"{url}/status/pause", headers=a).status_code == 200
    assert client.post(f"{url}/visual-records", headers=a, json=payload).status_code == 409
