import React from 'react';
import './style.css';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const navigate = useNavigate();

    function getData() {
        window.location.href = "http://localhost:5000/login";
    }

    return (
        <div className="App">
            <header className="App-header" style={{ backgroundColor: 'black', color: 'white' }}>
                <h1 style={{ fontSize: '4rem' }}>Muse</h1>

                <button onClick={getData}>Log into Spotify</button>
            </header>
        </div>
    );
};

export default LoginPage;