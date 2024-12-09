import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import LogoutButton from './LogoutButton';
import axios from 'axios';

function Welcome() {
    const [track, setTrack] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [danceability, setDanceability] = useState(0.5);
    const [energy, setEnergy] = useState(0.5);
    const [tempo, setTempo] = useState(120);
    const [valence, setValence] = useState(0.5);

    const [error, setError] = useState(null);
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);


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
        <div>
            <div>
            <LogoutButton />
            </div>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for a song..."
            required
          />
          <label> Danceability (0.0 - 1.0): </label>
          <input type="range" min="0.0" max="1.0" step="0.1" value={danceability} onChange={(e) => setDanceability(e.target.value)} />
  
          <label> Energy (0.0 - 1.0): </label>
          <input type="range" min="0.0" max="1.0" step="0.1" value={energy} onChange={(e) => setEnergy(e.target.value)} />
  
          <label> Tempo (BPM): </label>
          <input type="range" min="60" max="200" step="1" value={tempo} onChange={(e) => setTempo(e.target.value)} />
  
          <label> Valence (0.0 - 1.0): </label>
          <input type="range" min="0.0" max="1.0" step="0.1" value={valence} onChange={(e) => setValence(e.target.value)} />
  
        <button type="submit">Search</button>
        </form>

        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
  
        {/* Recommendation Results */}
        {recommendations.length > 0 && (
          <div>
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