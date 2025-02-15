import React, { useEffect, useState } from "react";
import { fetchQuestions } from "./services/api";  
import DragDropQueryBuilder from "./components/DragDropQueryBuilder";  // ✅ Import Drag-and-Drop Component

const Quiz = () => {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");

  useEffect(() => {
    const getQuestion = async () => {
      const data = await fetchQuestions();
      console.log("🔍 Debug: Questions from API:", data);

      // ✅ Select only the first SQL-type question
      const sqlQuestion = data.find(q => q.type === "sql");

      if (sqlQuestion) {
        console.log("✅ Selected SQL Question:", sqlQuestion);
        setQuestion(sqlQuestion);
      } else {
        console.error("🚨 No SQL questions found!");
      }
    };

    getQuestion();
  }, []);

  const handleSubmit = () => {
    console.log("🚀 Submitted Answer:", answer);
    if (answer.trim() === question.correct_answer.replace(/[\[\]"]/g, "")) {
      setFeedback("✅ Correct!");
    } else {
      setFeedback("❌ Incorrect! Try again.");
    }
  };

  return (
    <div style={{ maxWidth: "700px", margin: "auto", padding: "20px" }}>
      <h1 style={{ textAlign: "center" }}>NeuraLearn Quiz</h1>

      {!question ? (
        <p>Loading question...</p>
      ) : (
        <div style={{
          marginBottom: "20px",
          padding: "15px",
          border: "1px solid #ccc",
          borderRadius: "8px",
          backgroundColor: "#f9f9f9",
        }}>
          <strong>{question.content}</strong>
          <br />

          {/* ✅ Render Drag-and-Drop Query Builder for SQL Questions */}
          {question.options && question.options.length > 0 ? (
            <>
              {console.log("✅ Rendering DragDropQueryBuilder with options:", question.options)}
              <DragDropQueryBuilder
                options={question.options}  // ✅ Pass shuffled SQL components
                onQueryChange={setAnswer}  // ✅ Capture answer from DragDropQueryBuilder
              />
            </>
          ) : (
            <p>⚠️ No options available for this question!</p>
          )}

          <button
            onClick={handleSubmit}
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

          {feedback && (
            <p style={{ color: feedback.includes("✅") ? "green" : "red" }}>
              {feedback}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default Quiz;
