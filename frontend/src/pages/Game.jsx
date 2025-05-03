// File: frontend/src/pages/Game.jsx

import React, { useEffect, useState } from "react";
import { socket } from "../socket";
import { Joystick } from "react-joystick-component";
import { locations as locationList } from "./MysteryLocations";
import QuestionPopup from "../components/QuestionPopup";
import "./Game.css";

const Game = () => {
  const [players, setPlayers] = useState([]);
  const [mySID, setMySID] = useState(null);
  const [myPosition, setMyPosition] = useState({ x: 300, y: 300 });
  const [movementDirection, setMovementDirection] = useState(null);
  const [reachedLocation, setReachedLocation] = useState("");
  const [showQuestion, setShowQuestion] = useState(false);

  const detectionRadius = 60;

  useEffect(() => {
    const resizeGame = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`);
    };
    resizeGame();
    window.addEventListener("resize", resizeGame);
    return () => window.removeEventListener("resize", resizeGame);
  }, []);

  useEffect(() => {
    socket.on("connect", () => {
      const sid = socket.id;
      setMySID(sid);
      console.log("🧩 Connected with SID:", sid);
      socket.emit("player_move", myPosition);
    });

    socket.on("player_positions", (updatedPlayers) => {
      setPlayers(updatedPlayers);
      console.log("📦 Updated player positions:", updatedPlayers);
    });

    const moveInterval = setInterval(() => {
      if (movementDirection) {
        const step = 1;
        let newX = myPosition.x;
        let newY = myPosition.y;
        const halfSize = window.innerWidth < 768 ? 30 : 50;

        if (movementDirection === "FORWARD") newY -= step;
        if (movementDirection === "BACKWARD") newY += step;
        if (movementDirection === "LEFT") newX -= step;
        if (movementDirection === "RIGHT") newX += step;

        newX = Math.max(halfSize, Math.min(newX, window.innerWidth - halfSize));
        newY = Math.max(halfSize, Math.min(newY, window.innerHeight - halfSize));

        const updatedPos = { x: newX, y: newY };
        setMyPosition(updatedPos);
        socket.emit("player_move", updatedPos);
        checkLocationProximity(updatedPos);
      }
    }, 16);

    return () => {
      clearInterval(moveInterval);
      socket.off("player_positions");
    };
  }, [movementDirection, myPosition]);

  useEffect(() => {
    if (socket.connected) {
      socket.emit("player_move", myPosition);
    }

    const handleKeyDown = (e) => {
      const directionMap = {
        ArrowUp: "FORWARD",
        ArrowDown: "BACKWARD",
        ArrowLeft: "LEFT",
        ArrowRight: "RIGHT",
      };
      if (directionMap[e.key]) setMovementDirection(directionMap[e.key]);
    };
    const handleKeyUp = () => setMovementDirection(null);

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  const handleJoystickMove = (event) => {
    setMovementDirection(event.direction);
  };

  const handleJoystickStop = () => {
    setMovementDirection(null);
  };

  const checkLocationProximity = (pos) => {
    for (let loc of locationList) {
      const dx = pos.x - loc.x;
      const dy = pos.y - loc.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      if (distance < detectionRadius) {
        setReachedLocation(loc.name);
        return;
      }
    }
    setReachedLocation("");
  };

  const mockQuestion = {
    location: "Lab",
    question: "Write a SQL query to find the names of students with GPA above 3.5 from the student table.",
  };

  return (
    <div className="game-container">
      {/* Render players */}
      {players.map((player, index) => (
        <div
          key={index}
          className="player"
          style={{
            left: player.x,
            top: player.y,
          }}
        >
          <img
            src={`/character_images/${player.character}`}
            alt={player.username}
            className="player-image"
          />
          <p className="player-name">{player.username}</p>
        </div>
      ))}

      {/* Location reached banner */}
      {reachedLocation && (
        <div className="location-banner">
          🔍 You have reached <strong>{reachedLocation}</strong>
        </div>
      )}

      {/* Show question prompt if reached Lab */}
      {reachedLocation === "Lab" && !showQuestion && (
        <div className="see-question-button">
          <button onClick={() => setShowQuestion(true)}>See Question</button>
        </div>
      )}

      {/* Question Modal */}
      {showQuestion && (
        <QuestionPopup
          questionData={mockQuestion}
          onClose={() => setShowQuestion(false)}
        />
      )}

      {/* Joystick for mobile */}
      {window.innerWidth < 768 && (
        <div className="joystick-container">
          <Joystick
            size={80}
            baseColor="rgba(100, 100, 100, 0.5)"
            stickColor="rgba(255, 255, 0, 0.9)"
            move={handleJoystickMove}
            stop={handleJoystickStop}
            throttle={100}
            stickShape="circle"
          />
        </div>
      )}
    </div>
  );
};

export default Game;
