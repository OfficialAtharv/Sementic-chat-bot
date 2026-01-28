import { useState, useEffect, useRef } from "react";
import "./App.css";
import AntiqLogo from "./Assets/antiqAI.png";

function App() {
  const bottomRef = useRef(null);
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hello! I am Antiq AI. Ask me anything." },
  ]);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    // Temporary typing indicator
    setMessages((prev) => [...prev, { role: "ai", typing: true }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }),
      });

      const data = await res.json();

      // Remove "Thinking..." and add real answer
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "ai", text: data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "ai", text: "Error talking to backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };
  const TypingIndicator = () => (
    <span className="typing">
      Antiq AI is thinking<span>.</span>
      <span>.</span>
      <span>.</span>
    </span>
  );
  <header className="app-header">
    <div className="brand">
      <img src={AntiqLogo} alt="Antiq AI Logo" />
      <span>Antiq AI</span>
    </div>
  </header>;

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <img src={AntiqLogo} alt="Antiq AI Logo" />
          <span>Antiq AI</span>
        </div>
      </header>

      <div className="chat">
        {messages.map((msg, i) => (
          <div key={i} className={`bubble ${msg.role}`}>
            {msg.typing ? <TypingIndicator /> : msg.text}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="input-bar">
        <input
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
