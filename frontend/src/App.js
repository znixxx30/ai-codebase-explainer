import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {

  const [repoUrl, setRepoUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat]);

  const indexRepository = async () => {
    setStatus("Indexing repository...");

    const response = await fetch(
      `${API_URL}/index-repo?repo_url=${repoUrl}`,
      { method: "POST" }
    );

    const data = await response.json();

    setStatus(data.status);
  };

  const askQuestion = async () => {

    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      text: question
    };

    setChat(prev => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    const response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: userMessage.text
      })
    });

    const data = await response.json();

    const aiMessage = {
      role: "assistant",
      text: data.answer,
      sources: data.sources || [],
      snippets: data.snippets || []
    };

    setChat(prev => [...prev, aiMessage]);
    setLoading(false);
  };

  return (
    <div className="app-container">

      <header className="header">
        AI Codebase Explainer
      </header>

      <div className="repo-section">
        <input
          placeholder="Enter GitHub repository URL"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
        />

        <button onClick={indexRepository}>
          Index Repository
        </button>

        <p className="status">{status}</p>
      </div>

      <div className="chat-window">

        {chat.length === 0 && !loading && (
          <div className="cube-scene">
            <div className="orbit">
              <div className="cube">
                <div className="face front" />
                <div className="face back" />
                <div className="face left" />
                <div className="face right" />
                <div className="face top" />
                <div className="face bottom" />
              </div>
            </div>
            <p className="cube-hint">Index a repo and ask anything about the code</p>
          </div>
        )}

        {chat.map((msg, index) => (

          <div
            key={index}
            className={msg.role === "user" ? "chat-bubble user" : "chat-bubble ai"}
          >

            <div className="message-text">
              {msg.text}
            </div>

            {msg.sources && msg.sources.length > 0 && (
              <div className="sources">
                <b>Sources</b>
                <ul>
                  {msg.sources.map((src, i) => (
                    <li key={i}>{src}</li>
                  ))}
                </ul>
              </div>
            )}

            {msg.snippets && msg.snippets.length > 0 && (
              <div className="snippets">
                <b>Code Snippets</b>
                {msg.snippets.map((code, i) => (
                  <pre key={i}>
                    <code>{code}</code>
                  </pre>
                ))}
              </div>
            )}

          </div>

        ))}

        {loading && (
          <div className="chat-bubble ai">
            AI is thinking...
          </div>
        )}

        <div ref={chatEndRef} />

      </div>

      <div className="input-area">

        <input
          placeholder="Ask a question about the repository..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={askQuestion}>
          Send
        </button>

      </div>

    </div>
  );
}

export default App;