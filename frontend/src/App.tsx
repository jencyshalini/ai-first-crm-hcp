import { AIAssistantPanel } from "./components/AIAssistantPanel";
import { InteractionForm } from "./components/InteractionForm";

export default function App() {
  return (
    <main className="app-shell">
      <InteractionForm />
      <AIAssistantPanel />
    </main>
  );
}

