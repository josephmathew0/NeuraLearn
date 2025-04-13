// File: frontend/src/pages/TextAnswer.jsx

import React, { useEffect, useState } from "react";
import "./DragDrop.css"; // reuse existing styles

const TextAnswer = () => {
  const [data, setData] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [highlightedAnswer, setHighlightedAnswer] = useState("");
  const [score, setScore] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);

  useEffect(() => {
    fetch("http://localhost:5000/api/text")
      .then((res) => res.json())
      .then((q) => {
        setData(q);
        console.log("✅ Correct Answer:", q.answer);
      });
  }, []);

  const handleCheck = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/evaluate_text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_answer: userAnswer,
          correct_answer: data.answer,
        }),
      });

      const result = await response.json();
      console.log("🔍 Similarity Score:", result.score);

      setScore(result.score);
      setFeedback(result.feedback);
      setHighlightedAnswer(result.highlighted_answer);
      setShowFeedback(true);
    } catch (err) {
      console.error("❌ Evaluation error", err);
      setFeedback("Something went wrong while evaluating your answer.");
      setShowFeedback(true);
    }
  };

  const getLevel = () => {
    if (score >= 0.95) return "🌟 Excellent";
    if (score >= 0.85) return "👍 Good";
    if (score >= 0.7) return "✅ Fair";
    return "❗ Try Again";
  };

  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6 text-center max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">✍️ Sentence Answer</h2>
      <p className="mb-6 text-lg">{data.question}</p>

      <textarea
        className="w-full border border-gray-400 p-3 rounded mb-4"
        rows={5}
        placeholder="Type your answer here..."
        value={userAnswer}
        onChange={(e) => setUserAnswer(e.target.value)}
      />

      <div className="mb-4">
        <button
          onClick={handleCheck}
          className="bg-green-200 px-4 py-2 rounded hover:bg-green-300"
        >
          ✅ Check Answer
        </button>
      </div>

      {showFeedback && (
        <div className="mt-6 text-left bg-gray-100 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">🧠 Feedback</h3>
          <p className="mb-2">{feedback}</p>
          <p className="text-sm text-gray-600 mb-1">
            Similarity Score: <strong>{(score * 100).toFixed(2)}%</strong> –{" "}
            <span>{getLevel()}</span>
          </p>
          <p className="mt-3 text-gray-800">
            <strong>Model Answer:</strong>
          </p>
          <p
            className="mt-1 text-base leading-relaxed"
            dangerouslySetInnerHTML={{ __html: highlightedAnswer }}
          />
        </div>
      )}
    </div>
  );
};

export default TextAnswer;
