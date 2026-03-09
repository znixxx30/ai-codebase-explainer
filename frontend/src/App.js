import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
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
    setAnswer("Thinking...");

    const response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question
      })
    });

    const data = await response.json();

    setAnswer(data.answer);
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

      <button onClick={indexRepository}>Index Repository</button>

      <p>{status}</p>

      <h3>2. Ask Question</h3>

      <input
        style={{ width: "400px" }}
        placeholder="Ask a question about the repository"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>Ask</button>

      <h3>AI Answer</h3>
      <p>{answer}</p>
    </div>
  );
}

export default App;