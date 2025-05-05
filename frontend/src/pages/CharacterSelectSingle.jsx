import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CharacterSelect.css"; // reuse same styling as multiplayer

const CharacterSelectSingle = () => {
  const navigate = useNavigate();
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [role, setRole] = useState(null);

  const characters = Array.from({ length: 10 }, (_, i) => i);

  const handleCharacterClick = (charIndex) => {
    setSelectedCharacter(charIndex);
  };

  const handleStartGame = () => {
    if (selectedCharacter === null || !role) {
      alert("Please select a character and a role.");
      return;
    }

    const characterImg = `char${selectedCharacter}.png`;

    // Save in localStorage
    const playerData = {
      character: characterImg,
      role,
      username: "SinglePlayer",
      isMultiplayer: false,
    };
    localStorage.setItem("playerInfo", JSON.stringify(playerData));

    // Navigate to game
    navigate("/playground/dbms/mystery/single");
  };

  return (
    <div className="character-select-container">
      <h1 className="title">Choose Your Character</h1>

      <div className="character-grid">
        {characters.map((charIndex) => (
          <div
            key={charIndex}
            className={`character-item ${selectedCharacter === charIndex ? "selected" : ""}`}
            onClick={() => handleCharacterClick(charIndex)}
          >
            <img
              src={`/character_images/char${charIndex}.png`}
              alt={`Character ${charIndex}`}
              className="character-image"
            />
          </div>
        ))}
      </div>

      <h2 className="title mt-6">Select Role</h2>
      <div className="flex gap-4 justify-center mb-6">
        <button
          onClick={() => setRole("player")}
          className={`px-4 py-2 rounded ${role === "player" ? "bg-green-600 text-white" : "bg-gray-200"}`}
        >
          Player
        </button>
        <button
          onClick={() => setRole("murderer")}
          className={`px-4 py-2 rounded ${role === "murderer" ? "bg-red-600 text-white" : "bg-gray-200"}`}
        >
          Murderer
        </button>
      </div>

      <button
        className="start-button"
        onClick={handleStartGame}
        disabled={selectedCharacter === null || !role}
      >
        🚀 Start Game
      </button>
    </div>
  );
};

export default CharacterSelectSingle;
