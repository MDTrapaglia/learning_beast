"""Domain models used throughout the application."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Question(BaseModel):
    id: str
    prompt: str
    follow_up: str
    category: str
    weights: Dict[str, float]
    sample_answers: List[str] = Field(default_factory=list)


class LearningNode(BaseModel):
    id: str
    title: str
    summary: str
    category: str
    activity_type: str
    content: str
    estimated_minutes: int
    reward_on_completion: int
    next_nodes: List[str] = Field(default_factory=list)


class LearnerProfile(BaseModel):
    display_name: Optional[str] = None
    preferences: Dict[str, float] = Field(default_factory=dict)
    completed_nodes: List[str] = Field(default_factory=list)


class SessionStartRequest(BaseModel):
    """Payload expected when the client inicia una sesión."""

    display_name: Optional[str] = Field(
        default=None,
        max_length=80,
        description="Nombre opcional para mostrar dentro de la sesión.",
    )


class SessionState(BaseModel):
    id: str
    profile: LearnerProfile
    current_node_id: Optional[str] = None
    asked_questions: List[str] = Field(default_factory=list)
    question_index: int = 0
    conversation_log: List[Dict[str, str]] = Field(default_factory=list)
    created_at: datetime
    expires_at: datetime
    reward_points: int = 0


class QuestionResponse(BaseModel):
    answer: str


class NodeAnswer(BaseModel):
    answer: str
    confidence: Optional[float] = Field(
        default=0.7, ge=0.0, le=1.0, description="Self-reported confidence metric"
    )
