import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import LogoutButton from './LogoutButton';
import './style.css';
import axios from 'axios';

function Welcome() {
    const [track, setTrack] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [danceability, setDanceability] = useState(0.5);
    const [energy, setEnergy] = useState(0.5);
    const [tempo, setTempo] = useState(120);
    const [valence, setValence] = useState(0.5);
    const [acousticness, setAcousticness] = useState(0.5);
    const [instrumentalness, setInstrumentalness] = useState(0.5);
    const [loudness, setLoudness] = useState(30.0);

    const [error, setError] = useState(null);
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [visible, setVisible] = useState(false);

    useEffect(() => {
      setTimeout(() => {
        setVisible(true);
      }, 500);
    }, []);

    const handleSubmit = async (e) => {
      e.preventDefault();

      setLoading(true);
      setError(null);

      try {
        const response = await axios.get('http://localhost:5000/search');
        const data = await response.json();

        setTrack(data.track);
        setRecommendations(data.recommendations);
      } catch (error) {
        setError('Error fetching data');
      } finally {
        setLoading(false);
      }
    };

    return (
        <div className="welcome-container">
            <div>
            <LogoutButton />
            <br />
            </div>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <br />
            <br />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for a song..."
              required
            />
            </div>
          <div className="slider-container">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1 }}>
              <label><strong>Danceability</strong> (0.0 - 1.0): </label>
              <input type="range" min="0.0" max="1.0" step="0.01" value={danceability} onChange={(e) => setDanceability(e.target.value)} />
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1.5 }}>
              <label><strong>Energy</strong> (0.0 - 1.0): </label>
              <input type="range" min="0.0" max="1.0" step="0.01" value={energy} onChange={(e) => setEnergy(e.target.value)} />
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1.7 }}>
              <label><strong>Tempo</strong> (BPM): </label>
              <input type="range" min="0" max="240" step="1" value={tempo} onChange={(e) => setTempo(e.target.value)} />
            </motion.div>

            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1.9 }}>
              <label><strong>Valence</strong> (0.0 - 1.0): </label>
              <input type="range" min="0.0" max="1.0" step="0.01" value={valence} onChange={(e) => setValence(e.target.value)} />
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 2.1 }}>
              <label><strong>Acousticness</strong> (0.0 - 1.0): </label>
              <input type="range" min="0.0" max="1.0" step="0.01" value={acousticness} onChange={(e) => setAcousticness(e.target.value)} />
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 2.3 }}>
              <label><strong>Instrumentalness</strong> (0.0 - 1.0): </label>
              <input type="range" min="0.0" max="1.0" step="0.01" value={instrumentalness} onChange={(e) => setInstrumentalness(e.target.value)} />
            </motion.div>

            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 2.5 }}>
              <label><strong>Loudness</strong> (-60dB - 0): </label>
              <input type="range" min="0.0" max="60.0" step="0.01" value={loudness} onChange={(e) => setLoudness(e.target.value)} />
              </motion.div>
          </div>
          <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 2.5 }}>
            <button type="submit" disabled={loading}>
              {loading ? 'Searching...': 'Search'}
            </button>
            </motion.div>
        </form>

        {error && <p style={{ color: 'red' }}>{error}</p>}
  
        {/* Recommendation Results */}
        {recommendations.length > 0 && (
          <div className="results-container">
            <h1>Search Results</h1>
            <p><strong>Song:</strong> {track.name}</p>
            <p><strong>Artist:</strong> {track.artist}</p>
            <p><strong>Album:</strong> {track.album}</p>
            <p><a href={track.url} target="_blank" rel="noopener noreferrer">Listen on Spotify</a></p>
  
            <h2>Recommended Songs:</h2>
            <ul>
              {recommendations.map((rec, index) => (
                <li key={index}>
                  <strong>{rec.name}</strong> by {rec.artist} -
                  <p><a href={rec.url} target="_blank" rel="noopener noreferrer">Listen on Spotify</a></p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

export default Welcome;