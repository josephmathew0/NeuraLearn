import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "../../socket";
import "./CharacterSelect.css";

const CharacterSelect = () => {
  const navigate = useNavigate();
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [username, setUsername] = useState("");

  const characters = Array.from({ length: 10 }, (_, i) => i);

  const handleCharacterClick = (charIndex) => {
    const name = prompt("Enter your username:");
    if (name && name.trim() !== "") {
      const trimmedName = name.trim();
      const characterImg = `char${charIndex}.png`;

      setSelectedCharacter(charIndex);
      setUsername(trimmedName);

      // ✅ Emit immediately after both name and image are known
      socket.emit("player_join", {
        username: trimmedName,
        character: characterImg,
      });
      localStorage.setItem("playerData", JSON.stringify({ trimmedName, characterImg }));
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
