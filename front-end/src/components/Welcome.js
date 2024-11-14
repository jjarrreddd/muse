import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import LogoutButton from './LogoutButton';

const Welcome = () => {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    // const handleSuccess = async () => {
    //     navigate('/welcome');
    // };

    // useEffect(() => {
    //     // handleSuccess();
    //     axios.get('http://localhost:5000/welcome')
    //         .then(response => {
    //             setData(response.data.name);
    //         })
    //         .catch(error => {
    //             console.error(error);
    //         });
    // }, []);

    return (
        <div>
            <h1>Login Successful! Welcome to Muse!</h1>
            <LogoutButton />
            <h2>*ensure everything is centered, allow for users to input songs (parse their urls), and produce the recommendation*</h2>
        </div>
    );
};

export default Welcome;