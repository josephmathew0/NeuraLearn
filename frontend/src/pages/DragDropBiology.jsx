import React, { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import "./DragDrop.css";

const DragDrop = () => {
  const [dragData, setDragData] = useState(null);
  const [droppedItems, setDroppedItems] = useState([]);
  const [availableDrags, setAvailableDrags] = useState([]);
  const [highlightStatus, setHighlightStatus] = useState([]);
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/drag`)
      .then((res) => res.json())
      .then((data) => {
        const parsedDraggables = data.draggables.split(',').map(s => s.trim());
        setDragData(data);
        setAvailableDrags(parsedDraggables);
        setDroppedItems(Array((data.drag_question.match(/_____/g) || []).length).fill(null));
        console.log("🟨 Full Answer:", data.full_answer);
      });
  }, []);

  const handleDragEnd = (result) => {
    const { source, destination, draggableId } = result;
    if (!destination) return;

    if (source.droppableId === "draggables" && destination.droppableId.startsWith("drop-")) {
      const dropIndex = parseInt(destination.droppableId.split("-")[1]);
      const newDropped = [...droppedItems];
      newDropped[dropIndex] = draggableId;

      const newAvailable = [...availableDrags];
      newAvailable.splice(source.index, 1);

      setDroppedItems(newDropped);
      setAvailableDrags(newAvailable);
    } else if (source.droppableId.startsWith("drop-") && destination.droppableId === "draggables") {
      const dropIndex = parseInt(source.droppableId.split("-")[1]);
      const newAvailable = [...availableDrags];
      newAvailable.splice(destination.index, 0, droppedItems[dropIndex]);

      const newDropped = [...droppedItems];
      newDropped[dropIndex] = null;

      setDroppedItems(newDropped);
      setAvailableDrags(newAvailable);
    }
  };

  const handleReset = () => {
    const allDrags = [...availableDrags, ...droppedItems.filter(Boolean)];
    setDroppedItems(Array(droppedItems.length).fill(null));
    setAvailableDrags(allDrags);
    setHighlightStatus([]);
    setAttempts(0);
  };

  const sortCorrectWordsByFullAnswer = (correctWords, fullAnswer) => {
    const fullWords = fullAnswer
      .replace(/[.,!?\-]/g, "")
      .toLowerCase()
      .split(/\s+/);

    const clean = (word) => word.toLowerCase().replace(/[.,!?\-]/g, "");

    const getIndex = (word) => {
      const cleaned = clean(word);
      return fullWords.indexOf(cleaned) !== -1 ? fullWords.indexOf(cleaned) : Infinity;
    };

    return [...correctWords]
      .map(w => w.replace(/[.,!?\-]/g, ""))
      .sort((a, b) => getIndex(a) - getIndex(b));
  };

  const handleCheck = () => {
    const originalCorrectWords = dragData.correct_answer.trim().split(/\s+/);
    // const correctWords = sortCorrectWordsByFullAnswer(originalCorrectWords, dragData.full_answer);
    const userWords = droppedItems.map(item => item?.trim().toLowerCase());
    const correctWords = sortCorrectWordsByFullAnswer(dragData.correct_answer.trim().split(/\s+/), dragData.full_answer).map(w => w.toLowerCase());

    console.log("✅ Sorted Correct:", correctWords);
    console.log("🧠 User Words:", userWords);

    const newHighlight = userWords.map((word, idx) => word === correctWords[idx]);
    const isCorrect = newHighlight.every(Boolean);

    setHighlightStatus(newHighlight);
    setAttempts(prev => prev + 1);

    if (isCorrect) {
      alert("✅ Correct!");
      return;
    }

    if (attempts + 1 >= 2) {
      alert("❌ Showing correct answer.");
      const correctFilled = correctWords.slice(0, droppedItems.length);
      setDroppedItems(correctFilled);
      setAvailableDrags([]);
      setHighlightStatus(Array(correctFilled.length).fill(true));
    } else {
      alert("❌ Try again!");
    }
  };

  const renderSentence = () => {
    const parts = dragData.drag_question.split("_____");
    const sentence = [];
    for (let i = 0; i < parts.length; i++) {
      sentence.push(<span key={`text-${i}`}>{parts[i]}</span>);
      if (i < droppedItems.length) {
        sentence.push(
          <Droppable key={`drop-${i}`} droppableId={`drop-${i}`}>
            {(provided, snapshot) => (
              <span
                className={`droppable ${snapshot.isDraggingOver ? "drag-over" : ""}`}
                ref={provided.innerRef}
                {...provided.droppableProps}
              >
                {droppedItems[i] ? (
                  <Draggable draggableId={droppedItems[i]} index={i} key={droppedItems[i]}>
                    {(provided) => (
                      <span
                        className={`draggable-button ${highlightStatus.length > 0 ? (highlightStatus[i] ? "correct" : "incorrect") : ""}`}
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                      >
                        {droppedItems[i]}
                      </span>
                    )}
                  </Draggable>
                ) : (
                  <span className="blank">______</span>
                )}
                {provided.placeholder}
              </span>
            )}
          </Droppable>
        );
      }
    }
    return sentence;
  };

  if (!dragData) return <div>Loading...</div>;

  return (
    <div className="p-6 text-center">
      <h2 className="text-2xl font-bold mb-2">🧩 Drag and Drop</h2>
      <p className="mb-4">{dragData.question}</p>
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="sentence mb-6 text-lg flex flex-wrap justify-center">
          {renderSentence()}
        </div>
        <h3 className="text-lg font-semibold mb-2">🧠 Word Bank</h3>
        <Droppable droppableId="draggables" direction="horizontal">
          {(provided) => (
            <div
              className="draggableContainer flex flex-wrap justify-center gap-2"
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {availableDrags.map((word, index) => (
                <Draggable key={word} draggableId={word} index={index}>
                  {(provided) => (
                    <div
                      className="draggable-button"
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
      </DragDropContext>
      <div className="mt-4">
        <button onClick={handleCheck} className="mr-2 bg-green-200 rounded p-2">✅ Check</button>
        <button onClick={handleReset} className="bg-blue-200 rounded p-2">🔄 Reload</button>
      </div>
    </div>
  );
};

export default DragDrop;
