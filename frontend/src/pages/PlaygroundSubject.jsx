// File: frontend/src/pages/PlaygroundSubject.jsx

import React from "react";
import { useParams, Link } from "react-router-dom";

const PlaygroundSubject = () => {
  const { subject } = useParams();

  const options = {
    biology: [
      { name: "MCQ", path: "/playground/biology/mcq" },
      { name: "Text Answer", path: "/playground/biology/textanswer" },
      { name: "Drag & Drop", path: "/playground/biology/dragdrop" }
    ],
    dbms: [
      { name: "MCQ", path: "/playground/dbms/mcq" },
      { name: "Text Answer", path: "/playground/dbms/textanswer" },
      { name: "Drag & Drop", path: "/playground/dbms/dragdrop" },
      { name: "DTD Structure Correction", path: "/playground/dbms/dtd" },
      { name: "Murder Mystery Game", path: "/playground/dbms/mystery" } // 🕵️ ADD THIS LINE!
    ]
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen text-center p-6">
      <h1 className="text-4xl font-bold mb-8">
        🎯 {subject.toUpperCase()} Activities
      </h1>

      <div className="flex flex-col gap-4 w-full max-w-md">
        {options[subject]?.map((option, idx) => (
          <Link key={idx} to={option.path}>
            <button className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 rounded-lg shadow">
              {option.name}
            </button>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default PlaygroundSubject;
