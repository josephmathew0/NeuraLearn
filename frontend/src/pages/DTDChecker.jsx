import React, { useState, useEffect } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import "../styles/dtdChecker.css";

export default function DTDChecker() {
  const [lines, setLines] = useState([]);
  const [correctLines, setCorrectLines] = useState([]);
  const [editedLines, setEditedLines] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [questionId, setQuestionId] = useState(1);
  const [submitted, setSubmitted] = useState(false);
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/dtd/${questionId}`)
      .then(res => res.json())
      .then(data => {
        setPrompt(data.prompt);
        setLines(data.initial_lines);
        setCorrectLines(data.correct_lines);
        setEditedLines(data.initial_lines);
        setSubmitted(false);
        setAttempts(0);
      });
  }, [questionId]);

  const handleDragEnd = (result) => {
    if (!result.destination) return;
    const items = Array.from(lines);
    const edits = Array.from(editedLines);
    const [reordered] = items.splice(result.source.index, 1);
    const [editedReordered] = edits.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reordered);
    edits.splice(result.destination.index, 0, editedReordered);
    setLines(items);
    setEditedLines(edits);
  };

  const handleEdit = (index, newText) => {
    const updated = [...editedLines];
    updated[index] = newText;
    setEditedLines(updated);
  };

  const checkFixes = () => {
    const isCorrect = JSON.stringify(editedLines) === JSON.stringify(correctLines);

    if (isCorrect) {
      setSubmitted(true);
      setTimeout(() => {
        setQuestionId((prev) => prev + 1);
        setSubmitted(false);
      }, 1500);
    } else {
      setSubmitted(true);
      setAttempts(prev => prev + 1);
    }
  };

  const resetFixes = () => {
    setEditedLines([...lines]);
    setSubmitted(false);
    setAttempts(0);
  };

  return (
    <div className="min-h-screen p-6">
      <h2 className="text-2xl font-semibold mb-4">🛠️ Fix the XML Schema</h2>
      <p className="mb-4">{prompt}</p>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="schema">
          {(provided) => (
            <pre
              className="bg-gray-100 p-4 rounded text-sm whitespace-pre-wrap"
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <div className="flex flex-col gap-1">
                {editedLines.map((line, idx) => {
                  const isCorrect = submitted && editedLines[idx] === correctLines[idx];
                  const isIncorrect = submitted && editedLines[idx] !== correctLines[idx];

                  return (
                    <Draggable key={idx} draggableId={`line-${idx}`} index={idx}>
                      {(provided) => (
                        <div
                          className={`dtd-line flex items-center ${
                            isCorrect ? "correct" : isIncorrect ? "incorrect" : ""
                          }`}
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                        >
                          <span className="text-gray-400 w-6">{idx + 1}</span>
                          <span {...provided.dragHandleProps} className="drag-handle">⋮⋮</span>
                          <span
                            className="flex-1"
                            contentEditable
                            suppressContentEditableWarning={true}
                            onBlur={(e) => handleEdit(idx, e.target.textContent)}
                          >
                            {line}
                          </span>
                        </div>
                      )}
                    </Draggable>
                  );
                })}
                {provided.placeholder}
              </div>
            </pre>
          )}
        </Droppable>
      </DragDropContext>

      <div className="mt-4 flex gap-4">
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          onClick={checkFixes}
        >
          Submit Fixes
        </button>
        <button
          className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500"
          onClick={resetFixes}
        >
          Reset Fixes
        </button>
      </div>

      {submitted && (
        <div className="mt-4 text-md">
          {JSON.stringify(editedLines) === JSON.stringify(correctLines) ? (
            <p>✅ Well done! Loading next question...</p>
          ) : attempts >= 2 ? (
            <>
              <p>🧠 Here's the correct answer:</p>
              <div className="mt-2 bg-white p-3 rounded text-sm font-mono whitespace-pre-wrap border border-gray-300">
                {correctLines.join("\n")}
              </div>
            </>
          ) : (
            <p>❌ Not quite. Try again.</p>
          )}
        </div>
      )}
    </div>
  );
}
