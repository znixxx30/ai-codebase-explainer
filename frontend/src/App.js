import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {

  const [repoUrl, setRepoUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);
  const [status, setStatus] = useState("");

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
      sources: data.sources || []
    };

    setChat(prev => [...prev, aiMessage]);
  };

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>

      <h1>AI Codebase Explainer</h1>

      <h3>1. Index Repository</h3>

      <input
        style={{ width: "400px" }}
        placeholder="Enter GitHub repository URL"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
      />

      <button onClick={indexRepository}>
        Index Repository
      </button>

      <p>{status}</p>

      <h3>2. Ask Question</h3>

      <input
        style={{ width: "400px" }}
        placeholder="Ask a question about the repository"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <h3>Conversation</h3>

      <div style={{ marginTop: 20 }}>

        {chat.map((msg, index) => (

          <div key={index} style={{ marginBottom: 20 }}>

            <b>{msg.role === "user" ? "User" : "AI"}:</b>

            <p>{msg.text}</p>

            {msg.sources && msg.sources.length > 0 && (
              <div>

                <b>Sources:</b>

                <ul>
                  {msg.sources.map((src, i) => (
                    <li key={i}>{src}</li>
                  ))}
                </ul>

              </div>
            )}

          </div>

        ))}

      </div>

    </div>
  );
}

export default App;