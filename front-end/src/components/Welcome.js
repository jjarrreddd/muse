import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import LogoutButton from './LogoutButton';
import axios from 'axios';

function useQuery() {
    return new URLSearchParams(useLocation().search);
}

function Welcome() {
    const CLIENT_ID = "5d8b3c44a9a54407806a8fa01c89167d"
    const REDIRECT_URI = "http://localhost:5000/callback"
    const ENDPOINT = "https://accounts.spotify.com/authorize"
    const RESPONSE_TYPE = "token"    
    
    const [token, setToken] = useState(null);
    // const [track, setTrack] = useState(null);
    // const [recommendations, setRecommendations] = useState([]);

    // const [danceability, setDanceability] = useState(0.5);
    // const [energy, setEnergy] = useState(0.5);
    // const [tempo, setTempo] = useState(120);
    // const [valence, setValence] = useState(0.5);

    useEffect(() => {
        const hash = window.location.hash;
        let token = window.localStorage.getItem('token')

        if (!token && hash) {
            token = hash.substring(1).split("&").find(elem => elem.startsWith("access_token")).split('=')[1];
            
            window.location.hash = "";
            window.localStorage.setItem('token', token);
        }
        setToken(token);
    }, [])

    // const handleSubmit = async () => {
    //     if (!token) return;
    //     try {
    //         const response = await axios.get('https://api.spotify.com/v1/search', {
    //             headers: {
    //                 Authorization: 'Bearer ${token}'
    //             },
    //             params: {
    //                 q: query,
    //                 type: 'track',
    //                 limit: 1
    //             }
    //         });
    //         setTrack(response.data.tracks.items[0]);
    //     } catch (error) {
    //         console.error(error);
    //     }
    // };

    // if (loading) return <p>Loading...</p>
    // if (error) return <p style="background-color: red;">{error}</p>

    return (
        <div>
            <div>
            <LogoutButton />
            </div>
        {/* <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for a song..."
            required
          /> */}
          {/* <label> Danceability (0.0 - 1.0): </label>
          <input type="range" min="0.0" max="1.0" step="0.1" value={danceability} onChange={(e) => setDanceability(e.target.value)} />
  
          <label> Energy (0.0 - 1.0): </label>
          <input type="range" min="0.0" max="1.0" step="0.1" value={energy} onChange={(e) => setEnergy(e.target.value)} />
  
          <label> Tempo (BPM): </label>
          <input type="range" min="60" max="200" step="1" value={tempo} onChange={(e) => setTempo(e.target.value)} />
  
          <label> Valence (0.0 - 1.0): </label>
          <input type="range" min="0.0" max="1.0" step="0.1" value={valence} onChange={(e) => setValence(e.target.value)} /> */}
  
          {/* <button type="submit">Search</button>
        </form>

        {recommendations.length > 0 && (
            <div>
                <h3>Results</h3>
                <ul>
                    {recommendations.map((rec, index) => (
                        <li key={index}>
                            {rec.name} by {rec.artists[0].name}
                        </li>
                    ))}
                </ul>
            </div>
        )} */}
  
        {/* Recommendation Results */}
        {/* {recommendations.length > 0 && (
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
        )} */}
      </div>
    );
  };

export default Welcome;