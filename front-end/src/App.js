import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './App.css';

import LoginPage from './components/Login';
import Welcome from './components/Welcome';
import NavBar from './components/navbar';
import About from './components/About';
import Contact from './components/Contact'
import MusicPlayer from './components/MusicPlayer';

function App() {
  return (
    <>
      <BrowserRouter>
        <NavBar />
          <AnimatePresence>
            <Routes>
              <Route path="/" element={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  >
                    <LoginPage />
                  </motion.div>
              }
              />
              <Route path="/welcome" element={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  >
                    <Welcome />
                  </motion.div>
              } />
              <Route path="/about" element={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  >
                    <About />
                  </motion.div>
              } />
              <Route path="/contact" element={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  >
                    <Contact />
                  </motion.div>
              } />
              <Route path="/music-player" element={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  >
                    <MusicPlayer />
                  </motion.div>
              } />
            </Routes>
          </AnimatePresence>
      </BrowserRouter>
    </>
  );
}

export default App;
