// File: frontend/src/pages/UnifiedTextAnswer.jsx

import React, { useEffect, useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import "../styles/TextAnswer.css";

const UnifiedTextAnswer = () => {
  const location = useLocation();
  const subject = location.pathname.includes("dbms") ? "dbms" : "biology";

  const [data, setData] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [highlightedAnswer, setHighlightedAnswer] = useState("");
  const [modelScore, setModelScore] = useState(null);
  const [tokenScore, setTokenScore] = useState(null);
  const [usedScore, setUsedScore] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [t5Feedback, setT5Feedback] = useState("");
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  const fetchQuestion = async () => {
    setShowFeedback(false);
    setUserAnswer("");

    const endpoint =
    subject === "dbms"
      ? `${import.meta.env.VITE_API_URL}/api/sql/textanswer`
      : `${import.meta.env.VITE_API_URL}/api/text`;


    const res = await fetch(endpoint);
    const q = await res.json();
    setData(q);
    console.log("✅ Correct Answer:", q.correct_answer || q.answer);
  };

  useEffect(() => {
    fetchQuestion();
  }, [subject]);

  const replacements = {
    "greater than": ">",
    "less than": "<",
    "equal to": "=",
    "not equal to": "!=",
    "star": "*",
    "multiply": "*",
    "plus": "+",
    "minus": "-",
    "divide": "/",
    "mod": "%",
    "percent": "%",
    "semicolon": ";",
    "comma": ",",
    "dot": ".",
    "full stop": ".",
    "open bracket": "(",
    "close bracket": ")",
    "bracket": "BRACKET",
    "quote": "QUOTE",
    "single quote": "QUOTE",
  };

  const handleSpeechToggle = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    if (!recognitionRef.current) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = "en-US";
      recognition.continuous = true;
      recognition.interimResults = false;

      recognition.onresult = (event) => {
        let transcript = Array.from(event.results)
          .map((r) => r[0].transcript)
          .join(" ");

        for (const [key, value] of Object.entries(replacements)) {
          const regex = new RegExp(`\\b${key}\\b`, "gi");
          transcript = transcript.replace(regex, value);
        }

        let bracketCount = 0;
        transcript = transcript
          .split(" ")
          .map((word) => {
            if (word === "BRACKET") {
              bracketCount++;
              return bracketCount % 2 === 0 ? ")" : "(";
            }
            return word;
          })
          .join(" ");

        let quoteCount = 0;
        transcript = transcript
          .split(" ")
          .map((word) => {
            if (word === "QUOTE") {
              quoteCount++;
              return "'";
            }
            return word;
          })
          .join(" ");

        transcript = transcript.replace(/\s*'\s*/g, "'").replace(/'(?=\w)/g, "'");

        setUserAnswer(transcript.trim());
      };

      recognition.onerror = (event) => {
        console.error("🎤 Speech Error:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }

    if (!isListening) {
      recognitionRef.current.start();
      setIsListening(true);
    } else {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const handleCheck = async () => {
    try {
      const res = await fetch(
        subject === "dbms"
          ? `${import.meta.env.VITE_API_URL}/api/sql/evaluate_text`
          : `${import.meta.env.VITE_API_URL}/api/evaluate_text`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_answer: userAnswer,
            correct_answer: data.correct_answer || data.answer,
          }),
        }
      );      

      const result = await res.json();
      console.log("🧠 Model Score:", result.model_score || result.score);
      console.log("🔤 Token Score:", result.token_score || "Not Available");

      setModelScore(result.model_score || result.score);
      setTokenScore(result.token_score || result.score);
      setUsedScore(Math.max(result.model_score || result.score, result.token_score || result.score));

      setFeedback(result.feedback || result.level);
      setHighlightedAnswer(result.highlighted_answer);
      setT5Feedback(result.t5_feedback);
      setShowFeedback(true);
    } catch (err) {
      console.error("❌ Evaluation error", err);
      setFeedback("Something went wrong while evaluating your answer.");
      setShowFeedback(true);
    }
  };

  const getLevel = () => {
    if (usedScore >= 0.95) return "🌟 Excellent";
    if (usedScore >= 0.85) return "👍 Good";
    if (usedScore >= 0.7) return "✅ Fair";
    return "❗ Try Again";
  };

  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6 text-center max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">
        🧠 {subject === "dbms" ? "DBMS Text Answer" : "Biology Text Answer"}
      </h2>
      <p className="mb-6 text-lg">{data.question}</p>

      <textarea
        className="w-full border border-gray-400 p-3 rounded mb-4"
        rows={5}
        placeholder="Type your answer here..."
        value={userAnswer}
        onChange={(e) => setUserAnswer(e.target.value)}
      />

      <div className="mb-4 flex justify-center gap-4">
        <button
          onClick={handleCheck}
          className="bg-green-200 px-4 py-2 rounded hover:bg-green-300"
        >
          ✅ Check Answer
        </button>
        <button
          onClick={handleSpeechToggle}
          className={`px-4 py-2 rounded ${
            isListening ? "bg-red-200" : "bg-gray-200"
          } hover:bg-gray-300`}
        >
          🎙️ {isListening ? "Listening..." : "Speak"}
        </button>
        {showFeedback && (
          <button
            onClick={fetchQuestion}
            className="bg-blue-200 px-4 py-2 rounded hover:bg-blue-300"
          >
            ➡️ Next
          </button>
        )}
      </div>

      {showFeedback && (
        <div className="mt-6 text-left bg-gray-100 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">🧠 Feedback</h3>
          <p className="mb-2">{feedback}</p>
          <p className="text-sm text-gray-600 mb-1">
            Model Score: <strong>{(modelScore * 100).toFixed(2)}%</strong> <br />
            Token Score: <strong>{(tokenScore * 100).toFixed(2)}%</strong>
          </p>
          <p className="mt-2 text-lg font-bold">
            Final Score: <span className="font-normal">{(usedScore * 100).toFixed(2)}%</span> – {getLevel()}
          </p>
          <p className="mt-3 text-xl font-semibold text-gray-800">Model Answer:</p>
          <p
            className="mt-1 text-base leading-relaxed"
            dangerouslySetInnerHTML={{ __html: highlightedAnswer }}
          />
        </div>
      )}

      {t5Feedback && (
        <>
          <p className="mt-4 text-xl font-semibold text-gray-800">🧠 Additional Feedback (T5):</p>
          <p className="mt-1 text-base leading-relaxed italic text-indigo-700">
            {t5Feedback}
          </p>
        </>
      )}
    </div>
  );
};

export default UnifiedTextAnswer;
