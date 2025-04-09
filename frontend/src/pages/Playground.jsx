import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Playground() {
  const navigate = useNavigate();

  const activities = [
    { name: '📝 MCQ', path: '/playground/mcq' },
    { name: '🧩 Drag & Drop', path: '/playground/drag' },
    { name: '✍️ Sentence Answer', path: '/playground/sentence' },
    { name: '🗺️ Treasure Hunt', path: '/playground/treasure' },
    { name: '🕵️ Murder Mystery', path: '/playground/mystery' },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4 py-8">
      <h1 className="text-3xl font-bold text-blue-700 mb-6 text-center">
        Choose Your Playground Activity
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-md">
        {activities.map((activity, index) => (
          <button
            key={index}
            onClick={() => navigate(activity.path)}
            className="bg-white border border-blue-500 hover:bg-blue-50 text-blue-700 font-semibold py-3 px-6 rounded-lg shadow-md transition"
          >
            {activity.name}
          </button>
        ))}
      </div>
    </div>
  );
}
