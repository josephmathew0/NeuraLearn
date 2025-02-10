import React, { useEffect, useState } from "react";
import { fetchQuestions, submitAnswer, validateSQLQuery } from "./services/api";  

const Quiz = () => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState({}); // ✅ Track feedback properly

  useEffect(() => {
    const getQuestions = async () => {
      const data = await fetchQuestions();
      setQuestions(data);
    };
    getQuestions();
  }, []);

  const handleAnswerChange = (questionId, answer) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmit = async (questionId, questionType) => {
    const userAnswer = answers[questionId];
    if (!userAnswer) {
      alert("Please select or enter an answer before submitting.");
      return;
    }

    // ✅ If it's an SQL question, validate before submission
    if (questionType === "sql") {
      const validationResult = await validateSQLQuery(userAnswer);

      if (validationResult.validation.length > 0) {
        setFeedback((prev) => ({
          ...prev,
          [questionId]: validationResult.validation.join("\n"),  // ✅ Display SQL errors
        }));
        return;  // Stop submission if SQL errors exist
      }
    }

    try {
      const response = await submitAnswer(1, questionId, userAnswer);
      console.log("🔍 Submission Response:", response); // ✅ Debug Log

      setFeedback((prev) => ({
        ...prev,
        [questionId]: response.feedback, // ✅ Update feedback state
      }));
    } catch (error) {
      console.error("🚨 Error submitting response:", error);
    }
  };

  return (
    <div style={{ maxWidth: "700px", margin: "auto", padding: "20px" }}>
      <h1 style={{ textAlign: "center" }}>NeuraLearn Quiz</h1>
      {questions.length === 0 ? (
        <p>Loading questions...</p>
      ) : (
        <ul style={{ listStyle: "none", padding: "0" }}>
          {questions.map((q, index) => (
            <li
              key={q.id}
              style={{
                marginBottom: "20px",
                padding: "15px",
                border: "1px solid #ccc",
                borderRadius: "8px",
                backgroundColor: "#f9f9f9",
              }}
            >
              <strong>Q{index + 1}: {q.content}</strong>
              <br />

              {q.options.length > 0 ? (
                <div>
                  {q.options.map((option, idx) => (
                    <label key={idx} style={{ display: "block", margin: "5px 0" }}>
                      <input
                        type="radio"
                        name={`question-${q.id}`}
                        value={option}
                        onChange={() => handleAnswerChange(q.id, option)}
                      />
                      {" "}{option}
                    </label>
                  ))}
                </div>
              ) : (
                <input
                  type="text"
                  placeholder="Type your answer here"
                  style={{ width: "100%", padding: "8px", marginTop: "5px" }}
                  onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                />
              )}

              <button
                onClick={() => handleSubmit(q.id)}
                style={{
                  display: "block",
                  marginTop: "10px",
                  padding: "8px 12px",
                  backgroundColor: "#007BFF",
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                Submit
              </button>

              {feedback[q.id] && (
                <p style={{ color: feedback[q.id].includes("✅") ? "green" : "red" }}>
                  {feedback[q.id]}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Quiz;
