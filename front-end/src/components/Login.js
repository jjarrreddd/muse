import React from 'react';
import './Login.css';

const LoginPage = () => {
  const handleLogin = () => {
    // Redirect to the Flask app's home route for Spotify login
    window.location.href = 'http://localhost:5000/';
  };

  return (
    <div className="login-container">
      <h1>Muse</h1>
      <button onClick={handleLogin} className="login-button">
        Log into Spotify
      </button>
    </div>
  );
};

export default LoginPage;
