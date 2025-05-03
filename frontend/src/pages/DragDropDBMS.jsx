import React, { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import "../styles/DragDrop.css";

export default function PlaygroundDBMSDrag() {
  const [question, setQuestion] = useState("");
  const [draggables, setDraggables] = useState([]);
  const [correctAnswer, setCorrectAnswer] = useState([]);
  const [userAnswer, setUserAnswer] = useState([]);
  const [resultShown, setResultShown] = useState(false);
  const [correctnessMap, setCorrectnessMap] = useState([]);
  const [questionIndex, setQuestionIndex] = useState(1);
  const [previousWrong, setPreviousWrong] = useState(null);
  const [attempted, setAttempted] = useState(false);

  useEffect(() => {
    fetchQuestion(questionIndex);
  }, [questionIndex]);

  const fetchQuestion = async (index) => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/sql/dragdrop/${index}`);
      const data = await res.json();

      setQuestion(data.question);
      setCorrectAnswer(splitWithSemicolon(data.correct_answer));
      setDraggables(splitWithSemicolon(data.correct_answer));
      setUserAnswer([]);
      setResultShown(false);
      setCorrectnessMap([]);
      setAttempted(false);
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  const splitWithSemicolon = (sentence) => {
    return sentence.replace(";", " ;").split(" ").filter(Boolean);
  };

  const handleOnDragEnd = (result) => {
    const { source, destination } = result;
    if (!destination) return;

    const fromBank = source.droppableId === "draggable-bank";
    const toAnswer = destination.droppableId === "droppable-area";

    if (fromBank && toAnswer) {
      const item = draggables[source.index];
      const newUserAnswer = Array.from(userAnswer);
      newUserAnswer.splice(destination.index, 0, item);
      setUserAnswer(newUserAnswer);
    } else if (source.droppableId === "droppable-area" && toAnswer) {
      const reordered = Array.from(userAnswer);
      const [moved] = reordered.splice(source.index, 1);
      reordered.splice(destination.index, 0, moved);
      setUserAnswer(reordered);
    } else if (source.droppableId === "droppable-area" && destination.droppableId === "draggable-bank") {
      const updated = Array.from(userAnswer);
      updated.splice(source.index, 1);
      setUserAnswer(updated);
    }
  };

  const checkAnswer = () => {
    let correctMap = {};
    let userMap = {};

    correctAnswer.forEach((word, idx) => (correctMap[word] = idx));
    userAnswer.forEach((word, idx) => (userMap[word] = idx));

    let feedback = userAnswer.map((word, idx) => (userMap[word] === correctMap[word] ? "correct" : "incorrect"));
    setCorrectnessMap(feedback);
    setResultShown(true);
    setAttempted(true);

    const isCorrect = userAnswer.join(" ") === correctAnswer.join(" ");
    if (!isCorrect) setPreviousWrong(questionIndex);
    else setPreviousWrong(null);
  };

  const handleNext = () => {
    if (previousWrong && attempted) {
      setQuestionIndex(previousWrong);
      setPreviousWrong(null);
    } else {
      setQuestionIndex((prev) => prev + 1);
    }
  };

  const calculateCorrectness = () => {
    if (!correctnessMap.length) return 0;
    const correct = correctnessMap.filter((f) => f === "correct").length;
    return ((correct / correctAnswer.length) * 100).toFixed(0);
  };

  return (
    <div className="dragdrop-container">
      <h1>🥁 Drag-and-Drop SQL</h1>
      <p>{question}</p>

      <DragDropContext onDragEnd={handleOnDragEnd}>
        <Droppable droppableId="droppable-area" direction="horizontal">
          {(provided) => (
            <div className="drop-row" {...provided.droppableProps} ref={provided.innerRef}>
              {userAnswer.map((word, index) => (
                <Draggable key={word + index} draggableId={word + index} index={index}>
                  {(provided) => (
                    <div
                      className={`drop-item ${
                        resultShown ? (correctnessMap[index] === "correct" ? "correct" : "incorrect") : ""
                      }`}
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    >
                      {word}
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>

        <Droppable droppableId="draggable-bank" direction="horizontal">
          {(provided) => (
            <div className="drag-bank" {...provided.droppableProps} ref={provided.innerRef}>
              {draggables.map((word, index) => (
                <Draggable key={word + "-bank-" + index} draggableId={word + "-bank-" + index} index={index}>
                  {(provided) => (
                    <div className="draggable" ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                      {word}
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>

      <button className="check-button" onClick={checkAnswer}>
        ✅ Check
      </button>

      {resultShown && (
        <>
          <p>{calculateCorrectness()}% correct {calculateCorrectness() === "100" ? "✅ Correct" : "❌ Incorrect"}</p>
          <p>
            Correct Answer: <strong>{correctAnswer.join(" ")}</strong>
          </p>
          <button className="next-button" onClick={handleNext}>Next ⏭️</button>
        </>
      )}
    </div>
  );
}
