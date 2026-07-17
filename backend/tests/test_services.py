"""Unit tests for the TaskService business logic."""

from __future__ import annotations

import pytest
from app.models import TaskCreate, TaskUpdate
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


def test_update_changes_title_and_description() -> None:
    service = TaskService()
    task = service.create_task(TaskCreate(title="a", description="old"))
    updated = service.update_task(task.id, TaskUpdate(title="b", description="new"))
    assert (updated.title, updated.description) == ("b", "new")


def test_update_preserves_omitted_fields() -> None:
    service = TaskService()
    task = service.create_task(TaskCreate(title="a", description="old"))
    updated = service.update_task(task.id, TaskUpdate(title="b"))
    assert (updated.title, updated.description) == ("b", "old")


def test_update_unknown_raises() -> None:
    service = TaskService()
    with pytest.raises(TaskNotFoundError):
        service.update_task(42, TaskUpdate(title="b"))


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
