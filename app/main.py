"""FastAPI application exposing the Learning Beast MVP."""
from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.security import sanitize_free_text
from app.models.domain import NodeAnswer, QuestionResponse
from app.services.session_manager import session_manager

app = FastAPI(title="Learning Beast", version="0.1.0", description="Adaptive learning MVP")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency -----------------------------------------------------------
def get_session_token(x_session_id: str = Header(..., alias="X-Session-Id")) -> str:
    if not x_session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing session header.")
    return x_session_id


# Routes ---------------------------------------------------------------
@app.post("/session/start")
def start_session(display_name: str | None = None):
    session = session_manager.create_session(display_name=display_name)
    question = session_manager.get_next_question(session.id)
    return {"session_id": session.id, "question": question}


@app.get("/session/{session_id}/question")
def fetch_next_question(session_id: str):
    question = session_manager.get_next_question(session_id)
    if not question:
        return {"message": "Todas las preguntas iniciales fueron respondidas."}
    return question


@app.post("/session/{session_id}/question/{question_id}")
def answer_question(session_id: str, question_id: str, payload: QuestionResponse):
    sanitized = sanitize_free_text(payload.answer)
    question = session_manager.submit_question_answer(session_id, question_id, sanitized)
    next_question = session_manager.get_next_question(session_id)
    return {"answered": question, "next_question": next_question}


@app.get("/node/{node_id}")
def get_node(node_id: str, session_id: str = Depends(get_session_token)):
    node = session_manager.get_node(session_id, node_id)
    return node


@app.post("/node/{node_id}/answer")
def answer_node(node_id: str, payload: NodeAnswer, session_id: str = Depends(get_session_token)):
    sanitized = sanitize_free_text(payload.answer)
    reward_multiplier = max(0.5, min(1.5, payload.confidence or 0.7))
    node = session_manager.submit_node_answer(session_id, node_id, reward_multiplier)
    next_node_id = session_manager.get_session(session_id).current_node_id
    return {
        "node": node,
        "sanitized_answer": sanitized,
        "next_node_id": next_node_id,
    }


@app.get("/profile/{session_id}")
def get_profile(session_id: str):
    profile = session_manager.get_profile(session_id)
    session = session_manager.get_session(session_id)
    return {"profile": profile, "reward_points": session.reward_points, "current_node": session.current_node_id}
