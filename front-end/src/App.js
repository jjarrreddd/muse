import { useState } from 'react';
import axios from "axios";
import './App.css';

function App() {
  const [songInput, setSongInput] = useState(''); // State for the song input
  const [recommendations, setRecommendations] = useState([]); // State for song recommendations

  function getData() {
    window.location.href = "http://localhost:5000/login";
  }

  function getRecommendations() {
    axios({
      method: "POST",
      url: "/recommendations", // Create a new endpoint to handle recommendations
      data: { song: songInput },
    })
    .then((response) => {
      setRecommendations(response.data); // Assuming response contains recommendation data
    }).catch((error) => {
      console.log("Error fetching recommendations", error);
    });
  }

  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: 'black', color: 'white'}}>
        <h1 style={{fontSize: '4rem'}}>Muse</h1>
        
        <button onClick={getData}>Log into Spotify</button>
        
        <input 
          type="text" 
          placeholder="Enter a song" 
          value={songInput} 
          onChange={(e) => setSongInput(e.target.value)} 
        />
        <button onClick={getRecommendations}>Get Recommendations</button>

        {recommendations.length > 0 && (
          <div>
            <h2>Recommendations:</h2>
            <ul>
              {recommendations.map((song, index) => (
                <li key={index}>{song.name}</li> // Adjust based on response structure
              ))}
            </ul>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
