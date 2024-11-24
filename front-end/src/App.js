import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import LoginPage from './components/Login';
import Welcome from './components/Welcome';
import NavBar from './components/navbar'; 
import About from './components/About';
import Home from './components/Home';
import Contact from './components/contact';
import MusicPlayer from './components/MusicPlayer';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<LoginPage />} />
        <Route path="/welcome" element={<Welcome />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} /> {/* New Contact route */}
        <Route path="/music-player" element={<MusicPlayer />} /> {/* New Music Player */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
