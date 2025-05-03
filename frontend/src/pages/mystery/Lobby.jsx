// File: frontend/src/pages/mystery/Lobby.jsx

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "../../socket";
import "./Lobby.css";

const Lobby = () => {
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/lobby`)
      .then((res) => res.json())
      .then((data) => {
        if (data.players) {
          setPlayers(data.players);
          console.log("Players loaded:", data.players);
        }
      })
      .catch((err) => console.error("Failed to fetch players:", err));

    socket.on("lobby_update", (data) => {
      console.log("Lobby updated:", data.players);
      setPlayers(data.players);
    });

    return () => {
      socket.off("lobby_update");
    };
  }, []);

  const requestFullscreen = () => {
    const el = document.documentElement;

    if (el.requestFullscreen) el.requestFullscreen();
    else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    else if (el.msRequestFullscreen) el.msRequestFullscreen();
    else console.warn("Fullscreen not supported");
  };

  const handleStartGame = () => {
    requestFullscreen();
    navigate("/playground/dbms/mystery/game");
  };

  return (
    <div className="lobby-container">
      <h1>👬 Players in Lobby</h1>

      <div className="players-grid">
        {players.length === 0 && <p>No players yet...</p>}
        {players.map((player, index) => (
          <div key={index} className="player-card">
            <img
              src={`/character_images/${player.character}`}
              alt={`Character ${player.character}`}
              className="player-avatar"
            />
            <div className="player-name">{player.username}</div>
          </div>
        ))}
      </div>

      <button className="start-button" onClick={handleStartGame}>
        🚀 Start Game
      </button>
    </div>
  );
};

export default Lobby;
