"""Unit tests for the TaskService business logic."""

from __future__ import annotations

import pytest
from app.models import TaskCreate
from app.services import TaskNotFoundError, TaskService


def test_create_assigns_incrementing_ids() -> None:
    service = TaskService()
    first = service.create_task(TaskCreate(title="a"))
    second = service.create_task(TaskCreate(title="b"))
    assert (first.id, second.id) == (1, 2)


def test_complete_marks_task_done() -> None:
    service = TaskService()
    task = service.create_task(TaskCreate(title="a"))
    assert service.complete_task(task.id).completed is True


def test_get_unknown_raises() -> None:
    service = TaskService()
    with pytest.raises(TaskNotFoundError):
        service.get_task(42)


def test_delete_removes_task() -> None:
    service = TaskService()
    task = service.create_task(TaskCreate(title="a"))
    service.delete_task(task.id)
    assert service.list_tasks() == []


def test_delete_unknown_raises() -> None:
    service = TaskService()
    with pytest.raises(TaskNotFoundError):
        service.delete_task(1)
