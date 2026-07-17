"""Pydantic models exposed by the API."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class Task(TaskCreate):
    """A task tracked by the service."""

    id: int
    completed: bool = False
    created_at: datetime = Field(default_factory=_utcnow)


class HealthResponse(BaseModel):
    """Health probe response."""

    status: str = "ok"
    service: str
    environment: str
    version: str
