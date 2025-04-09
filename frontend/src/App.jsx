import React from 'react';  // ✅ ← Add this line
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Playground from './pages/Playground';
import PlaygroundMCQ from './pages/PlaygroundMCQ';
import DragDrop from './pages/DragDrop';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/playground" element={<Playground />} />
        <Route path="/playground/mcq" element={<PlaygroundMCQ />} />
        <Route path="/playground/drag" element={<DragDrop />} />
      </Routes>
    </Router>
  );
}

export default App;
