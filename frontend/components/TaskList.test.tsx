import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import TaskList from "@/components/TaskList";
import { api, type Task } from "@/lib/api";

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: {
      listTasks: vi.fn(),
      createTask: vi.fn(),
      completeTask: vi.fn(),
    },
  };
});

const mockedApi = vi.mocked(api);

function makeTask(id: number, completed: boolean): Task {
  return {
    id,
    title: `Task ${id}`,
    description: "",
    completed,
    created_at: new Date().toISOString(),
  };
}

describe("TaskList", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders tasks and a progress summary", async () => {
    mockedApi.listTasks.mockResolvedValue([makeTask(1, true), makeTask(2, false)]);

    render(<TaskList />);

    expect(await screen.findByText("Task 1")).toBeInTheDocument();
    expect(screen.getByTestId("summary")).toHaveTextContent("1/2 complete (50%)");
  });

  it("shows an error when the backend is unreachable", async () => {
    mockedApi.listTasks.mockRejectedValue(new Error("boom"));

    render(<TaskList />);

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent("Unable to reach the backend API."),
    );
  });
});
