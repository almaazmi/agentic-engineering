import TaskList from "@/components/TaskList";

export default function Home() {
  return (
    <main>
      <h1>Agentic Engineering</h1>
      <p>Issues → agent PR → CI → security → review → Azure. All on autopilot.</p>
      <TaskList />
    </main>
  );
}
