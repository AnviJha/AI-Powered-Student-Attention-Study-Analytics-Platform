import os
import mongomock
import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from jose import jwt
from pymongo.errors import ServerSelectionTimeoutError

from app.main import app, get_db


@pytest.fixture
def client():
    os.environ["JWT_SECRET"] = "test-secret-that-is-long-enough-for-hs256"
    db = mongomock.MongoClient(tz_aware=True).study_test
    db.users.create_index("email", unique=True)
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def register(client, email):
    response = client.post("/api/auth/register", json={"name":"Student", "email":email, "password":"password1234"})
    assert response.status_code == 201, response.text
    return {"Authorization": "Bearer " + response.json()["access_token"]}


def test_auth_profile_and_validation(client):
    assert client.get("/api/profile").status_code in (401, 403)
    headers = register(client, "one@example.com")
    assert client.get("/api/profile", headers=headers).json()["name"] == "Student"
    assert client.patch("/api/profile", headers=headers, json={"daily_goal_minutes": 10}).status_code == 422
    assert client.patch("/api/profile", headers=headers, json={"daily_goal_minutes": 180}).json()["daily_goal_minutes"] == 180
    assert client.post("/api/auth/login", json={"email":"one@example.com", "password":"wrong"}).status_code == 401
    assert client.patch("/api/profile", headers=headers, json={"time_zone":"Not/AZone"}).status_code == 422
    assert client.patch("/api/profile", headers=headers, json={"time_zone":"Asia/Kolkata"}).json()["time_zone"] == "Asia/Kolkata"
    assert client.post("/api/auth/register", json={"name":"Again", "email":"one@example.com", "password":"password1234"}).status_code == 409
    expired = jwt.encode({"sub": client.get("/api/profile", headers=headers).json()["id"],
                          "exp": datetime.now(timezone.utc) - timedelta(seconds=1)}, os.environ["JWT_SECRET"], algorithm="HS256")
    assert client.get("/api/profile", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_owned_sessions_records_and_empty_analytics(client):
    a = register(client, "a@example.com")
    b = register(client, "b@example.com")
    assert client.get("/api/analytics", headers=a).json()["data_status"] == "empty"
    started = client.post("/api/sessions", headers=a, json={"subject":"Algebra", "topic":"Matrices", "goal_minutes":45})
    assert started.status_code == 201, started.text
    sid = started.json()["id"]
    assert client.post("/api/sessions", headers=a, json={"subject":"Another"}).status_code == 409
    assert client.get(f"/api/sessions/{sid}", headers=b).status_code == 404
    assert client.post(f"/api/sessions/{sid}/digital-records", headers=b, json={}).status_code == 404
    recorded = client.post(f"/api/sessions/{sid}/digital-records", headers=a, json={"mouse_moves":100})
    assert recorded.status_code == 201, recorded.text
    assert recorded.json()["visual_attention_score"] is None
    assert client.post(f"/api/sessions/{sid}/distractions", headers=a, json={"category":"idle"}).status_code == 201
    assert client.post(f"/api/sessions/{sid}/status/pause", headers=a).json()["status"] == "paused"
    assert client.post(f"/api/sessions/{sid}/status/pause", headers=a).status_code == 409
    assert client.post(f"/api/sessions/{sid}/status/resume", headers=a).json()["status"] == "active"
    assert client.post(f"/api/sessions/{sid}/status/end", headers=a).json()["status"] == "ended"
    report = client.get("/api/analytics?period=daily", headers=a).json()
    assert report["session_count"] == 1
    assert report["potential_distraction_count"] == 1
    assert report["average_visual_attention_score"] is None
    assert client.get("/api/focus/plan", headers=a).json()["score_source"] == "digital_engagement"
    assert client.get(f"/api/focus/plan?session_id={sid}", headers=b).status_code == 404
    assert client.get("/api/sessions/not-an-id", headers=a).status_code == 400
    assert client.post(f"/api/sessions/{sid}/digital-records", headers=a, json={"idle_seconds":-1}).status_code == 422
    assert client.post(f"/api/sessions/{sid}/distractions", headers=a, json={"category":"diagnosis"}).status_code == 422
    assert client.get("/api/analytics?period=yearly", headers=a).status_code == 422
    assert client.get(f"/api/sessions/{sid}/attention-records", headers=b).status_code == 404
    assert client.get("/api/analytics", headers=b).json()["session_count"] == 0


def test_database_failure_returns_503(client):
    app.dependency_overrides[get_db] = lambda: (_ for _ in ()).throw(ServerSelectionTimeoutError("offline"))
    response = client.post("/api/auth/login", json={"email":"one@example.com", "password":"password1234"})
    assert response.status_code == 503
    assert response.json() == {"detail":"Database unavailable"}
