"""API-level tests exercised by CI."""

from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"]
    assert body["version"]


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
