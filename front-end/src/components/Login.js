import React from 'react';
import { motion } from 'framer-motion';
import './style.css';

const LoginPage = () => {
    function login() {
        window.location.href = "http://localhost:5000/login";
    }

    return (
        <div className="App">
            <header className="App-header">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 3 }}>
                    <h1 style={{ fontSize: '4rem' }}>Muse</h1>
                </motion.div>
                <motion.div
                    initial={{ x: "-100vw" }}
                    animate={{ x: "-0.2vw" }}
                    transition={{
                        type: "spring",
                        stiffness: 80,
                        damping: 10,
                        duration: 1.5,
                    }}>
                <button onClick={login}>Log in with Spotify</button>
                </motion.div>
            </header>
        </div>
    );
};

export default LoginPage;