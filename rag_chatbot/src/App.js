import { useEffect } from "react";

function App() {
  useEffect(() => {
    fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: "What is semantic search?",
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Backend response:", data);
      })
      .catch((err) => {
        console.error("Error calling backend:", err);
      });
  }, []);

  return (
    <div>
      <h2>React → FastAPI connection test</h2>
      <p>Check browser console</p>
    </div>
  );
}

export default App;
