"""Shared pytest fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.main import app
from app.services import TaskService, task_service
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _reset_store() -> Iterator[None]:
    """Ensure every test runs against a clean in-memory store."""
    fresh = TaskService()
    task_service.__dict__.update(fresh.__dict__)
    return


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
