import React from "react";
import { useNavigate } from "react-router-dom";

function ModeSelect() {
  const navigate = useNavigate();

  const handleSinglePlayer = () => {
    // (You can later design single player mode separately)
    alert("Single Player mode is under construction!");
  };

  const handleMultiPlayer = () => {
    const password = prompt("Enter Multiplayer Password:");
    if (password === "XYZZY") {
      navigate("/playground/dbms/mystery/characterselect");
    } else {
      alert("Incorrect password! Try again.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-4xl font-bold mb-8">🕵️ Murder Mystery Game</h1>
      <div className="flex flex-col space-y-4">
        <button
          onClick={handleSinglePlayer}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg"
        >
          Single Player
        </button>
        <button
          onClick={handleMultiPlayer}
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg"
        >
          Multiplayer
        </button>
      </div>
    </div>
  );
}

export default ModeSelect;
