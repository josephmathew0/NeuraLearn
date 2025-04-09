import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function PlaygroundMCQ() {
  const [questionData, setQuestionData] = useState(null);
  const [selected, setSelected] = useState(null);
  const [feedback, setFeedback] = useState('');
  const navigate = useNavigate();

  const fetchQuestion = async () => {
    try {
      const res = await fetch('/api/mcq');
      const data = await res.json();
      setQuestionData(data);
      setSelected(null);
      setFeedback('');
    } catch (err) {
      setFeedback('⚠️ Failed to load question.');
    }
  };

  useEffect(() => {
    fetchQuestion();
  }, []);

  const handleSelect = (option) => {
    setSelected(option);
    if (option === questionData.correct_answer) {
      setFeedback('✅ Correct!');
    } else {
      setFeedback(`❌ Incorrect. ${questionData.explanation}`);
    }
  };

  if (!questionData) return <div className="p-4 text-center">Loading...</div>;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-white">
      <h1 className="text-3xl font-bold text-center text-blue-800 mb-4">🧠 MCQ Practice</h1>

      <p className="text-lg text-center text-gray-700 mb-6 max-w-xl">
        {questionData.question}
      </p>

      <div className="flex flex-col gap-3 w-full max-w-xs">
        {questionData.options.map((option, index) => (
          <button
            key={index}
            onClick={() => handleSelect(option)}
            className={`px-4 py-2 rounded text-left border transition-all duration-200
              ${selected === option
                ? option === questionData.correct_answer
                  ? 'bg-green-100 border-green-600 text-green-800'
                  : 'bg-red-100 border-red-500 text-red-700'
                : 'bg-white border-gray-300 hover:bg-gray-100'}`}
            disabled={!!selected}
          >
            {option}
          </button>
        ))}
      </div>

      {feedback && (
        <div className="mt-6 text-center text-lg font-medium text-gray-800 whitespace-pre-wrap">
          {feedback}
        </div>
      )}

      {selected && (
        <button
          onClick={fetchQuestion}
          className="mt-6 px-6 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white"
        >
          Next Question
        </button>
      )}

      <button
        onClick={() => navigate('/playground')}
        className="mt-4 px-4 py-2 text-sm text-gray-500 hover:underline"
      >
        Back
      </button>
    </div>
  );
}
