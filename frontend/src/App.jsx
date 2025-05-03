// File: frontend/src/App.jsx

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PlaygroundHome from "./pages/PlaygroundHome";
import PlaygroundDBMS from "./pages/PlaygroundDBMS"; 
import PlaygroundBiology from "./pages/PlaygroundBiology"; // 🆕 Import this!
import UnifiedMCQ from "./pages/UnifiedMCQ";
import UnifiedTextAnswer from "./pages/UnifiedTextAnswer";
import DragDropBiology from "./pages/DragDropBiology";
import DragDropDBMS from "./pages/DragDropDBMS";
import DTDChecker from "./pages/DTDChecker";
import MysteryGame from "./pages/MysteryGame"; 
import Game from "./pages/Game";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PlaygroundHome />} />
        <Route path="/playground" element={<PlaygroundHome />} />

        {/* 🛠️ Hardcoded Beautiful Pages */}
        <Route path="/playground/biology" element={<PlaygroundBiology />} />
        <Route path="/playground/dbms" element={<PlaygroundDBMS />} />

        {/* Activity-specific routes */}
        <Route path="/playground/biology/mcq" element={<UnifiedMCQ subject="biology" />} />
        <Route path="/playground/biology/textanswer" element={<UnifiedTextAnswer subject="biology" />} />
        <Route path="/playground/biology/dragdrop" element={<DragDropBiology />} />

        <Route path="/playground/dbms/mcq" element={<UnifiedMCQ subject="dbms" />} />
        <Route path="/playground/dbms/textanswer" element={<UnifiedTextAnswer subject="dbms" />} />
        <Route path="/playground/dbms/dragdrop" element={<DragDropDBMS />} />
        <Route path="/playground/dbms/dtd" element={<DTDChecker />} />
        <Route path="/playground/dbms/mystery/*" element={<MysteryGame />} />
        <Route path="/playground/dbms/mystery/game" element={<Game />} />
      </Routes>
    </Router>
  );
}

export default App;
