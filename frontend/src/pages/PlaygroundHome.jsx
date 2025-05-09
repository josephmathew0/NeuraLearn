// File: frontend/src/pages/PlaygroundHome.jsx

import React from "react";
import { useNavigate } from "react-router-dom";

const PlaygroundHome = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear(); // Clear user data
    navigate("/login");   // Redirect to login page
  };

  return (
    <div className="relative p-10 text-center min-h-screen bg-gray-50">
      {/* Logout Button */}
      <button
        onClick={handleLogout}
        className="absolute top-4 right-4 px-4 py-2 bg-red-500 text-white font-semibold rounded hover:bg-red-600"
      >
        Logout
      </button>

      {/* Main Content */}
      <h1 className="text-3xl font-bold mb-8">🎯 Choose a Subject</h1>
      <div className="flex justify-center gap-6">
        <button
          className="bg-blue-300 px-6 py-3 rounded hover:bg-blue-400"
          onClick={() => navigate("/playground/biology")}
        >
          🧬 Biology
        </button>
        <button
          className="bg-green-300 px-6 py-3 rounded hover:bg-green-400"
          onClick={() => navigate("/playground/dbms")}
        >
          🗄️ DBMS
        </button>
      </div>
    </div>
  );
};

export default PlaygroundHome;
