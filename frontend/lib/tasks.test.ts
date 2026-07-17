import { describe, expect, it } from "vitest";
import type { Task } from "@/lib/api";
import { sortTasks, summarize } from "@/lib/tasks";

function makeTask(id: number, completed: boolean): Task {
  return {
    id,
    title: `Task ${id}`,
    description: "",
    completed,
    created_at: new Date().toISOString(),
  };
}

describe("sortTasks", () => {
  it("puts open tasks before completed ones", () => {
    const tasks = [makeTask(1, true), makeTask(2, false), makeTask(3, false)];
    const sorted = sortTasks(tasks);
    expect(sorted.map((task) => task.id)).toEqual([2, 3, 1]);
  });

  it("does not mutate the input array", () => {
    const tasks = [makeTask(2, false), makeTask(1, false)];
    sortTasks(tasks);
    expect(tasks.map((task) => task.id)).toEqual([2, 1]);
  });
});

describe("summarize", () => {
  it("computes progress for an empty list", () => {
    expect(summarize([])).toEqual({
      total: 0,
      completed: 0,
      open: 0,
      percentComplete: 0,
    });
  });

  it("computes progress with mixed tasks", () => {
    const tasks = [makeTask(1, true), makeTask(2, false), makeTask(3, true), makeTask(4, false)];
    expect(summarize(tasks)).toEqual({
      total: 4,
      completed: 2,
      open: 2,
      percentComplete: 50,
    });
  });
});
