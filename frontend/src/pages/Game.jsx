// File: frontend/src/pages/Game.jsx

import React, { useEffect, useState } from "react";
import { socket } from "../socket";
import { Joystick } from "react-joystick-component";
import { locations, locations_with_questions } from "./MysteryLocations";
import "./Game.css";

const Game = () => {
  const [players, setPlayers] = useState([]);
  const [mySID, setMySID] = useState(null);
  const [myPosition, setMyPosition] = useState({ x: 300, y: 300 });
  const [movementDirection, setMovementDirection] = useState(null);
  const [reachedLocation, setReachedLocation] = useState("");
  const [showQuestion, setShowQuestion] = useState(false);
  const [questionData, setQuestionData] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [hint, setHint] = useState(null);
  const [error, setError] = useState("");
  const [highlightedAnswer, setHighlightedAnswer] = useState("");
  const [gameOverData, setGameOverData] = useState(null);

  const screenHeight = window.innerHeight;
  const isMobile = window.innerWidth < 768;
  const scaleFactor = isMobile ? screenHeight / 700 : 1;
  const detectionRadius = 60 * scaleFactor;
  const playerSize = isMobile ? 40 : 60;

  const scaledLocations = locations.map(loc => ({
    ...loc,
    x: loc.x * scaleFactor,
    y: loc.y * scaleFactor,
  }));

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
      const playerInfo = JSON.parse(localStorage.getItem("playerInfo"));
      if (playerInfo) {
        socket.emit("player_move", { ...myPosition, character: playerInfo.character });
      }
    });

    socket.on("player_positions", (updatedPlayers) => {
      setPlayers(updatedPlayers);
    });

    socket.on("game_over", ({ winner, murderers }) => {
      setGameOverData({ winner, murderers });
    });

    return () => {
      socket.off("connect");
      socket.off("player_positions");
      socket.off("game_over");
    };
  }, [myPosition]);

  useEffect(() => {
    const moveInterval = setInterval(() => {
      if (movementDirection) {
        const step = 1.5 * scaleFactor;
        let newX = myPosition.x;
        let newY = myPosition.y;
        const halfSize = playerSize / 2;

        if (movementDirection === "FORWARD") newY -= step;
        if (movementDirection === "BACKWARD") newY += step;
        if (movementDirection === "LEFT") newX -= step;
        if (movementDirection === "RIGHT") newX += step;

        newX = Math.max(halfSize, Math.min(newX, window.innerWidth - halfSize));
        newY = Math.max(halfSize, Math.min(newY, window.innerHeight - halfSize));

        const updatedPos = { x: newX, y: newY };
        setMyPosition(updatedPos);

        const playerInfo = JSON.parse(localStorage.getItem("playerInfo"));
        socket.emit("player_move", { ...updatedPos, character: playerInfo?.character });
        checkLocationProximity(updatedPos);
      }
    }, 16);

    return () => clearInterval(moveInterval);
  }, [movementDirection, myPosition]);

  useEffect(() => {
    const directionMap = {
      ArrowUp: "FORWARD",
      ArrowDown: "BACKWARD",
      ArrowLeft: "LEFT",
      ArrowRight: "RIGHT",
    };
    const handleKeyDown = (e) => directionMap[e.key] && setMovementDirection(directionMap[e.key]);
    const handleKeyUp = () => setMovementDirection(null);

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  const handleJoystickMove = (event) => setMovementDirection(event.direction);
  const handleJoystickStop = () => setMovementDirection(null);

  const checkLocationProximity = (pos) => {
    for (let loc of scaledLocations) {
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

  const fetchQuestion = async () => {
    const locMap = locations_with_questions.find((l) => l.name === reachedLocation);
    if (!locMap) return;

    const playerInfo = JSON.parse(localStorage.getItem("playerInfo"));
    const path = ["char4.png", "char5.png"].includes(playerInfo.character) ? "murderer" : "player";

    try {
      const url = `${import.meta.env.VITE_API_URL}/api/gamequestion/${path}/${locMap.q}`;
      const res = await fetch(url);
      const data = await res.json();
      setQuestionData({
        location: reachedLocation,
        question: data.question,
        answer_query: data.answer_query,
        hint: data.hint,
        order: data.question_order,
      });
      setShowQuestion(true);
    } catch (err) {
      console.error("❌ Error fetching question:", err);
    }
  };

  const handleSubmit = async () => {
    setError("");
    setFeedback(null);
    setHint(null);
    setHighlightedAnswer("");

    if (!questionData || !questionData.answer_query?.trim()) {
      setError("⚠️ Missing question data. Please try a different location.");
      return;
    }

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/sql/evaluate_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_answer: userAnswer.trim(),
          correct_answer: questionData.answer_query.trim(),
        }),
      });
      const data = await res.json();
      setHighlightedAnswer(data.highlighted_answer || "");

      if (data.score >= 0.95) {
        setFeedback("✅ Excellent! You've nailed it.");
        setHint(`💡 Hint: ${questionData.hint}`);
        const playerInfo = JSON.parse(localStorage.getItem("playerInfo"));

        if (questionData.order == 10) {
          socket.emit("game_over", {
            winner: playerInfo.username,
            murderers: players.filter((p) => p.role === "murderer").map((p) => p.username),
          });
        } else {
          socket.emit("question_correct", { sid: mySID });
        }
      } else if (data.score >= 0.85) {
        setFeedback("👍 Good job! You're almost there.");
        setHint(`💡 Hint: ${questionData.hint}`);
      } else if (data.score >= 0.7) {
        setFeedback("⚠️ Fair attempt. Try to include more keywords.");
      } else {
        setFeedback("❌ Your answer misses key concepts. Try again.");
      }
    } catch (err) {
      console.error("Error evaluating answer:", err);
      setError("❌ Server error occurred. Please try again.");
    }
  };

  return (
    <div className="game-container">
      {players.map((player, index) => (
        <div
          key={index}
          className="player"
          style={{
            left: player.x,
            top: player.y,
            width: playerSize,
            height: playerSize,
          }}
        >
          <img
            src={`/character_images/${player.character}`}
            alt={player.username}
            className="player-image"
            style={{ width: "100%", height: "100%", objectFit: "contain" }}
          />
          <p className="player-name">{player.username}</p>
        </div>
      ))}

      {reachedLocation && !showQuestion && (
        <>
          <div className="location-banner">🔍 You have reached {reachedLocation}</div>
          <div className="see-question-button">
            <button onClick={fetchQuestion}>See Question</button>
          </div>
        </>
      )}

      {showQuestion && questionData && (
        <div className="popup-overlay">
          <div className="popup-box">
            <h2>📘 Question at {questionData.location}</h2>
            <p>{questionData.question}</p>
            <textarea
              placeholder="Type your SQL answer here..."
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
            />
            <button onClick={handleSubmit}>Submit</button>
            {error && <p className="feedback error">{error}</p>}
            {feedback && <p className="feedback">{feedback}</p>}
            {hint && <p className="hint">{hint}</p>}
            {highlightedAnswer && (
              <div className="highlighted-box">
                <strong>✅ Answer Reference:</strong>
                <p dangerouslySetInnerHTML={{ __html: highlightedAnswer }} />
              </div>
            )}
            <button className="close-btn" onClick={() => setShowQuestion(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      {gameOverData && (
        <div className="popup-overlay">
          <div className="popup-box">
            <h2>🏁 Game Over!</h2>
            <p>🎉 <strong>{gameOverData.winner}</strong> has finished all questions first!</p>
            <p>🕵️‍♂️ Murderers: <strong>{gameOverData.murderers.join(", ")}</strong></p>
            <button className="close-btn" onClick={() => window.location.reload()}>
              Restart
            </button>
          </div>
        </div>
      )}

      {isMobile && (
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
