import { FormEvent, useState } from "react";

import { useAppDispatch, useAppSelector } from "../app/hooks";
import { addUserMessage, sendChatMessage } from "../features/chat/chatSlice";

export function AIAssistantPanel() {
  const dispatch = useAppDispatch();
  const { messages, isLoading, error } = useAppSelector((state) => state.chat);
  const [draft, setDraft] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const message = draft.trim();

    if (!message || isLoading) {
      return;
    }

    dispatch(addUserMessage(message));
    dispatch(sendChatMessage(message));
    setDraft("");
  };

  return (
    <section className="panel chat-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">AI Assistant</p>
          <h2>CRM Copilot</h2>
        </div>
        <span className="live-dot">LLM</span>
      </div>

      <div className="messages">
        {messages.map((message) => (
          <div
            className={`message ${
              message.role === "user" ? "message-user" : "message-assistant"
            }`}
            key={message.id}
          >
            {message.content}
          </div>
        ))}
        {isLoading ? (
          <div className="message message-assistant">Updating the form...</div>
        ) : null}
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      <form className="chat-input" onSubmit={handleSubmit}>
        <textarea
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Example: I met Dr. Priya Menon yesterday at Fortis..."
        />
        <button type="submit" disabled={isLoading || !draft.trim()}>
          Send
        </button>
      </form>
    </section>
  );
}

