// File: frontend/src/App.jsx

import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";

import PlaygroundHome from "./pages/PlaygroundHome";
import PlaygroundDBMS from "./pages/PlaygroundDBMS"; 
import PlaygroundBiology from "./pages/PlaygroundBiology";
import UnifiedMCQ from "./pages/UnifiedMCQ";
import UnifiedTextAnswer from "./pages/UnifiedTextAnswer";
import DragDropBiology from "./pages/DragDropBiology";
import DragDropDBMS from "./pages/DragDropDBMS";
import DTDChecker from "./pages/DTDChecker";
import MysteryGame from "./pages/MysteryGame"; 
import Game from "./pages/Game";
import CharacterSelectSingle from "./pages/CharacterSelectSingle";
import GameSinglePlayer from "./pages/GameSinglePlayer";
import Login from "./pages/Login";
import Register from "./pages/Register";

function ProtectedRoute({ children }) {
  const isLoggedIn = localStorage.getItem("email");
  const location = useLocation();

  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

function RedirectIfLoggedIn({ children }) {
  const isLoggedIn = localStorage.getItem("email");
  return isLoggedIn ? <Navigate to="/playground" replace /> : children;
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<RedirectIfLoggedIn><Login /></RedirectIfLoggedIn>} />
        <Route path="/register" element={<RedirectIfLoggedIn><Register /></RedirectIfLoggedIn>} />

        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <PlaygroundHome />
            </ProtectedRoute>
          }
        />
        <Route
          path="/playground"
          element={
            <ProtectedRoute>
              <PlaygroundHome />
            </ProtectedRoute>
          }
        />
        <Route path="/playground/biology" element={<ProtectedRoute><PlaygroundBiology /></ProtectedRoute>} />
        <Route path="/playground/dbms" element={<ProtectedRoute><PlaygroundDBMS /></ProtectedRoute>} />

        {/* Activity-specific routes (all protected) */}
        <Route path="/playground/biology/mcq" element={<ProtectedRoute><UnifiedMCQ subject="biology" /></ProtectedRoute>} />
        <Route path="/playground/biology/textanswer" element={<ProtectedRoute><UnifiedTextAnswer subject="biology" /></ProtectedRoute>} />
        <Route path="/playground/biology/dragdrop" element={<ProtectedRoute><DragDropBiology /></ProtectedRoute>} />

        <Route path="/playground/dbms/mcq" element={<ProtectedRoute><UnifiedMCQ subject="dbms" /></ProtectedRoute>} />
        <Route path="/playground/dbms/textanswer" element={<ProtectedRoute><UnifiedTextAnswer subject="dbms" /></ProtectedRoute>} />
        <Route path="/playground/dbms/dragdrop" element={<ProtectedRoute><DragDropDBMS /></ProtectedRoute>} />
        <Route path="/playground/dbms/dtd" element={<ProtectedRoute><DTDChecker /></ProtectedRoute>} />
        <Route path="/playground/dbms/mystery/*" element={<ProtectedRoute><MysteryGame /></ProtectedRoute>} />
        <Route path="/playground/dbms/mystery/game" element={<ProtectedRoute><Game /></ProtectedRoute>} />
        <Route path="/playground/dbms/mystery/singleplayer" element={<ProtectedRoute><CharacterSelectSingle /></ProtectedRoute>} />
        <Route path="/playground/dbms/mystery/single" element={<ProtectedRoute><GameSinglePlayer /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
