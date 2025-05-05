import React, { useState } from "react";

const QuestionPopup = ({ question, onSubmit, hint }) => {
  const [userAnswer, setUserAnswer] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (userAnswer.trim() !== "") {
      onSubmit(userAnswer);
      setUserAnswer("");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-11/12 max-w-xl shadow-xl">
        <h2 className="text-xl font-bold mb-2">🧠 Question</h2>
        <p className="mb-4 text-gray-700 whitespace-pre-line">{question.prompt}</p>

        <form onSubmit={handleSubmit}>
          <textarea
            rows={4}
            className="w-full border border-gray-300 rounded px-3 py-2 mb-3 focus:outline-none focus:ring"
            placeholder="Type your SQL answer here..."
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
          />

          {hint && (
            <p className="mb-3 text-green-600 font-semibold">
              💡 Hint: {hint}
            </p>
          )}

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Submit Answer
          </button>
        </form>
      </div>
    </div>
  );
};

export default QuestionPopup;
