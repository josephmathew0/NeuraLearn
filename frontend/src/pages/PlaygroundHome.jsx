import React from "react";
import { useNavigate } from "react-router-dom";

const PlaygroundHome = () => {
  const navigate = useNavigate();

  return (
    <div className="p-10 text-center">
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
