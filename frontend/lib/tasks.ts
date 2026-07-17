import type { Task } from "./api";

/** Sort tasks: open tasks first, then by id. Pure + easily unit-tested. */
export function sortTasks(tasks: Task[]): Task[] {
  return [...tasks].sort((a, b) => {
    if (a.completed !== b.completed) {
      return a.completed ? 1 : -1;
    }
    return a.id - b.id;
  });
}

export interface TaskSummary {
  total: number;
  completed: number;
  open: number;
  percentComplete: number;
}

/** Derive a progress summary from a list of tasks. */
export function summarize(tasks: Task[]): TaskSummary {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed).length;
  const open = total - completed;
  const percentComplete =
    total === 0 ? 0 : Math.round((completed / total) * 100);
  return { total, completed, open, percentComplete };
}
