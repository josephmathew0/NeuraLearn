// File: frontend/src/components/QuestionPopup.jsx

import React from "react";
import "./QuestionPopup.css";

const QuestionPopup = ({ questionData, onClose }) => {
  return (
    <div className="question-popup-overlay">
      <div className="question-popup">
        <h2>🧪 Question: {questionData.location}</h2>
        <p>{questionData.question}</p>
        <textarea
          placeholder="Write your SQL answer here..."
          rows={5}
          className="question-input"
        />
        <div className="question-actions">
          <button onClick={onClose}>Submit</button>
        </div>
      </div>
    </div>
  );
};

export default QuestionPopup;
