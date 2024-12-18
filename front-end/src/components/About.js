import React from 'react';
import { motion } from 'framer-motion';

function About() {
  return (
    <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1 }}>
      <div className="header mt-5">
        <h1>About</h1>
        <br />
        <p className="body">Welcome to <strong><span style={{ color: '#1DB954'}}>Muse</span></strong>! A recommendation app, powered by Spotify, designed to improve your music discovery experience!
          Log into your Spotify account and fine-tune various song attributes such as, danceability, energy, tempo, and 
          valence! Muse provides more focused song suggestions that match your style!</p>
        <p className="body">We decided to create an app that refines the recommendation experience by aiming for a <strong>90% hit rate</strong>! In other words, we want our
          application to produce accurate suggestions that users can add to their playlist!</p>
      </div>
    </motion.div>
  );
}

export default About;