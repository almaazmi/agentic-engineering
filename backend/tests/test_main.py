"""API-level tests exercised by CI."""

from __future__ import annotations

import json
import logging

from app.main import settings
from fastapi import status
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"]
    assert body["version"]


def test_access_log_excludes_sensitive_data(client: TestClient, caplog, monkeypatch) -> None:
    monkeypatch.setattr(settings, "environment", "production")
    caplog.set_level(logging.INFO, logger="app.access")

    response = client.post(
        "/api/tasks?token=do-not-log",
        json={"title": "body-do-not-log"},
        headers={"Authorization": "header-do-not-log"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "body-do-not-log"
    access_log_messages = [
        record.message for record in caplog.records if record.name == "app.access"
    ]
    assert len(access_log_messages) == 1
    access_log = access_log_messages[0]
    payload = json.loads(access_log)
    assert payload["method"] == "POST"
    assert payload["path"] == "/api/tasks"
    assert payload["status"] == status.HTTP_201_CREATED
    assert isinstance(payload["duration_ms"], float)
    assert "do-not-log" not in access_log
    assert "body-do-not-log" not in access_log
    assert "header-do-not-log" not in access_log


def test_create_and_list_task(client: TestClient) -> None:
    created = client.post("/api/tasks", json={"title": "Wire up CI"})
    assert created.status_code == status.HTTP_201_CREATED
    task = created.json()
    assert task["id"] == 1
    assert task["completed"] is False

    listed = client.get("/api/tasks")
    assert listed.status_code == status.HTTP_200_OK
    assert len(listed.json()) == 1


def test_complete_task(client: TestClient) -> None:
    task_id = client.post("/api/tasks", json={"title": "Ship it"}).json()["id"]
    completed = client.post(f"/api/tasks/{task_id}/complete")
    assert completed.status_code == status.HTTP_200_OK
    assert completed.json()["completed"] is True


def test_update_task(client: TestClient) -> None:
    task_id = client.post(
        "/api/tasks", json={"title": "Old title", "description": "Old description"}
    ).json()["id"]
    updated = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "New title", "description": "New description"},
    )
    assert updated.status_code == status.HTTP_200_OK
    assert updated.json()["title"] == "New title"
    assert updated.json()["description"] == "New description"


def test_update_missing_task_returns_404(client: TestClient) -> None:
    response = client.patch("/api/tasks/999", json={"title": "New title"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_validation_error(client: TestClient) -> None:
    task_id = client.post("/api/tasks", json={"title": "Existing"}).json()["id"]
    response = client.patch(f"/api/tasks/{task_id}", json={"title": ""})
    assert response.status_code == 422


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/api/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task(client: TestClient) -> None:
    task_id = client.post("/api/tasks", json={"title": "Remove me"}).json()["id"]
    deleted = client.delete(f"/api/tasks/{task_id}")
    assert deleted.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/api/tasks/{task_id}").status_code == status.HTTP_404_NOT_FOUND


def test_create_task_validation_error(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422  # Unprocessable content
