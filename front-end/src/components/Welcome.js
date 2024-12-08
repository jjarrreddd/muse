import React, { useEffect, useState } from 'react';
<<<<<<< Updated upstream
import { useNavigate } from 'react-router-dom';
=======
import LogoutButton from './LogoutButton';
import './style.css'; // Link to your CSS file
>>>>>>> Stashed changes
import axios from 'axios';
import LogoutButton from './LogoutButton';

<<<<<<< Updated upstream
const Welcome = () => {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    // const handleSuccess = async () => {
    //     navigate('/welcome');
    // };

    // useEffect(() => {
    //     // handleSuccess();
    //     axios.get('http://localhost:5000/welcome')
    //         .then(response => {
    //             setData(response.data.name);
    //         })
    //         .catch(error => {
    //             console.error(error);
    //         });
    // }, []);

    return (
        <div>
            <h1>Login Successful! Welcome to Muse!</h1>
            <LogoutButton />
            <h2>*ensure everything is centered, allow for users to input songs (parse their urls), and produce the recommendation*</h2>
        </div>
    );
};
=======
function Welcome() {
    // const CLIENT_ID = "5d8b3c44a9a54407806a8fa01c89167d";
    // const REDIRECT_URI = "http://localhost:5000/callback";
    // const ENDPOINT = "https://accounts.spotify.com/authorize";
    // const RESPONSE_TYPE = "token";

    const [token, setToken] = useState(null);
    const [query, setQuery] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const [danceability, setDanceability] = useState(0.5);
    const [energy, setEnergy] = useState(0.5);
    const [tempo, setTempo] = useState(120);
    const [valence, setValence] = useState(0.5);

    // Fetch token on load
    useEffect(() => {
        const hash = window.location.hash;
        let storedToken = window.localStorage.getItem('token');

        if (!storedToken && hash) {
            storedToken = hash
                .substring(1)
                .split('&')
                .find((item) => item.startsWith('access_token'))
                ?.split('=')[1];
            window.location.hash = '';
            window.localStorage.setItem('token', storedToken);
        }

        setToken(storedToken);
    }, []);

    // Handle song search and fetch recommendations
    const handleSearch = async (e) => {
        e.preventDefault();
        if (!token) {
            setError('You need to log in with Spotify first!');
            return;
        }

        try {
            setLoading(true);
            setError('');

            // Fetch the track details
            const response = await axios.get('https://api.spotify.com/v1/search', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                params: {
                    q: query,
                    type: 'track',
                    limit: 1,
                },
            });

            const track = response.data.tracks.items[0];
            if (!track) {
                setError('No track found. Try another query.');
                setLoading(false);
                return;
            }

            // Fetch recommendations based on the track
            const recommendationsResponse = await axios.get(
                'https://api.spotify.com/v1/recommendations',
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    params: {
                        seed_tracks: track.id,
                        target_danceability: danceability,
                        target_energy: energy,
                        target_tempo: tempo,
                        target_valence: valence,
                        limit: 5,
                    },
                }
            );

            setRecommendations(recommendationsResponse.data.tracks);
        } catch (err) {
            setError('Error fetching recommendations. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    // Logout function
    const handleLogout = () => {
        setToken(null);
        window.localStorage.removeItem('token');
    };

    return (
        <div className="welcome-container">
            <LogoutButton onLogout={handleLogout} />

            <h1>Welcome to Spotify Song Finder</h1>

            {error && <p className="error-message">{error}</p>}

            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search for a song..."
                    required
                />
                <div className="slider-container">
                    <label> Danceability (0.0 - 1.0): </label>
                    <input
                        type="range"
                        min="0.0"
                        max="1.0"
                        step="0.1"
                        value={danceability}
                        onChange={(e) => setDanceability(e.target.value)}
                    />

                    <label> Energy (0.0 - 1.0): </label>
                    <input
                        type="range"
                        min="0.0"
                        max="1.0"
                        step="0.1"
                        value={energy}
                        onChange={(e) => setEnergy(e.target.value)}
                    />

                    <label> Tempo (BPM): </label>
                    <input
                        type="range"
                        min="60"
                        max="200"
                        step="1"
                        value={tempo}
                        onChange={(e) => setTempo(e.target.value)}
                    />

                    <label> Valence (0.0 - 1.0): </label>
                    <input
                        type="range"
                        min="0.0"
                        max="1.0"
                        step="0.1"
                        value={valence}
                        onChange={(e) => setValence(e.target.value)}
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>

            {recommendations.length > 0 && (
                <div className="results-container">
                    <h2>Recommended Songs</h2>
                    <ul>
                        {recommendations.map((rec) => (
                            <li key={rec.id}>
                                <strong>{rec.name}</strong> by {rec.artists[0].name} -{' '}
                                <a
                                    href={rec.external_urls.spotify}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Listen on Spotify
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
>>>>>>> Stashed changes

export default Welcome;
