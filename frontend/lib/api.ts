export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

/**
 * Base URL for API calls from the browser.
 *
 * Left empty by default so the browser calls the frontend's own origin
 * (`/api/...`), which is proxied to the backend by `app/api/[...path]/route.ts`
 * using the server-side `BACKEND_URL` runtime env var. This keeps the built
 * image independent of the backend's address.
 */
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    ...init,
  });
  if (!response.ok) {
    throw new Error(`API ${path} failed with ${response.status}`);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export const api = {
  listTasks: () => request<Task[]>("/api/tasks"),
  createTask: (title: string, description = "") =>
    request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title, description }),
    }),
  completeTask: (id: number) =>
    request<Task>(`/api/tasks/${id}/complete`, { method: "POST" }),
  deleteTask: (id: number) => request<void>(`/api/tasks/${id}`, { method: "DELETE" }),
};
