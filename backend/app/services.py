"""Business logic for the tasks domain.

An intentionally small, dependency-free in-memory store so that the whole
SDLC pipeline (tests, build, deploy) has real behaviour to exercise.
"""

from __future__ import annotations

from itertools import count
from threading import Lock

from app.models import Task, TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a task id does not exist."""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task {task_id} not found")
        self.task_id = task_id


class TaskService:
    """Thread-safe in-memory task repository."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._ids = count(1)
        self._lock = Lock()

    def list_tasks(self) -> list[Task]:
        with self._lock:
            return sorted(self._tasks.values(), key=lambda task: task.id)

    def create_task(self, payload: TaskCreate) -> Task:
        with self._lock:
            task_id = next(self._ids)
            task = Task(id=task_id, **payload.model_dump())
            self._tasks[task_id] = task
            return task

    def get_task(self, task_id: int) -> Task:
        with self._lock:
            try:
                return self._tasks[task_id]
            except KeyError as exc:
                raise TaskNotFoundError(task_id) from exc

    def complete_task(self, task_id: int) -> Task:
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(task_id)
            task = self._tasks[task_id].model_copy(update={"completed": True})
            self._tasks[task_id] = task
            return task

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task:
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(task_id)
            updates = payload.model_dump(exclude_unset=True, exclude_none=True)
            task = self._tasks[task_id].model_copy(update=updates)
            self._tasks[task_id] = task
            return task

    def delete_task(self, task_id: int) -> None:
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(task_id)
            del self._tasks[task_id]


# Module-level singleton used by the API layer.
task_service = TaskService()
