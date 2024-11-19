import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Welcome.css';

const Welcome = () => {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    // Fetch data from Flask's `/welcome` route
    axios
      .get('http://localhost:5000/welcome')
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => {
        console.error('Error fetching user data:', error);
      });
  }, []);

  return (
    <div className="welcome-container">
      {userData ? (
        <>
          <h1>Welcome, {userData.name}!</h1>
          <p>{userData.hello}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Welcome;
