import React, { useState } from 'react';
import axios from 'axios';
import './style.css'

function MusicPlayer() {
  const [trackId, setTrackId] = useState('');
  const [trackData, setTrackData] = useState(null);

  const fetchTrack = async () => {
    if (!trackId) return;

    try {
      const response = await axios.get(`http://localhost:5000/track?id=${trackId}`);
      setTrackData(response.data);
    } catch (error) {
      console.error('Error fetching track:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Test Play Music</h2>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter Spotify Track ID"
          value={trackId}
          onChange={(e) => setTrackId(e.target.value)}
          required
        />
      </div>
      <button onClick={fetchTrack}>
        Fetch Track
      </button>

      {trackData && (
        <div className="mt-4">
          <h4>{trackData.name}</h4>
          <p>{trackData.artist}</p>
          {trackData.preview_url ? (
            <audio controls>
              <source src={trackData.preview_url} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          ) : (
            <p>Preview not available for this track.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default MusicPlayer;