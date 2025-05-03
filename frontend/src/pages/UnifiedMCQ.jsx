// File: frontend/src/pages/UnifiedMCQ.jsx

import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

const UnifiedMCQ = () => {
  const location = useLocation();
  const subject = location.pathname.includes("dbms") ? "dbms" : "biology";

  const [question, setQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);
  const [topicOrder, setTopicOrder] = useState(1);
  const [retryQuestion, setRetryQuestion] = useState(null);
  console.log("🌐 VITE_API_URL =", import.meta.env.VITE_API_URL);


  const fetchBiologyMCQ = async () => {
    const url = `${import.meta.env.VITE_API_URL}/api/mcq`;
    console.log("📡 Fetching Biology MCQ from:", url);
    try {
      const res = await fetch(url);
      const text = await res.text();
      console.log("📥 Raw response:", text);
      const data = JSON.parse(text);
      console.log("✅ Parsed Biology MCQ:", data);

      setQuestion({
        question: data.question,
        options: shuffleOptions([data.correct_answer, ...data.options.slice(1)]),
        correctAnswer: data.correct_answer,
        explanation: data.explanation,
      });
    } catch (error) {
      console.error("❌ Failed to fetch Biology MCQ:", error);
    }
  };

  const fetchDBMSMCQ = async () => {
    const url = `${import.meta.env.VITE_API_URL}/api/sqlmcq/structured/${topicOrder}`;
    console.log("📡 Fetching DBMS MCQ from:", url);
    try {
      const res = await fetch(url);
      const text = await res.text();
      console.log("📥 Raw response:", text);
      const data = JSON.parse(text);
      console.log("✅ Parsed DBMS MCQs:", data);

      if (data.length > 0) {
        const randomQuestion = data[Math.floor(Math.random() * data.length)];
        setQuestion({
          question: randomQuestion.question,
          options: shuffleOptions([
            randomQuestion.correct_answer,
            randomQuestion.distractor1,
            randomQuestion.distractor2,
            randomQuestion.distractor3,
          ]),
          correctAnswer: randomQuestion.correct_answer,
          explanation: randomQuestion.explanation,
        });
      }
    } catch (error) {
      console.error("❌ Failed to fetch DBMS MCQ:", error);
    }
  };

  const fetchQuestion = async () => {
    setShowFeedback(false);
    setSelectedAnswer("");

    if (subject === "biology") {
      await fetchBiologyMCQ();
    } else if (subject === "dbms") {
      await fetchDBMSMCQ();
    }
  };

  const shuffleOptions = (options) => {
    return options.sort(() => Math.random() - 0.5);
  };

  useEffect(() => {
    fetchQuestion();
  }, [topicOrder]);

  const handleCheckAnswer = () => {
    if (!selectedAnswer) return;
    setShowFeedback(true);
    if (selectedAnswer === question.correctAnswer) {
      setFeedback("✅ Correct!");
      setRetryQuestion(null);
    } else {
      setFeedback("❌ Incorrect. We'll retry this question after one more.");
      setRetryQuestion(question);
    }
  };

  const handleNextQuestion = () => {
    if (retryQuestion) {
      setQuestion(retryQuestion);
      setRetryQuestion(null);
      setShowFeedback(false);
      setSelectedAnswer("");
    } else {
      if (subject === "dbms") {
        setTopicOrder((prev) => prev + 1);
      } else {
        fetchQuestion();
      }
    }
  };

  if (!question) return <div>Loading...</div>;

  return (
    <div className="p-6 text-center max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">🧠 {subject === "dbms" ? "DBMS MCQ" : "Biology MCQ"}</h2>
      <p className="mb-6 text-lg">{question.question}</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {question.options.map((option, idx) => (
          <button
            key={idx}
            onClick={() => setSelectedAnswer(option)}
            className={`border rounded p-3 ${
              selectedAnswer === option ? "bg-green-100" : "bg-white"
            } hover:bg-gray-100`}
          >
            {option}
          </button>
        ))}
      </div>

      <div className="mb-4">
        <button
          onClick={handleCheckAnswer}
          className="bg-green-300 px-4 py-2 rounded hover:bg-green-400"
        >
          ✅ Check Answer
        </button>
      </div>

      {showFeedback && (
        <div className="mt-6 text-left bg-gray-100 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">🧠 Feedback</h3>
          <p className="mb-2">{feedback}</p>
          {question.explanation && (
            <p className="text-gray-700">
              <strong>Explanation:</strong> {question.explanation}
            </p>
          )}
          <button
            onClick={handleNextQuestion}
            className="mt-4 bg-blue-300 px-4 py-2 rounded hover:bg-blue-400"
          >
            ➡️ Next Question
          </button>
        </div>
      )}
    </div>
  );
};

export default UnifiedMCQ;
