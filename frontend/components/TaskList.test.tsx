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
      deleteTask: vi.fn(),
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

  it("deletes a task and refreshes the list", async () => {
    mockedApi.listTasks
      .mockResolvedValueOnce([makeTask(1, false)])
      .mockResolvedValueOnce([]);
    mockedApi.deleteTask.mockResolvedValue(undefined);

    render(<TaskList />);

    expect(await screen.findByText("Task 1")).toBeInTheDocument();
    const deleteButton = await screen.findByRole("button", { name: "Delete" });
    deleteButton.click();

    await waitFor(() => expect(mockedApi.deleteTask).toHaveBeenCalledWith(1));
    await waitFor(() => expect(screen.queryByText("Task 1")).not.toBeInTheDocument());
    expect(mockedApi.listTasks).toHaveBeenCalledTimes(2);
  });
});
