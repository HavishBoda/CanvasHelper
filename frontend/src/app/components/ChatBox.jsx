import { useState, useEffect } from "react";

const BACKEND_URL = "http://localhost:8000";


export default function ChatBox({ courseId, selectedFiles }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [processing, setProcessing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentUserId, setCurrentUserId] = useState("");
  const [currentCourseId, setCurrentCourseId] = useState("");

  useEffect(() => {
    if (selectedFiles.length > 0) {
      setProcessing(true);
      fetch("http://localhost:8000/session/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_urls: selectedFiles }),
      }).then(() => setProcessing(false));
    }
  }, [selectedFiles]);

  async function handleAsk(question) {
    // Clear old answer and show loading
    setAnswer("");
    setIsLoading(true);
  
    try {
      let endpoint = "/chat";
      let params = new URLSearchParams({
        user_id: currentUserId,
        course_id: currentCourseId,
        question: question,
      });
  
      const response = await fetch(`${BACKEND_URL}${endpoint}?${params.toString()}`);
      const data = await response.json();
  
      if (data.answer) {
        setAnswer(data.answer);
      } else {
        setAnswer("No answer found.");
      }
    } catch (error) {
      console.error("Error fetching answer:", error);
      setAnswer("Error getting answer. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }
  
  
  

  return (
    <div className="p-4 border rounded mt-4">
      <div className="text-black">
        Context:{" "}
        {selectedFiles.length === 0
          ? "Full Course Knowledge Base"
          : `Selected PDFs (${selectedFiles.length})`}
      </div>
      {processing ? (
        <p className="text-gray-500 text-black">Processing selected PDFs...</p>
      ) : (
        <>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="border p-2 w-full text-black"
          />
          <button
            onClick={handleAsk}
            className="bg-purple-600 text-white px-4 py-2 mt-2 rounded"
          >
            Ask
          </button>
          {answer && <div className="mt-4 text-black">Answer: {answer}</div>}
        </>
      )}
    </div>
  );
}