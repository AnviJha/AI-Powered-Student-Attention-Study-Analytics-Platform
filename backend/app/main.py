"""Phase 2 study API. No camera, AI provider, or demo fixture ingestion."""
import os
from datetime import datetime, timedelta, timezone
from functools import lru_cache

import bcrypt
from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field, field_validator
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.services.analytics import summarize
from app.services.engagement import score_digital
from app.services.planner import recommend_plan, break_check

app = FastAPI(title="Student Study Analytics API", version="0.1.0")


@app.exception_handler(PyMongoError)
async def database_unavailable(_request: Request, _error: PyMongoError):
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})

app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in os.getenv(
    "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()],
    allow_credentials=False, allow_methods=["GET", "POST", "PATCH"], allow_headers=["Authorization", "Content-Type"])
bearer = HTTPBearer()


def utcnow():
    return datetime.now(timezone.utc)


@lru_cache
def get_client():
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError("MONGO_URI is required for database routes")
    return MongoClient(uri, tz_aware=True, serverSelectionTimeoutMS=3000)


def get_db():
    db = get_client()[os.getenv("MONGO_DB", "study_attention")]
    db.users.create_index("email", unique=True)
    db.sessions.create_index([("user_id", ASCENDING), ("started_at", ASCENDING)])
    db.attention_records.create_index([("user_id", ASCENDING), ("session_id", ASCENDING), ("captured_at", ASCENDING)])
    db.distractions.create_index([("user_id", ASCENDING), ("session_id", ASCENDING), ("occurred_at", ASCENDING)])
    return db


def secret():
    value = os.getenv("JWT_SECRET")
    if not value or len(value) < 32:
        raise RuntimeError("JWT_SECRET must contain at least 32 characters")
    return value


def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db=Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, secret(), algorithms=["HS256"])
        user_id = payload["sub"]
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except (JWTError, KeyError, ValueError, TypeError):
        raise HTTPException(401, "Invalid or expired token") from None
    if not user:
        raise HTTPException(401, "Account not found")
    return user


def oid(value):
    if not ObjectId.is_valid(value):
        raise HTTPException(400, "Invalid ID")
    return ObjectId(value)


def owned_session(db, user, session_id):
    session = db.sessions.find_one({"_id": oid(session_id), "user_id": str(user["_id"])})
    if not session:
        raise HTTPException(404, "Session not found")
    return session


def session_out(session):
    active_seconds = session.get("active_seconds", 0)
    if session["status"] == "active" and session.get("active_since"):
        active_seconds += max(0, int((utcnow() - session["active_since"]).total_seconds()))
    return {"id": str(session["_id"]), "subject": session["subject"], "topic": session.get("topic"),
            "goal_minutes": session["goal_minutes"], "status": session["status"],
            "started_at": session["started_at"].isoformat(),
            "ended_at": session["ended_at"].isoformat() if session.get("ended_at") else None,
            "active_seconds": active_seconds, "estimated_focused_seconds": None}


class Register(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    password: str = Field(min_length=10, max_length=72)

    @field_validator("password")
    @classmethod
    def password_bytes(cls, value):
        if len(value.encode()) > 72:
            raise ValueError("Password exceeds bcrypt's 72-byte limit")
        return value


class Login(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    daily_goal_minutes: int | None = Field(default=None, ge=30, le=720)
    preferred_session_minutes: int | None = Field(default=None, ge=10, le=180)
    notifications_enabled: bool | None = None


class SessionCreate(BaseModel):
    subject: str = Field(min_length=1, max_length=100)
    topic: str | None = Field(default=None, max_length=150)
    goal_minutes: int = Field(default=45, ge=10, le=180)


class DigitalSnapshot(BaseModel):
    mouse_moves: int = Field(default=0, ge=0, le=10000)
    mouse_clicks: int = Field(default=0, ge=0, le=1000)
    keyboard_events: int = Field(default=0, ge=0, le=10000)
    tab_visible: bool = True
    idle_seconds: float = Field(default=0, ge=0, le=86400)


class DistractionCreate(BaseModel):
    category: str = Field(pattern="^(looking_away|face_absent|phone_signal|tab_hidden|idle|other)$")
    detail: str | None = Field(default=None, max_length=200)


def public_user(user):
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"],
            "daily_goal_minutes": user.get("daily_goal_minutes", 240),
            "preferred_session_minutes": user.get("preferred_session_minutes", 45),
            "notifications_enabled": user.get("notifications_enabled", True)}


def token_for(user):
    return jwt.encode({"sub": str(user["_id"]), "exp": utcnow() + timedelta(hours=12)}, secret(), algorithm="HS256")


@app.get("/api/health")
def health():
    return {"status": "ok", "phase": 2}


@app.post("/api/auth/register", status_code=201)
def register(body: Register, db=Depends(get_db)):
    doc = {"name": body.name.strip(), "email": body.email.lower(),
           "password_hash": bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode(),
           "daily_goal_minutes": 240, "preferred_session_minutes": 45,
           "notifications_enabled": True, "created_at": utcnow()}
    if not doc["name"]:
        raise HTTPException(422, "Name cannot be blank")
    try:
        doc["_id"] = db.users.insert_one(doc).inserted_id
    except DuplicateKeyError:
        raise HTTPException(409, "Email already registered") from None
    return {"access_token": token_for(doc), "token_type": "bearer", "user": public_user(doc)}


@app.post("/api/auth/login")
def login(body: Login, db=Depends(get_db)):
    user = db.users.find_one({"email": body.email.lower()})
    if not user or not bcrypt.checkpw(body.password.encode(), user["password_hash"].encode()):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": token_for(user), "token_type": "bearer", "user": public_user(user)}


@app.get("/api/profile")
def profile(user=Depends(current_user)):
    return public_user(user)


@app.patch("/api/profile")
def update_profile(body: ProfileUpdate, user=Depends(current_user), db=Depends(get_db)):
    changes = body.model_dump(exclude_unset=True)
    if "name" in changes and not changes["name"].strip():
        raise HTTPException(422, "Name cannot be blank")
    if changes:
        db.users.update_one({"_id": user["_id"]}, {"$set": changes})
    return public_user(db.users.find_one({"_id": user["_id"]}))


@app.post("/api/sessions", status_code=201)
def start_session(body: SessionCreate, user=Depends(current_user), db=Depends(get_db)):
    if not body.subject.strip():
        raise HTTPException(422, "Subject cannot be blank")
    now = utcnow()
    doc = {"user_id": str(user["_id"]), "subject": body.subject.strip(), "topic": body.topic,
           "goal_minutes": body.goal_minutes, "status": "active", "started_at": now,
           "active_since": now, "active_seconds": 0, "ended_at": None}
    doc["_id"] = db.sessions.insert_one(doc).inserted_id
    return session_out(doc)


@app.get("/api/sessions")
def list_sessions(user=Depends(current_user), db=Depends(get_db)):
    return [session_out(s) for s in db.sessions.find({"user_id": str(user["_id"])}).sort("started_at", -1).limit(100)]


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str, user=Depends(current_user), db=Depends(get_db)):
    return session_out(owned_session(db, user, session_id))


@app.post("/api/sessions/{session_id}/status/{action}")
def change_session(session_id: str, action: str, user=Depends(current_user), db=Depends(get_db)):
    if action not in {"pause", "resume", "end"}:
        raise HTTPException(404, "Unknown session action")
    session = owned_session(db, user, session_id)
    expected = "paused" if action == "resume" else "active" if action == "pause" else None
    if expected and session["status"] != expected or action == "end" and session["status"] == "ended":
        raise HTTPException(409, "Invalid session transition")
    now = utcnow()
    updates = {}
    if session["status"] == "active":
        updates["active_seconds"] = session.get("active_seconds", 0) + max(0, int((now - session["active_since"]).total_seconds()))
    if action == "pause":
        updates.update(status="paused", active_since=None)
    elif action == "resume":
        updates.update(status="active", active_since=now)
    else:
        updates.update(status="ended", active_since=None, ended_at=now)
    result = db.sessions.find_one_and_update(
        {"_id": session["_id"], "user_id": str(user["_id"]), "status": session["status"]},
        {"$set": updates}, return_document=True)
    if not result:
        raise HTTPException(409, "Session changed; retry")
    return session_out(result)


@app.post("/api/sessions/{session_id}/digital-records", status_code=201)
def add_digital_record(session_id: str, body: DigitalSnapshot, user=Depends(current_user), db=Depends(get_db)):
    session = owned_session(db, user, session_id)
    if session["status"] != "active":
        raise HTTPException(409, "Session is not active")
    score = score_digital(**body.model_dump())
    doc = {"user_id": str(user["_id"]), "session_id": session_id, "captured_at": utcnow(),
           "visual_attention_score": None, **score}
    db.attention_records.insert_one(doc)
    return {"captured_at": doc["captured_at"].isoformat(), **score,
            "visual_attention_score": None, "combined_study_engagement": None}


@app.get("/api/sessions/{session_id}/attention-records")
def attention_records(session_id: str, user=Depends(current_user), db=Depends(get_db)):
    owned_session(db, user, session_id)
    return [{"captured_at": r["captured_at"].isoformat(),
             "digital_engagement_score": r.get("digital_engagement_score"),
             "visual_attention_score": r.get("visual_attention_score"),
             "reasons": r.get("reasons", [])} for r in db.attention_records.find(
                 {"user_id": str(user["_id"]), "session_id": session_id}).sort("captured_at", 1).limit(1000)]


@app.post("/api/sessions/{session_id}/distractions", status_code=201)
def add_distraction(session_id: str, body: DistractionCreate, user=Depends(current_user), db=Depends(get_db)):
    session = owned_session(db, user, session_id)
    if session["status"] != "active":
        raise HTTPException(409, "Session is not active")
    doc = {"user_id": str(user["_id"]), "session_id": session_id,
           "category": body.category, "detail": body.detail, "occurred_at": utcnow(),
           "source": "client_reported"}
    doc["_id"] = db.distractions.insert_one(doc).inserted_id
    return {"id": str(doc["_id"]), "category": body.category, "occurred_at": doc["occurred_at"].isoformat(),
            "source": doc["source"]}


@app.get("/api/analytics")
def analytics(period: str = Query(default="daily", pattern="^(daily|weekly|monthly)$"),
              user=Depends(current_user), db=Depends(get_db)):
    query = {"user_id": str(user["_id"])}
    sessions = list(db.sessions.find(query))
    for session in sessions:
        if session["status"] == "active" and session.get("active_since"):
            session["active_seconds"] = session.get("active_seconds", 0) + max(0, int((utcnow() - session["active_since"]).total_seconds()))
    return summarize(sessions, list(db.attention_records.find(query)),
                     list(db.distractions.find(query)), period)


@app.get("/api/focus/plan")
def focus_plan(elapsed_minutes: float | None = Query(default=None, ge=0),
               session_id: str | None = None, user=Depends(current_user), db=Depends(get_db)):
    if session_id:
        owned_session(db, user, session_id)
    records = list(db.attention_records.find({"user_id": str(user["_id"])}).sort("captured_at", -1).limit(30))
    records.reverse()
    # Phase 2 has no validated visual signal. Plan from digital engagement only.
    scores = [r["digital_engagement_score"] for r in records if r.get("digital_engagement_score") is not None]
    plan = recommend_plan(scores)
    plan["score_source"] = "digital_engagement"
    if elapsed_minutes is not None:
        recent = [r["digital_engagement_score"] for r in records if r.get("session_id") == session_id] if session_id else scores
        plan["break_check"] = break_check(elapsed_minutes, plan["focus_minutes"], recent)
    return plan
