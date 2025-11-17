"""In-memory session manager for the MVP."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from fastapi import HTTPException, status

from app.config import get_settings
from app.core.security import compute_expiration, ensure_session_is_active, generate_session_token
from app.models.domain import LearnerProfile, LearningNode, Question, SessionState
from app.services.data_provider import provider


PREFERENCE_KEYS = {"creativity", "analysis", "communication", "problem_solving", "wellbeing"}


class SessionManager:
    """Stores sessions in memory and runs the adaptive logic."""

    def __init__(self) -> None:
        self._sessions: Dict[str, SessionState] = {}
        self._settings = get_settings()

    # Session lifecycle -------------------------------------------------
    def create_session(self, display_name: Optional[str] = None) -> SessionState:
        session_id = generate_session_token()
        now = datetime.utcnow()
        profile = LearnerProfile(display_name=display_name, preferences=self._initial_vector())
        session = SessionState(
            id=session_id,
            profile=profile,
            created_at=now,
            expires_at=compute_expiration(self._settings.session_ttl_minutes),
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> SessionState:
        session = self._sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
        ensure_session_is_active(session.expires_at)
        return session

    # Question flow ----------------------------------------------------
    def get_next_question(self, session_id: str) -> Optional[Question]:
        session = self.get_session(session_id)
        if session.question_index >= len(provider.questions):
            return None
        return provider.questions[session.question_index]

    def submit_question_answer(self, session_id: str, question_id: str, sanitized_answer: str) -> Question:
        session = self.get_session(session_id)
        question = self._ensure_question(question_id)
        if question.id in session.asked_questions:
            raise HTTPException(status_code=400, detail="Question already answered.")

        self._update_preferences(session, question)
        session.conversation_log.append({"question_id": question.id, "answer": sanitized_answer})
        session.asked_questions.append(question.id)
        session.question_index += 1

        if session.question_index >= len(provider.questions):
            session.current_node_id = self._choose_first_node(session)

        return question

    # Node flow --------------------------------------------------------
    def get_node(self, session_id: str, node_id: str) -> LearningNode:
        session = self.get_session(session_id)
        node = self._ensure_node(node_id)
        session.current_node_id = node.id
        return node

    def submit_node_answer(self, session_id: str, node_id: str, reward_multiplier: float) -> LearningNode:
        session = self.get_session(session_id)
        node = self._ensure_node(node_id)
        if node.id not in session.profile.completed_nodes:
            session.profile.completed_nodes.append(node.id)
            session.reward_points += int(node.reward_on_completion * reward_multiplier)
        session.current_node_id = self._select_next_node(node)
        return node

    # Profile ----------------------------------------------------------
    def get_profile(self, session_id: str) -> LearnerProfile:
        session = self.get_session(session_id)
        return session.profile

    # Internal helpers -------------------------------------------------
    def _initial_vector(self) -> Dict[str, float]:
        return {key: 0.0 for key in PREFERENCE_KEYS}

    def _ensure_question(self, question_id: str) -> Question:
        for question in provider.questions:
            if question.id == question_id:
                return question
        raise HTTPException(status_code=404, detail="Question not found.")

    def _ensure_node(self, node_id: str) -> LearningNode:
        node = provider.nodes.get(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found.")
        return node

    def _update_preferences(self, session: SessionState, question: Question) -> None:
        for key, weight in question.weights.items():
            current = session.profile.preferences.get(key, 0.0)
            session.profile.preferences[key] = current + float(weight)

    def _choose_first_node(self, session: SessionState) -> Optional[str]:
        if not provider.nodes:
            return None
        # Select node whose category has the highest score
        sorted_categories = sorted(
            session.profile.preferences.items(), key=lambda item: item[1], reverse=True
        )
        for category, _ in sorted_categories:
            for node in provider.nodes.values():
                if node.category == category:
                    return node.id
        # Fallback: return first node
        return next(iter(provider.nodes.values())).id

    def _select_next_node(self, current_node: LearningNode) -> Optional[str]:
        for next_node_id in current_node.next_nodes:
            if next_node_id in provider.nodes:
                return next_node_id
        return None


session_manager = SessionManager()
