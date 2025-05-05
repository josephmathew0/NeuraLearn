// File: frontend/src/pages/mystery/Lobby.jsx

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { socket } from "../../socket";
import "./Lobby.css";

const Lobby = () => {
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // 🔁 Fetch current lobby players from backend
    fetch(`${import.meta.env.VITE_API_URL}/api/lobby`)
      .then((res) => res.json())
      .then((data) => {
        if (data.players) {
          console.log("📦 Initial Lobby:");
          data.players.forEach((p, i) =>
            console.log(`   ${i + 1}. ${p.username} (${p.character}) → ${p.role}`)
          );
          setPlayers(data.players);
        }
      })
      .catch((err) => console.error("❌ Failed to fetch players:", err));

    // 🔔 Listen for lobby updates
    socket.on("lobby_update", (data) => {
      console.log("🔄 [Socket] Lobby update received:");
      data.players.forEach((p, i) =>
        console.log(`   ${i + 1}. ${p.username} (${p.character}) → ${p.role}`)
      );
      setPlayers(data.players);
    });

    return () => {
      socket.off("lobby_update");
    };
  }, []);

  useEffect(() => {
    socket.on("connect", () => {
      const playerInfo = JSON.parse(localStorage.getItem("playerInfo"));
      if (playerInfo) {
        socket.emit("player_join", {
          sid: socket.id,
          username: playerInfo.username,
          character: playerInfo.character,
          role: playerInfo.role,
        });
        console.log(`📤 Sent player_join → ${playerInfo.username} (${playerInfo.character}) → Role: ${playerInfo.role}`);
      }
    });

    return () => {
      socket.off("connect");
    };
  }, []);

  const requestFullscreen = () => {
    const el = document.documentElement;
    if (el.requestFullscreen) el.requestFullscreen();
    else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    else if (el.msRequestFullscreen) el.msRequestFullscreen();
  };

  const handleStartGame = () => {
    requestFullscreen();
    socket.emit("start_game");
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
            {/* Role removed as per instruction */}
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
