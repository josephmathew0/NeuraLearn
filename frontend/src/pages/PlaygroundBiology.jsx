// File: frontend/src/pages/PlaygroundBiology.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

export default function PlaygroundBiology() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-6">🧬 Choose Your Biology Activity</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <button
          onClick={() => navigate("/playground/biology/mcq")}
          className="p-4 bg-green-100 rounded-2xl shadow hover:bg-green-200"
        >
          🧪 MCQ
        </button>
        <button
          onClick={() => navigate("/playground/biology/textanswer")}
          className="p-4 bg-blue-100 rounded-2xl shadow hover:bg-blue-200"
        >
          📝 Text Answer
        </button>
        <button
          onClick={() => navigate("/playground/biology/dragdrop")}
          className="p-4 bg-pink-100 rounded-2xl shadow hover:bg-pink-200"
        >
          📦 Drag-and-Drop
        </button>
      </div>
    </div>
  );
}
