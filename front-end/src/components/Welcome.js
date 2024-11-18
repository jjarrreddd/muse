import React, { useState } from 'react';
import axios from 'axios';

const Welcome = () => {
  const [songName, setSongName] = useState('');  // State to store the song name input
  const [songInfo, setSongInfo] = useState(null); // State to store the fetched song data
  const [error, setError] = useState(''); // State to store error message

  // Function to handle the song search and send POST request to Flask back-end
  const handleSearchSong = () => {
    axios.post('http://localhost:5000/search-song', { song_name: songName })
      .then((response) => {
        setSongInfo(response.data);  // Store the song info from the response
        setError('');  // Clear any previous errors
      })
      .catch((err) => {
        setError(err.response ? err.response.data.error : 'An unknown error occurred');
      });
  };

  return (
    <div>
      <h1>Search for a Song</h1>
      <input 
        type="text" 
        value={songName} 
        onChange={(e) => setSongName(e.target.value)} 
        placeholder="Enter song name"
      />
      <button onClick={handleSearchSong}>Search</button>

      {/* Display song information if available */}
      {songInfo && (
        <div>
          <h2>Song Info:</h2>
          <p>Name: {songInfo.name}</p>
          <p>Artist: {songInfo.artist}</p>
          <p>Album: {songInfo.album}</p>
          <p>URI: {songInfo.uri}</p>
        </div>
      )}

      {/* Display error message if there is one */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Welcome;
