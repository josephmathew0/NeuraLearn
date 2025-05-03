// File: frontend/src/pages/MysteryMap.jsx

import React, { useState, useEffect } from "react";
import { Joystick } from "react-joystick-component";
import { locations as fullLocations } from "./MysteryLocations";

const MysteryMap = () => {
  const [playerPos, setPlayerPos] = useState({ x: 300, y: 300 });
  const [message, setMessage] = useState("");
  const [movingDirection, setMovingDirection] = useState(null);

  const speed = 2; // Consistent smooth speed

  const movePlayerByKeyboard = (e) => {
    e.preventDefault();
    if (!["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) return;
    const directionMap = {
      ArrowUp: "FORWARD",
      ArrowDown: "BACKWARD",
      ArrowLeft: "LEFT",
      ArrowRight: "RIGHT",
    };
    setMovingDirection(directionMap[e.key]);
  };

  const stopMovingByKeyboard = (e) => {
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
      setMovingDirection(null);
    }
  };

  const handleJoystickMove = (event) => {
    setMovingDirection(event.direction);
  };

  const handleJoystickStop = () => {
    setMovingDirection(null);
  };

  // Get dynamic scaling based on screen size
  const getScaleX = () => window.innerWidth / 1450;
  const getScaleY = () => window.innerHeight / 800;

  const scaledLocations = fullLocations.map((loc) => ({
    name: loc.name,
    x: loc.x * getScaleX(),
    y: loc.y * getScaleY(),
  }));

  useEffect(() => {
    const interval = setInterval(() => {
      if (movingDirection) {
        setPlayerPos((pos) => {
          let newX = pos.x;
          let newY = pos.y;

          if (movingDirection === "FORWARD") newY -= speed;
          if (movingDirection === "BACKWARD") newY += speed;
          if (movingDirection === "LEFT") newX -= speed;
          if (movingDirection === "RIGHT") newX += speed;

          newX = Math.max(0, Math.min(newX, window.innerWidth - 30));
          newY = Math.max(0, Math.min(newY, window.innerHeight - 30));

          return { x: newX, y: newY };
        });
      }
    }, 16);
    return () => clearInterval(interval);
  }, [movingDirection]);

  useEffect(() => {
    window.addEventListener("keydown", movePlayerByKeyboard);
    window.addEventListener("keyup", stopMovingByKeyboard);
    return () => {
      window.removeEventListener("keydown", movePlayerByKeyboard);
      window.removeEventListener("keyup", stopMovingByKeyboard);
    };
  }, []);

  useEffect(() => {
    checkCollision();
  }, [playerPos]);

  let detectionRadius = 20;

  const getDetectionRadius = () => {
    const widthScale = window.innerWidth / 1450;
    const heightScale = window.innerHeight / 800;
    return 30 * Math.min(widthScale, heightScale);
  };  

  const checkCollision = () => {
    for (const location of scaledLocations) {
      const dx = playerPos.x - location.x;
      const dy = playerPos.y - location.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      if (distance < detectionRadius) {
        setMessage(`🔍 You found the ${location.name}!`);
        return;
      }
    }
    setMessage("");
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        backgroundImage: "url('/mystery_map.png')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Player */}
      <div
        style={{
          width: 30,
          height: 30,
          borderRadius: "50%",
          backgroundColor: "yellow",
          position: "absolute",
          left: playerPos.x,
          top: playerPos.y,
        }}
      />

      {/* Message */}
      {message && (
        <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-80 text-white px-4 py-2 rounded-lg shadow-lg text-center">
          {message}
        </div>
      )}

      {/* Joystick on Mobile */}
      {window.innerWidth < 768 && (
        <div className="absolute bottom-10 left-10">
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

export default MysteryMap;
