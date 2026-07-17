"""FastAPI application entrypoint."""

from __future__ import annotations

import json
import logging
from time import perf_counter

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app import __version__
from app.config import get_settings
from app.models import HealthResponse, Task, TaskCreate, TaskUpdate
from app.services import TaskNotFoundError, task_service

settings = get_settings()
access_logger = logging.getLogger("app.access")

app = FastAPI(
    title="Agentic Engineering API",
    version=__version__,
    summary="Reference backend for the agentic SDLC pipeline.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Log request metadata without including headers, query strings, or bodies."""
    started = perf_counter()
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration_ms = round((perf_counter() - started) * 1000, 2)
        if settings.environment.lower() == "production":
            access_logger.info(
                json.dumps(
                    {
                        "method": request.method,
                        "path": request.url.path,
                        "status": status_code,
                        "duration_ms": duration_ms,
                    },
                    separators=(",", ":"),
                )
            )
        else:
            access_logger.info(
                "%s %s %s %.2fms",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
            )


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Liveness/readiness probe consumed by Azure Container Apps."""
    return HealthResponse(
        service=settings.app_name,
        environment=settings.environment,
        version=__version__,
    )


@app.get("/api/tasks", response_model=list[Task], tags=["tasks"])
def list_tasks() -> list[Task]:
    return task_service.list_tasks()


@app.post(
    "/api/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> Task:
    return task_service.create_task(payload)


@app.get("/api/tasks/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: int) -> Task:
    try:
        return task_service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.post("/api/tasks/{task_id}/complete", response_model=Task, tags=["tasks"])
def complete_task(task_id: int) -> Task:
    try:
        return task_service.complete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.patch("/api/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.delete(
    "/api/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: int) -> None:
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
