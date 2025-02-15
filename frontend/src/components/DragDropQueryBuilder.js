import React, { useState, useEffect } from "react";

// ✅ Function to shuffle an array randomly
const shuffleArray = (array) => {
  return [...array].sort(() => Math.random() - 0.5);
};

const DragDropQueryBuilder = ({ options, onQueryChange }) => {
  const [queryParts, setQueryParts] = useState([]);
  const [shuffledOptions, setShuffledOptions] = useState([]);

  // ✅ Shuffle options once when the component loads
  useEffect(() => {
    if (options && options.length > 0) {
      setShuffledOptions(shuffleArray(options));
    }
  }, [options]);

  // Handle dropping SQL parts
  const handleDrop = (event) => {
    event.preventDefault();
    const draggedSQL = event.dataTransfer.getData("text");
    const newQueryParts = [...queryParts, draggedSQL];
    setQueryParts(newQueryParts);

    // ✅ Ensure `onQueryChange` is correctly passed
    if (typeof onQueryChange === "function") {
      onQueryChange(newQueryParts.join(" "));
    } else {
      console.error("❌ onQueryChange is not a function! Check the Quiz.js import.");
    }
  };

  // Handle drag events
  const handleDragStart = (event, sql) => {
    event.dataTransfer.setData("text", sql);
  };

  return (
    <div>
      <h3>Drag & Drop to Build Your Query</h3>

      {/* Draggable SQL components */}
      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
        {shuffledOptions.map((sql, index) => (
          <div
            key={index}
            draggable
            onDragStart={(event) => handleDragStart(event, sql)}
            style={{
              padding: "8px",
              border: "1px solid black",
              cursor: "grab",
              backgroundColor: "#e0e0e0",
              borderRadius: "5px",
            }}
          >
            {sql}
          </div>
        ))}
      </div>

      {/* Drop area for query */}
      <div
        onDrop={handleDrop}
        onDragOver={(event) => event.preventDefault()}
        style={{
          minHeight: "50px",
          marginTop: "10px",
          padding: "10px",
          border: "2px dashed black",
          backgroundColor: "#f5f5f5",
        }}
      >
        {queryParts.length === 0 ? "Drop query elements here..." : queryParts.join(" ")}
      </div>
    </div>
  );
};

export default DragDropQueryBuilder;
