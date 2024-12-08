import React, { useState } from 'react';
<<<<<<< Updated upstream
import axios from 'axios';
import './style.css';

const LoginPage = () => {
    function getData() {
        window.location.href = "http://localhost:5000/";
    }

    return (
        <div className="App">
            <header className="App-header" style={{ backgroundColor: 'black', color: 'white' }}>
                <h1 style={{ fontSize: '4rem' }}>Muse</h1>

                <button onClick={getData}>Log in with Spotify</button>
            </header>
=======

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        console.log('Logging in with:', { username, password });
        // Implement login functionality here
    };

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>
>>>>>>> Stashed changes
        </div>
    );
}

export default Login;
