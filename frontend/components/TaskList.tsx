"use client";

import { useCallback, useEffect, useState } from "react";
import { api, type Task } from "@/lib/api";
import { sortTasks, summarize } from "@/lib/tasks";

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      setTasks(await api.listTasks());
      setError(null);
    } catch {
      setError("Unable to reach the backend API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function handleAdd(event: React.FormEvent) {
    event.preventDefault();
    if (!title.trim()) return;
    await api.createTask(title.trim());
    setTitle("");
    await refresh();
  }

  async function handleComplete(id: number) {
    await api.completeTask(id);
    await refresh();
  }

  const summary = summarize(tasks);

  return (
    <section>
      <form onSubmit={handleAdd} aria-label="Create task">
        <input
          aria-label="Task title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="What needs doing?"
        />
        <button type="submit">Add task</button>
      </form>

      {error && <p role="alert">{error}</p>}
      {loading ? (
        <p>Loading tasks…</p>
      ) : (
        <>
          <p data-testid="summary">
            {summary.completed}/{summary.total} complete ({summary.percentComplete}%)
          </p>
          <ul>
            {sortTasks(tasks).map((task) => (
              <li key={task.id} data-completed={task.completed}>
                <span>{task.title}</span>
                {!task.completed && (
                  <button onClick={() => handleComplete(task.id)}>Done</button>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
