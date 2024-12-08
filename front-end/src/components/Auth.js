import React, { useState } from 'react';
import axios from 'axios';

function Auth() {
    const [isLogin, setIsLogin] = useState(true); // Toggle between login and register
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleToggle = () => {
        setIsLogin(!isLogin);
        setMessage('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const endpoint = isLogin
                ? 'http://127.0.0.1:5000/api/login'
                : 'http://127.0.0.1:5000/api/register';

            const response = await axios.post(endpoint, { username, password });

            setMessage(response.data.message);

            if (isLogin && response.data.success) {
                // Save the token in localStorage for future API calls
                localStorage.setItem('token', response.data.token);

                // Redirect to Flask's Spotify Song Finder page
                window.location.href = 'http://127.0.0.1:5000/welcome';
            }
        } catch (error) {
            setMessage(error.response?.data?.message || 'An error occurred.');
            console.error('Error:', error);
        }
    };

    return (
        <div className="auth-container">
            <h1>{isLogin ? 'Login' : 'Register'}</h1>
            <form onSubmit={handleSubmit} className="auth-form">
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
                <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
            </form>
            {message && <p className="message">{message}</p>}
            <button className="toggle-btn" onClick={handleToggle}>
                {isLogin ? 'New here? Register' : 'Already have an account? Login'}
            </button>
        </div>
    );
}

export default Auth;
