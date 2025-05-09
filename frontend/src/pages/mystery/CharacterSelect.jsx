// File: frontend/src/pages/CharacterSelect.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "../../socket";
import "./CharacterSelect.css";

const CharacterSelect = () => {
  const navigate = useNavigate();
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [username, setUsername] = useState("");

  const characters = Array.from({ length: 10 }, (_, i) => i);

  const handleCharacterClick = async (charIndex) => {
    const name = prompt("Enter your username:");
    if (name && name.trim() !== "") {
      const trimmedName = name.trim();
      const characterImg = `char${charIndex}.png`;
      const assignedRole = (charIndex === 4 || charIndex === 5) ? "murderer" : "player";

      const playerData = {
        username: trimmedName,
        character: characterImg,
        role: assignedRole,
        sid: socket.id,
      };

      localStorage.setItem("playerInfo", JSON.stringify(playerData));

      socket.emit("player_join", {
        sid: playerData.sid,
        username: playerData.username,
        character: playerData.character,
        role: playerData.role,
      });

      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/player/save`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: trimmedName,
            character: characterImg,
          }),
        });

        const data = await res.json();
        if (!res.ok) {
          console.warn("⚠️ Failed to save player:", data.error);
        } else {
          console.log("✅ Player saved to DB:", data);
        }
      } catch (err) {
        console.error("❌ Error saving player to DB:", err);
      }

      setSelectedCharacter(charIndex);
      setUsername(trimmedName);
    } else {
      alert("Username is required!");
    }
  };

  const handleGoToLobby = () => {
    if (selectedCharacter !== null && username !== "") {
      navigate("/playground/dbms/mystery/lobby");
    } else {
      alert("Please select a character and enter a username.");
    }
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

      <button
        className="start-button"
        onClick={handleGoToLobby}
        disabled={selectedCharacter === null || username === ""}
      >
        🚀 Go to Lobby
      </button>
    </div>
  );
};

export default CharacterSelect;
