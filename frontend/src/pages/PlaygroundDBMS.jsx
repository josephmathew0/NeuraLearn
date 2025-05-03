// File: frontend/src/pages/PlaygroundDBMS.jsx

import React from "react";
import { useNavigate } from "react-router-dom";

export default function PlaygroundDBMS() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-6">🛢️ Choose Your DBMS Activity</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        
        <button
          onClick={() => navigate("/playground/dbms/mcq")}
          className="p-4 bg-blue-100 rounded-2xl shadow hover:bg-blue-200"
        >
          ✅ Multiple Choice (MCQ)
        </button>

        <button
          onClick={() => navigate("/playground/dbms/textanswer")}
          className="p-4 bg-green-100 rounded-2xl shadow hover:bg-green-200"
        >
          📝 Text Answer
        </button>

        <button
          onClick={() => navigate("/playground/dbms/dragdrop")}
          className="p-4 bg-pink-100 rounded-2xl shadow hover:bg-pink-200"
        >
          📦 Drag-and-Drop SQL
        </button>

        <button
          onClick={() => navigate("/playground/dbms/dtd")}
          className="p-4 bg-yellow-100 rounded-2xl shadow hover:bg-yellow-200"
        >
          🔍 DTD Structure Check
        </button>

        <button
          onClick={() => navigate("/playground/dbms/mystery")}
          className="p-4 bg-red-100 rounded-2xl shadow hover:bg-red-200"
        >
          🕵️ Murder Mystery Game
        </button>

      </div>
    </div>
  );
}
