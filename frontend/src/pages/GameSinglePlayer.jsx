import React, { useEffect, useState } from "react";
import { Joystick } from "react-joystick-component";
import { locations, locations_with_questions } from "./MysteryLocations";
import "./Game.css";

const GameSinglePlayer = () => {
  const [myPosition, setMyPosition] = useState({ x: 300, y: 300 });
  const [movementDirection, setMovementDirection] = useState(null);
  const [reachedLocation, setReachedLocation] = useState("");
  const [showQuestion, setShowQuestion] = useState(false);
  const [questionData, setQuestionData] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [hint, setHint] = useState(null);
  const [highlightedAnswer, setHighlightedAnswer] = useState("");
  const [gameOver, setGameOver] = useState(false);

  const detectionRadius = 60;
  const scaleFactor = window.innerWidth < 768 ? 1.5 : 1;
  const API_URL = import.meta.env.VITE_API_URL;

  const playerInfo = JSON.parse(localStorage.getItem("playerInfo")) || {};
  const character = playerInfo.character;
  const role = playerInfo.role || "player";

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
    const scaledX = pos.x / scaleFactor;
    const scaledY = pos.y / scaleFactor;

    for (let loc of locations) {
      const dx = scaledX - loc.x;
      const dy = scaledY - loc.y;
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

    const path = role === "murderer" ? "murderer" : "player";
    try {
      const res = await fetch(`${API_URL}/api/gamequestion/${path}/${locMap.q}`);
      const data = await res.json();
      setQuestionData({ ...data, location: reachedLocation });
      setShowQuestion(true);
    } catch (err) {
      console.error("❌ Error fetching question:", err);
    }
  };

  const handleSubmit = async () => {
    const trimmedUser = userAnswer.trim();
    const trimmedCorrect = questionData.answer_query.trim();

    try {
      const res = await fetch(`${API_URL}/api/sql/evaluate_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_answer: trimmedUser, correct_answer: trimmedCorrect }),
      });

      const data = await res.json();
      setHighlightedAnswer(data.highlighted_answer || "");
      const score = data.score || 0;

      if (score >= 0.95) {
        setFeedback("✅ Excellent! You've nailed it.");
        setHint(`💡 Hint: ${questionData.hint}`);

        if (parseInt(questionData.order) === 10) {
          setTimeout(() => {
            setGameOver(true);
            setShowQuestion(false);
          }, 1500);
        } else {
          setTimeout(() => {
            setShowQuestion(false);
            setUserAnswer("");
            setFeedback(null);
            setHint(null);
            setHighlightedAnswer("");
          }, 1500);
        }
      } else {
        setFeedback("❌ Not quite right. Try again.");
      }
    } catch (err) {
      console.error("Evaluation error:", err);
      setFeedback("❌ Server error.");
    }
  };

  return (
    <div className="game-container">
      <div className="player" style={{ left: myPosition.x, top: myPosition.y }}>
        <img src={`/character_images/${character}`} alt="Player" className="player-image" />
        <p className="player-name">You</p>
      </div>

      {reachedLocation && !showQuestion && (
        <>
          <div className="location-banner">📍 You reached {reachedLocation}</div>
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
            {feedback && <p className="feedback">{feedback}</p>}
            {hint && <p className="hint">{hint}</p>}
            {highlightedAnswer && (
              <div className="highlighted-box">
                <strong>✅ Reference Answer:</strong>
                <p dangerouslySetInnerHTML={{ __html: highlightedAnswer }} />
              </div>
            )}
            <button className="close-btn" onClick={() => setShowQuestion(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      {gameOver && (
        <div className="popup-overlay">
          <div className="popup-box">
            <h2>🏁 Game Over! You Won!</h2>
            <p>🎉 You've solved the final mystery clue and cracked the case!</p>
            <button className="close-btn" onClick={() => window.location.reload()}>
              Play Again
            </button>
          </div>
        </div>
      )}

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

export default GameSinglePlayer;
