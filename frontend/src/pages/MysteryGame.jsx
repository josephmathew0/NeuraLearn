// File: frontend/src/pages/MysteryGame.jsx

import React from "react";
import { Routes, Route } from "react-router-dom";
import ModeSelect from "./mystery/ModeSelect";
import CharacterSelect from "./mystery/CharacterSelect";
import Lobby from "./mystery/Lobby";
import WaitingRoom from "./mystery/WaitingRoom";
import MysteryMap from "./MysteryMap"; // (if MysteryMap is still directly inside /pages/)

function MysteryGame() {
  return (
    <Routes>
      <Route path="/" element={<ModeSelect />} /> {/* Default page: Single/Multi */}
      <Route path="/characterselect" element={<CharacterSelect />} />
      <Route path="/lobby" element={<Lobby />} />
      <Route path="/waiting" element={<WaitingRoom />} />
      <Route path="/map" element={<MysteryMap />} />
    </Routes>
  );
}

export default MysteryGame;

