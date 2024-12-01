import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const LogoutButton = () => {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState(null);

    const handleLogout = async () => {
        try {
            const response = await axios.get('http://localhost:3000/logout', {}, { withCredentials: true });
            if (response.status === 200) {
                setErrorMessage(null);
                navigate('/');
            } else {
                // Error handling for logging out
                setErrorMessage("Failed to log out. Please try again.");
            }
        } catch (error) {
            // Error handling if server type error
            if (error.response && error.response.data.message) {
                setErrorMessage(error.response.data.message);
            } else {
                setErrorMessage("An error has occurred. Please try again.");
            }
        }
    };

    return (
        <div>
            <button onClick={handleLogout}>Logout</button>
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        </div>
    );
};

export default LogoutButton