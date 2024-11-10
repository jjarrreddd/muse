import React, { useState } from 'react';
import axios from 'axios';
import './style.css';

const LoginPage = () => {
    function getData() {
        window.location.href = "http://localhost:5000/login";
    }

    return (
        <div className="App">
            <header className="App-header" style={{ backgroundColor: 'black', color: 'white' }}>
                <h1 style={{ fontSize: '4rem' }}>Muse</h1>

                <button onClick={getData}>Log in with Spotify</button>
            </header>
        </div>
    );
};

export default LoginPage;