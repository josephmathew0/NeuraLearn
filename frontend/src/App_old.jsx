import React from 'react';  // ✅ ← Add this line
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
// import PlaygroundBiology from './pages/PlaygroundBiology';
import PlaygroundBiology from "./pages/PlaygroundBiology"; 
import PlaygroundMCQ from './pages/PlaygroundMCQ';
import DragDrop from './pages/DragDropBiology';
import TextAnswer from './pages/TextAnswer';
import SubjectSelector from "./pages/SubjectSelector";
import PlaygroundDBMS from "./pages/PlaygroundDBMS";
import DTDChecker from "./pages/DTDChecker";
import PlaygroundDBMSStructuredMCQ from "./pages/PlaygroundDBMSStructuredMCQ";
import PlaygroundDBMSDrag from "./pages/DragDropDBMS";
import PlaygroundDBMSTextAnswer from './pages/PlaygroundDBMSTextAnswer';
// import other DBMS pages as you build them...

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SubjectSelector />} />
        {/* <Route path="/playground" element={<Playground />} /> */}
        <Route path="/playground/mcq" element={<PlaygroundMCQ />} />
        <Route path="/playground/drag" element={<DragDrop />} />
        <Route path="/playground/sentence" element={<TextAnswer />} />
        <Route path="/playground/biology" element={<PlaygroundBiology />} />  {/* ✅ Right here */}
        <Route path="/playground/dbms" element={<PlaygroundDBMS />} />
        <Route path="/playground/dbms/dtd" element={<DTDChecker />} />
        <Route path="/playground/dbms/mcq" element={<PlaygroundDBMSStructuredMCQ />} />
        <Route path="/playground/dbms/drag" element={<PlaygroundDBMSDrag />} />
        <Route path="/playground/dbms/text" element={<PlaygroundDBMSTextAnswer />} />
      </Routes>
    </Router>
  );
}

export default App;
