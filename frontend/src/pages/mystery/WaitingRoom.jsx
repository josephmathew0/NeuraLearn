// File: frontend/src/pages/mystery/WaitingRoom.jsx

import React from "react";
import { useLocation } from "react-router-dom";

export default function WaitingRoom() {
  const location = useLocation();
  const { character } = location.state || {};

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-6">⏳ Waiting Room</h1>

      {character ? (
        <div className="flex flex-col items-center">
          <p className="text-xl mb-4">You selected:</p>
          <img
            src={`/characters/${character}`}
            alt="Selected Character"
            className="w-32 h-32 object-contain mb-6"
          />
        </div>
      ) : (
        <p className="text-lg">No character selected!</p>
      )}

      <p className="text-lg">Waiting for others to join and start the game...</p>
    </div>
  );
}
