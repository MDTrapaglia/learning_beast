"""Helper functions to load static data for the MVP."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from fastapi import HTTPException, status

from app.config import get_settings
from app.models.domain import LearningNode, Question


class StaticDataProvider:
    """Loads questions and learning nodes from JSON fixtures."""

    def __init__(self) -> None:
        settings = get_settings()
        self._questions_path = settings.data_dir / "questions.json"
        self._nodes_path = settings.data_dir / "nodes.json"
        self._questions: List[Question] = []
        self._nodes: Dict[str, LearningNode] = {}
        self._load_all()

    @property
    def questions(self) -> List[Question]:
        return self._questions

    @property
    def nodes(self) -> Dict[str, LearningNode]:
        return self._nodes

    def _load_all(self) -> None:
        self._questions = [Question(**item) for item in self._read_json(self._questions_path)]
        raw_nodes = self._read_json(self._nodes_path)
        self._nodes = {node["id"]: LearningNode(**node) for node in raw_nodes}

    @staticmethod
    def _read_json(path: Path):  # type: ignore[override]
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Missing data file: {path}",
            )
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)


provider = StaticDataProvider()
