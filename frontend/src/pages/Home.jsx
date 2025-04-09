import React from 'react';
import { useNavigate } from 'react-router-dom'; // ✅ Add this

export default function Home() {
  const navigate = useNavigate(); // ✅ Define the navigate function

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md text-center">
        <h1 className="text-4xl font-bold text-blue-800 mb-4 leading-tight">
          Welcome to NeuraLearn
        </h1>
        <p className="text-base text-gray-600 mb-8">
          Your AI-powered biology adventure starts here. Practice, play, and learn smarter.
        </p>

        <div id="mainbuttons" className="flex flex-col gap-4 sm:flex-row sm:justify-center">
          <button className="buttons w-full sm:w-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
            📘 Continue Learning
          </button>
          <button
            onClick={() => navigate('/playground')}
            className="buttons w-full sm:w-auto px-6 py-3 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-100 transition"
          >
            🎮 Playground Mode
          </button>
        </div>
      </div>
    </div>
  );
}
