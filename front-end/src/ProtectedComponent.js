import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ProtectedComponent() {
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProtectedData = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No token found. Please log in.');
                return;
            }

            try {
                const response = await axios.get('http://127.0.0.1:5000/api/protected', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setMessage(response.data.message);
            } catch (err) {
                setError('Failed to fetch protected data.');
                console.error('Error:', err);
            }
        };

        fetchProtectedData();
    }, []);

    return (
        <div>
            <h1>Protected Page</h1>
            {message && <p>{message}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default ProtectedComponent;
